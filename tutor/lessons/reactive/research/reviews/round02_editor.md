# Script Review

## 1. Opening question → ending answer

**Pass, strong callback.** Opening: "How does a system like that decide what to recompute, and in what order? And what goes wrong when it gets that wrong?" Ending directly answers both clauses ("what is out of date... in what order...") and calls back the glitch by name: "you'll see values that never should exist, like a total of sixty-four." No fix needed.

## 2. Segment chain (but / therefore / and then)

Reconstructed as single sentences:
1. Code computes once; a spreadsheet stays right — how does it decide what and in what order?
2. **Therefore**, a dependency graph: a change makes everything downstream out of date.
3. **But** the obvious fix (observer pattern) hits a diamond, producing a glitch ($64) and doubled work.
4. **But** stacked diamonds make that doubling exponential (1,024 at ten).
5. **Therefore**, mark then recompute in height order, once each.
6. **[But]** that still wastes work, so cut with early cutoff and laziness.
7. **But** the order is only as good as the graph — recorded vs. declared deps, and cycles have none.
8. **Therefore**, the same machine underlies spreadsheets, build tools, UI frameworks.

**"and then" count: zero.** Good — no step is a bare sequence hiding a missing causal claim.

**SHOULD FIX** — step 6's actual connector in the script is "still" (a *but*: work remains despite the fix), but the Chain document labels it "Therefore." That's a real mismatch: early cutoff/laziness aren't a consequence of the ordering fix, they're a separate optimization prompted by a leftover problem.
> Chain doc: "Therefore two refinements save work..."
Rewrite label: "**But** the ordered wave still does wasted work — early cutoff and laziness cut it."

## 3. Ideas announced vs. derived

All major ideas are derived from a shown problem (graph from the cart, height-order from the glitch, cutoff/laziness from wasted recomputation, recorded-deps from "where do the arrows come from?"). One exception:

**SHOULD FIX** — cycles arrive as a stated fact, not a derived necessity: "And one kind of graph can't be ordered at all." Nothing on screen has shown a formula trying to depend on itself before this line asserts the rule.
Rewrite: "Now try to give heights in a cart where the loyalty discount depends on the total, and the total depends on the loyalty discount. Walk the rule — a value's height is one more than what it reads — and you can't finish. That's a cycle, and Excel calls it a circular reference."

## 4. Setups without payoffs / payoffs without setups

**SHOULD FIX** — "though it can be told to iterate toward an answer" is a payoff-less setup: it names a third resolution mode (iteration) that's never explained and never used again.
Rewrite: cut the clause entirely — "By default it warns instead of computing." Nothing downstream needs iteration.

**SHOULD FIX** — the coupon-cart aside ("Imagine a different cart, whose total reads a coupon cell only when the customer has a coupon") is a setup that pays off only in one abstract follow-on sentence about recording-on-run, then is dropped. See test 9.

## 5. Terms before explained / multi-named concepts

Glitch, diamond, height, early cutoff, laziness — all defined at first use. Good.

