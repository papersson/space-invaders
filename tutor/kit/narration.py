"""Render a lesson's narration from its locked script (SCRIPT.md) with a TTS engine.

SCRIPT.md is the single source of truth: every "> " line under a "### N. Title" heading is a
paragraph of narration, split here into sentences. Writes audio/narration.wav, audio/narration.mp3
and audio/timings.json with every sentence's id, spoken text, caption text, start and end, so the
scenes can cue off sentence ids. Per-lesson settings (holds after sentences, spoken spellings, the
end-card tail) come from narration.json in the lesson folder, when it exists.

Engines (narration.json "engine"):
  kokoro (default)  Kokoro-82M, one call per sentence, joined with fixed gaps. Needs: kokoro.
  pocket            Kyutai Pocket TTS, one call per paragraph (so intonation carries across
                    sentences and pauses follow the punctuation); sentence timings come from forced
                    alignment (kit/align.py). Settings in narration.json "pocket": model, voice, seed.
                    Needs: pocket-tts, torchaudio, num2words. Weights and the built-in voices are
                    CC-BY-4.0, so timings.json carries a credit line that the page shows.

    python kit/narration.py LESSON_DIR            # render with the lesson's engine
    python kit/narration.py LESSON_DIR --estimate # timings only, from word counts (no audio)
    python kit/narration.py LESSON_DIR --list     # print the sentence ids
"""
import json
import re
import subprocess
import sys
from pathlib import Path

VOICE = "af_heart"
SPEED = 0.92
RATE = 24_000
LEAD_IN = 0.8        # silence before the first sentence
SENTENCE_GAP = 0.3   # between sentences of one paragraph
PARAGRAPH_GAP = 0.5  # between paragraphs
SEGMENT_GAP = 1.2    # between segments

HERE = Path(sys.argv[1]).resolve()
OUT = HERE / "audio"
_CFG = json.loads((HERE / "narration.json").read_text()) if (HERE / "narration.json").exists() else {}
TAIL = _CFG.get("tail", 6.0)          # silence after the last sentence (end card)
# Extra silence after particular sentences, where the picture needs time to be read.
HOLDS = _CFG.get("holds", {})
# Written form -> spoken form, everywhere and for particular sentences.
SPOKEN = [tuple(p) for p in _CFG.get("spoken", [])]
SPOKEN_BY_ID = {k: [tuple(p) for p in v] for k, v in _CFG.get("spoken_by_id", {}).items()}
ENGINE = _CFG.get("engine", "kokoro")
POCKET = {"model": "english_2026-09_24l", "voice": "alba", "seed": 0, **_CFG.get("pocket", {})}
CHUNK_WORDS = 90     # longest run of sentences sent to Pocket TTS in one call
ATTEMPTS = 4         # Pocket TTS sometimes drops or garbles a sentence: re-synthesize up to this often
MIN_MATCH = 0.8      # ... when a speech recogniser matches less than this share of any sentence (align.match)


def load_script():
    """[(segment id, title, [(sentence id, caption text, paragraph index)])] from SCRIPT.md."""
    text = (HERE / "SCRIPT.md").read_text()
    body = text[text.index("## Script"):text.index("## Evidence")]
    segs = []
    for block in re.split(r"^### ", body, flags=re.M)[1:]:
        head, rest = block.split("\n", 1)
        num, title = head.split(". ", 1)
        sid = f"s{int(num)}"
        sentences, n = [], 0
        paras = [l[2:].strip() for l in rest.splitlines() if l.startswith("> ")]
        for pi, para in enumerate(paras):
            for sent in re.split(r'(?<=[.!?])\s+(?=[A-Z"])', para):
                n += 1
                sentences.append((f"{sid}_{n:02d}", sent.strip(), pi))
        segs.append((sid, title.strip(), sentences))
    return segs


def spoken(text, lid=None):
    for written, said in SPOKEN + SPOKEN_BY_ID.get(lid, []):
        text = text.replace(written, said)
    return text


