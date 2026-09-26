# Review

## BLOCKING

**Quote:** "Every block is still read once and written once, so this is a single pass, however many runs there are."

**What's wrong:** This is stated as an unconditional fact, but it's false in general and is directly contradicted by the very next section, which establishes that fan-in is capped at "one [block] per block of memory, minus one for the output." If there are more runs than memory has blocks for, you cannot merge them all in one pass — you need multiple merge rounds. As written, a student watching only this section learns something false (unlimited fan-in), and the next section then appears to retract it without ever flagging the retraction, which is confusing rather than a deliberate build-up.

**Fix:** Qualify the claim before generalizing, e.g.: *"Every block is still read once and written once, so merging is a single pass — as long as memory has a block for every run. [→ next section] How many runs is that?"* Let Section 5's question flow as an elaboration of a stated caveat, not as a surprise correction.

## SHOULD FIX

**Quote:** "One per block of memory, minus one for the output." … "holds about sixteen thousand blocks, so one merge can combine sixteen thousand runs." … Formula card: `passes = 1 + ⌈log_{M/B}(N/M)⌉`

**What's wrong:** The script states the fan-in rule correctly once (blocks minus one, for the output buffer), then silently drops the "−1" in both the 16,384-blocks arithmetic and the displayed formula (which uses `M/B` as the merge base rather than `M/B − 1`). It's a defensible asymptotic simplification (the two are algebraically equivalent up to the additive constant, and match the Aggarwal–Vitter/R&G formula that way), but stated right after emphasizing "minus one," the inconsistency looks like a mistake rather than an intentional approximation.

**Fix:** Either keep the −1 through all three restatements ("just under sixteen thousand runs"), or add one clause acknowledging the simplification, e.g.: *"...about sixteen thousand blocks — near enough sixteen thousand runs, once you set aside one block for output."*

**Quote:** "A laptop with sixteen gigabytes of memory and one-megabyte blocks holds about sixteen thousand blocks, so one merge can combine sixteen thousand runs. Two passes can sort files of hundreds of terabytes. Real systems share memory between jobs, and usually finish in two or three."

**What's wrong:** This generalization sits right after "It's exactly what sort did at the end," inviting the viewer to read it as "so the `sort` command would do this too." In fact GNU coreutils `sort` caps simultaneous merge inputs at a fixed default (`NMERGE` = 16, overridable only via `--batch-size`), independent of how much memory is available — it will *not* automatically widen its fan-in to thousands of runs just because the machine has 16 GB free. The theoretical bound is correct; the implicit link to the demonstrated tool is not.

**Fix:** Add a one-clause caveat separating the theoretical bound from the specific tool used in the demo, e.g.: *"That's the theoretical limit — real tools often cap it lower for other reasons (GNU sort merges at most 16 runs at a time by default), but database engines that tune this to available memory usually land in two or three passes."*

**Quote:** "In symbols: with N items, memory for M, and blocks of B, the number of passes grows as a logarithm of N over M, in base M over B."

**What's wrong:** Standard database textbooks (e.g., Ramakrishnan & Gehrke, the source cited in your own evidence table) use `B` for *number of buffer pages*, not block/page size — the opposite of this script's usage. A student who goes on to read that chapter will hit a symbol collision right where the material lines up otherwise exactly.

**Fix:** Either add a one-line disclaimer ("we're using B for block size here — some textbooks use B for the number of buffers instead") or rename the script's variable (e.g., use `b` for block size) to avoid the clash.

## NIT

**Quote:** "more than twenty times fewer I/Os"

**What's wrong:** "Times fewer" is a common but sloppy construction; also somewhat undersells the actual ratio (≈22.8×).

**Fix:** "well under a twentieth of the I/Os" or "nearly 23 times fewer I/Os."

**Quote:** "about a thousand times slower than reading memory"

**What's wrong:** Your own evidence table gives a range of roughly 500–1000× for SSD vs. memory latency; "about a thousand" is the top of that range, not a central estimate.

**Fix:** "several hundred to a thousand times slower" or simply hedge harder: "hundreds to a thousand times slower."

**Quote:** "Aggarwal and Vitter proved in 1988 that for comparison sorting, no algorithm can do asymptotically better."

**What's wrong:** The precise Aggarwal–Vitter lower bound is usually stated for the I/O model under the *indivisibility assumption* (records are atomic, movable but not decomposable) — a framing that is closely related to but not identical to "comparison sorting" in the classical RAM-model sense. Minor, but a domain expert would want the model named.

**Fix:** "...proved in 1988 that in this I/O model, no algorithm that treats records as indivisible units can do asymptotically better" (or keep current wording but add "in this disk-I/O model" for scoping).

VERDICT: REVISE
