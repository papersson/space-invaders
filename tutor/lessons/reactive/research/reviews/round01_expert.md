# Review: "The Dependency Graph" explainer script

I checked every arithmetic claim, all terminology, and each generalization against the cited sources. The core mechanism (dependency graph → mark reachable nodes → recompute in topological/height order → early cutoff → push-pull laziness → dynamic vs. declared dependencies → cycles) is correctly presented and matches the evidence table closely. Arithmetic checks out throughout: $40/$4/$44 → $60/$6/$66 → $80/$8/$88, heights 0,0,1,2,3,4,5, glitch value 64, recomputation counts 8→5, and 2^10=1,024 / 2^20=1,048,576 are all internally consistent and correctly derived. I found no BLOCKING errors, but several places would benefit from a caveat before a domain expert would sign off.

## SHOULD FIX

**1. Excel circular-reference claim omits the iterative-calculation escape hatch**
> "Excel calls this a circular reference, and warns instead of computing."

This is true of Excel's default behavior, but Excel has a documented "Enable iterative calculation" option (File > Options > Formulas) that lets it converge circular references to a value — used routinely in financial models (circular interest, plug figures). As worded, this reads as "Excel simply cannot resolve cycles," which is incomplete enough that a Excel-literate viewer will object.
**Fix:** "...and by default warns instead of computing — though it can be told to iterate toward an answer instead."

**2. Make's dependency model is presented as more rigid than it is**
> "Build tools like Make take the other route: you write the dependencies down by hand. If one is missing, the graph is wrong, and the result goes stale."

Accurate for a bare Makefile (and it's exactly what the `make_stale` demo shows), but your own evidence cites the GNU Make manual section "Generating Prerequisites Automatically" — compilers routinely emit `.d` files (`-MMD`) that Make includes to keep dependencies accurate, which is the standard production fix for exactly this failure mode. Presenting Make as inherently manual-only overstates the contrast with spreadsheets; the real distinguishing fact is whether dependencies are *derived from what's read* or *declared*, not automatic-vs-manual per se.
**Fix:** add a clause, e.g., "...you write the dependencies down by hand — unless you go out of your way to generate them from the compiler."

**3. The glitch example doesn't actually show a wrong outcome**
> "Anything that reads the total at this moment, like the free-shipping check, runs on a wrong number."

True as stated (64 vs. eventual 66), but both 64 and 66 exceed the $50 threshold, so free shipping evaluates to "yes" either way — the audience never sees the glitch change a decision. This is the one place where the demonstrated harm is weaker than the claim; an attentive viewer could conclude the glitch was harmless here, which undercuts the motivation for fixing it in §5.
**Fix:** either add a line acknowledging "the answer happens to come out the same here — it won't always," or pick numbers where the transient value (64) and final value (66) straddle the threshold.

**4. The coupon formula silently redefines "total"**
> "A total with a discount might read a coupon cell only when the customer has a coupon."

Up to this point "total" has been fixed as `total = subtotal + tax` (shown on screen twice). Introducing a coupon term while still calling it "the total," without flagging it as a separate hypothetical, risks viewers thinking the running cart example gained a field.
**Fix:** frame it explicitly as a different example, e.g., "Imagine instead a cart whose total reads a coupon cell only when there's a coupon."

## NIT

**5. "Push-pull" citation is a slightly loose fit.** Elliott's 2009 paper addresses combining eager event propagation with demand-driven behavior sampling in FRP — closely related to "mark eagerly, compute lazily" but not identical framing. The term is used this way colloquially now (MobX, Solid), so it's defensible, but pairing it with a closer signals-library source alongside Elliott would be more precise.

**6. No mention that heights must be recomputed when the graph is dynamic.** §5 treats height as fixed per node; §7 explains dependencies can change shape at runtime. One sentence connecting the two (heights are recomputed along with the graph on each run) would close an implicit gap an attentive viewer might notice.

## What's solid (no notes needed)
The diamond/glitch trace, the 2^k blow-up chain (matches Minsky's "Seven Implementations of Incremental" almost verbatim), the height assignment and its use as a topological order, the mark/compute two-phase split, early cutoff mechanics (free shipping *is* recomputed, only the banner is skipped — correctly distinguished from "skip recomputation entirely"), the dynamic-dependency/Excel recording behavior, and the closing generalization to Excel/Make/Bazel/Vue/Solid/Angular signals are all accurate and appropriately hedged ("some version of this").

VERDICT: PASS
