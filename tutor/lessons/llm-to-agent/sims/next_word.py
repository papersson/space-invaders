"""Real next-word probabilities from a small open model (GPT-2, the 124M-parameter version, 2019).

    HF_HOME=... python next_word.py ../data/next_word.json

For the prompt, prints the model's top candidates for the next piece of text and their
probabilities (softmax of the final logits, no temperature), then adds the most likely one and
repeats: the model predicting the next word, over and over. Every candidate shown in the video is a
whole word with its leading space, so "next word" is exact for this example (in general a model
predicts a token, a word or a piece of one).
"""
import json
import sys

import torch
import transformers
from transformers import AutoModelForCausalLM, AutoTokenizer

MODEL, PROMPT, STEPS, TOP = "gpt2", "I made a cup of", 3, 5

tok = AutoTokenizer.from_pretrained(MODEL)
model = AutoModelForCausalLM.from_pretrained(MODEL).eval()
ids = tok(PROMPT, return_tensors="pt").input_ids
steps = []
for _ in range(STEPS):
    with torch.no_grad():
        p = torch.softmax(model(ids).logits[0, -1].double(), -1)
    top = torch.topk(p, TOP)
    cands = [{"token": tok.decode([i]), "p": round(v, 4), "whole_word": tok.decode([i]).startswith(" ")}
             for v, i in zip(top.values.tolist(), top.indices.tolist())]
    steps.append({"text": tok.decode(ids[0]), "top": cands})
    ids = torch.cat([ids, top.indices[:1].view(1, 1)], 1)
out = {"model": MODEL, "parameters": sum(t.numel() for t in model.parameters()),
       "transformers": transformers.__version__, "torch": torch.__version__,
       "prompt": PROMPT, "decoding": "most likely next token each step (greedy)", "steps": steps,
       "final_text": tok.decode(ids[0])}
open(sys.argv[1], "w").write(json.dumps(out, indent=1))
for s in steps:
    print(repr(s["text"]), " | ".join(f"{c['token']!r} {c['p']:.3f}" for c in s["top"]))
print(out["parameters"], "parameters")
