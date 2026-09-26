Watching this straight through as that engineer persona, here's my reaction.

## 1. Where I'd lose the thread

- **"Say it tells the total first."** — Why total first and not tax first? The script never says the order is arbitrary/unspecified; it just picks one, which made me think there was a rule I'd missed rather than realizing "arbitrary order" *is* the point being illustrated.
- **"The total becomes sixty-four."** — I had to hold "new subtotal (60) + old tax (4)" in my head with no visual aid described beyond a caption; a fast listen (not watching) would lose this.
- **"This is the observer pattern"** — named right after being described, but no indication of how well-known a term this is supposed to be; I wasn't sure if I was supposed to already know it.
- **"Give each value a height."** — brand new concept, and in the same paragraph it's immediately applied across five nodes (subtotal=1, tax=2, total=3, free shipping=4, banner=5). That's one new idea (height) plus five instantiations of it landing at once — I had to pause to be sure I was updating heights, not values.
- **"Two refinements cut the work further. The first is early cutoff... The second is laziness."** — two distinct new mechanisms back-to-back in the same short section, each with its own scenario; by the time laziness arrived I was still processing early cutoff.
- **"Here's a program whose source file includes a header, but whose Makefile lists only the source file."** — this assumes I know what a Makefile is and how `app: main.c` dependency syntax works. Section 1 mentioned "build tools" only as a label, never explained the mechanics, so this whole example ran ahead of what was taught.
- **"push-pull"** — comes right as a label for something just explained, fine, but stacked onto early cutoff + laziness in the same breath, it's a third new term in one short span.

## 2. Questions I'd ask afterward

- When a value is "told" by two different readers in the naive scheme, who decides which one goes first — is that order actually random in real systems, or fixed by insertion order?
- Does the height-ordering scheme need to recompute the *entire* graph on every change, or only the marked subset? (I think it's only marked, but the walkthrough didn't say it explicitly.)
- How does a real system compute "height" — is it recalculated every time the graph changes, or cached?
- For dynamic dependencies (the coupon example), if a formula stops reading something, does the old arrow get removed immediately, or only discovered stale on the next run?
- Is push-pull the same technique used in things like React or is that a different model entirely?

## 3. What I learned (written without looking back)

Spreadsheets, build tools, and UI frameworks all solve the same problem: when one value changes, figure out what else needs recomputing, and in what order. They build a dependency graph — arrows from a value to whatever reads it. A naive approach recomputes readers immediately as each input changes, but this causes "diamonds" (two paths to the same downstream value) to produce wrong intermediate values called glitches, and causes exponential blowup in recomputation count as diamonds chain together. The fix is to first mark everything downstream of a change as stale, then recompute in dependency order (using a "height" number per node), so each value computes exactly once. Further optimizations include stopping early if a value doesn't actually change, and being lazy about computing values nobody's reading yet.

## 4. Direct answers

- **One main idea:** correct, efficient reactive updates require computing a dependency graph, marking what's downstream of a change, then recomputing in dependency order exactly once — rather than eagerly cascading changes value-by-value.
- **Numbers I remember:** the cart example ($20 × 2 → $40 subtotal, $4 tax, $44 total; then qty 3 → $60/$6/$66, crossing the $50 free-shipping threshold); the naive scheme took 8 recomputations for that graph vs. 5 with ordering; and the scary one — 10 chained diamonds naively means 1,024 recomputations, 20 diamonds means over a million.
- **Starting question / answer:** "How does a system decide what to recompute, and in what order, and what goes wrong when it gets that wrong?" Answer: recompute everything downstream of the change (nothing else), in dependency order by height, each value exactly once, stopping where nothing actually changed.

## 5. Ratings

- **Pull of the opening (1–5):** 4 — the stale-total-in-ordinary-code vs. always-correct-spreadsheet contrast is a genuinely relatable itch, and framing it as one underlying mechanism behind three tools I use (build tools, spreadsheets, UI frameworks) made me want the answer.
- **How often I felt lost:** a few times — mainly at the arbitrary-order moment in section 3, the height concept's rapid-fire application in section 5, and the Makefile syntax in section 7.
