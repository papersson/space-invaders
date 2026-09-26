"""Render the narration of the locked script (SCRIPT.md) with Kokoro TTS, one sentence at a time.

SCRIPT.md is the single source of truth: every "> " line under a "### N. Title" heading is a
paragraph of narration, split here into sentences. Writes audio/narration.wav, audio/narration.mp3
and audio/timings.json with every sentence's id, spoken text, caption text, start and end, so the
scenes can cue off sentence ids.

    python narration.py            # render with Kokoro
    python narration.py --estimate # timings only, from word counts (no audio)
    python narration.py --list     # print the sentence ids
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
TAIL = 3.0           # silence after the last sentence (end card)

# Extra silence after particular sentences, where the picture needs time to be read.
HOLDS = {
    "s1_05": 2.8,    # title card
    "s2_16": 1.2,    # the time bar: the I/Os decide
    "s3_12": 1.0,    # the twelve temp files labelled as runs
    "s4_13": 1.5,    # the merge replay finishing
    "s4_18": 1.2,    # sort's runs vanish
    "s5_12": 1.0,    # the PostgreSQL line
}

# Written form -> spoken form.
SPOKEN = [("PostgreSQL", "Post gress Q L")]

HERE = Path(__file__).parent
OUT = HERE / "audio"


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


def spoken(text):
    for written, said in SPOKEN:
        text = text.replace(written, said)
    return text


def layout(segs, durations):
    t, out = LEAD_IN, []
    for si, (sid, title, sents) in enumerate(segs):
        if si:
            t += SEGMENT_GAP
        seg = {"id": sid, "title": title, "start": t, "lines": []}
        prev_p = None
        for lid, cap, pi in sents:
            if prev_p is not None:
                t += SENTENCE_GAP if pi == prev_p else PARAGRAPH_GAP
            d = durations[lid]
            seg["lines"].append({"id": lid, "text": spoken(cap), "caption": cap, "paragraph": pi,
                                 "start": round(t, 3), "end": round(t + d, 3)})
            t += d + HOLDS.get(lid, 0.0)
            prev_p = pi
        out.append(seg)
    total = t + TAIL
    out[0]["start"] = 0.0
    for a, b in zip(out, out[1:]):
        b["start"] = round(b["lines"][0]["start"] - 0.35, 3)
        a["end"] = b["start"]
    out[-1]["end"] = round(total, 3)
    return {"voice": VOICE, "speed": SPEED, "total": round(total, 3), "segments": out}


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
    from kokoro import KPipeline

    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    clips, phonemes = {}, {}
    for key, cap in sents:
        parts = list(pipe(spoken(cap), voice=VOICE, speed=SPEED, split_pattern=None))
        audio = np.concatenate([p.audio.numpy() for p in parts])
        nz = np.flatnonzero(np.abs(audio) > 0.01)   # trim Kokoro's own silence
        clips[key] = audio[max(nz[0] - 240, 0): nz[-1] + 480]
        phonemes[key] = " ".join(p.phonemes for p in parts)
        print(f"{key}: {len(clips[key]) / RATE:5.2f}s  {phonemes[key][:80]}")

    timings = layout(segs, {k: len(a) / RATE for k, a in clips.items()})
    track = np.zeros(int(timings["total"] * RATE) + RATE, dtype=np.float32)
    for seg in timings["segments"]:
        for ln in seg["lines"]:
            i = int(round(ln["start"] * RATE))
            track[i: i + len(clips[ln["id"]])] = clips[ln["id"]]
    track = track[: int(timings["total"] * RATE)]
    sf.write(OUT / "narration.wav", track, RATE)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUT / "narration.wav"),
                    "-codec:a", "libmp3lame", "-b:a", "128k", str(OUT / "narration.mp3")], check=True)
    timings["phonemes"] = phonemes
    timings["peak"] = float(np.abs(track).max())
    (OUT / "timings.json").write_text(json.dumps(timings, indent=1))
    print(f"total {timings['total']:.1f}s, peak {timings['peak']:.2f}")


if __name__ == "__main__":
    main()
