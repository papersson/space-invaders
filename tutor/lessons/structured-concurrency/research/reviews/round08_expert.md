I reviewed this against the project's primary sources rather than taking the evidence table on faith — the actual sim code (`sims/handler.py`, `sims/except_check.py`, `sims/control_unretrieved.py`, `sims/goleak/main.go`), the measured output (`data/runs.txt`, `data/timeline.json`, `data/except_check.txt`), the verified docstrings/primary-sources files, and the two research dossiers. I also found this script is byte-for-byte what went through seven prior expert/editor/student review rounds (all VERDICT: PASS) — so I cross-checked my own findings against theirs rather than duplicating their work, and looked specifically for anything a correctness-focused pass might still catch.

Every number checks out exactly against `data/runs.txt`/`data/timeline.json` (0.10 s, 1.00 s, 1.10 s, 0.50 s, 1.2 s, 1,000/0 leftover counts, the Go 0.11 s figures), every quoted doc/docstring text matches `verified_python_docstrings.txt`/`verified_primary_sources.md` verbatim, the JEP numbering and Dijkstra/Wirth/Sústrik/Smith history matches `canonical_web_agent.md`, and the `except ConnectionError` vs `except*` behavior matches `data/except_check.txt`. No arithmetic, unit, or attribution errors.

## Findings

**SHOULD FIX** — Quote: *"Structured concurrency gives every task an owner: a block that can't end until its tasks have. When one fails, the rest are cancelled and the error comes back. When the caller is cancelled, so are its tasks."* (Ch. 8)
Problem: Ch. 5 correctly scopes the three guarantees to *a task group* (the concrete `asyncio.TaskGroup` just demonstrated). Ch. 8 restates them under the general term "structured concurrency," which turns a demonstrated *policy* into an implied universal law. The project's own research file lists this exact move as a standard overstatement: *"'A child failure always cancels its siblings.' False for Swift `TaskGroup` unless the body rethrows, false for supervisor scopes, false for Go errgroup goroutines that ignore `ctx`, and false for Rust `thread::scope`"* (`canonical_web_agent.md` §9). The video even names Swift/Java/Kotlin two lines earlier without showing their cancellation semantics, so the generalization isn't earned by what's on screen.
Corrected wording: Keep the subject concrete rather than switching to the abstract term for the two policy-guarantees, e.g.: *"A task group gives every task an owner: a block that can't end until its tasks have. In the systems shown here, when one fails, the rest are cancelled and the error comes back; when the caller is cancelled, so are its tasks."*

**SHOULD FIX** (confirms, from a correctness angle, the editor's F1) — Quote: *"ending `except* Exception as eg:` with a log line: `return` is not allowed inside an `except*` block"* (Ch. 5 screen note)
This restriction is real (a PEP 654 syntax restriction on jumping out of an `except*` suite), and it's consistent with the actual repo — `sims/handler.py`'s `handler_taskgroup` deliberately never uses `return` inside its `except*` clause. I could not execute Python in this review pass to re-verify the precise scope against Python 3.11.15 myself (tooling in this session blocked interpreter execution), so this rests on the codebase's own consistency plus my own recollection rather than a fresh empirical check. Recommend one quick `compile()` sanity check before lock, since it's a specific, falsifiable syntax claim placed on screen as fact.

**NIT** (still open from round 7) — Quote: *"a name Martin Sústrik had given it two years earlier"* (Ch. 4)
Correct as stated (Sústrik 2016, Smith 2018-04-25), but `canonical_web_agent.md`'s own source table flags the exact month of Sústrik's 2016 post as **[uncertain]**. The script doesn't state a month, so it isn't exposed — flagging only so a future edit doesn't add one without re-checking.

**NIT** — Quote: *"It arrives inside an exception group, a container for errors, since more than one task could fail."* (Ch. 5)
The general justification for `ExceptionGroup` (it can hold several errors) is correct, but paired with the concrete `[ConnectionError]` run right after, a viewer could momentarily expect two errors where there's one. Corrected wording: *"...a container for errors, since a task group could have more than one task fail at once — here, just the one."*

**NIT** (still open from round 7) — Quote: *"Swift and Java have the same kind of block built in, Java's still as a preview feature."* (Ch. 7)
Factually fine (JEP 533: preview through JDK 27), just a parse hazard on first hearing. Corrected wording: *"Swift and Java have the same kind of block built in — Java's is still a preview feature."*

Nothing here is BLOCKING: no wrong number, no misattributed quote, no fabricated API behavior. The one genuinely new item (Ch. 8's generalization) is a hedge, not a rewrite of the argument, and the rest are either already-known nits or a recommended pre-flight check rather than corrections to something stated wrong.

VERDICT: PASS
