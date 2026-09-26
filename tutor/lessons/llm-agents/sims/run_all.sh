#!/bin/sh
# Run every variant of the agent on a fresh copy of sims/project, then scrub and save the records
# to captures/. Usage: sh run_all.sh WORKROOT   (WORKROOT: a scratch folder outside the repo)
# The first run of each variant is the one the video replays; the repeats are reported as counts.
set -e
cd "$(dirname "$0")"
W=${1:?scratch folder}
mkdir -p "$W" ../captures
run() {  # variant, run number
  d="$W/$1_$2"; rm -rf "$d"; cp -r project "$d"
  python3 agent.py "$1" "$d" "$W/$1_$2.json" > "$W/$1_$2.log" 2>&1
  python3 scrub.py "$W/$1_$2.json" "$d" "../captures/$1_$2.json"
}
run loop 1 & run no_tests 1 & run bare 1 & run one_tool 1 & wait
run loop 2 & run no_tests 2 & run loop 3 & run no_tests 3 & wait
python3 summarize.py ../captures > ../data/runs.txt
cat ../data/runs.txt
