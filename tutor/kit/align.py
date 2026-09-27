"""Sentence timings for TTS engines that return one clip per paragraph: CTC forced alignment of the
known text (wav2vec2, torchaudio), then each sentence edge snapped to the nearest silence.

    spans = sentence_spans(audio, sr, ["First sentence.", "Second one."])   # [(start, end)] in seconds

The text must be what was actually spoken: spell out numbers first (see say() in narration.py),
since the aligner knows only the letters A-Z and the apostrophe.
"""
import difflib
import re

import numpy as np

_MODEL = None


class AlignError(Exception):
    """The audio doesn't fit the text (a dropped or garbled sentence): re-synthesize and try again."""


def _model():
    import torchaudio

    global _MODEL
    bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
    if _MODEL is None:
        _MODEL = bundle.get_model().eval()
    return bundle, _MODEL


def heard(audio, sr):
    """The words a speech recogniser hears in a clip (wav2vec2, greedy CTC)."""
    import torch
    import torchaudio.functional as AF

    bundle, model = _model()
    wav = AF.resample(torch.from_numpy(audio).float().unsqueeze(0), sr, bundle.sample_rate)
    with torch.inference_mode():
        em, _ = model(wav)
    labels, out, prev = bundle.get_labels(), [], None
    for i in em[0].argmax(-1).tolist():
        if i != prev and i != 0:
            out.append(labels[i])
        prev = i
    return "".join(out).replace("|", " ").split()


def match(text, audio, sr):
    """How well a clip matches the sentence it should say, 0..1 (word-level similarity)."""
    return difflib.SequenceMatcher(None, words(text), heard(audio, sr)).ratio()


def words(text):
    """The aligner's view of a sentence: upper-case words of A-Z and apostrophes."""
    text = text.upper().replace("’", "'")
    return [w.strip("'") for w in re.sub(r"[^A-Z' ]", " ", text).split() if w.strip("'")]


def _silence_runs(audio, sr, below=35.0):
    """[(start, end)] of 10 ms frames quieter than the loud (95th percentile) level by `below` dB."""
    hop, win = int(0.01 * sr), int(0.025 * sr)
    frames = np.lib.stride_tricks.sliding_window_view(np.pad(audio, (0, win)), win)[::hop]
    db = 20 * np.log10(np.sqrt((frames ** 2).mean(1)) + 1e-9)
    sil = db < np.percentile(db, 95) - below
    runs, i = [], 0
    while i < len(sil):
        if sil[i]:
            j = i
            while j < len(sil) and sil[j]:
                j += 1
            if j - i >= 4:                   # at least 40 ms
                runs.append((i * 0.01, j * 0.01))
            i = j
        else:
            i += 1
    return runs


def sentence_spans(audio, sr, sentences):
    import torch
    import torchaudio.functional as AF

    bundle, model = _model()
    labels = bundle.get_labels()
    index = {c: i for i, c in enumerate(labels)}

    per = [words(s) for s in sentences]
    flat = [w for ws in per for w in ws]
    wav = AF.resample(torch.from_numpy(audio).float().unsqueeze(0), sr, bundle.sample_rate)
    with torch.inference_mode():
        emission, _ = model(wav)
        emission = torch.log_softmax(emission, dim=-1)
    targets = torch.tensor([[index[c] for c in "|".join(flat)]], dtype=torch.int32)
    try:
        ali, scores = AF.forced_align(emission, targets, blank=0)
    except RuntimeError as e:                 # more letters than audio frames: speech is missing
        raise AlignError(str(e)) from e
    spans = AF.merge_tokens(ali[0], scores[0].exp())
    sec = wav.size(1) / emission.size(1) / bundle.sample_rate

    wspans, cur = [], []
    for sp in spans:
        if labels[sp.token] == "|":
            wspans.append(cur)
            cur = []
        else:
            cur.append(sp)
    wspans.append(cur)
    if len(wspans) != len(flat) or any(not w for w in wspans):
        raise AlignError(f"{len(wspans)} word spans for {len(flat)} words")

    out, k = [], 0
    for ws in per:
        first, last = wspans[k], wspans[k + len(ws) - 1]
        out.append((first[0].start * sec, last[-1].end * sec))
        k += len(ws)

    # snap: a start to the end of the silence just before it (within 0.2 s), an end to the start of
    # the silence just after it (within 0.35 s), so no clip cuts into a word or a breath
    runs = _silence_runs(audio, sr)
    snapped = []
    for st, en in out:
        s = [b for a, b in runs if st - 0.2 <= b <= st + 0.1]
        e = [a for a, b in runs if en - 0.1 <= a <= en + 0.35]
        snapped.append((max(s) if s else st, min(e) if e else en))
    for i in range(len(snapped) - 1):         # a snap must never overlap the next sentence
        if snapped[i][1] > snapped[i + 1][0]:
            snapped[i], snapped[i + 1] = (snapped[i][0], out[i][1]), (out[i + 1][0], snapped[i + 1][1])
    for (a, b), (c, _) in zip(snapped, snapped[1:] + [(float("inf"), None)]):
        if not a < b <= c:
            raise AlignError(f"sentence span {a:.2f}-{b:.2f} s runs into the next at {c:.2f} s")
    return snapped
