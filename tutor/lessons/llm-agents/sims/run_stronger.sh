#!/bin/sh
# Run B (the loop without run_tests) three more times with a more capable model than the claude
# command-line tool's default, chosen by its alias through AGENT_MODEL (the alias is passed at run
# time and not recorded). Usage: AGENT_MODEL=<alias> sh run_stronger.sh WORKROOT
set -e
cd "$(dirname "$0")"
W=${1:?scratch folder}
: "${AGENT_MODEL:?set AGENT_MODEL to the model alias}"
mkdir -p "$W"
run() {
  d="$W/no_tests_strong_$1"; rm -rf "$d"; cp -r project "$d"
  python3 agent.py no_tests "$d" "$W/no_tests_strong_$1.json" > "$W/no_tests_strong_$1.log" 2>&1
  python3 scrub.py "$W/no_tests_strong_$1.json" "$d" "../captures/no_tests_strong_$1.json"
}
run 1 & run 2 & run 3 & wait
python3 summarize.py ../captures > ../data/runs.txt
grep -A4 "no_tests_strong" ../data/runs.txt
