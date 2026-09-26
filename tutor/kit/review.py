"""Run one review round on a lesson's SCRIPT.md with three fresh-context reviewers.

    python kit/review.py LESSON_DIR ROUND [--only expert,student,editor]

Each reviewer is a separate `claude -p` process (a fresh context) that sees only its own material:
  expert:  the script with screen notes, and the evidence table
  student: the learner model (who they are playing) and the script with screen notes
  editor:  the argument and chain, and the script with screen notes
The inputs are cut from SCRIPT.md by section and checked before anything runs, so the review log,
the ledgers and earlier reviews never reach a reviewer. Reviews are written to
research/reviews/roundNN_<role>.md, and each one's verdict line is printed.
"""
import re
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

KIT = Path(__file__).resolve().parent
LESSON = Path(sys.argv[1]).resolve()
ROUND = int(sys.argv[2])
ONLY = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else ["expert", "student", "editor"]
OUT = LESSON / "research" / "reviews"


def sections(text):
    parts = re.split(r"^## ", text, flags=re.M)
    return {p.split("\n", 1)[0].strip(): "## " + p for p in parts[1:]}


def learner_brief():
    t = (KIT.parent / "learner.md").read_text()
    s = sections(t)
    keep = [s[k] for k in ("Background", "Standing instructions for the student reviewer") if k in s]
    assert keep, "learner.md is missing its Background section"
    return "\n".join(keep).replace("## ", "")


def inputs():
    text = (LESSON / "SCRIPT.md").read_text()
    # A round reviews the revision made for it: the status line must name this round.
    assert f"review round {ROUND}" in text.split("\n## ", 1)[0], \
        f"SCRIPT.md status does not say 'before review round {ROUND}'; revise it first"
    s = sections(text)
    script, evidence = s["Script"], s["Evidence"]
    argument = s["Argument"] + "\n" + s["Chain"]
    prompts = {n: (KIT / "reviewers" / f"{n}.md").read_text() for n in ("expert", "student", "editor")}
    prompts["student"] = prompts["student"].replace("{{LEARNER}}", learner_brief())
    out = {
        "expert": prompts["expert"] + "\n\n---\n\n" + script + "\n" + evidence,
        "student": prompts["student"] + "\n\n---\n\n" + script,
        "editor": prompts["editor"] + "\n\n---\n\n" + argument + "\n" + script,
    }
    # Each reviewer sees only its own material.
    for name, text in out.items():
        assert "## Review log" not in text and "## Ledgers" not in text, name
        assert "VERDICT" not in text.split("---", 1)[1], name
        assert "## Script" in text and "### 1." in text, name
    assert "## Evidence" in out["expert"] and "| Claim |" in out["expert"]
    assert "## Evidence" not in out["student"] and "## Argument" not in out["student"]
    assert "## Evidence" not in out["editor"] and "## Argument" in out["editor"]
    return out


def run(item):
    name, text = item
    path = OUT / f"round{ROUND:02d}_{name}.md"
    r = subprocess.run(["claude", "-p"], input=text, capture_output=True, text=True, timeout=1800)
    path.write_text(r.stdout)
    verdict = [l for l in r.stdout.splitlines() if "VERDICT" in l]
    return name, verdict[-1].strip() if verdict else "(no verdict line)", len(r.stdout)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    todo = [(k, v) for k, v in inputs().items() if k in ONLY]
    for name, text in todo:
        (OUT / f"round{ROUND:02d}_{name}.input.md").write_text(text)
    with ThreadPoolExecutor(max_workers=3) as ex:
        for name, verdict, n in ex.map(run, todo):
            print(f"{name:8s} {verdict}  ({n} chars)")


if __name__ == "__main__":
    main()
