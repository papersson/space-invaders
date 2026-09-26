#!/bin/sh
# The same task, run once by a production agent harness (Claude Code), captured as stream-json.
# Its tools are limited to reading, editing and one test command; nothing else is allowed.
# Usage: sh run_claude_code.sh WORKROOT   (a scratch folder outside the repo)
set -e
cd "$(dirname "$0")"
H=$(pwd)
W=${1:?scratch folder}
d="$W/claude_code_1"; rm -rf "$d"; cp -r project "$d"
(cd "$d" && claude -p "The test in test_report.py fails. Fix report.py so that the test passes." \
   --output-format stream-json --verbose --tools "Read,Edit,Bash" \
   --allowedTools "Read" "Edit" "Bash(python3 -m unittest*)" --permission-prompts none \
   --no-session-persistence < /dev/null > "$W/claude_code_1.jsonl")
python3 parse_stream.py "$W/claude_code_1.jsonl" "$W/claude_code_1.parsed.json"
python3 scrub.py "$W/claude_code_1.jsonl" "$d" ../captures/claude_code_1.jsonl
python3 scrub.py "$W/claude_code_1.parsed.json" "$d" ../captures/claude_code_1.parsed.json
(cd "$d" && python3 -m unittest 2>&1 | tail -1)
