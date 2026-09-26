# Reactive programming: canonical treatment

## 1. Canonical worked example
**The spreadsheet cell-dependency graph** (cell formulas + a "diamond" case: `A1→B1`, `A1→C1`, `B1,C1→D1`) is the dominant academic example, because every reader already has the mental model, it's a DAG with an obvious recompute order, and the diamond shape cleanly demonstrates the glitch problem.
- Mokhov, Mitchell & Peyton Jones, **"Build Systems à la Carte"** (ICFP/Haskell Symposium 2018; JFP 2020) — uses Excel as the running example against Make, Shake, Bazel, Nix.
- Bainomugisha et al., **"A Survey on Reactive Programming"**, ACM Computing Surveys 2013 — spreadsheet + diamond graph as motivating example for glitches.
- Maier & Odersky, **"Deprecating the Observer Pattern with Scala.React"**, EPFL tech report 2012 — introduces the diamond example specifically to define glitch-freedom.

A **second, competing example** exists in industry sources: a tiny UI (a counter/name label bound to two input fields), used by framework docs — Knockout.js's `computed observables` tutorial, Vue's "Reactivity in Depth" guide, MobX's Celsius/Fahrenheit example. The spreadsheet example is more common/foundational in academic and cross-domain treatments; the UI example dominates framework-specific tutorials.

