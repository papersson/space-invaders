#!/bin/sh
# Run the agent three times, each on a fresh copy of sims/project, then scrub the records and save
# them to captures/. Usage: sh run_all.sh WORKROOT   (WORKROOT: a scratch folder outside the repo)
# Run 1 is the one the video replays (decided before any run was made); runs 2 and 3 are reported
# in data/runs.txt. The model is called with its own tools switched off (--tools ""), so the only
# things that act on the project are this folder's tools, run by agent.py.
set -e
cd "$(dirname "$0")"
W=${1:?scratch folder}
mkdir -p "$W" ../captures
run() {  # run number
  d="$W/run_$1"; rm -rf "$d"; cp -r project "$d"; rm -rf "$d/__pycache__"
  python3 agent.py "$d" "$W/run_$1.json" > "$W/run_$1.log" 2>&1
  python3 scrub.py "$W/run_$1.json" "$d" "../captures/run_$1.json"
}
run 1 & run 2 & run 3 & wait
python3 summarize.py ../captures > ../data/runs.txt
cat ../data/runs.txt
