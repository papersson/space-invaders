# Script Review: "Why Busy Servers Get Slow"

## Test 1 — Opening question / ending callback
**Pass.** The opening asks two fused facets of one question: "Why?" (does traffic doubling response time) and "where do forty of those fifty milliseconds come from?" The ending explicitly closes both: "So that's where the forty milliseconds went: not into work, but into waiting... halved the spare capacity, from twenty percent to ten, and the response time doubled with it, from fifty milliseconds to a hundred." Clean callback, same numbers, same phrasing echo ("forty milliseconds").

## Test 2 — Chain as single sentences with connectives; report every "and then"
1. A server does 10 ms of work; at 80% busy a request takes 50 ms, at 90% busy it takes 100 ms — **but** the work itself doesn't change, so the extra time is waiting — **therefore** the question is really about queues.
2. **But** evenly-spaced requests with fixed work times never queue, even at 90% — **therefore** queues must come from variability in arrival and work size.
3. **Therefore** look at what clears a queue — spare time — and at 90% there's half as much of it as at 80%, so a queue takes twice as long to clear.
4. **Therefore** the general curve is response = work ÷ spare capacity, flat then steep, and a simulation confirms it.
5. **Therefore** the answer: the missing 40 ms is waiting, doubled because spare capacity halved, and the same logic says burstier traffic needs more headroom, which sets the practical rule.

**"And then" count: zero.** The whole script is causally chained, no merely-sequential joins. This is a genuine strength — flag it as such rather than a finding.

## Test 3 — Ideas announced vs. derived
- "Spare capacity" (Section 4) is derived on-screen from a visible problem ("a queue shrinks only when the server finishes work faster than new work arrives... call it spare capacity"). Good.
- "Utilization" (Section 5) is just a label for the already-familiar "percent busy" — explicitly tied, not sprung. Fine.
- **SHOULD FIX** — Burstier traffic needing more headroom (Section 6, Objective 4) is *asserted* rather than derived or shown: "Burstier traffic, or more variable work, makes this worse... So they need more spare capacity for the same response time," backed only by a dashed curve labeled **"illustrative"** — i.e., not actually simulated, unlike every other claim in the video. This breaks the evidentiary standard the script itself sets up (every other number is "a simulation... lands on the curve").
  **Rewrite:** Either run and show a real simulation with burstier (e.g., batch-arrival) traffic overlaid at the same utilizations, or soften the on-screen label and narration to mark it explicitly as a qualitative extension: "This second curve isn't measured — it's what the same logic predicts. Bigger clumps mean bigger queues for the same spare capacity, so the curve turns up earlier." At minimum, don't let "illustrative" quietly do the work of "simulated" elsewhere in the video.

## Test 4 — Setups without payoffs / payoffs without setups
- "Simulated server" (Section 1) → paid off in Sections 4 and 5. Good.
- Queue-counter visual (Section 3) → paid off in Section 4. Good.
- **NIT** — M/M/c ("many servers sharing one queue stay flat for longer...") appears only in the end card with no setup anywhere in the narrated script. It's clearly reference material, not a taught concept, so this is low severity, but a viewer who reads the end card may feel a claim landed with no support at all.

## Test 5 — Terms before explanation / dual naming
No unflagged case: "utilization" is explicitly bound to "percent busy" the moment it's introduced; "spare capacity" is used consistently throughout (script never drifts into the planning doc's "spare time"). Poisson/exponential are named at the same moment they're glossed in plain English. Clean.

## Test 6 — Numbers: which 2–3 matter, which do no work
**Numbers worth remembering:** (1) 10 ms fixed work time, (2) spare capacity 20%→10% causing response time 50 ms→100 ms (the core relation), (3) the actionable rule "5× work-time budget → keep ≤80% busy."

**NIT — numbers doing no analytical work:**
- "an eighth more traffic / +12.5%" (Section 1) is never reused in the derivation — the actual explanation runs through spare-capacity percentages, not the traffic-increase percentage. It's a fine rhetorical hook but flag it as decorative, not load-bearing.
- "twenty million requests" and "400 requests" are flavor/credibility numbers, not something the viewer needs to retain.
- "eleven milliseconds" (evenly-spaced gap, Section 3) is used once for the thought experiment and never returns.