## 2. Standard progression
1. Static dependency graph (nodes = values, edges = formulas), assume a DAG.
2. Push vs. pull propagation (eager notify vs. lazy recompute) — from Conal Elliott, **"Push-Pull Functional Reactive Programming"**, Haskell Symposium/TFP 2009.
3. Correct recompute order via topological sort / dirty-marking.
4. The diamond example → glitches → need for atomic/batched updates.
5. Minimal (incremental) recomputation vs. recompute-everything, as a design spectrum (Build Systems à la Carte's rebuilding strategies: dirty bit / verifying trace / constructive trace).
6. Dynamic dependencies (a formula's inputs depend on its own prior output, e.g. `IF`) — presented as the hard case, per Mokhov et al.'s **applicative vs. monadic** task distinction.
7. Cycles / circular references, handled last as the error/edge case.

This order is mirrored in Acar's self-adjusting computation material (from-scratch consistency introduced before incremental update) and in most FRP courses (behaviors/events before arrowized/dynamic switching).

## 3. Models and terminology
- **Dataflow programming**: nodes = computations, edges = data dependencies, propagation is push-based. Generic term used across build systems, spreadsheets, stream processors.
- **Functional Reactive Programming (FRP)**: values are **Behaviors** (continuous, time-varying) and **Events** (discrete occurrences); denotational semantics as functions of time. Elliott & Hudak, **"Functional Reactive Animation" (Fran)**, ICFP 1997. Arrowized variant: Yampa (Hudak et al.).
- **Observer pattern**: classic push-based subscribe/notify, no ordering guarantee. Gamma, Helm, Johnson, Vlissides, **Design Patterns** ("Observer", 1994) — this is the pattern later shown to admit glitches.
- **Self-adjusting computation**: "modifiable references," change propagation; guarantee is **from-scratch consistency** (incremental result == full recompute). Acar, Blelloch, Harper, **"Adaptive Functional Programming"**, POPL 2002 / TOPLAS 2006; Acar's PhD thesis, CMU 2005.
- **Build-system terms** (Mokhov et al. 2018): "task," "key/value store," "trace"; tasks are **applicative** (static deps, analyzable ahead of time) or **monadic** (deps depend on earlier results, only discoverable during the build).
- **Terminology drift across sources**: "signal" (pre-0.17 Elm) ≈ "Behavior" (FRP) ≈ "Observable" (Rx/MobX/Knockout) ≈ "ref"/"computed" (Vue) ≈ "formula" (spreadsheets) ≈ "task" (build systems). *Uncertain: exact first use of "signal" in this sense — likely traces to synchronous dataflow languages (Esterel/Lustre), not to Elm.*

## 4. Key results and where they break
- **Topological order guarantees correctness** for a static DAG, O(V+E) via Kahn's algorithm/DFS — but only while the graph doesn't change and has no cycle.
- **Glitch-freedom** (Maier & Odersky 2012): no observer ever sees a value computed from a stale mix of updated/un-updated inputs. Achieved via transactional/batched propagation (Vue's job queue microtask, MobX's transactions, Scala.React's turns) — breaks down if updates are applied eagerly/synchronously node-by-node.
- **From-scratch consistency** (Acar et al., POPL 2002/TOPLAS 2006): incremental result provably equals full re-execution — holds only for computations expressed through the library's modifiable references/monadic style; ordinary mutation outside that discipline invalidates the guarantee.
- **Build Systems à la Carte's** central result: characterizes real systems along two orthogonal axes — task dependencies (applicative/monadic) and scheduler+rebuilder strategy — and shows dynamic (monadic) dependencies force a **restarting** (Excel-style: rerun and detect new deps) or **suspending** (Shake-style: continuation-based) scheduler, since static topological scheduling no longer applies.
- Breaks down further with **impure/volatile computations** (Excel's `NOW()`, `RAND()`), which must be re-run every cycle regardless of dependency state, and with **true cycles**, which need either an error (Excel's circular-reference warning) or iterative fixed-point evaluation (Excel's "enable iterative calculation" mode).

## 5. Standard concrete examples in the sources
- Spreadsheet: `A1=5, A2=10, A3=A1+A2`; diamond: `B1=A1*2, C1=A1*3, D1=B1+C1`.
- Excel's circular-reference dialog as the canonical cycle-failure case.
- Knockout.js docs: `fullName = ko.computed(() => firstName() + " " + lastName())`.
- Vue "Reactivity in Depth": literally uses spreadsheet-style names, `const A2 = computed(() => A0.value + A1.value)`, and explicitly compares Vue's reactivity to a spreadsheet.
- MobX docs: Celsius/Fahrenheit temperature converter with `observable`, `computed`, `autorun`.
- Make: `foo.o: foo.c foo.h` — Feldman, **"Make — A Program for Maintaining Computer Programs"**, 1979; GNU Make manual.
- Self-adjusting computation tutorials: incremental list-sum / incremental quicksort under a single element change (Acar's course notes; *uncertain on exact canonical published example*).

## 6. Misconceptions the canonical treatment corrects
- Conflating "reactive programming" (dependency-graph value propagation) with **ReactiveX/Rx** (async event streams + backpressure) — Bainomugisha et al. explicitly separate these as related but distinct.
- Conflating it with the **Reactive Manifesto** (Bonér et al., 2014) — that's about distributed-system resilience/elasticity, an unrelated usage of "reactive."
- Assuming recompute-everything is always the "wrong"/naive choice — Build Systems à la Carte frames it as one legitimate point in the design space (simplicity vs. minimality trade-off), which is also why React's re-render-and-diff model is a defensible design, not a mistake.
- Assuming dependency graphs are always static and acyclic — real systems must handle dynamic deps and cycles.
- Assuming push propagation is always synchronous/immediate — most production systems batch (push a "dirty" signal, pull/recompute later), per Elliott's push-pull framing.

## 7. For a short lesson
- **Essential**: dependency graph model; push vs. pull; topological/dirty-based recompute order; the diamond glitch example; one guarantee stated informally (glitch-freedom).
- **Common extra**: dynamic dependencies (applicative vs. monadic), minimal-rebuild via memo/traces, one real mechanism case study (Proxy-based Vue, or Make's timestamps).
- **Leave out**: FRP's formal denotational semantics (Behaviors as functions of continuous time), self-adjusting computation's type-theoretic guarantees, the full applicative/monadic × scheduler/rebuilder taxonomy, distributed/concurrent reactive systems.

## 8. Real systems and their mechanism
- **Excel**: dependency graph + dirty-bit minimal recalculation; falls back for volatile functions/cycles. (Mokhov et al. 2018; *exact Microsoft engineering source for calc-engine internals uncertain — commonly cited talks by Simon Peyton Jones on Excel exist but I can't confirm a precise citation.*)
- **Make**: file-mtime comparison as staleness check (Feldman 1979).
- **Shake**: monadic tasks, continuation-based suspending scheduler, verifying traces (Mitchell, **"Shake Before Building"**, ICFP 2012).
- **Bazel/Buck**: mostly applicative (statically declared) deps, content-hash caching.
- **Nix**: content-addressed build dependencies.
- **Vue 3**: Proxy-based getter/setter interception, effect tracking ("Reactivity in Depth" docs); Vue 2 used `Object.defineProperty` + Dep/Watcher (Observer pattern).
- **MobX**: calls itself "Transparent Functional Reactive Programming," dependency tracking + transactions.
- **SolidJS**: fine-grained signals compiled directly into DOM updates, no virtual DOM (Ryan Carniato's talks/blog).
- **React**: NOT dependency-graph reactivity — re-renders a subtree and diffs a virtual DOM; often contrasted with the above (Rich Harris, **"Virtual DOM is pure overhead"**, 2018).
- **Elm**: pre-0.17 used FRP "Signals" (Czaplicki, **"Asynchronous Functional Reactive Programming for GUIs"**, 2012 thesis/PLDI paper); replaced by The Elm Architecture (not dependency-graph based).
- **Self-adjusting computation implementations**: CEAL, and Adapton (Hammer et al., ~2014). *Uncertain on exact venues.*

## 9. Overstated or subtly wrong claims
- "Reactive programming removes the need to reason about order" — false; scheduling *is* the hard problem the field exists to solve.
- "Fine-grained reactivity is strictly faster than virtual-DOM diffing" — an ongoing engineering debate, not a settled result; workload-dependent.
- "Spreadsheets always recompute only what changed" — true for pure formulas, false for volatile functions and iterative/circular modes.
- Using "reactive" for Rx/Reactive Streams and for spreadsheet-style reactivity interchangeably — different concerns (async streams/backpressure vs. dependency propagation) that the standard survey explicitly keeps apart.

## 10. Best learned by watching / doing / reading
- **Watch (narrated animation)**: the DAG lighting up over time, push vs. pull timing, and the diamond glitch — inherently temporal and best shown, not described.
- **Do (interactive/code)**: wire up a `computed` in Vue/MobX/Knockout, or hand-build topological sort + watch a cycle break it, or touch a file and trace `make`'s rebuild — scheduling intuition is kinesthetic.
- **Read**: the formal guarantees (glitch-freedom definition, from-scratch consistency theorem) and comparative taxonomies (applicative vs. monadic tasks) — dense, precise claims better absorbed as text you can pause on.

---
**Confidence note**: paper/author/year attributions above (Fran 1997, Adaptive Functional Programming POPL 2002, Scala.React 2012, Bainomugisha survey 2013, Push-Pull FRP 2009, Build Systems à la Carte 2018, Shake ICFP 2012, Make 1979, Elm thesis 2012) are ones I'm confident in. Items marked *uncertain* above (Excel's internal calc-engine publication, exact SAC canonical example, precise venue for Adapton) should be verified before quoting in the video if you want an on-screen citation.
