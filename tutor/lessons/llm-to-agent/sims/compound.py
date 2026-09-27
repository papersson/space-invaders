"""The compounding arithmetic: if each step of a task goes right with probability p, independently,
and nothing catches a mistake, all n steps go right with probability p ** n.

    python3 compound.py ../data/compound.json
"""
import json
import sys

rows = {str(p): [round(p ** n, 4) for n in range(0, 21)] for p in (0.95, 0.99)}
out = {"model": "p ** n: independent steps, no mistake caught or undone", "n": list(range(0, 21)), "p": rows,
       "check": {"0.95**20": round(0.95 ** 20, 4), "0.99**20": round(0.99 ** 20, 4)}}
open(sys.argv[1], "w").write(json.dumps(out, indent=1))
print(out["check"])