def say(text):
    """Numbers spelled out, so the speech and the aligner's transcript agree (pocket engine)."""
    from num2words import num2words

    text = re.sub(r"(?<=\d),(?=\d{3})", "", text)
    text = re.sub(r"(\d)\s*%", r"\1 percent", text)
    text = re.sub(r"\b(1[89]\d\d|20\d\d)\b", lambda m: num2words(int(m.group()), to="year"), text)
    text = re.sub(r"\d+\.\d+", lambda m: num2words(float(m.group())), text)
    return re.sub(r"\d+", lambda m: num2words(int(m.group())), text)


def layout(segs, durations, gaps=None):
    """Place every sentence on one track. `gaps` (pocket engine): the natural pause after a sentence,
    measured in its paragraph's audio; it replaces SENTENCE_GAP there."""
    gaps = gaps or {}
    t, out = LEAD_IN, []
    for si, (sid, title, sents) in enumerate(segs):
        if si:
            t += SEGMENT_GAP
        seg = {"id": sid, "title": title, "start": t, "lines": []}
        prev_p = prev_id = None
        for lid, cap, pi in sents:
            if prev_p is not None:
                t += gaps.get(prev_id, SENTENCE_GAP) if pi == prev_p else PARAGRAPH_GAP
            d = durations[lid]
            seg["lines"].append({"id": lid, "text": spoken(cap, lid), "caption": cap, "paragraph": pi,
                                 "start": round(t, 3), "end": round(t + d, 3)})
            t += d + HOLDS.get(lid, 0.0)
            prev_p, prev_id = pi, lid
        out.append(seg)
    total = t + TAIL
    out[0]["start"] = 0.0
    for a, b in zip(out, out[1:]):
        b["start"] = round(b["lines"][0]["start"] - 0.35, 3)
        a["end"] = b["start"]
    out[-1]["end"] = round(total, 3)
    if ENGINE == "pocket":
        return {"engine": "pocket", "voice": f"{POCKET['model']}/{POCKET['voice']}", "speed": 1.0,
                "credit": f"Narration voice: Kyutai Pocket TTS ({POCKET['model']}), voice \u201c{POCKET['voice']}\u201d, CC BY 4.0",
                "total": round(total, 3), "segments": out}
    return {"voice": VOICE, "speed": SPEED, "total": round(total, 3), "segments": out}


