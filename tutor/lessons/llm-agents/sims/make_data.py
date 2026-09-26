"""Write data/strips.json: every run the video replays, as a strip of cards, from captures/.

Each card: kind (cli, instr, task, model, result), label and sub (short text on the card), text
(the real message, for cards that open), tokens (the width in the token view), and marks
(fail / pass / bom). Token widths: the tokens each call added to the context, measured as the
difference between consecutive calls' context sizes, split between that step's model card and
result card by characters. The first call's context is split into the command-line tool's notes
(the measured baseline, data/overhead.txt) and our system prompt plus task (split by characters).
The final reply is read by no call, so it has no token width.
    python3 make_data.py      (from sims/)
"""
import json
from pathlib import Path

from agent import parse_tool_call, render

HERE = Path(__file__).resolve().parent
CAP, DATA = HERE.parent / "captures", HERE.parent / "data"
BASE = 1179 - 2   # a one-character system prompt and prompt read 1,179 tokens (data/overhead.txt)


def model_card(reply):
    t = parse_tool_call(reply)
    if t is None:
        first = reply.strip().split("\n")[0]
        return {"kind": "model", "label": "Fixed." if first.startswith("Fixed") else "reply", "sub": "",
                "text": reply, "tool": None}
    verb = {"list_files": "list", "read_file": "read", "write_file": "write", "run_tests": "test"}[t["tool"]]
    return {"kind": "model", "label": verb, "sub": t.get("path", ""), "text": reply, "tool": t}


def result_card(text):
    marks = []
    if "KeyError" in text:
        marks.append("fail")
    if text.rstrip().endswith("OK"):
        marks.append("pass")
    if text.startswith("﻿"):
        marks.append("bom")
    return {"kind": "result", "label": "", "sub": "", "text": text, "marks": marks}


def strip(name):
    r = json.loads((CAP / f"{name}.json").read_text())
    ctx, calls = r["context"], r["calls"]
    sys_chars, task_chars = len(r["system"]), len(render(ctx[:1]))
    first = calls[0]["context_tokens"]
    ours = first - BASE
    cards = [{"kind": "cli", "label": "notes", "tokens": BASE},
             {"kind": "instr", "label": "instructions", "tokens": round(ours * sys_chars / (sys_chars + task_chars)),
              "text": r["system"]},
             {"kind": "task", "label": "task", "tokens": 0, "text": ctx[0][1]}]
    cards[2]["tokens"] = ours - cards[1]["tokens"]
    # pairs (model reply, tool result) after the task
    rest = ctx[1:]
    i, step = 0, 0
    while i < len(rest):
        m = model_card(rest[i][1])
        res = result_card(rest[i + 1][1]) if i + 1 < len(rest) and rest[i + 1][0] == "result" else None
        if res is not None and step + 1 < len(calls):
            added = calls[step + 1]["context_tokens"] - calls[step]["context_tokens"]
            a = len(render([rest[i]])) + 2
            b = len(render([rest[i + 1]])) + 2
            m["tokens"] = round(added * a / (a + b))
            res["tokens"] = added - m["tokens"]
        else:
            m["tokens"] = 0          # read by no call (the last reply, or an unanswered tool call)
            if res is not None:
                res["tokens"] = 0
        cards.append(m)
        if res is not None:
            cards.append(res)
        i += 2 if res is not None else 1
        step += 1
    return {"name": name, "cards": cards, "calls": [c["context_tokens"] for c in calls],
            "passed_after": r["passed_after"], "test_after": r["test_after"].strip().splitlines()[-1],
            "last_error": next((l for l in r["test_after"].splitlines() if l.startswith("KeyError")), "")}


def main():
    out = {n: strip(n) for n in ["bare_1", "one_tool_1", "loop_1", "no_tests_1", "no_tests_strong_1",
                                  "no_tests_strong_2", "no_tests_strong_3"]}
    cc = json.loads((CAP / "claude_code_1.parsed.json").read_text())
    out["claude_code_1"] = {"calls": [c["context"] for c in cc["calls"]],
                            "tool_calls": cc["summary"]["tool_calls"], "total": cc["summary"]["tokens_read_total"]}
    for n in ["loop_1", "no_tests_1"]:
        s = out[n]
        # check: the token widths add up to each call's context
        tot, k = 0, 0
        for c in s["cards"]:
            tot += c["tokens"]
        assert tot == s["calls"][-1], (n, tot, s["calls"][-1])
    (DATA / "strips.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
    for n, s in out.items():
        if "cards" in s:
            print(n, len(s["cards"]), [(c["kind"][0], c.get("label"), c.get("sub"), c["tokens"]) for c in s["cards"]][:24])


if __name__ == "__main__":
    main()