None of these need to be cut — they're reasonable texture — just don't expect a viewer to carry them forward.

## Test 7 — Abstraction before the concrete case
**Pass.** Concrete numbers (80/90% busy, 50/100 ms) are fully worked through in Sections 1–4 before the general formula T = S/(1−ρ) appears in Section 5. Good ordering.

## Test 8 — Wrong intuition confronted and shown failing
**Pass, with a soft spot.** "You might expect a little more traffic to mean a little more delay. Instead, the response time doubled" directly names the proportional-growth intuition and shows it failing via the 50→100 ms jump.
**NIT** — the disproof is qualitative ("a little more" vs. "doubled") rather than quantified against what proportional growth would actually predict (~12.5% increase). A single clause would sharpen it: "A proportional model would put it at fifty-six milliseconds. It doubled instead."

## Test 9 — Examples named but not understood
**NIT** — M/M/c in the end card is named with a one-line claim about its behavior ("stay flat for longer, then eventually turn up much the same way") but zero mechanism, since it's outside this lesson's scope. Fine as a citation-card pointer, but worth being aware it's an appeal to authority, not understanding.

## Test 10 — On-screen text vs. narration; pictures vs. lines
No blocking redundancy. On-screen panels mostly restate *numbers* (useful for retention: "+12.5% traffic" / "2× response time") rather than transcribing full narration sentences, and the bar charts, timelines, and curve genuinely carry information the audio doesn't (queue counters, to-scale wait/work splits, simulated dot overlays). This is good practice, not a finding.

## Test 11 — Deletable lines
Script is unusually tight — nearly every line is on the chain (confirmed by the zero "and then" count above).
**NIT** — "These are averages, and some requests take several times longer. The slowest requests are the next lesson" (Section 6) is the one line that doesn't serve *this* video's question or takeaway; it's a scope disclaimer + forward pointer. Defensible (prevents a viewer from mistaking the mean for the worst case) but it's the most cuttable sentence in the script if length pressure ever appears.

## Test 12 — Hard-to-follow-aloud sentences; rushed/padded beats
**SHOULD FIX** — Section 3: "At ninety percent busy, ten milliseconds of work fills ninety percent of the gap between requests, so a new one arrives about every eleven milliseconds." Four numbers stacked in one breath (90%, 10 ms, 90%, 11 ms) is a lot to hold in working memory from audio alone.
**Rewrite:** "Ten milliseconds of work is ninety percent of the gap between requests when a new one shows up every eleven milliseconds or so at ninety percent busy." — or simpler, split it: "At ninety percent busy, requests arrive about every eleven milliseconds. Ten milliseconds of work is ninety percent of that gap."

**SHOULD FIX** — Section 5: "The case is one server, requests arriving at random, each unrelated to the others, and work times that vary just as randomly: mostly short, sometimes several times longer." This is the *entire* delivery of Objective 3's "say what it assumes," compressed into one dense compound sentence sandwiched between the utilization definition and the formula reveal. Given it's a whole stated objective, it reads as the most rushed beat in the script relative to its billed importance — even though the caption reinforces it visually. Consider giving the two assumptions (random arrivals, variable work) one short sentence each, with a beat between them, rather than one clause each in a single breath.

**NIT** — Section 5's "At fifty percent busy, that's twenty milliseconds. At eighty, fifty. At ninety, a hundred. At ninety-five, two hundred" elides units after the first item; fine for a video with synchronized captions, but would fail as audio-only.

**NIT** — Section 6: "if a request may take five times its work time on average, keep the server at or below eighty percent busy" — "on average" placement is momentarily ambiguous (modifies the budget, not the work time). Minor.

---

No finding rises above SHOULD FIX: the causal chain is unbroken, the callback lands, the wrong intuition is confronted, and concreteness precedes abstraction throughout. The two SHOULD FIX items both cluster around the same risk — the video holds itself to a "simulation confirms it" standard everywhere except the one place (burstiness, Objective 4) where it most needs one, and the one place (assumptions, Objective 3) where the objective is most compressed into a single breath.

VERDICT: PASS
