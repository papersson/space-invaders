You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Argument

**Question.** In ordinary code, `total = subtotal + tax` runs once. Change the quantity later and the total is stale until someone remembers to recompute it. In a spreadsheet, change a cell and every formula that depends on it updates, correctly. Build tools and UI frameworks do the same job. How does a system that keeps derived values up to date decide what to recompute, and in what order, and what goes wrong when it gets that wrong?

**Answer.** It keeps a dependency graph: for each formula, the values it reads. A change makes everything downstream out of date. The obvious approach, where each changed value immediately tells its readers to recompute (the observer pattern), breaks on a diamond: a value reached by two paths is computed from one fresh and one stale input, briefly showing a total that was never true (a glitch), and is computed twice; stacked diamonds double the work each time. The fix is order: mark everything downstream as out of date, then recompute in dependency order, each value once, after all its inputs. Two refinements save work: stop where a recomputed value didn't change, and don't compute what nobody is looking at. The graph must be complete: systems that record what each formula actually read get it right; a dependency declared by hand and forgotten gives a stale result; a cycle has no order at all.

**Takeaway.** A reactive system is a dependency graph plus two answers: what is out of date, and in what order to recompute it. Recompute in dependency order, each value once, and stop where nothing changed.

**Wrong model.** When a value changes, just notify everything that uses it (the observer pattern); as long as everything eventually gets recomputed, the order doesn't matter.

**Objectives.**
1. Describe a dependency graph and which values a change makes out of date.
2. Explain why notifying dependents immediately produces a glitch and repeated work on a diamond, and why stacked diamonds make it exponential.
3. Explain the fix: mark, then recompute in dependency (height) order, each value once.
4. Explain early cutoff and laziness.
5. Explain why dependencies are recorded as formulas run, what a forgotten dependency does, and why a cycle can't be ordered.
6. Recognize the same machine in spreadsheets, build systems and UI frameworks.


## Chain

