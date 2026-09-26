# Script Review

## Test-by-test pass

**1. Opening question ↔ ending answer.** The opening asks two tightly coupled things: why response time doubled, and where the other 40 ms at 80% comes from. The ending answers both with the same numbers: *"So that's where the forty milliseconds went... the response time doubled with it, from fifty milliseconds to a hundred."* Clean callback — pass.

**2. Chain in but/therefore/and-then.** Mapping the six sections: (1) puzzle stated → (2) *but* work is constant, *therefore* the rest is waiting/queues → (3) *but* fixed-spacing traffic never queues, *therefore* queues come from variability → (4) *therefore* spare capacity is what clears them, and it halved → (5) *therefore* the general curve, confirmed by simulation → (6) *therefore* the answer plus the practical rule. **"and then" count: 0.** The whole script is causal connectives, no bare sequencing — this is a real strength.

**3. Ideas announced vs. derived.** Nothing is asserted cold. Even "spare capacity" is coined only after §4 needs a name for something just shown; "Poisson/exponential" are attached only after the plain-language behavior (§3, §5) is already on screen. One partial exception: the "burstier traffic needs more headroom" claim in §6 *is* derived (recombines §3's clumping with §4's spare-capacity mechanism) — but the visual accompanying it is not (see Finding 1).

**4. Setups/payoffs.** No orphaned setups found. "Simulated server" label (§1) pays off in §4/§5. "The slowest requests are the next lesson" (§6) is an explicit, honest deferral, not a dangling thread.

**5. Terms before explanation / multiple names.** "Utilization" is defined in §5 right as it's introduced, bridging from the already-familiar "busy." Poisson/exponential are glossed in narration before being named. One soft issue: "busy" → "utilization" → "ρ" is three labels for one quantity (Finding 3). "Delay" is used once as a stray synonym for "response time" (Finding 5).

**6. Numbers.** Full list: 10 ms work; 80 req/s; 80% busy; 50 ms; 90 req/s; "an eighth"/12.5%; 90% busy; 100 ms; 40 ms wait; "4×"; 90 ms wait; 11 ms gap; 20%/10% spare; 50%→20 ms, 80%→50 ms, 90%→100 ms, 95%→200 ms; 20,000,000 simulated requests; "5×" → 80% limit; 400 (screen only). **Worth remembering: 10 ms baseline, the 80%→90% pair (20%→10% spare, 50→100 ms), and T = S/(1−ρ).** Everything else does real derivational work except the "400 requests" screen detail, which is flavor with no callback (Finding 7).

**7. Abstraction before concrete.** Not found — the script is disciplined about concrete-first (specific server, specific ms) then naming the abstraction after. This is well ordered throughout.

**8. Wrong intuition.** Named directly: *"You might expect a little more traffic to mean a little more delay."* Shown failing immediately (*"Instead, the response time doubled"*) and again more sharply in §3 (evenly-spaced traffic never queues even at 90%, isolating that busyness alone isn't the driver). Pass, and a good double-hit.

**9. Named-but-not-understood examples.** None in the main narrative — Poisson/exponential get plain-language content before the label. The M/M/c aside in the end card asserts a behavior without support, but it's citation material, not core content (Finding 6).

**10. On-screen text vs. narration; unsupported pictures.** Several places narrate and caption the same numbers (§1's panel, §5's assumption caption) — defensible for a number-dense pause-and-read video, but §4's caption *"spare capacity 20%: shrinks the queue"* duplicates the narration's defining clause almost verbatim (Finding 4). The one picture that doesn't earn its claim: the "illustrative" burstier-traffic curve in §6, sitting on the same axes as a curve that was actually simulated 20M times (Finding 1).

**11. Deletable lines.** Only one real candidate: *"and more than one busy resource"* in §6, introduced with no setup and never explained (Finding 2). Nothing else is filler — the averages/tail caveat in §6 earns its place given §5's "exact average" claim.

**12. Hard-to-say-aloud / pacing.** §3's *"ten milliseconds of work fills ninety percent of the gap... arrives about every eleven milliseconds"* stacks numbers densely for the ear (Finding 8). §5's four-point rundown (20/50/100/200 ms) is terse but intentional — the visual is carrying the "flat then steep" reveal, so it reads as pacing, not rushing. No padded beats found.

## Findings

**SHOULD FIX — visual claims outrun their evidence.**
Quote: *"A second curve above it, dashed, 'burstier traffic or more variable work (illustrative)'."*
The main curve earned its authority via a 20M-request simulation; this curve is hand-drawn and only flagged as illustrative in small print, on the same axes, same visual language. Rewrite: either simulate a bursty arrival process and overlay real points, or make the lower rigor audible: *"Here's roughly the shape — I haven't simulated this one, but it's flat, then steep, just earlier."*

**SHOULD FIX — unexplained scope creep.**
Quote: *"Real systems, with burstier traffic and more than one busy resource, usually need more headroom than this curve says."*
"More than one busy resource" has no setup anywhere and isn't unpacked. Rewrite: cut it (*"Real systems, with burstier traffic, usually need more headroom than this curve says."*) or ground it: *"...and more than one busy resource in the path — a database as well as this server — usually need more headroom."*

**NIT — three names for one number.**
Quote: *"busy"* (§1–4) → *"utilization"* (§5) → *"ρ"* (§5 screen). Each rename is bridged with a definition, so it's not confusing, but ρ adds nothing narration needs. Rewrite: keep ρ as a screen-only aside; never say "rho" aloud.

**NIT — caption duplicates the definition, not just the numbers.**
Narration: *"Call that twenty percent the spare capacity: it's what clears the queue."* Screen: *"spare capacity 20%: shrinks the queue."* Rewrite: let the screen carry just *"spare capacity: 20%"* and leave the definition to narration alone.

**NIT — stray synonym.**
Quote: *"a little more traffic to mean a little more delay"* — "delay" appears nowhere else; "response time" is the term used everywhere else. Rewrite: *"...a little more response time."*

**NIT — unsupported end-card claim.**
Quote: *"many servers sharing one queue stay flat for longer, then eventually turn up much the same way (M/M/c)."* Fine as a citation pointer, but as written it's an assertion the video hasn't earned. Rewrite: *"many servers sharing one queue behave similarly (see M/M/c in the references)."*

**NIT — a number that does no work.**
Quote: *"the same random draws at 80% and 90% busy (400 requests, simulated)."* Never referenced again, unlike the 20M figure in §5 which is the actual evidence. Consider dropping it from the screen direction.

**NIT — dense sentence for the ear.**
Quote: *"At ninety percent busy, ten milliseconds of work fills ninety percent of the gap between requests, so a new one arrives about every eleven milliseconds."* Rewrite: split into two sentences — *"At ninety percent busy, ten milliseconds of work fills ninety percent of the gap between requests. So a new request arrives only every eleven milliseconds or so."*

No BLOCKING items — the causal chain is intact end to end, the wrong model is stated and shown failing, every technical term is earned before use, and the opening/closing calls back precisely.

VERDICT: PASS
