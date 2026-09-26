You are a professor who has taught this material for years. Below is the script of a short narrated explainer video, with a note of what is on screen at each moment, followed by the list of numbers it uses and where each comes from. Review it for correctness and canonicity. You are the only domain expert who will see it before it is produced, so be exacting. Report every problem with: severity (BLOCKING = wrong, misleading, or non-canonical in a way a professor would object to; SHOULD FIX = imprecise, a missing caveat, non-standard terminology; NIT), the exact quote, what is wrong, and the corrected wording. Check every factual and numerical claim including arithmetic and units; that terminology and notation match the standard sources and simplifications teach nothing false; whether anything essential is missing or anything peripheral gets too much weight; and overstated claims about optimality, generality and real systems. End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> An online cart holds two items at twenty dollars each. The subtotal is forty dollars, tax at ten percent is four, and the total is forty-four.
> In ordinary code, the total is computed once. If the customer changes the quantity to three, the total still says forty-four, until some piece of code remembers to compute it again.
> In a spreadsheet, you never have to remember. Change the quantity, and the subtotal, the tax and the total all update, correctly, every time.
> Build tools do the same with files: change one source file, and exactly the parts that depend on it are rebuilt. So do many UI frameworks: change a value, and the screen updates.
> How does a system like that decide what to recompute, and in what order? And what goes wrong when it gets that wrong?

*Screen:* a small sheet: price $20, qty 2, subtotal $40, tax (10%) $4, total $44, and "free shipping (from $65)": no. First a code box: `total = subtotal + tax` and a value "44"; qty changes to 3; the code's total still reads 44 (coral, "stale"). Then the sheet: qty → 3 and the column updates to $60, $6, $66, free shipping: yes. Three labels: "spreadsheets", "build tools", "UI frameworks". The question.

### 2. The dependency graph

> Say the shop gives free shipping from sixty-five dollars.
> Each formula reads some other values. The subtotal reads the price and the quantity. The tax reads the subtotal. The total reads the subtotal and the tax. Free shipping reads the total, and the banner at the top of the cart reads free shipping.
> Draw an arrow from each value to every formula that reads it, and you have a dependency graph.
> When the quantity changes, follow the arrows. Everything you can reach is now out of date: the subtotal, the tax, the total, free shipping, the banner.
> Everything you can't reach is still correct. The price didn't change, and nothing it feeds needs recomputing because of this edit.

*Screen:* the sheet's cells lift off into nodes: price and qty at the left, subtotal, tax, total, free shipping and the banner ("Spend $65 for free shipping") to the right, arrows from inputs to readers. qty flashes; a wave follows the arrows and colours every reachable node amber ("out of date"); price stays grey.

### 3. Just tell the readers

> The obvious way to update them is to let each value tell its readers. When the quantity changes, it tells the subtotal to recompute. The subtotal then tells each of its own readers, and so on down the arrows.
> This is the observer pattern, and it's how a lot of hand-written code keeps things in sync.
> Follow it. The quantity becomes three, and the subtotal becomes sixty. The subtotal has two readers, the tax and the total. Which does it tell first? Whichever subscribed first; nothing in the pattern decides. Say it's the total.
> The total adds the new subtotal, sixty, to the tax, which is still the old four. The total becomes sixty-four.
> Sixty-four was never a correct total. The right answer was forty-four before the change and sixty-six after it. And the free-shipping check runs on sixty-four, and says no, though the right answer is yes. A value like that, built from a mix of new and old inputs, is called a glitch.
> Then the subtotal tells the tax, which becomes six. The tax tells the total, which is computed again: sixty-six. Free shipping runs a second time too.
> The trouble comes from one shape. The subtotal reaches the total by two paths, directly and through the tax. A shape like that is called a diamond.

*Screen:* the graph. qty turns 3; subtotal 60 (ICE). An arrow pulses from subtotal to total first: total shows "64" in coral with "60 + 4 (old tax)"; free shipping recomputes on 64. Then subtotal → tax: 6; tax → total: 66; free shipping recomputes again. On 64, free shipping flashes "no" in coral. A counter "recomputations: 8" (from the simulation: subtotal, total, free shipping, banner, tax, total, free shipping, banner). The final total 66 and "yes" in ICE against the coral 64 and "no". The two paths subtotal → total and subtotal → tax → total outlined: "diamond".

### 4. Diamonds multiply

