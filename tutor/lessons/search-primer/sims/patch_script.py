"""Apply exact text replacements to SCRIPT.md; every replacement must match exactly once, or nothing is written.

    python sims/patch_script.py PATCH.json      # [[old, new], ...]
"""
import json
import sys
from pathlib import Path

P = Path(__file__).resolve().parent.parent / "SCRIPT.md"
s = P.read_text()
pairs = json.loads(Path(sys.argv[1]).read_text())
bad = [(i, s.count(o)) for i, (o, _) in enumerate(pairs) if s.count(o) != 1]
if bad:
    for i, n in bad:
        print(f"replacement {i} matched {n} times: {pairs[i][0][:90]!r}")
    sys.exit(1)
for o, n in pairs:
    s = s.replace(o, n)
P.write_text(s)
print(f"applied {len(pairs)} replacements")
