## Review

I checked every numeric claim (all arithmetic in §1, §3, §4, §5, §6 is correct: 2×20=40+10%=44; 3×20=60+6=66; 4×20=80+8=88; the diamond-doubling table 2,4,8,1024,1,048,576 all check out against 2^k), every term against the evidence table (glitch, diamond, height, early cutoff, laziness, observer pattern, circular reference all match the cited sources precisely — "height" in particular is exactly Jane Street Incremental's term, which lines up with the Minsky citation), and the Make/Excel behavioral claims against how those systems actually work. Overall this is unusually well-sourced for a script of this length. My objections are precision/caveat issues, not correctness failures.

---

**SHOULD FIX** — Overstated generality
> "A spreadsheet or a user interface is full of diamonds, and they chain one after another."

This states as a general fact about real spreadsheets/UIs what is actually a worst-case topology constructed for the demonstration (a literal serial chain of doubling diamonds). Most real dependency graphs don't compound this cleanly, and a professor would want the exponential-blowup point flagged as illustrative, not descriptive of typical systems.
Suggested wording: *"A spreadsheet or a user interface can contain many diamonds, and when they chain one after another, the naive cost compounds."*

**SHOULD FIX** — Missing scope caveat on the height-order guarantee
> "Recompute only the marked values, from the lowest height up. By the time a value is computed, every one of its inputs is already up to date."

This guarantee (from FrTime §3.2 / Maier et al. §6.2 / BSALC §4) holds specifically for a *static, acyclic* graph — i.e., one whose edges don't change during the very recomputation pass that uses those heights. The script only surfaces the dynamic-dependency case three sections later (§7) and never explicitly ties it back to this guarantee. A viewer could reasonably conclude the height-order fix is unconditional.
Suggested addition (end of §5 or start of §7): *"That guarantee assumes the graph's shape doesn't change mid-update — the next question is what happens when it does."*

**NIT** — Screen/narration sequencing
> §1 screen direction shows "free shipping (from $65): no" before the concept of free shipping is introduced in the voiceover ("Say the shop gives free shipping from sixty-five dollars," §2).

Not a factual error, but it front-loads a mechanic the narration hasn't explained yet. Consider holding the "free shipping" line off-screen until §2, or having §1's narration mention it in passing.

**NIT** — Slightly elliptical height derivation
> "The total reads the tax, so it sits above it: height three."

Total actually reads *both* subtotal (height 1) and tax (height 2); the height is the max of the two plus one, which happens to be driven by tax. As worded it reads as if total's height derives only from tax, in slight tension with §2's "the total reads the subtotal and the tax." Not wrong, but could confuse a careful viewer.
Suggested wording: *"The total reads both the subtotal and the tax — height is one more than the *higher* of what it reads, so the total sits above tax, at height three."*

---

No BLOCKING issues found: all cart arithmetic, dependency-graph semantics, glitch/diamond definitions, height-ordering algorithm, Make/header staleness behavior, and Excel circular-reference behavior are correct and properly sourced.

VERDICT: PASS
