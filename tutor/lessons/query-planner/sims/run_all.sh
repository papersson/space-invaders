#!/bin/sh
# Rebuild the data set and rerun every query in the lesson; output goes to data/runs.txt.
# Needs a running PostgreSQL 16 reachable as: psql -h $PGHOST -d postgres (this lesson used the
# Nix package postgresql_16 from Nixpkgs 24.11, revision 50ab793786d9).
set -e
cd "$(dirname "$0")"
psql -q -d postgres -f setup.sql > /dev/null
psql -d postgres -f queries.sql > ../data/runs.txt 2>&1
cat ../data/runs.txt
