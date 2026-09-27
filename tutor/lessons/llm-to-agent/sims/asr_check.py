"""The audio review, since the narration can't be listened to here: transcribe every sentence's clip
from audio/narration.wav with a speech recogniser (wav2vec2, greedy CTC) and compare it with the text
that should have been spoken. Low scores mark sentences to listen to or re-render.

    TTS-venv python asr_check.py [LESSON_COPY] > ../data/narration_asr_check.txt
"""
import difflib
import json
import re
import sys
from pathlib import Path

import soundfile as sf
import torch
import torchaudio

HOME = Path(__file__).resolve().parent.parent
ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else HOME
sys.path.insert(0, str(HOME.parent.parent / "kit"))
sys.argv = [sys.argv[0], str(ROOT)]
import narration  # noqa: E402  (for say() and spoken(), as the engine used them)
from align import words  # noqa: E402

t = json.loads((ROOT / "audio" / "timings.json").read_text())
audio, sr = sf.read(ROOT / "audio" / "narration.wav", dtype="float32")
bundle = torchaudio.pipelines.WAV2VEC2_ASR_BASE_960H
model = bundle.get_model().eval()
labels = bundle.get_labels()
worst = []
for seg in t["segments"]:
    for ln in seg["lines"]:
        a, b = int(max(ln["start"] - 0.05, 0) * sr), int((ln["end"] + 0.05) * sr)
        wav = torchaudio.functional.resample(torch.from_numpy(audio[a:b]).unsqueeze(0), sr, bundle.sample_rate)
        with torch.inference_mode():
            em, _ = model(wav)
        ids = em[0].argmax(-1).tolist()
        out, prev = [], None
        for i in ids:
            if i != prev and i != 0:
                out.append(labels[i])
            prev = i
        heard = "".join(out).replace("|", " ").split()
        want = words(narration.say(narration.spoken(ln["caption"], ln["id"])))
        r = difflib.SequenceMatcher(None, want, heard).ratio()
        worst.append((r, ln["id"]))
        flag = "  <-- check" if r < 0.75 else ""
        print(f"{ln['id']} {r:.2f} {b / sr - a / sr:5.2f}s  heard: {' '.join(heard).lower()}{flag}")
print("lowest:", ", ".join(f"{i} {r:.2f}" for r, i in sorted(worst)[:8]))
