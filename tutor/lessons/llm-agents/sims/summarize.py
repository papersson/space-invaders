"""Summarize the captured runs: per call, the tokens the model read; per run, the tools it asked
for and whether the test really passed afterwards (checked by us, outside the agent).
python3 summarize.py CAPTURES_DIR"""
import json
import sys
from pathlib import Path

from agent import parse_tool_call

caps = sorted(Path(sys.argv[1]).glob("*.json"))
for p in caps:
    r = json.loads(p.read_text())
    if "context" not in r:  # the Claude Code capture has its own format
        continue
    calls = r["calls"]
    steps = []
    for role, text in r["context"]:
        if role == "model":
            t = parse_tool_call(text)
            steps.append(t["tool"] + (f"({t['path']})" if "path" in t else "") if t else "reply")
    ctx = [c["context_tokens"] for c in calls]
    print(f"== {p.stem}: {len(calls)} model calls, test afterwards: {'PASS' if r['passed_after'] else 'FAIL'}"
          f" ({r['test_after'].strip().splitlines()[-1]})")
    print(f"   steps: {' > '.join(steps)}")
    print(f"   tokens read per call: {', '.join(f'{c:,}' for c in ctx)}; total {sum(ctx):,}")
    last = r["context"][-1]
    if last[0] == "model" and parse_tool_call(last[1]) is None:
        print(f"   final reply: {last[1][:400]!r}")
    print()

cc = Path(sys.argv[1]) / "claude_code_1.parsed.json"
if cc.exists():
    r = json.loads(cc.read_text())
    ctx = [c["context"] for c in r["calls"]]
    steps = " > ".join("+".join(t["name"] for t in c["tools"]) or "reply" for c in r["calls"])
    print(f"== claude_code_1 (Claude Code, stream-json): {len(ctx)} model calls, {r['summary']['tool_calls']} tool calls")
    print(f"   steps: {steps}")
    print(f"   tokens read per call: {', '.join(f'{c:,}' for c in ctx)}; total {sum(ctx):,}")
    print(f"   final reply: {r['summary']['final_text'][:400]!r}")
