"""Check every piece of code the video shows, by running it. Output: data/screen_code_check.txt
    python3 check_screen_code.py      (from sims/)
"""
import inspect
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import agent

HERE = Path(__file__).resolve().parent
CAP = HERE.parent / "captures"
out = []

# 1. the loop on screen (ch. 4) is agent.agent's own source: it compiles, and it is the function that ran
src = inspect.getsource(agent.agent)
compile(src, "agent.py", "exec")
out.append(f"agent(): source compiles ({len(src.splitlines())} lines), shown verbatim from sims/agent.py")

# 2. the tool formats on screen (ch. 3) are valid JSON, and the parser reads each as a tool call
for name, doc in agent.TOOL_DOCS.items():
    j = doc.split("  ")[0]
    obj = json.loads(j)
    assert agent.parse_tool_call(j) == obj and obj["tool"] == name
    out.append(f"tool format {j}: valid JSON, parsed as tool {name}")

# 3. the bug line (ch. 4) is in the project's report.py as the model read it
BUG = 'totals[region] = totals.get(region, 0) + int(row["units"]) + float(row["unit_price"])'
FIX = 'totals[region] = totals.get(region, 0) + int(row["units"]) * float(row["unit_price"])'
OPEN = 'with open(path, newline="", encoding="utf-8-sig") as f:'
assert BUG in (HERE / "project" / "report.py").read_text()
out.append("bug line: present in sims/project/report.py")

# 4. run A's two writes, replayed on a fresh copy: the first has FIX and still fails; the second adds OPEN and passes
ctx = json.loads((CAP / "loop_1.json").read_text())["context"]
writes = [agent.parse_tool_call(t) for r, t in ctx if r == "model" and (agent.parse_tool_call(t) or {}).get("tool") == "write_file"]
assert len(writes) == 2
with tempfile.TemporaryDirectory() as d:
    shutil.copytree(HERE / "project", d, dirs_exist_ok=True)
    for i, w in enumerate(writes, 1):
        (Path(d) / w["path"]).write_text(w["content"])
        compile(w["content"], "report.py", "exec")
        r = subprocess.run([sys.executable, "-m", "unittest"], cwd=d, capture_output=True, text=True)
        last = (r.stdout + r.stderr).strip().splitlines()[-1]
        has = [n for n, l in (("FIX", FIX), ("OPEN", OPEN)) if l in w["content"]]
        out.append(f"run A write {i}: compiles, contains {'+'.join(has)}; test: {last}")
assert FIX in writes[0]["content"] and OPEN not in writes[0]["content"] and OPEN in writes[1]["content"]

text = "\n".join(out) + "\n"
(HERE.parent / "data" / "screen_code_check.txt").write_text(text)
print(text)
