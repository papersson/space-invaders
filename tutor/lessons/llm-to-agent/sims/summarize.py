"""Summarize the captured runs: the requests in order, the tokens the model read on each call, and
whether the tests really passed afterwards (checked outside the agent). python3 summarize.py CAPTURES"""
import json
import sys
from pathlib import Path

from agent import parse_request


def short(req):
    kind, args = req
    return {"search": lambda: f"search: {args[0]}", "open_file": lambda: f"open file: {args[0]}",
            "edit_file": lambda: f"edit file: {args[0]}", "run_tests": lambda: "run tests"}[kind]()


for p in sorted(Path(sys.argv[1]).glob("run_*.json")):
    r = json.loads(p.read_text())
    steps = []
    for i, (role, text) in enumerate(r["context"]):
        if role == "model":
            q = parse_request(text)
            if q is None:
                steps.append("reply")
                continue
            res = r["context"][i + 1][1] if i + 1 < len(r["context"]) else ""
            tag = ""
            if q[0] == "run_tests":
                tag = " [" + res.strip().splitlines()[-1] + "]"
            steps.append(short(q) + tag)
    ctx = [c["context_tokens"] for c in r["calls"]]
    print(f"== {p.stem}: {len(ctx)} model calls, tests afterwards: {'PASS' if r['passed_after'] else 'FAIL'}; "
          f"program afterwards: {' '.join(r['program_after'].split())}")
    for n, s in enumerate(steps, 1):
        print(f"   {n:2d}. {s}")
    print(f"   tokens read per call: {', '.join(f'{c:,}' for c in ctx)}; total {sum(ctx):,}")
    last = r["context"][-1]
    if last[0] == "model" and parse_request(last[1]) is None:
        print(f"   final reply: {last[1]!r}")
    print()