> A spreadsheet or a user interface is full of diamonds, and they chain one after another.
> In the observer pattern, each diamond makes everything after it run twice. Two diamonds in a row make the last value run four times. Three make it eight.
> With ten diamonds in a row, a single change recomputes the last value one thousand and twenty-four times. With twenty, over a million.
> Recomputing everything in the right order would compute each value exactly once.

*Screen:* a chain of diamonds, drawn left to right. A counter on the last node as the naive wave runs: 2, 4, 8… Then a table from the simulation: "diamonds: 1 → 2 runs, 2 → 4, 3 → 8, 10 → 1,024". "in order: 1 run each".

### 5. Mark, then compute in order

> So the fix works in two phases.
> First, mark. Follow the arrows from the change, and mark everything reachable as out of date. Nothing is computed yet.
> Then compute, in order. To get the order, give each value a height. The price and the quantity are inputs: height zero. The subtotal reads only inputs: height one. The tax reads the subtotal: height two. The total reads the tax, so it sits above it: height three. Free shipping is four, and the banner five.
> The rule: a value's height is one more than the highest height it reads.
> Recompute only the marked values, from the lowest height up. By the time a value is computed, every one of its inputs is already up to date.
> The total waits until the tax is six, and becomes sixty-six the first time. There's no sixty-four, and each value is computed once: five recomputations instead of eight.
> On the chain of ten diamonds, the last value runs once instead of a thousand and twenty-four times.
> Spreadsheets, build tools and reactive libraries all use some version of this: dependencies first, each value once.
> And the free-shipping check runs once, on sixty-six, and says yes.

*Screen:* the graph with heights written on each node: 0, 0, 1, 2, 3, 4, 5. Phase 1: an amber wave marks subtotal, tax, total, free shipping, banner (no values change). Phase 2: nodes recompute in height order, each ticking once: 60, 6, 66, yes, "Free shipping!". Counter "recomputations: 5". The chain of ten diamonds: "last value: 1 run (was 1,024)".

### 6. Doing less

> The ordered wave still recomputes everything downstream, even a value that comes out the same, and even a value nobody is looking at. Two refinements cut that out.
> The first is early cutoff. Change the quantity again, from three to four. The subtotal, the tax and the total all change: eighty, eight, eighty-eight. Free shipping is recomputed, and it's still yes. It didn't change, so nothing that reads it needs to run. The wave stops there.
> The second is laziness. A value nobody is looking at doesn't need to be computed yet. The system marks it as out of date, and computes it only when something reads it.

*Screen:* qty → 4; subtotal 80, tax 8, total 88, free shipping recomputes: "yes (unchanged)". A barrier appears on its outgoing arrow; the banner that reads it stays untouched ("not recomputed"). Then a hidden cell (greyed "not on screen") gets an amber mark but no value until a reader asks for it: "marked now, computed when read".

### 7. Where do the arrows come from?

> All of this depends on the graph being right. So where do the arrows come from?
> Some formulas read different values depending on the data. Imagine a different cart, whose total reads a coupon cell only when the customer has a coupon. There, the arrows change as the values change.
> Spreadsheets and modern UI frameworks handle this by recording what each formula actually read, every time it runs. The graph, and the heights with it, are always the ones from the last run.
> Make, the classic build tool, takes the other route. You list, in a file called a Makefile, what each output is built from, unless you set up the compiler to write that list for you. If one is missing, the graph is wrong, and the result goes stale.
> Here's a program built from a source file that includes a header, whose Makefile lists only the source file. Change the free-shipping threshold in the header from sixty-five to seventy-five, and run make. Make says the program is up to date, and it still says sixty-five.
> Declare the header, and make rebuilds it.
> And one kind of graph can't be ordered at all. If a formula depends, through others, on itself, no value can come first. Excel calls this a circular reference. By default it warns instead of computing, though it can be told to iterate toward an answer.

*Screen:* a separate example, labelled "another cart": `total = subtotal + tax − IF(has_coupon, coupon, 0)`: with has_coupon = no, there's no arrow from coupon; with yes, the arrow appears. A small "recorded on last run" list under the formula. Then a terminal (data/make_stale.txt): the Makefile `app: main.c`; `free shipping from $65`; util.h edited to 75; `make: 'app' is up to date.`; `free shipping from $65` (coral). Then `app: main.c util.h`; `cc -o app main.c`; `free shipping from $75`. Then a three-node loop A → B → C → A with no height possible; Excel's circular-reference warning as a caption.

### 8. The answer

