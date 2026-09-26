# Script Review

## 1. Opening question → ending callback
Opening: "How does a system like that decide what to recompute, and in what order? And what goes wrong when it gets that wrong?" Ending (§8): "It knows the dependency graph. From that graph it answers two questions: what is out of date... and in what order... Get the order wrong and you see values that never should exist, like a total of sixty-four." Both halves of the question are answered, and "sixty-four" calls back to §3. **Passes.**

## 2. Segment chain (but/therefore/and then)
1. Code goes stale but spreadsheets stay right — question.
2. Therefore: a dependency graph marks everything downstream.
3. The obvious fix is notify-on-write, but diamonds make it glitch and double-compute.
4. **[and then]** Stacked diamonds double that cost each time.
5. Therefore: mark first, then compute in height order, once each.
6. **[and then]** Two more refinements — cutoff and laziness — cut the work further.
7. But all of this only works if the graph is complete, and recorded/manual/cyclic graphs differ.
8. Therefore: same machine everywhere.

Two "and then" links (4, 6) — both are escalations/additions rather than pivots. Not fatal, but worth naming (see §3 below for #6).

## 3. Ideas announced vs. derived
- **SHOULD FIX** — Early cutoff and laziness are announced, not motivated by a shown problem. Quote: *"Two refinements cut the work further."* Nothing on screen has shown wasted work at this point (the count is already down to 5). Rewrite: precede it with a beat that shows waste under the "always recompute everyone downstream" rule — e.g., "But the fix still recomputes free shipping and the banner even when nothing about them changed, and it computes values nobody's looking at. Two refinements cut that out: ..." This turns the refinement into an answer to a visible inefficiency instead of a bonus feature.

Everything else (dependency graph, observer pattern, height order, recorded-vs-manual dependencies, cycles) is properly derived from a shown problem before being named.

## 4. Setups/payoffs
No orphaned setups or unearned payoffs found. Free shipping, the diamond shape, height numbers, and the $44/$66 totals are all set up and paid off. The coupon example in §7 is a self-contained setup+payoff within one beat — fine.

## 5. Terms before explanation / multiple names for one concept
- **SHOULD FIX** — The eager-notify approach is named four different ways: the section title "Just tell the readers," "the obvious way," "the observer pattern," and (in §4) "the notify-right-away scheme." Rewrite: pick one term after the first naming ("the observer pattern") and reuse it verbatim in §4 instead of coining "notify-right-away scheme" — e.g., "In the observer pattern, each diamond makes everything after it run twice."
- **NIT** — The ordering fix is called "height order" in §5 but "dependency order" in §8 and in the Takeaway. Quote (§8): *"The answer to the second is dependency order, each value once."* Rewrite: "...is height order — lowest first — each value once," to tie the recap back to the term the audience actually learned.

All other terms (diamond, glitch, height, push-pull) are defined at first use before being relied on.

## 6. Numbers
All numbers: $20/qty 2/$40/$4/$44/10%; qty 3/$60/$6/$66; $50 threshold; recomputations 8; diamonds table 2/4/8/1,024/1,048,576; heights 0,0,1,2,3,4,5; recomputations 5; qty 4/$80/$8/$88; threshold $50→$65.

Worth remembering: **64** (the glitch total — the video's central image), **1,024** (ten diamonds — the cost of getting order wrong at scale), and **44→66** (the correct before/after totals, which anchor the opening and the ending).

- **NIT** — The 20-diamond row (1,048,576) does no extra work beyond the 10-diamond row; narration already says "over a million" without needing the exact digit string on screen. Rewrite: drop the 20-diamond row from the table, or replace it with a repeat of the same 10-diamond figure zoomed in, keeping the point to one memorable number.

## 7. Abstraction before the concrete case
- **NIT** — In §5, the height rule is stated in general form before being anchored: *"Give each value a height. An input has height zero. A formula's height is one more than the highest of its inputs. So the subtotal is one..."* Rewrite to match the rest of the script's concrete-first discipline: "The subtotal only reads inputs, so call it height one. The tax reads the subtotal, one level up, so height two. The total reads both, so height three. In general: a formula's height is one more than its highest input." Elsewhere the script is disciplined about concrete-first; this is the one spot it inverts.

## 8. Wrong intuition confronted
Wrong model: "notify immediately, order doesn't matter." It is shown failing concretely — the $64 glitch and the doubled/exponential recompute count — not just asserted. **Passes, and passes well.**

## 9. Examples named but not understood
- **NIT** — Vue, Solid, Angular signals, and Bazel appear only in the closing relabel montage, with no worked example (unlike Make and Excel, which each get one). This is a defensible closing-credibility move, but flag in case the editor wants to trim the list rather than name tools that are never actually shown working.

## 10. On-screen text vs. narration; pictures vs. line
- **SHOULD FIX** — §3 caption *"right totals: $44 before, $66 after"* nearly restates the narration verbatim ("The right answer was forty-four before the change and sixty-six after it"). Rewrite: drop the caption text and instead color-code the correct total green against the coral flash of 64, letting the visual carry what the line already says.
- **NIT** — §4's on-screen table repeats the spoken numbers (1,024 / over a million) exactly. Lower severity than the §3 case since numeric reinforcement is a legitimate retention aid, but the 20-diamond row should go per §6 above.

## 11. Deletable lines
- **NIT** — §6: *"Marking eagerly and computing lazily is often called push-pull: the 'out of date' marks are pushed forward, and the values are pulled when needed."* Cutoff and laziness are already fully explained by this point; this sentence only adds a label, no new mechanism. Deletable without losing any taught content — keep only if the "push-pull" term is needed later (it isn't).

## 12. Hard-to-follow sentences / rushed or padded beats
- **NIT** — §8: *"Get the order wrong and you see values that never should exist, like a total of sixty-four, and do the same work many times over."* The dropped repetition of the subject makes the second clause hard to track by ear. Rewrite: "Get the order wrong, and you'll see values that never should exist — like a total of sixty-four — and you'll do the same work many times over."
- **NIT** — §7 ("Where do the arrows come from?") compresses three distinct sub-ideas — conditional dependencies, Make's forgotten-dependency staleness, and Excel's circular reference — into one beat, where every other section carries exactly one idea. This follows Objective 5 faithfully, but it's the densest beat in the script; consider whether the coupon aside earns its place or could be cut to give the Make and Excel demos more room.

---

**VERDICT: PASS**

(No BLOCKING items — the argument, callback structure, and the wrong-model-shown-failing beat are all solid. The SHOULD FIX items are worth doing: consolidate the four names for the naive approach, motivate cutoff/laziness with a shown inefficiency rather than announcing them, and cut the redundant §3 caption.)
