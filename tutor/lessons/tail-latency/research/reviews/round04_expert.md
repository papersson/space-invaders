I verified the script's numeric claims against the primary source (Dean & Barroso 2013) via this project's own fact-checked research notes (`lessons/tail-latency/research/canonical_web_agent.md`), which quote the paper directly. The core arithmetic (0.99¹⁰⁰≈37%, 63% slow), the Table 1 figures (10ms → 140ms), and the Bigtable hedging numbers (1,000 keys/100 servers, 10ms trigger, 1,800ms→74ms, +2%) all check out exactly against the verified quotes. The script is unusually careful — it states the independence assumption before using it, avoids the "1ms average / 1s p99" impossibility that even Dean's own talk slides get wrong, and closes with the correlation caveat instead of overselling hedging as a universal fix. Here are the issues I did find.

## Findings

**SHOULD FIX** — Section 3, screen note and narration: *"one server's own ninety-ninth percentile was just ten milliseconds. But for a request that waited on all of that service's servers, the ninety-ninth percentile was a hundred and forty."*

What's wrong: This cites only the first and third rows of the paper's actual Table 1, which has three: one random leaf (p99 = 10ms), **95% of leaves (p99 = 70ms)**, all leaves (p99 = 140ms). The paper's own headline reading of that table — "waiting for the slowest 5% of the requests to complete is responsible for half of the total 99%-percentile latency" — is the more surprising and more citable takeaway, and it's dropped. Separately, the script never says how many leaves are in this real tree; sitting right after a 10×10 grid of exactly 100 servers, a viewer will naturally assume this is the same N=100, when the real measurement is a deeper root→intermediate→leaf fan-out over a different (likely much larger and non-uniform) set of servers.

Corrected wording: add the middle figure and name the point it's making, e.g. *"...one server's own ninety-ninth percentile was ten milliseconds; for 95% of the servers to answer, seventy; for all of them, a hundred and forty. Half of that total tail came from waiting on just the slowest five percent."* This also avoids implying it's the same 100-way fan-out as the toy example.

**SHOULD FIX** — Section 3, general framing of the percentile-matching point.

What's missing: The script states the forward direction (100 calls → typical page latency is the servers' p99) but omits the converse framing the source material treats as the other essential half of this insight: for a 100-way fan-out to hit its own p99, *each* leaf must independently hit its p99.99 (since 0.99¹⁄¹⁰⁰ ≈ 0.9999). That inverse statement is what makes the "you can't spot-fix your way out of this" argument in Section 4 land quantitatively rather than just qualitatively.

Corrected wording: one added line before moving to Section 4, e.g. *"Turn that around: for the page's ninety-ninth percentile to be good, each of its hundred servers would need to be slow only one time in ten thousand — a much harder target than 'one in a hundred.'"*

**NIT** — Section 6: *"When a request fans out, watch your servers' ninety-ninth percentile, not their average."*

This flattens the earlier, more accurate point ("with more calls per page, an even rarer, slower percentile decides") into a single fixed percentile. It's forgivable as a memorable closing line tied to the N=100 example running through the video, but a stricter phrasing would be *"watch the percentile matching your fan-out size, not the average."*

**NIT** — Section 4's cause list (queueing, GC, background jobs, noisy neighbor) covers 4 of the roughly 8 causes the paper enumerates (it omits network effects, power/energy management, maintenance activities like log compaction). Reasonable for time budget; consider one appositive like "...and others" to avoid implying the list is exhaustive.

**NIT** — "hiccup" is used throughout as the only informal term for a stall; the script does correctly introduce "tail latency" as the formal term in Section 3, so this is just a style note, not an error. The paper's own term for a single such instance is "straggler," which could be worth one mention if terminology alignment with the literature matters for this course.

## What I checked and found solid
- Independence assumption stated before use; 0.99¹⁰⁰≈37%, 1−37%=63% (matches paper's own rounding, not just raw 63.4%).
- Average (20ms), median (10ms), p99 (~1s) for the single-server toy distribution — all consistent with the paper's exact phrasing ("typically responds in 10ms but with a 99th-percentile latency of one second").
- Slow-page-fraction table for N=1/10/50/100 (1%/9.6%/39.5%/63.4%) — correct arithmetic (1−0.99^N).
- Hedged-request mechanics (delayed copy at p95, ~5% extra load, cancel the loser, route the copy to an independent-failure-domain replica) match the paper's "within-request short-term adaptations" section precisely, and are correctly distinguished from a plain retry-on-timeout.
- Bigtable benchmark numbers (1,000 keys/100 servers, hedge at 10ms, p99.9 1,800ms→74ms, +2% load) match the source exactly.
- The closing correlation caveat ("hedging only helps when hiccups are independent... a hedge's copy may be stalled too") matches the paper's own stated limitation nearly verbatim, and the script correctly avoids the two most common overstatements in this space: treating 63% as a universal law, and citing unreliable business-impact figures (e.g., "100ms costs 1% of sales") that the paper doesn't make and that later literature (DDIA 2nd ed.) actively disowns.
- Hedging correctly scoped to reads, with the write/idempotency caveat deferred to a stated next lesson rather than glossed over.

VERDICT: PASS