> So what does the spreadsheet know that your code doesn't? It knows the dependency graph.
> From that graph it answers two questions: what is out of date after a change, and in what order to recompute it.
> The answer to the first is everything downstream of the change, and nothing else. The answer to the second is height order, lowest first, each value once, stopping where nothing changed.
> Get the order wrong, and you'll see values that never should exist, like a total of sixty-four. And you'll do the same work many times over.
> That same machine is inside Excel, inside build systems like Make and Bazel, and inside the reactive parts of UI frameworks such as Vue, Solid and Angular's signals.

*Screen:* the cart graph once more, with the ordered wave: 60, 6, 66, yes. Two questions as two lines: "what is out of date? → everything downstream" and "in what order? → by height, once each, stop where unchanged". Then the same graph shape relabelled three times: cells (Excel), files (Make, Bazel), UI state (Vue, Solid, Angular signals). End card with the takeaway and references: Bainomugisha et al., "A Survey on Reactive Programming", ACM Computing Surveys (2013); Mokhov, Mitchell & Peyton Jones, "Build Systems à la Carte", ICFP (2018); Cooper & Krishnamurthi, "Embedding Dynamic Dataflow in a Call-by-Value Language" (FrTime), ESOP (2006); Microsoft, "Excel Recalculation"; Minsky, "Seven Implementations of Incremental" (2016).


## Evidence

| Claim | Source |
|---|---|
| Reactive programming "is essentially about embedding the spreadsheet-like model in programming languages"; the spreadsheet is the canonical opening example | Bainomugisha et al., ACM Computing Surveys 45(4), 2013, §1-2 |
| Build systems and spreadsheets are the same problem ("Excel is a build system in disguise") | Mokhov, Mitchell & Peyton Jones, "Build Systems à la Carte", ICFP 2018, §2 |
| The observer pattern gives no ordering or consistency guarantee | Maier, Rompf & Odersky, "Deprecating the Observer Pattern", EPFL 2010, §1; Gamma et al., Design Patterns (1994) |
| Glitch: a momentarily inconsistent value from combining fresh and stale inputs; the diamond example | Bainomugisha et al. 2013 §3.3; Cooper & Krishnamurthi (FrTime), ESOP 2006, §3.2 |
| Cart numbers: $20 × 2 = $40, tax $4, total $44; qty 3: $60, $6, $66; free shipping from $65; the notify-total-first trace computes $64, free shipping "no", and 8 recomputations; height order 5 | sims/propagate.py, data/propagate.json |
| Stacked diamonds: naive depth-first push recomputes the last node 2^k times (1,024 for 10, 1,048,576 for 20); height order once | sims/propagate.py, data/propagate.json; Minsky, "Seven Implementations of Incremental" (2016): "one update becomes two, becomes four, becomes eight" |
| Heights plus ordered recomputation guarantee no glitches and no redundant computation (static, acyclic graph) | FrTime §3.2; Maier et al. §6.2 (levels); BSALC §4 (topological scheduler) |
| Early cutoff: an unchanged value stops propagation | BSALC §2.3; Bainomugisha et al. §3.3; Jane Street Incremental "cutoff"; sims/propagate.py (qty 3 → 4: free shipping unchanged, banner not recomputed) |
| Laziness: out-of-date marks pushed eagerly, values computed when read | TC39 Signals proposal README (2024), FAQ "push-pull"; MobX docs ("Computed values are updated lazily"); Milo, "Super-Charging Fine-Grained Reactive Performance" (2022); Elliott, "Push-Pull Functional Reactive Programming", Haskell Symposium 2009 |
| Dynamic dependencies (IF, INDIRECT); recording what each formula read on its last run | BSALC §2.2; Knockout docs (dependencies re-detected on each evaluation); TC39 Signals README; Vue "Reactivity in Depth" |
| Make relies on declared prerequisites (or compiler-generated ones, -MMD); a missing header gives a stale build | GNU Make manual, "Generating Prerequisites Automatically"; sims/make_stale/run.sh, data/make_stale.txt (GNU Make, cc; threshold 65 → 75) |
| Excel detects circular references and warns by default; iterative calculation is an option | Microsoft, "Excel Recalculation"; Excel circular reference documentation |
| Excel builds a dependency tree and calc chain, marks dirty cells, recalculates in chain order | Microsoft, "Excel Recalculation" |
| Vue, Solid and Angular signals track dependencies at run time | Vue "Reactivity in Depth"; Carniato, "A Hands-on Introduction to Fine-Grained Reactivity" (2021); Angular signals guide |
| Bazel: build graph with content-based caching and dependency tracking | BSALC §2.4 |

