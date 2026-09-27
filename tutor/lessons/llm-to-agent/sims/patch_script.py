"""Apply exact replacements to SCRIPT.md: every old string must match exactly once, or nothing is written.
python3 patch.py SCRIPT.md patches.json   (a JSON list of [old, new])"""
import json, sys
path, pf = sys.argv[1], sys.argv[2]
s = open(path).read()
pairs = json.load(open(pf))
bad = [(i, s.count(o)) for i, (o, n) in enumerate(pairs) if s.count(o) != 1]
if bad:
    for i, c in bad:
        print(f"patch {i}: matched {c} times: {pairs[i][0][:80]!r}")
    sys.exit(1)
for o, n in pairs:
    s = s.replace(o, n)
open(path, "w").write(s)
print(f"applied {len(pairs)} patches")
