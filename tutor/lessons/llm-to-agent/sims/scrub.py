"""Copy a run record into the repo with the scratch path, any model identifier and any email address
removed. python3 scrub.py RECORD.json WORKDIR OUT.json"""
import re
import sys
from pathlib import Path

src, workdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
s = Path(src).read_text()
s = s.replace(str(Path(workdir).resolve()), "<workdir>").replace(workdir, "<workdir>")
s = re.sub(r"claude-(?:opus|sonnet|haiku|fable|mythos|instant)[a-z0-9.\-]*", "<model>", s)
s = re.sub(r"[\w.+-]+@[\w-]+\.[\w.]+", "<email>", s)
s = re.sub(r"/tmp/claude-0/[^\s\"'\\]*", "<scratch>", s)
Path(out).write_text(s)
