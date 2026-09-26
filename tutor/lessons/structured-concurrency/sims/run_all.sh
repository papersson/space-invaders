#!/bin/sh
# Rerun every demo in the lesson; the output goes to data/runs.txt and data/timeline.json.
set -e
cd "$(dirname "$0")"
{
  echo "##### Python asyncio: sims/handler.py"
  python3 handler.py
  echo
  echo "##### Control: a plain task's unretrieved error is logged (sims/control_unretrieved.py)"
  python3 control_unretrieved.py 2>&1 | head -2
  echo
  echo "##### Go: sims/goleak (errgroup from golang.org/x/sync)"
  (cd goleak && go run .)
} > ../data/runs.txt 2>&1
cat ../data/runs.txt
