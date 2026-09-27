"""Check that the code shown on screen runs: replay run 1's edits on a fresh copy of the project,
through the same tools the agent used, and run the tests and the program.

    python3 check_screen_code.py > ../data/screen_code_check.txt
"""
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

from agent import Tools, parse_request

HERE = Path(__file__).resolve().parent
run = json.loads((HERE.parent / "captures" / "run_1.json").read_text())
with tempfile.TemporaryDirectory() as tmp:
    work = Path(tmp) / "project"
    shutil.copytree(HERE / "project", work, ignore=shutil.ignore_patterns("__pycache__"))
    tools = Tools(work)
    print("before:", tools.run_tests().strip().splitlines()[-1])
    for role, text in run["context"]:
        if role == "model":
            req = parse_request(text)
            if req and req[0] == "edit_file":
                print(f"edit {req[1][0]}:", tools.run(req))
    for f in ("prices.py", "invoice.py"):
        src = (work / f).read_text()
        compile(src, f, "exec")
        for line in src.splitlines():
            if "key =" in line or "BULK:" in line:
                print(f"{f}: {line.strip()}")
    print("after:", tools.run_tests().strip().splitlines()[-1])
    out = subprocess.run([sys.executable, "invoice.py", "orders.csv"], cwd=work, capture_output=True, text=True)
    print("program:", " | ".join(out.stdout.strip().splitlines()))
