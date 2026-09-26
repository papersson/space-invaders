#!/bin/sh
# Re-run every program behind a number in the lesson; output goes to data/runs.txt.
set -e
cd "$(dirname "$0")"
{
  echo "== counter.c: two threads, 10,000,000 increments each (expected 20,000,000)"
  gcc -O2 -pthread -o /tmp/counter counter.c
  echo "no lock:";   for i in 1 2 3 4 5; do /tmp/counter 0; done
  echo "with lock:"; for i in 1 2 3; do /tmp/counter 1; done
  echo "== locks/: transfers A->B and B->A with two mutexes"
  (cd locks && go run .)
  echo "== deadlock/: transfers A->B and B->A between two account processes over unbuffered channels"
  (cd deadlock && go run .)
  echo "== race/: two cash machines, balance \$100, each withdraws \$100 if it saw at least \$100"
  (cd race && go run .)
  echo "== $(gcc --version | head -1); $(go version); $(nproc) CPUs"
} > ../data/runs.txt 2>&1
cat ../data/runs.txt