def pocket_clips(segs):
    """{sentence id: clip}, {sentence id: natural pause after it}, {sentence id: text as spoken},
    {sentence id: recogniser match}. Each paragraph (split into runs of at most CHUNK_WORDS words) is
    one call; the clip boundaries come from aligning the known text and snapping to silence. A run
    whose audio won't align, or in which a recogniser misses too much of a sentence, is synthesized
    again (the next draw from the same seeded stream), keeping the best attempt."""
    import numpy as np
    import torch
    from pocket_tts import TTSModel
    sys.path.insert(0, str(Path(__file__).parent))
    from align import AlignError, match, sentence_spans

    torch.manual_seed(POCKET["seed"])
    model = TTSModel.load_model(language=POCKET["model"])
    state = model.get_state_for_audio_prompt(POCKET["voice"])
    assert model.sample_rate == RATE, model.sample_rate
    clips, gaps, said, check = {}, {}, {}, {}
    for _, _, sents in segs:
        chunks, cur, n = [], [], 0
        for lid, cap, pi in sents:
            text = say(spoken(cap, lid))
            w = len(text.split())
            if cur and (pi != cur[-1][2] or n + w > CHUNK_WORDS):
                chunks.append(cur)
                cur, n = [], 0
            cur.append((lid, text, pi))
            n += w
        chunks.append(cur)
        for chunk in chunks:
            texts, best = [t for _, t, _ in chunk], None
            for attempt in range(1, ATTEMPTS + 1):
                audio = model.generate_audio(state, " ".join(texts)).numpy().astype(np.float32)
                try:
                    spans = sentence_spans(audio, RATE, texts)
                except AlignError as e:
                    print(f"  {chunk[0][0]}: attempt {attempt} doesn't align ({e})")
                    continue
                scores = [match(t, audio[int(a * RATE): int(b * RATE)], RATE) for t, (a, b) in zip(texts, spans)]
                if best is None or min(scores) > min(best[2]):
                    best = (audio, spans, scores)
                if min(scores) >= MIN_MATCH:
                    break
                print(f"  {chunk[0][0]}: attempt {attempt} heard only {min(scores):.2f} of a sentence")
            if best is None:
                raise SystemExit(f"{chunk[0][0]}: no attempt aligned; change the pocket seed or the text")
            audio, spans, scores = best
            for i, ((lid, text, _), (a, b)) in enumerate(zip(chunk, spans)):
                clip = audio[int(a * RATE): int(b * RATE)].copy()
                fade = min(len(clip) // 2, int(0.005 * RATE))
                if fade:
                    clip[:fade] *= np.linspace(0, 1, fade)
                    clip[-fade:] *= np.linspace(1, 0, fade)
                clips[lid], said[lid], check[lid] = clip, text, round(scores[i], 2)
                if i + 1 < len(chunk):
                    gaps[lid] = spans[i + 1][0] - b
                flag = "  <-- listen" if scores[i] < MIN_MATCH else ""
                print(f"{lid}: {len(clip) / RATE:5.2f}s  gap {gaps.get(lid, 0):.2f}  heard {scores[i]:.2f}  {text[:60]}{flag}")
    return clips, gaps, said, check


def main():
    OUT.mkdir(exist_ok=True)
    segs = load_script()
    sents = [(lid, cap) for _, _, ss in segs for lid, cap, _ in ss]
    if "--list" in sys.argv:
        for lid, cap in sents:
            print(lid, cap)
        return
    if "--estimate" in sys.argv:
        timings = layout(segs, {k: len(c.split()) / 2.8 + 0.3 for k, c in sents})
        (OUT / "timings.json").write_text(json.dumps(timings, indent=1))
        print(f"estimated total {timings['total']:.1f}s")
        return

    import numpy as np
    import soundfile as sf

    gaps = check = None
    if ENGINE == "pocket":
        clips, gaps, phonemes, check = pocket_clips(segs)
    else:
        from kokoro import KPipeline

        pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
        clips, phonemes = {}, {}
        for key, cap in sents:
            parts = list(pipe(spoken(cap, key), voice=VOICE, speed=SPEED, split_pattern=None))
            audio = np.concatenate([p.audio.numpy() for p in parts])
            nz = np.flatnonzero(np.abs(audio) > 0.01)   # trim Kokoro's own silence
            clips[key] = audio[max(nz[0] - 240, 0): nz[-1] + 480]
            phonemes[key] = " ".join(p.phonemes for p in parts)
            print(f"{key}: {len(clips[key]) / RATE:5.2f}s  {phonemes[key][:80]}")

    timings = layout(segs, {k: len(a) / RATE for k, a in clips.items()}, gaps)
    track = np.zeros(int(timings["total"] * RATE) + RATE, dtype=np.float32)
    for seg in timings["segments"]:
        for ln in seg["lines"]:
            i = int(round(ln["start"] * RATE))
            track[i: i + len(clips[ln["id"]])] = clips[ln["id"]]
    track = track[: int(timings["total"] * RATE)]
    if ENGINE == "pocket":                      # Pocket TTS runs quiet; match Kokoro's level
        track *= 0.89 / max(float(np.abs(track).max()), 1e-6)
    sf.write(OUT / "narration.wav", track, RATE)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUT / "narration.wav"),
                    "-codec:a", "libmp3lame", "-b:a", "128k", str(OUT / "narration.mp3")], check=True)
    timings["phonemes"] = phonemes
    if check:
        timings["asr_match"] = check
        low = [f"{k} {v:.2f}" for k, v in check.items() if v < MIN_MATCH]
        if low:
            print("listen to these (the recogniser heard too little):", ", ".join(low))
    timings["peak"] = float(np.abs(track).max())
    (OUT / "timings.json").write_text(json.dumps(timings, indent=1))
    print(f"total {timings['total']:.1f}s, peak {timings['peak']:.2f}")


if __name__ == "__main__":
    main()
