"""The same model on its own: one call, no request format, no program to carry anything out.

    python3 bare.py WORKDIR OUT.json

Same task as agent.py; the model is asked through the same command-line tool with its own tools
switched off, from a copy of the project, so it could not read or change a file even if it tried.
Afterwards the tests are run, to show that nothing changed."""
import json
import subprocess
import sys
from pathlib import Path

from agent import TASK, Tools

SYSTEM = "You are a helpful assistant."

workdir, out = sys.argv[1], sys.argv[2]
r = subprocess.run(["claude", "-p", "--tools", "", "--system-prompt", SYSTEM, "--output-format", "json",
                    "--no-session-persistence", "--safe-mode", "--disable-slash-commands", "--strict-mcp-config"],
                   input=TASK, capture_output=True, text=True, timeout=600, cwd=workdir)
reply = json.loads(r.stdout)["result"].strip()
after = Tools(workdir).run_tests()
Path(out).write_text(json.dumps({"task": TASK, "system": SYSTEM, "reply": reply, "test_after": after,
                                 "passed_after": after.rstrip().endswith("OK")}, indent=1))
print(reply)
print("TEST AFTER:", after.strip().splitlines()[-1])
