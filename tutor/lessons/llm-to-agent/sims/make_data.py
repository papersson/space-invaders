"""Write data/trace.json, the replay the scenes draw from, out of the captured runs.

    python3 make_data.py

Every piece of text the video shows from a run is cut from the capture itself, and checked here to
be a substring of the real request or result, so the screen can only abridge, never invent.
"""
import json
from pathlib import Path

from agent import parse_request

ROOT = Path(__file__).resolve().parent.parent
run = json.loads((ROOT / "captures" / "run_1.json").read_text())
bare = json.loads((ROOT / "captures" / "bare_1.json").read_text())
ctx = run["context"]

# For each request: the excerpt of its result to show (a line of the real result), and any tag.
SHOW = {
    1: ("prices.py:8: raise LookupError", None),
    2: ('PRICES = {… "Gadget": 10.00, …', None),
    3: ('invoice.py:16: cost = quantity * price_of(row["product"])', None),
    4: ("if quantity > BULK:", None),
    5: ("edited prices.py", "gadget → Gadget"),
    6: ("AssertionError: 39.5 != 37.0", None),
    7: ("edited prices.py", "no real change"),
    8: ('… owed["Ben"], 37.00)', None),
    9: ("invoice.py:17: if quantity > BULK:", None),
    10: ("Ben,Widget,10", None),
    11: ("edited invoice.py", "> BULK  →  >= BULK"),
    12: ("OK", None),
}

steps, n = [], 0
for i, (role, text) in enumerate(ctx):
    if role != "model":
        continue
    req = parse_request(text)
    if req is None:
        steps.append({"kind": "reply", "request": None, "text": text})
        continue
    n += 1
    result = ctx[i + 1][1]
    first = text.strip().splitlines()[0].strip()
    # the request as the model wrote it: first line (an edit's first line names the file)
    line = next(l.strip() for l in text.splitlines() if l.strip().startswith(("search:", "open file:", "edit file:", "run tests")))
    show, tag = SHOW[n]
    # an excerpt may be abridged with "…": each piece must appear in the result, in order
    pos = 0
    for piece in [x.strip() for x in show.split("…") if x.strip()]:
        pos = result.index(piece, pos) + len(piece)
    status = None
    if req[0] == "run_tests":
        status = "pass" if result.rstrip().endswith("OK") else "fail"
    steps.append({"n": n, "kind": req[0], "request": line, "result_excerpt": show, "tag": tag,
                  "status": status, "result_lines": len(result.strip().splitlines())})

# the checks behind the tags
assert "key = product.strip().title()" in ctx[9][1]
e7 = [s for s in steps if s.get("n") == 7][0]
old7 = ctx[13][1].split("replace:")[1].split("with:")[0].strip()
new7 = ctx[13][1].split("with:")[1].split("end edit")[0].strip()
assert old7 == new7, "request 7 changes more than blank lines"
assert "if quantity >= BULK:" in ctx[21][1] and "if quantity > BULK:" in ctx[21][1]

reply = steps[-1]["text"]
assert reply.rstrip().endswith("Tests now pass.")
fail = ctx[12][1]
assert "AssertionError: 39.5 != 37.0 within 7 places (2.5 difference)" in fail
assert 'owed["Ben"], 37.00' in fail

bare_first = bare["reply"].splitlines()[0]
assert bare_first == "I'll start by exploring the project structure to find the relevant code."
assert "**Tool: bash**" in bare["reply"] and "find " in bare["reply"] and "-type f" in bare["reply"]

task = run["task"]
assert "LookupError: no price for 'gadget'" in task
system = run["system"]
formats = ["search: TEXT", "open file: NAME", "edit file: NAME", "run tests"]
for f in formats:
    assert f in system, f

nw = json.loads((ROOT / "data" / "next_word.json").read_text())
cmp_ = json.loads((ROOT / "data" / "compound.json").read_text())

out = {
    "task_lines": ["… stops with this error:", "LookupError: no price for 'gadget'", "Please fix it, and check that", "the tests pass."],
    "formats": formats,
    "bare": {"first": bare_first, "tool": "Tool: bash · find … -type f …", "test_after": bare["test_after"].strip().splitlines()[-1]},
    "steps": steps,
    "reply_excerpt": "… Tests now pass.",
    "context_chars": [c["prompt_chars"] for c in run["calls"]],
    "next_word": [[c["token"].strip(), c["p"]] for c in nw["steps"][0]["top"]],
    "then": [[s["top"][0]["token"].strip(), s["top"][0]["p"]] for s in nw["steps"][1:]],
    "runs95": [round(100 * 0.95 ** k) for k in range(1, 21)],
    "runs99": [round(100 * 0.99 ** k) for k in range(1, 21)],
}
assert out["runs95"][-1] == round(100 * cmp_["p"]["0.95"][20]) == 36
assert out["runs99"][-1] == round(100 * cmp_["p"]["0.99"][20]) == 82
assert out["runs95"][1] == 90
(ROOT / "data" / "trace.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
for s in steps:
    print(s.get("n"), s["kind"], s.get("request"), "|", s.get("result_excerpt"), "|", s.get("tag"), s.get("status"))
print(out["runs95"])
print(out["runs99"])