1. The question: code computes a total once; a spreadsheet keeps it right. How does it decide what to recompute, and in what order?
2. Therefore a dependency graph: each formula's inputs. A change makes everything downstream out of date, and nothing else.
3. The obvious way: each value tells its readers to recompute right away. But on a diamond, the total is computed from a fresh subtotal and a stale tax: $64, a total that never existed. And it's computed twice.
4. But stack diamonds and the repeated work doubles each time: ten diamonds, 1,024 recomputations of the last value.
5. Therefore two phases: mark everything downstream, then recompute in height order, each once, after its inputs. No glitch, no repeats.
6. Therefore do less: stop where a value didn't change (early cutoff); don't compute what nobody reads (laziness).
7. But the order is only as good as the graph: dependencies must be recorded as formulas run; a forgotten one gives a stale result (Make); a cycle has no order (Excel's circular reference).
8. Therefore the answer: spreadsheets, build systems and UI frameworks are the same machine; recompute in dependency order, each once, stop where nothing changed.

Deviation from the canonical progression: the observer pattern's other problems (leaked listeners, side effects) are left out; the research lists them as standard but the diamond carries the argument. Push-pull is introduced only as "don't compute what nobody reads".


## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> An online cart holds two items at twenty dollars each. The subtotal is forty dollars, tax at ten percent is four, and the total is forty-four.
> In ordinary code, the total is computed once. If the customer changes the quantity to three, the total still says forty-four, until some piece of code remembers to compute it again.
> In a spreadsheet, you never have to remember. Change the quantity, and the subtotal, the tax and the total all update, correctly, every time.
> Build tools do the same with files: change one source file, and exactly the parts that depend on it are rebuilt. So do many UI frameworks: change a value, and the screen updates.
> How does a system like that decide what to recompute, and in what order? And what goes wrong when it gets that wrong?

*Screen:* a small sheet: price $20, qty 2, subtotal $40, tax (10%) $4, total $44, and "free shipping (over $50)": no. First a code box: `total = subtotal + tax` and a value "44"; qty changes to 3; the code's total still reads 44 (coral, "stale"). Then the sheet: qty → 3 and the column updates to $60, $6, $66, free shipping: yes. Three labels: "spreadsheets", "build tools", "UI frameworks". The question.

### 2. The dependency graph

> Each formula reads some other values. The subtotal reads the price and the quantity. The tax reads the subtotal. The total reads the subtotal and the tax. Free shipping reads the total, and the banner at the top of the cart reads free shipping.
> Draw an arrow from each value to every formula that reads it, and you have a dependency graph.
> When the quantity changes, follow the arrows. Everything you can reach is now out of date: the subtotal, the tax, the total, free shipping, the banner.
> Everything you can't reach is still correct. The price didn't change, and nothing it feeds needs recomputing because of this edit.

*Screen:* the sheet's cells lift off into nodes: price and qty at the left, subtotal, tax, total, free shipping and the banner ("Spend $50 for free shipping") to the right, arrows from inputs to readers. qty flashes; a wave follows the arrows and colours every reachable node amber ("out of date"); price stays grey.

### 3. Just tell the readers

> The obvious way to update them is to let each value tell its readers. When the quantity changes, it tells the subtotal to recompute. The subtotal then tells each of its own readers, and so on down the arrows.
> This is the observer pattern, and it's how a lot of hand-written code keeps things in sync.
> Follow it. The quantity becomes three, and the subtotal becomes sixty. The subtotal has two readers, the tax and the total. Say it tells the total first.
> The total adds the new subtotal, sixty, to the tax, which is still the old four. The total becomes sixty-four.
> Sixty-four was never a correct total. The right answer was forty-four before the change and sixty-six after it. Anything that reads the total at this moment, like the free-shipping check, runs on a wrong number. A value like that, built from a mix of new and old inputs, is called a glitch.
> Then the subtotal tells the tax, which becomes six. The tax tells the total, which is computed again: sixty-six. Free shipping runs a second time too.
> The trouble comes from one shape. The subtotal reaches the total by two paths, directly and through the tax. A shape like that is called a diamond.

*Screen:* the graph. qty turns 3; subtotal 60 (ICE). An arrow pulses from subtotal to total first: total shows "64" in coral with "60 + 4 (old tax)"; free shipping recomputes on 64. Then subtotal → tax: 6; tax → total: 66; free shipping recomputes again. A counter "recomputations: 8" (from the simulation: subtotal, total, free shipping, banner, tax, total, free shipping, banner). The two paths subtotal → total and subtotal → tax → total outlined: "diamond". Caption: "right totals: $44 before, $66 after".

### 4. Diamonds multiply

> A spreadsheet or a user interface is full of diamonds, and they chain one after another.
> In the notify-right-away scheme, each diamond makes everything after it run twice. Two diamonds in a row make the last value run four times. Three make it eight.
> With ten diamonds in a row, a single change recomputes the last value one thousand and twenty-four times. With twenty, over a million.
> Recomputing everything in the right order would compute each value exactly once.

*Screen:* a chain of diamonds, drawn left to right. A counter on the last node as the naive wave runs: 2, 4, 8… Then a table from the simulation: "diamonds: 1 → 2 runs, 2 → 4, 3 → 8, 10 → 1,024, 20 → 1,048,576". "in order: 1 run each".

### 5. Mark, then compute in order

> So the fix works in two phases.
> First, mark. Follow the arrows from the change, and mark everything reachable as out of date. Nothing is computed yet.
> Then compute, in order. Give each value a height. An input has height zero. A formula's height is one more than the highest of its inputs. So the subtotal is one, the tax is two, the total is three, free shipping is four, the banner is five.
> Recompute the marked values from the lowest height up. By the time a value is computed, every one of its inputs is already up to date.
> The total waits until the tax is six, and becomes sixty-six the first time. There's no sixty-four, and each value is computed once: five recomputations instead of eight.
> On the chain of ten diamonds, the last value runs once instead of a thousand and twenty-four times.
> Spreadsheets, build tools and reactive libraries all use some version of this: dependencies first, each value once.

*Screen:* the graph with heights written on each node: 0, 0, 1, 2, 3, 4, 5. Phase 1: an amber wave marks subtotal, tax, total, free shipping, banner (no values change). Phase 2: nodes recompute in height order, each ticking once: 60, 6, 66, yes, "Free shipping!". Counter "recomputations: 5". The chain of ten diamonds: "last value: 1 run (was 1,024)".

### 6. Doing less

> Two refinements cut the work further.
> The first is early cutoff. Change the quantity again, from three to four. The subtotal, the tax and the total all change: eighty, eight, eighty-eight. Free shipping is recomputed, and it's still yes. It didn't change, so nothing that reads it needs to run. The wave stops there.
> The second is laziness. A value nobody is looking at doesn't need to be computed yet. The system marks it as out of date, and computes it only when something reads it.
> Marking eagerly and computing lazily is often called push-pull: the "out of date" marks are pushed forward, and the values are pulled when needed.

*Screen:* qty → 4; subtotal 80, tax 8, total 88, free shipping recomputes: "yes (unchanged)". A barrier appears on its outgoing arrow; the banner that reads it stays untouched ("not recomputed"). Then a hidden cell (greyed "not on screen") gets an amber mark but no value until a reader asks for it: "push: mark", "pull: compute".

### 7. Where do the arrows come from?

> All of this depends on the graph being right. So where do the arrows come from?
> Some formulas read different values depending on the data. A total with a discount might read a coupon cell only when the customer has a coupon. So the arrows can change as values change.
> Spreadsheets and modern UI frameworks handle this by recording what each formula actually read, every time it runs. The graph is always the one from the last run.
> Build tools like Make take the other route: you write the dependencies down by hand. If one is missing, the graph is wrong, and the result goes stale.
> Here's a program whose source file includes a header, but whose Makefile lists only the source file. Change the free-shipping threshold in the header from fifty to sixty-five, and run make. Make says the program is up to date, and it still says fifty.
> Declare the header, and make rebuilds it.
> And one kind of graph can't be ordered at all. If a formula depends, through others, on itself, no value can come first. Excel calls this a circular reference, and warns instead of computing.

*Screen:* a formula `total = subtotal + tax − IF(has_coupon, coupon, 0)`: with has_coupon = no, there's no arrow from coupon; with yes, the arrow appears. A small "recorded on last run" list under the formula. Then a terminal (data/make_stale.txt): the Makefile `app: main.c`; `free shipping from $50`; util.h edited to 65; `make: 'app' is up to date.`; `free shipping from $50` (coral). Then `app: main.c util.h`; `cc -o app main.c`; `free shipping from $65`. Then a three-node loop A → B → C → A with no height possible; Excel's circular-reference warning as a caption.

### 8. The answer

> So what does the spreadsheet know that your code doesn't? It knows the dependency graph.
> From that graph it answers two questions: what is out of date after a change, and in what order to recompute it.
> The answer to the first is everything downstream of the change, and nothing else. The answer to the second is dependency order, each value once, stopping where nothing changed.
> Get the order wrong and you see values that never should exist, like a total of sixty-four, and do the same work many times over.
> That same machine is inside Excel, inside build systems like Make and Bazel, and inside the reactive parts of UI frameworks such as Vue, Solid and Angular's signals.

*Screen:* the cart graph once more, with the ordered wave: 60, 6, 66, yes. Two questions as two lines: "what is out of date? → everything downstream" and "in what order? → by height, once each, stop where unchanged". Then the same graph shape relabelled three times: cells (Excel), files (Make, Bazel), UI state (Vue, Solid, Angular signals). End card with the takeaway and references: Bainomugisha et al., "A Survey on Reactive Programming", ACM Computing Surveys (2013); Mokhov, Mitchell & Peyton Jones, "Build Systems à la Carte", ICFP (2018); Cooper & Krishnamurthi, "Embedding Dynamic Dataflow in a Call-by-Value Language" (FrTime), ESOP (2006); Microsoft, "Excel Recalculation"; Minsky, "Seven Implementations of Incremental" (2016).