**NIT** — the same concept gets three labels in one breath: "depends, through others, on itself" (paraphrase) → "circular reference" (Excel's term, in narration) → "loop" (screen-note label, never spoken). Pick one word and use it in both channels.
Rewrite: narrate "circular reference" and label the screen diagram "circular reference," not "three-node loop."

## 6. Numbers: worth remembering vs. dead weight

Worth remembering: **$64** (the glitch — a total that never existed), **1,024** (ten diamonds, naive recompute count), **$65** (the threshold that turns correctness visible via yes/no).

**NIT** — do no real work: the 8-vs-5 recomputation counters in sections 3 and 5 compete with the much more dramatic 1-vs-1,024 for the "remember this" slot, and "over a million" (twenty diamonds) just restates the same point a second time.
Rewrite: drop the 8/5 counters (let the visual wave do that job silently) and cut "with twenty, over a million" — one exponential example is enough.

## 7. Abstraction before the concrete case

**SHOULD FIX** — cycles are the one concept in the whole script that never touches the cart. Every other idea (graph, diamond, height, cutoff, laziness, recorded-vs-declared deps) is shown in the cart or in the real Make/terminal demo; the cycle example jumps straight to generic nodes A→B→C.
Rewrite (screen + line): keep it in the cart — "loyalty discount reads total, total reads loyalty discount" — and show *that* failing to get a height, instead of an unlabeled A/B/C loop.

## 8. Wrong intuition confronted and shown failing

Pass. The observer-pattern model is stated as the "wrong model," then walked through concretely in section 3 (producing the $64 glitch) and section 4 (exponential blowup) — shown failing, not just asserted.

## 9. Examples named but not understood

**SHOULD FIX** — "Vue, Solid and Angular's signals" and "Bazel" are bare name-drops in the closing line with zero explanation of what each actually does differently. A viewer who doesn't already know these frameworks gets no anchor.
> "inside build systems like Make and Bazel, and inside the reactive parts of UI frameworks such as Vue, Solid and Angular's signals."
Rewrite: "inside build systems like Make, and inside the reactive parts of frameworks like Vue and Angular's signals, which recompute a component only when something it read has changed." (Cut Bazel and Solid — neither is explained, and Make already carries the build-tool case.)

**SHOULD FIX** — the coupon-cart example is named but never resolved: we don't see its graph actually change or its result recompute, so the viewer can't verify the claim.
Rewrite: show the has_coupon toggle actually firing — arrow appears, total recomputes with the coupon subtracted — the way every other example in the script does.

## 10. On-screen text vs. narration; unsupported pictures

**NIT** — section 8's screen notes ("what is out of date? → everything downstream" / "in what order? → by height, once each, stop where unchanged") caption the narration almost verbatim at the same moment it's spoken.
Rewrite: let the two lines appear as a silent written recap *after* the line finishes, or drop them and let the graph animation alone carry it — don't run text and speech in lockstep saying the same thing twice.

**NIT** — the section-4 recap table ("diamonds: 1→2, 2→4, 3→8, 10→1,024") repeats numbers already delivered by both narration and the live counter animation in the same beat — triple redundancy for one point.
Rewrite: keep the animated counter, cut the table (or vice versa).

## 11. Lines deletable without breaking anything

- "though it can be told to iterate toward an answer" (section 7) — cut, see test 4.
- "and Bazel" / "and Solid" (section 8) — cut, see test 9.
- The 8-vs-5 recomputation counters (sections 3 & 5) — cut, see test 6.

## 12. Hard-to-follow sentences; rushed/padded beats

**SHOULD FIX** — section 7 is overloaded: it carries three distinct sub-arguments (dynamic dependencies via the coupon cart, Make's staleness bug via the terminal demo, and cycles) in one segment, and the least concrete of the three (cycles) gets the least room, right before the finale.
Rewrite: split into two beats — one on "where do the arrows come from" (recorded vs. declared, ending on the Make demo), a second, short beat solely on cycles, grounded in the cart per test 7's rewrite.

**NIT** — "Sixty-four was never a correct total. The right answer was forty-four before the change and sixty-six after it." stacks three numbers (64/44/66) in one breath; fine on screen with synced visuals, but reads dense aloud. Give each number its own beat in the edit (a half-second hold on each) rather than compressing them into one sentence.

**NIT** — "Which does it tell first? Whichever subscribed first; nothing in the pattern decides." — awkward semicolon construction for read-aloud.
Rewrite: "Which does it tell first? Whatever subscribed first — the pattern itself doesn't decide."

---

No item breaks the spine of the argument: the opening question is answered and called back, the wrong model is concretely shown failing, and the chain holds with zero "and then" filler. The findings above are refinements to concreteness, redundancy, and pacing — concentrated in the cycle/frameworks material at the end.

VERDICT: PASS
