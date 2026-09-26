I reviewed the script against the actual project sources — `sims/handler.py`, `sims/goleak/main.go`, `data/runs.txt`, `data/timeline.json`, and the verified-primary-sources files — rather than taking the evidence table on faith, and I found this is deep into an existing review pipeline (round 7 of expert/editor/student passes; rounds 1–6 already fixed the JEP-number sourcing, the Dijkstra/Wirth title credit, the bare-`except` code/narration mismatch, the `except*` mention, the Kotlin-vs-Swift/Java "built in" distinction, and the errgroup cooperative-cancellation caveat). I re-verified all of those fixes are actually present and correct in this text, then looked for anything new. Here is what I found.

## Findings

**NIT** — Quote: *"Swift and Java have the same kind of block built in, Java's still as a preview feature."* (ch. 7)
Problem: "Java's still as a preview feature" is grammatically ambiguous on first read (parses momentarily as "Java's still" + "as a preview feature"). Not a factual error — Java's `StructuredTaskScope` genuinely is preview-only through JDK 27 per JEP 533 — just a parse hazard for narration.
Corrected wording: "Swift and Java have the same kind of block built in — Java's is still a preview feature."

**NIT** (weighting, not correctness) — Quote: *"Swift and Java have the same kind of block built in, Java's still as a preview feature. Kotlin has it in its official coroutines library."* (ch. 7)
Problem: this names three more languages with zero mechanism, code, or number after a fully-instrumented Go section (real code, a real goroutine-leak count, a real fix). It isn't wrong — every claim in it checks out against the research file (`canonical_web_agent.md` §8: Swift is a language feature since 5.5; Java's `StructuredTaskScope` is preview-only through JDK 27; Kotlin's `coroutineScope` is in `kotlinx.coroutines`, not the stdlib) — but as a professor I'd flag it as the one place the script trades depth for a list. This is the same thing the round-7 editor pass already caught (Test 9/11) from a pacing angle; from a canonicity angle it's defensible under the lesson's own "leave out: Swift priority escalation… Kotlin `Job` wiring" scoping rule in the research, so I wouldn't block on it — but I'd side with the editor's rewrite (give the sentence one concrete grip, e.g. naming `async let`/`StructuredTaskScope`/`coroutineScope` as the same shape) over cutting it, since dropping it entirely would leave the "not just a Python or Go thing" claim resting on Go alone.

**NIT** — Quote: *"a name Martin Sústrik had given it two years earlier"* (ch. 4)
Problem: this is correct (Sústrik 2016, Smith 2018) but the research file itself flags the exact month of Sústrik's 2016 post as **[uncertain]** (`canonical_web_agent.md`, source key table: "The exact month in 2016 is [uncertain]"). The script doesn't state a month, only "two years earlier," so it isn't exposed to this uncertainty — just noting it so nobody later "improves" the line by adding a month without re-checking.

## What I re-verified holds up

- The central technical claim of the whole video — that `gather`'s sibling task, once orphaned, fails silently with *no* log message, unlike a plain unretrieved task's `"Task exception was never retrieved"` — is exactly what CPython's `gather()` does: its per-child done-callback calls `child.exception()` purely to mark it retrieved even after the outer future is already resolved, which suppresses the logger while still discarding the result. The script's `control_unretrieved.py` contrast run makes this an apples-to-apples demonstration, not an assertion. Correct and non-trivial to get right.
- Every timestamp in the narration (0.10 s, 1.00 s, 1.10 s, 0.50 s, 1.2 s, 1,000/0 leftover counts, the Go 0.11 s figures) matches `data/runs.txt` exactly, including the retry-loop arithmetic (cancelled at 0.10 s mid-sleep, full 1.0 s retry → 1.10 s return).
- The `asyncio.gather` and `asyncio.TaskGroup` quotes shown on screen match the cited docs verbatim (`verified_python_docstrings.txt`, `verified_primary_sources.md`).
- The JEP numbering (533 = seventh preview/JDK 27, 543 = Candidate targeting JDK 28) matches the openjdk.org check recorded in `verified_primary_sources.md`, including the full preview history (428→437→453→462→480→499→505→525→533).
- The Dijkstra/Wirth title-credit, Sústrik's 2016 coinage, and Smith's exact 2018 essay title are all correct and sourced.
- The Go code shown (`main.go`) matches the on-screen snippets and the channel-leak mechanism narrated in ch. 7 exactly.
- Cooperative cancellation, the `except*`/`ExceptionGroup` mechanics, the "only tasks created through the group" scoping limit, and the "not about shared data" caveat are all stated with the correct hedges and match the TaskGroup docstring and `canonical_web_agent.md` §4's guarantee list (G2–G5) precisely — no overstated generality anywhere I could find.

Nothing here rises to a level a professor would object to on camera; the round-1–6 process has already caught and fixed everything that would have been BLOCKING or SHOULD FIX. My own pass adds only cosmetic items.

VERDICT: PASS
