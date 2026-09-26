# Reactive programming, the canonical treatment: how derived values stay up to date

Research answer for the lesson prompt in `canonical_prompt.md`. The topic goes by different names in different fields. Programming-language research calls it **reactive programming**. Algorithms and programming-language research on efficiency call it **incremental or self-adjusting computation**. Tooling calls it **build systems**. UI frameworks call it **fine-grained reactivity / signals**. All four study the same thing: propagating changes over a dependency graph.

## Key sources (short tags used inline)

- **[Survey]** Bainomugisha, Lombide Carreton, Van Cutsem, Mostinckx, De Meuter, "A Survey on Reactive Programming", *ACM Computing Surveys* 45(4), 2013 ([tech-report PDF](http://soft.vub.ac.be/Publications/2012/vub-soft-tr-12-13.pdf)). This is the standard taxonomy paper.
- **[BSALC]** Mokhov, Mitchell, Peyton Jones, "Build Systems à la Carte", ICFP 2018 (PACMPL 2, art. 79) ([PDF](https://www.microsoft.com/en-us/research/uploads/prod/2018/03/build-systems.pdf)). An extended version is "Build systems à la carte: Theory and practice", *JFP* 30, 2020. It is the standard source that puts spreadsheets and build systems in one framework.
- **[FrTime]** Cooper & Krishnamurthi, "Embedding Dynamic Dataflow in a Call-by-Value Language", ESOP 2006 ([PDF](https://cs.brown.edu/~sk/Publications/Papers/Published/ck-frtime/paper.pdf)).
- **[DOP]** Maier, Rompf, Odersky, "Deprecating the Observer Pattern", EPFL tech report 2010 (Scala.React) ([PDF](https://raw.githubusercontent.com/papers-we-love/papers-we-love/refs/heads/main/languages-paradigms/functional_reactive_programming/deprecating-the%20observer-pattern.pdf)).
- **[Minsky16]** Yaron Minsky, "Seven Implementations of Incremental", Jane Street tech talk, 2016 ([transcript](https://www.janestreet.com/tech-talks/seven-implementations-of-incremental/)).
  - **[Minsky15]** "Introducing Incremental", 2015 ([blog](https://blog.janestreet.com/introducing-incremental/)).
  - **[Minsky14]** "Breaking down FRP", 2014 ([blog](https://blog.janestreet.com/breaking-down-frp/)).
- **[Milo22]** Milo (SolidJS team), "Super-Charging Fine-Grained Reactive Performance", 2022 ([dev.to](https://dev.to/modderme123/super-charging-fine-grained-reactive-performance-47ph)). The TC39 proposal cites it for "graph coloring".
- **[TC39]** JavaScript Signals proposal README, Stage 1, April 2024 ([GitHub](https://github.com/tc39/proposal-signals)). It was co-designed with the authors of Angular, MobX, Preact, Qwik, Solid, Svelte, Vue and others.
- **[MobX15]** Michel Weststrate, "Becoming fully reactive: an in-depth explanation of MobX", Dec 2015 ([HackerNoon](https://hackernoon.com/becoming-fully-reactive-an-in-depth-explanation-of-mobservable-55995262a254)).
- **[Elliott09]** Conal Elliott, "Push-Pull Functional Reactive Programming", Haskell Symposium 2009 ([page](http://conal.net/papers/push-pull-frp/)).
  - **[Fran97]** Elliott & Hudak, "Functional Reactive Animation", ICFP 1997.
- **[Adapton]** Hammer, Khoo, Hicks, Foster, "Adapton: Composable, Demand-Driven Incremental Computation", PLDI 2014.
  - **[miniAdapton]** Fisher, Hammer, Byrd, Might, 2016 ([arXiv](https://arxiv.org/abs/1609.05337)).
- **[Excel]** Microsoft Learn, "Excel Recalculation" ([docs](https://learn.microsoft.com/en-us/office/client-developer/excel/excel-recalculation)).
- **[lord20]** Lord, "How to Recalculate a Spreadsheet", Nov 2020 ([lord.io](https://lord.io/spreadsheets/)). A widely shared engineering article.
- **[Carniato21]** Ryan Carniato (SolidJS author), "A Hands-on Introduction to Fine-Grained Reactivity" and "Building a Reactive Library from Scratch", Feb 2021 (dev.to).
- **[Odersky]** EPFL/Coursera, *Functional Program Design in Scala*. The lectures are "Imperative Event Handling: The Observer Pattern", "Functional Reactive Programming" and "A Simple FRP Implementation". They were kept as week 5 of the 2020 redesign ([scala-lang](https://www.scala-lang.org/2020/03/10/functional-program-re-design.html)).
- **[rustc]** rustc-dev-guide, "Incremental compilation in detail" ([link](https://rustc-dev-guide.rust-lang.org/queries/incremental-compilation.html)).
  - **[Salsa]** Salsa book, "The red-green algorithm" ([link](https://salsa-rs.github.io/salsa/reference/algorithm.html)).
- **[SICP]** Abelson & Sussman, *SICP* 2nd ed.: §3.3.4 "A Simulator for Digital Circuits" (event agenda) and §3.3.5 "Propagation of Constraints".

---

## 1. The canonical worked example

There are two standard examples. They do different jobs and are almost always used together.

**(a) The spreadsheet formula: "C = A + B, and C stays correct when A changes."** This is the universal opening example.

- [Survey] §2 opens with `var1 = 1; var2 = 2; var3 = var1 + var2`. It contrasts imperative assignment, where var3 stays 3, with reactive semantics, where var3 is recomputed. It says "Reactive programming is essentially about embedding the spreadsheet-like model in programming languages" (§1).
- Wikipedia's "Reactive programming" article uses `a := b + c`.
- Vue's "Reactivity in Depth" opens with a spreadsheet where `A2 = A0 + A1`.
- [BSALC] §2.2 and §3.2 use `A1: 10, A2: 20, B1: A1 + A2, B2: B1 * 2`, and state "Excel is a build system in disguise."
- Adapton's motivating example is an incremental spreadsheet evaluator ([miniAdapton] App. C: `n1..n3`, `p1 = n1+n2`, `p2 = p1+n3`).
- Jane Street calls Incremental "a fancy spreadsheet" [Minsky15].
- Rich Harris's talk "Rethinking reactivity" (2019) also uses the spreadsheet.

Why it is standard: every engineer has used one. It separates *what* (a formula, i.e. a relation) from *when* (recalculation). And it is literally all three systems at once: derived values, a UI, and a build system with dirty bits and a calc chain [BSALC Table 2].

**(b) The diamond, or "glitch", example.** One source reaches a node by two paths.

- [Survey] §3.3: `var1 = 1; var2 = var1 * 1; var3 = var1 + var2`. When var1 goes from 1 to 2, a naive implementation can momentarily show var3 = 3 before it settles at 4 (Fig. 3).
- [FrTime] §3.2: `(< seconds (+ 1 seconds))` should always be true, but it can be false if the outer node updates first. Wikipedia restates this as `t = seconds + 1; g = (t > seconds)`.
- [Milo22] uses an A→{B,C}→D diamond. [Minsky16] calls it a "recombinant graph".

Why it is standard: it is the smallest graph where recomputation **order** matters. It shows both failure modes at once: an inconsistent intermediate value (the glitch) and duplicated work.

**Which is more common:** the spreadsheet as the opener, and the diamond as the inevitable second example. For a single running example, the best choice is a small spreadsheet that contains a diamond. Examples are BSALC's `A1/A2/B1/B2` plus one cell that reads both `A1` and `B1`, or the Survey's `var1/var2/var3`.

Community-specific alternatives:

- **UI:** `counter → isEven → parity` [TC39]; `count → doubleCount` (Angular and Solid docs); `firstName, lastName → fullName` (Knockout docs, [MobX15], React's "You Might Not Need an Effect").
- **Builds:** `util.c, util.h, main.c → util.o, main.o → main.exe` [BSALC §2.1].
- The **temperature converter** (SICP §3.3.5 `9C = 5(F − 32)`; 7GUIs task 2, "bidirectional data flow") is the standard example of *multidirectional constraints*. That is a different model, so don't use it as the main example.

## 2. The standard progression

Sources that teach this from scratch follow almost the same order.

1. **An assignment versus a maintained relation** (the spreadsheet). Sources: [Survey] §2; Vue; the "VanillaJS counter" in [TC39].
2. **The manual solution: callbacks / the Observer pattern** (Gamma et al., *Design Patterns*, 1994), and its problems.
   - [Odersky] lecture 1 builds a `BankAccount` publisher/subscriber.
   - [DOP] §1 uses a mouse-drag example and lists the problems: side effects, broken encapsulation, composability, separation of concerns, scalability ("no guarantee for data consistency… a glitch"), uniformity, abstraction, resource management, semantic distance.
   - [TC39] shows pub/sub leading to "boilerplate… and a potential memory leak disaster".
   - Blackheath & Jones, *Functional Reactive Programming* (Manning 2016), ch. 1 "Stop listening!", §1.8 "Banishing the six plagues of listeners". *Uncertain:* the list, as I recall it, is unpredictable order, missed first event, messy state, threading issues, leaking callbacks, accidental recursion.
3. **The dependency graph and automatic dependency tracking.** A global "currently evaluating" stack records what a computation reads.
   - [Odersky] "A Simple FRP Implementation" uses a `caller` stack, then `DynamicVariable`.
   - [Carniato21] builds `createSignal` → `createEffect` → `createMemo`.
   - Knockout's docs (2010) describe the same idea.
4. **Naive push on the diamond fails.**
   - It produces a glitch plus double work [Survey §3.3; FrTime §3.2].
   - Stacked diamonds make the double work *exponential*. Breadth-first order does not fix it when the two paths have different lengths [Minsky16].
5. **Fix it with order.** Two standard ways:
   - Topological order via height/level plus a priority queue [FrTime; DOP §6.2; BSALC's "topological scheduler"; Excel's calc chain].
   - Or two-phase marking with counts: MobX's stale/ready notifications [MobX15]; Incremental v1 [Minsky16].
6. **Fix it with less work.**
   - Early cutoff: an unchanged value stops propagation [Survey §3.3 last paragraph; BSALC §2.3].
   - Laziness: compute only what is observed. Combined with pushed invalidation this gives push-pull [Elliott09; TC39; Milo22's "diamond problem" and "equality check problem"].
7. **Dynamic dependencies.**
   - `IF`/`INDIRECT` [BSALC §2.2]; conditional reads (Angular docs).
   - Re-tracking the dependencies on every run (Knockout).
   - Re-levelling nodes [FrTime §3.3; DOP §6.2.1; Incremental `bind`].
8. **Side effects, batching/transactions, cycles.**
   - MobX transactions; [TC39] effects and Watcher.
   - Excel circular-reference detection with optional iteration [Excel].
   - FrTime's `delay` operator for cycles [FrTime §3.5].
9. **Advanced topics:**
   - Memory that persists across runs (build systems: timestamps versus hashes/traces, cloud caches) [BSALC §4.2].
   - Distribution [Survey §5].
   - Continuous time [Fran97].

**Simpler versions are shown before the full ones:**

- Static DAG before dynamic dependencies.
- Eager push before push-pull.
- "Recompute everything" before minimal recomputation. [lord20] goes: VisiCalc sweeps → natural-order recalculation → dirty marking → topological sort → demand-driven (Salsa/Adapton/Incremental).
- Declared dependencies before tracked ones. [BSALC] §2 goes Make (static, timestamps) → Excel (dynamic, restarting) → Shake (suspending, early cutoff) → Bazel (cloud).
- [Minsky16]: two-pass counting → timestamp top-sort with a heap → heights → pseudo-heights.
- [Carniato21] explicitly says his toy library "is not glitch-free" before pointing to Solid's real algorithm.
- The [Survey]'s own axis order is: abstractions → evaluation model (push/pull) → glitch avoidance → lifting → multidirectionality → distribution.

## 3. Models and terminology

### The models

**Observer / callbacks** (GoF 1994)
- How it works: the source calls registered listeners.
- What it guarantees: only that listeners get called. There is no ordering or consistency guarantee ("no guarantee for data consistency in the observer pattern", [DOP] §1).

**Push, data-driven** ([Survey] §3.2.2)
- How it works: when a source changes, it immediately pushes to its dependents.
- What it guarantees: low latency. It is glitch-free and runs each node once per update *only if* the scheduler respects topological order. With order, per [FrTime] §3.2: "guarantees the absence of glitches and redundant computation."

**Pull, demand-driven** ([Survey] §3.2.1; Fran)
- How it works: a consumer computes a value when it needs it.
- What it guarantees: only demanded values are computed, from one consistent snapshot.
- The criticism: latency, and space/time leaks in lazy FRP [Survey quoting Hudak et al. 2003]. Without caching it re-samples, causing "wasteful recomputation and high reaction latency" [Elliott09].

**Push-pull hybrid** ([Elliott09]; [TC39] FAQ "push-pull"; Preact Signals; Reactively; Adapton)
- How it works: invalidation (dirty/stale/"check") is pushed eagerly; recomputation is pulled lazily on read.
- What it guarantees: glitch-free reads, laziness and memoization. With equality cutoff it gives [Milo22]'s two goals: "Efficient: never overexecute… Glitch free: never allow user code to see intermediate state."

**Two-phase count** ([MobX15])
- How it works: the change sends "stale" notifications downstream, then "ready" notifications. A derivation recomputes after it has received one ready for every stale.
- What it guarantees: synchronous, glitch-free updates, each derivation run at most once.

**Build-system model** ([BSALC])
- How it works: a store (keys → values), tasks, a **scheduler** (topological / restarting / suspending) and a **rebuilder** (dirty bit / verifying traces / constructive traces / deep constructive traces).
- What it guarantees: **correctness** (Def. 3.1) and **minimality** (Def. 2.1), with or without early cutoff (see §4).

**Self-adjusting / incremental computation** (Acar et al., POPL 2002 onward; [Adapton]; Incremental)
- How it works: a run records a dynamic dependence graph; change propagation re-executes only the affected parts.
- What it guarantees: "from-scratch consistency", i.e. the result equals a from-scratch run [miniAdapton §2.1].

**FRP proper** ([Fran97]; Elliott 2015 talk)
- How it works: *behaviors*, which are functions of continuous time, plus discrete *events*, with a denotational semantics.
- What it guarantees: in Elliott's words, the essence is "a precise and simple denotation" and "continuous time" ([talk abstract](https://github.com/conal/talk-2015-essence-and-origins-of-frp)).

**Event streams / Rx** ([ReactiveX intro](https://reactivex.io/intro.html))
- How it works: an Observable pushes discrete events. It is the "push 'dual' to the synchronous/pull Iterable."
- What it guarantees: every event is delivered in order. There is no general glitch-freedom (`combineLatest` in a diamond emits intermediate values; Staltz, "Rx glitches aren't actually a problem", 2015).

**Synchronous dataflow languages** (Esterel, Lustre, Signal; Benveniste et al., *Proc. IEEE* 2003)
- How it works: the synchrony hypothesis, i.e. time advances in logical ticks and a static schedule is compiled.
- What it guarantees: deterministic, glitch-free ticks. The [Survey] says reactive programming "is based on the synchronous dataflow programming paradigm… but with relaxed real-time constraints."

### Terminology that differs between fields and tools

**The input / source**
- Excel: a constant cell. Make and [BSALC]: an input file / input key.
- Incremental and Odersky: `Var`. Solid: signal. TC39: `Signal.State`.
- MobX and Knockout: "observable". Vue: `ref`/`reactive`. Salsa: input.

**The derived value**
- Excel: formula. Vue, MobX, Knockout, Angular: computed. TC39: `Signal.Computed`.
- Solid: memo. MobX: "derivation". Incremental: `map`/`bind` node (`Incr`).
- Adapton: athunk. Salsa and rustc: tracked function / query.
- Make and BSALC: target / task / rule.
- FRP, Elm (≤0.16) and Scala.React: "behavior" or "signal".

**The side-effect sink**
- Solid, Vue, Angular: effect. MobX: reaction / autorun.
- TC39: `Watcher`. Incremental and Scala.React: observer.
- Rx: subscription. Make: the recipe command.

**"Might be out of date"**
- Excel, Adapton, Incremental v1: *dirty*. MobX: *stale*. Reactively: *check* ("maybe dirty"). [TC39]: "potentially dirty".
- rustc uses red/green with **green = verified unchanged** and red = changed. Reactively uses **red = dirty** and **green = check**. Same colours, different meanings.

**The ordering key**
- *Height* (FrTime, Incremental), *level* (Scala.React), *calc chain* (Excel), *topological order* (BSALC).

**Skipping unchanged values**
- *Early cutoff* (BSALC, Shake); *cutoff* (Incremental); *backdating* (Salsa); *equality check* (Milo22).
- *Propagation capping* (DOP); custom `equals` (TC39, Angular); *bail out* (React).

**"Glitch"**
- [Survey] and [FrTime]: a momentary inconsistent state, when "fresh values [are] combined with stale values". The term comes via Courtney's Frappé (2001), which FrTime cites. *Uncertain:* it probably originates in digital-logic hazards.
- [TC39] defines "glitch-free" as "no unnecessary calculations are ever performed". That conflates consistency with minimality.
- In Rx, it means extra intermediate emissions.

**"Signal"**
- In FRP, Elm and Odersky: a time-varying value.
- In JS frameworks: a mutable observable cell. [TC39] notes these are "lossy".

**"Observable"**
- In Rx: an event stream. In MobX and Knockout: a state cell.

**"Reactive"**
- The Reactive Manifesto (2013/2014) means *systems* that are responsive, resilient, elastic and message-driven. That is a different topic (Bonér & Klang, "Reactive Programming versus Reactive Systems", O'Reilly/Lightbend 2016).

**"FRP"**
- For Elliott it requires continuous time plus a denotation. He says many systems now called FRP "lack both of FRP's fundamental properties" (2015 talk abstract).
- ReactiveX says being called FRP "is a misnomer".

**Push / pull in build systems**
- Make is goal-directed: it pulls from the target and compares timestamps.
- Tup's "beta" build systems start from a file-change list, i.e. push (Shal, "Build System Rules and Algorithms", 2009).

**SAC versus FRP**
- "FRP is mostly concerned with time-like computations, and SAC is mostly about optimizing DAG-structured computations… closely related, especially at the implementation level" [Minsky15].

## 4. Key results and guarantees, with their assumptions

**R1. Topological-order propagation gives glitch-freedom and at most one recomputation per node per update.**
- Sources: [FrTime] §3.2: heights plus a priority queue "guarantees the absence of glitches and redundant computation". [DOP] §6.2: levels, where sources are 0 and each dependent is 1 + the maximum of its dependencies. [BSALC] §4: "The only way to achieve the 'at most once' requirement while producing a correct build result is to build all keys in an order that respects their dependencies."
- *Assumes:* an acyclic graph that does not change during propagation; one atomic, synchronous update round; pure derivations.
- *Stops holding when:*
  - **Dependencies change mid-round.** FrTime must re-adjust heights and notify the queue (§3.3). Scala.React aborts and reschedules a node on a level mismatch, which is "only safe because we disallow side-effects in signal expressions". It runs observers at level ∞ (§6.2.1).
  - **There are cycles.** They must pass through a `delay` [FrTime §3.5].
  - **The graph is distributed.** "glitch avoidance cannot be ensured in distributed reactive programs using the current techniques" [Survey, abstract]. Later work (Distributed REScala, OOPSLA 2014; Margara & Salvaneschi, *IEEE TSE* 2018, "the cost of consistency") pays coordination costs for it.
  - **An effect writes back into a source.** That starts a new round.

**R2. Naive traversal is not enough.**
- Depth-first push re-fires shared descendants, and stacked diamonds make that exponential: "one update becomes two, becomes four, becomes eight" [Minsky16].
- "The obvious candidates of depth-first and breadth-first search are susceptible to glitches" [FrTime §3.2].

**R3. Early cutoff: if a recomputed value equals its old value, dependents are skipped.**
- Sources: [Survey] §3.3; [BSALC] §2.3 (e.g. adding a comment to main.c leaves main.o unchanged); Incremental "cutoff" (example: the max of two numbers when the smaller one changes, [Minsky16]); Salsa "backdating"; the rustc red-green algorithm.
- *Assumes:* a meaningful equality (a content hash, or `Object.is` on values that are never mutated in place) and deterministic tasks.
- *Limits:*
  - Dirty-bit designs make cutoff hard: "difficult" for Excel and "impossible" for Make [BSALC §4.2.1]. Neither Make nor Excel supports early cutoff (Table 1).
  - Two-pass mark-then-fire cannot cut off. The first pass "can't look at the values" [Minsky16].
  - Deep constructive traces cannot cut off either [BSALC §4.2.4].
  - Before Vue 3.4, a `watchEffect` re-ran "even if the computed result remains the same" ([Vue 3.4 blog](https://blog.vuejs.org/posts/vue-3-4)).

**R4. BSALC correctness and minimality.**
- *Correct:* inputs are untouched, and every reachable non-input key equals its task recomputed on the final store (Def. 3.1).
- *Minimal:* each task runs "at most once per build and only if [it] transitively depend[s] on inputs that changed" (Def. 2.1).
- *Assumes:* acyclic tasks (§3.6), all dependencies known (declared or tracked), deterministic tasks.
- *Where real systems fall short:*
  - Make is minimal "only under the assumption that you do not" `touch` files. It needs timestamps to go forward in time, which "can be violated by backup software" (fn. 5, §4.2.1).
  - Excel is *not* minimal. It over-approximates for `INDIRECT` and follows both branches of `IF` (§2.2, §4.2.1).
  - Bazel is not minimal because it restarts tasks (§2.4).
  - Deep constructive traces need deterministic tasks (§4.2.4).

**R5. From-scratch consistency** [Adapton; miniAdapton §2.1]: forcing a thunk after changes "is the same as if one had computed them from scratch".
- *Assumes:* mutation happens only through tracked references, and computations are pure.
- Efficiency is workload-dependent. Self-adjusting computation promises asymptotic speedups only when a change touches a small, "stable" part of the recorded trace. *Uncertain on exact terminology; see Acar's thesis, CMU 2005.*
- The classical optimality yardstick is Reps's POPL 1982 attribute-grammar result: time proportional to |AFFECTED|.

**R6. Laziness (pull / push-pull).**
- Only demanded nodes are computed, and reads are glitch-free [TC39 FAQ].
- Signals are **lossy by design**: "if you write to a state Signal twice in a row… the first write is 'lost'", unlike streams [TC39 FAQ].
- *Limits:*
  - Effects still need a scheduler.
  - Synchronous notification "may expose 'glitches' if improperly used" [TC39, Soundness].
  - When formulas are cheap, "most of your costs come from wasted graph walking" [lord20].

**R7. Dynamic tracking records exactly what the last run read.**
- Knockout "redetects them every time"; [TC39]: "that precise dependency set is kept fresh".
- *Assumes:* all reads happen synchronously inside the tracking scope.
- *Limits:* reads after `await`, in callbacks, or through `untrack` are invisible. [TC39] marks `untrack` as a "soundness risk".

**R8. Glitch-freedom is per propagation round, not global.**
- Rx `combineLatest` has no such guarantee (Staltz 2015).
- React 18 describes "tearing", where "a UI has shown multiple values for the same state", when concurrent rendering reads an external store mid-change (React 18 Working Group, [discussion #69](https://github.com/reactwg/react-18/discussions/69), 2021).

## 5. Standard concrete examples, as they appear in the sources

```text
# Survey §2 and §3.3 (imperative vs reactive; the glitch)
var1 = 1; var2 = 2; var3 = var1 + var2        # var3 tracks var1+var2
var1 = 1; var2 = var1 * 1; var3 = var1 + var2 # var1:=2 may show var3=3, then 4
```

```scheme
; FrTime §3.2: should always be #t; it is a glitch if the outer node updates first
(< seconds (+ 1 seconds))
```

```text
# BSALC §2.2 / §3.2: the spreadsheet, then a dynamic dependency
A1: 10   B1: A1 + A2       B2: B1 * 2
A2: 20
B1: INDIRECT("A" & C1)   C1: 1     # deps depend on C1's *value*
```

```make
# BSALC §2.1: editing util.h triggers a full rebuild; editing main.c a partial one
util.o: util.h util.c
	gcc -c util.c
main.o: util.h main.c
	gcc -c main.c
main.exe: util.o main.o
	gcc util.o main.o -o main.exe
```

```js
// TC39 Signals README (vanilla pub/sub version first, then this)
const counter = new Signal.State(0);
const isEven = new Signal.Computed(() => (counter.get() & 1) == 0);
const parity = new Signal.Computed(() => isEven.get() ? "even" : "odd");
effect(() => element.innerText = parity.get());
setInterval(() => counter.set(counter.get() + 1), 1000);
// the vanilla version "do[es] unnecessary computation" when counter goes 2 -> 4
```

```js
// Milo22: the "equality check problem"; C should run only once
const A = reactive(3);
const B = reactive(() => A.value * 0); // always 0
const C = reactive(() => B.value + 1);
```

```js
// Angular signals guide: a dynamic dependency
const showCount = signal(false);
const count = signal(0);
const conditionalCount = computed(() =>
  showCount() ? `The count is ${count()}.` : 'Nothing to see here!');
// while showCount is false, changing count does not recompute
```

```scala
// DOP §6.2.1: the level is 2 or 3 depending on x
val x = Var(2); val y = Cache { f(x()) }; val z = Cache { g(y()) }
val result = Signal { if (x() == 2) y() else z() }
```

```ocaml
(* Minsky15: Jane Street Incremental *)
let base_area = Inc.map2 width depth ~f:( *. )
let volume    = Inc.map2 base_area height ~f:( *. )
let volume_obs = Inc.observe volume   (* then Var.set ...; Inc.stabilize () *)
```

More examples, in words:

- **Excel** [Excel]: "if B1 depends on A1, and C1 depends on B1, when A1 is changed, both B1 and C1 are marked as dirty", then both are recalculated in calc-chain order. The volatile functions (`NOW`, `TODAY`, `RANDBETWEEN`, `OFFSET`, `INDIRECT`, and sometimes `INFO`, `CELL`, `SUMIF`) are recalculated on every recalculation, together with all their dependents. Circular references trigger a warning; iterative calculation is optional (default 100 iterations per [BSALC] §6.6).
- **UI "fullName"**: Knockout's `ko.computed(() => firstName() + " " + lastName())`; [MobX15]'s Person/profileView. React's docs show the anti-pattern of deriving `fullName` in an Effect. The fix is to compute it during render, which "avoids an entire render pass with stale values" ([react.dev](https://react.dev/learn/you-might-not-need-an-effect)).
- **[Odersky]**: `BankAccount` with `balance = Var(0)`, and `consolidated = Signal(accts.map(_.balance()).sum)`. The course points out that `s() = s() + 1` "makes no sense" for signals.
- **Rx BMI** (Staltz 2015): `combineLatest(height, weight)` emits 23 and then 25 when both inputs change "at the same time".
- **7GUIs "Cells"** (Kiss 2014): "one should not just recompute the value of every cell but only of those cells that depend on another cell's changed value."

## 6. Misconceptions practitioners bring, and the canonical correction

1. **"Just notify the subscribers."**
   - Correction: the diamond shows that ordering is part of correctness, not an optimization. You get a glitch plus duplicate work, and it compounds exponentially [Survey §3.3; FrTime; Minsky16].
2. **"Visit the graph breadth-first and it will be fine."**
   - Correction: it will not, because path lengths differ [Minsky16; FrTime §3.2]. You need heights / a topological order, or mark-then-count.
3. **"Everything downstream of a change gets recomputed."**
   - Correction: only nodes that are both *affected* and *needed*. An unchanged value stops propagation (early cutoff).
   - Unobserved nodes need not run: Incremental uses observers [Minsky15]; Adapton's demanded computation graph; lazy computeds [TC39; MobX docs "Computed values are updated lazily"].
4. **"Reactive = RxJS / streams."**
   - Correction: the literature separates *behaviors/cells* (current value; lossy; [TC39 FAQ]) from *events/streams* (every occurrence matters) [Survey §2.1; Blackheath & Jones use Cell and Stream].
   - "FRP" in Elliott's sense is a third, narrower thing (see §3).
5. **"React is fine-grained reactive."**
   - Correction: React re-runs component functions recursively and diffs the result. "React only changes the DOM nodes if there's a difference between renders" ([react.dev, Render and Commit](https://react.dev/learn/render-and-commit)).
   - `useMemo` dependencies are *declared* and the cache is only a hint: "You should only rely on `useMemo` as a performance optimization" ([react.dev](https://react.dev/reference/react/useMemo)).
   - Signal frameworks *track* dependencies instead. Svelte 5 moved to signals, "essentially what Knockout was doing in 2010" (Svelte "Introducing runes", 2023).
6. **"Declared dependencies are the same as real dependencies."**
   - Correction: a missing declaration means silently stale output. This is why GNU Make has "Generating Prerequisites Automatically" (`cc -M`, the `defs.h` example).
   - Recursive make gives each sub-make an incomplete DAG (Miller, "Recursive Make Considered Harmful", AUUGN 1998).
   - Bazel sandboxes actions for hermeticity ([bazel.build](https://bazel.build/basics/hermeticity)).
   - Auto-tracking fixes this, but only for reads it can see (R7).
7. **"Put derived state in an effect or watcher."**
   - Correction: canonical guidance says derive, don't synchronize.
   - MobX: "Always use computed if you want to create a value based on the current state"; computeds "should be pure".
   - React: "If you can calculate something during render, you don't need an Effect", and it warns against "chains of Effects".
8. **"Spreadsheets recompute cells left-to-right, top-to-bottom."**
   - Correction: that was VisiCalc (1979), with row- or column-order passes. "Natural order" recalculation (dependencies first) dates from LANPAR (1969; US patent 4,398,249) and returned with Lotus 1-2-3 [lord20; Wikipedia "Spreadsheet"].
   - Modern Excel builds a dependency tree and a calc chain that reorders itself during recalculation [Excel].
9. **"Cycles are just infinite loops."**
   - Correction: systems detect and reject cycles (Excel warns; BSALC assumes acyclic). Some allow them only in controlled forms: bounded iteration (Excel), `delay` (FrTime), fixed points (Pluto/LaTeX, [BSALC] §6.6).

## 7. For a short lesson: essential, common extra, leave out

**Essential**

- The spreadsheet framing, and the graph of sources → derived values → effects.
- The two questions every such system answers. BSALC calls them the rebuilder and the scheduler:
  - (1) *What* is out of date: dirty marking or a comparison of recorded dependencies.
  - (2) In *what order* to recompute: topological order.
- The diamond: naive push gives a glitch and double work; ordering fixes it.
- Early cutoff: an unchanged value stops propagation.
- Push vs pull vs push-pull, in one picture: mark eagerly, compute lazily, only what is observed.
- Dynamic dependencies (`IF`/`INDIRECT`, conditional reads) and why tracking happens at run time.
- What goes wrong:
  - glitches;
  - redundant or exponential recomputation;
  - stale results from missing or untracked dependencies;
  - cycles;
  - side effects inside derivations;
  - leaked subscriptions.

**Common extras**

- Build systems' memory across runs: timestamps vs hashes/traces, and cloud caches [BSALC Table 2].
- Excel's restarting calc chain and volatile functions.
- Batching/transactions and effect scheduling.
- The terminology map (§3).
- Signals vs Rx streams.
- Contrast with React's re-render-and-diff model.

**Leave out**

- Continuous-time FRP semantics, arrowized FRP / Yampa, space-time leaks, higher-order FRP.
- Distributed glitch-freedom protocols.
- Self-adjusting-computation cost theory.
- Library internals: pseudo-heights, version numbers vs colouring, linked lists.
- Multidirectional constraints (one sentence at most).
- Synchronous languages.
- Incremental view maintenance / differential dataflow. You could give a one-line nod to database materialized views, which this audience knows.

## 8. Systems canonically cited, and their mechanisms

**Spreadsheets**

- **Excel** [Excel; BSALC §2.2, §5.2]
  - Model: push (dirty bits) + ordered recalculation + a restarting scheduler.
  - Mechanism: a dependency tree plus a calc chain. A cell that needs an uncalculated cell is moved down the chain (the chain is reused next time).
  - Also: volatile functions; circular-reference detection; optional iteration; multithreaded recalculation since Excel 2007.
  - No early cutoff; not minimal. Self-tracking (a formula edit is itself a change).
- **VisiCalc / LANPAR / Lotus 1-2-3** [lord20; Wikipedia]
  - VisiCalc used order-based sweeps. LANPAR and Lotus used natural order (dependency order).

**Build systems**

- **Make** (Feldman 1979; [BSALC])
  - Topological scheduler with a dirty bit based on file mtimes.
  - Dependencies are static and declared. No cutoff.
- **Ninja** [BSALC §7.1]
  - Topological scheduler with verifying traces (recorded hashes of inputs and commands).
- **Shake** (Mitchell, ICFP 2012)
  - Suspending scheduler with verifying traces.
  - Dynamic dependencies (`need`), minimal, with early cutoff.
- **Bazel** [BSALC §2.4]
  - Restarting scheduler with constructive traces: a content-addressable cache plus a command history, shared remotely.
  - Early cutoff; not minimal; hermetic sandboxing.
- **Buck / Nix / CloudBuild / Redo / Tup** [BSALC Table 2, §7.1; Shal 2009]
  - Buck: topological + deep constructive traces. Nix: suspending + deep constructive traces. CloudBuild: topological + constructive traces.
  - Redo is roughly like Shake. Tup is a Make-like refined dirty bit driven by a file-change list.

**Compilers**

- **rustc incremental** [rustc]
  - The query DAG is recorded during execution, including the order in which inputs were read.
  - Red-green "try-mark-green": if all inputs are green, the node is green without re-running.
  - Early cutoff by comparing result fingerprints.
- **Salsa** (used by rust-analyzer) [Salsa; its README says it was "heavily inspired by adapton, glimmer, and rustc's query system"]
  - A global revision counter; each value has `changed_at` and verified revisions.
  - Backdating (early cutoff); "durability" levels to skip verification.

**Incremental-computation libraries**

- **Jane Street Incremental** [Minsky15; Minsky16]
  - `Var` / `map` / `map2` / `bind` / `observe` / `stabilize`.
  - Height-ordered recompute. The later versions use pseudo-heights that "never go down", with an array of lists instead of a heap.
  - Cutoffs. Only "necessary" (observed) nodes are kept.
- **Adapton** [Adapton; miniAdapton]
  - A demanded computation graph: dirtying is pushed eagerly upward, and re-evaluation happens only when a thunk is forced.
  - Memoization lets it switch back to earlier sub-computations.

**Research reactive languages**

- **FrTime** (Racket) [FrTime]
  - Push, with a height-ordered priority queue.
  - Heights are re-adjusted on dynamic reconfiguration; cycles only through `delay`.
- **Scala.React** [DOP]
  - Push, with levels and a priority queue.
  - On a level mismatch it aborts and reschedules; observers get level ∞.
- **Flapjax** (Meyerovich et al., OOPSLA 2009)
  - Push, with topological order [Survey].
- **Fran → push-pull FRP** [Fran97; Elliott09]
  - Pull/sampling of continuous behaviors, later a push-pull hybrid.
- **Elm (≤0.16)** (Czaplicki & Chong, PLDI 2013)
  - Signals forming a static graph. They were removed in 0.17 in favour of The Elm Architecture plus subscriptions ("A Farewell to FRP", May 2016).

**Event streams**

- **Rx / ReactiveX** (Meijer, "Your Mouse is a Database", ACM Queue 2012)
  - Push-based Observable streams with operators. No glitch-freedom guarantee.

**UI frameworks and libraries**

- **Knockout** (2010)
  - Observables plus `ko.computed`. Dependencies are re-detected on each evaluation.
- **MobX** [MobX15; mobx.js.org]
  - Two-phase stale/ready counting; synchronous and glitch-free.
  - Computeds are lazy when unobserved. Actions/transactions batch updates.
- **Preact Signals** (2022)
  - Lazy computeds and eager effects.
  - Version numbers on nodes and edges; doubly-linked-list dependency lists ([blog](https://preactjs.com/blog/signal-boosting/)).
- **Reactively / Solid** [Milo22; Carniato21]
  - Reactively: three colours (clean / check / dirty); a push colouring phase, then a pull `updateIfNecessary`.
  - Solid: a tracking-context stack; the algorithm is related (per Milo22).
- **Vue** ([Reactivity in Depth](https://vuejs.org/guide/extras/reactivity-in-depth.html))
  - Proxy / getter interception gives `track`/`trigger`. Computeds are cached and lazy.
  - Since 3.4, a computed triggers its effects only when its value actually changed.
- **Angular signals** (introduced v16, 2023 — *version detail uncertain*)
  - `signal` / `computed` / `effect`. Computeds are "lazily evaluated and memoized".
  - Custom `equal`; dynamic dependencies.
- **Svelte**
  - Svelte 3/4: dependencies of `$:` are fixed at compile time.
  - Svelte 5 (2023): runes built on signals.
- **React**
  - Re-renders and reconciles, with dependency arrays declared by hand.
  - React Compiler does automatic memoization. `useSyncExternalStore` addresses tearing.

**Standards and runtime proposals**

- **TC39 Signals** [TC39]
  - Stage 1. `State`, `Computed`, `Watcher`; push-then-pull; auto-tracking; lazy and memoized; no built-in `effect`.

**Distributed reactive programming**

- Distributed REScala (OOPSLA 2014); DREAM (Margara & Salvaneschi, TSE 2018).
- Both give glitch-freedom across nodes at a coordination cost, with selectable consistency levels (DREAM).

## 9. Claims that are commonly overstated or subtly wrong

- **"Signals / reactive systems are glitch-free."**
  - Only some are, and only within a synchronous round. Rx is not.
  - Carniato's teaching implementation is explicitly not.
  - Distributed settings are not, without extra protocol [Survey].
  - TC39 warns that synchronous watchers can expose glitches.
- **"Glitches can only happen with push."**
  - [Survey] §3.3 says this. It is true for one synchronous snapshot. But pull-based UIs can still *tear* across time (React 18 WG), and async derivations can mix old and new state.
- **"Glitch-free means no unnecessary computation."**
  - [TC39]'s wording merges two separate properties: consistency (no mixed fresh/stale reads) and minimality or efficiency ([BSALC] Def. 2.1; [Milo22] lists them as separate goals).
- **"Topological sort solves it."**
  - Only for a graph that does not change during the update.
  - Dynamic dependencies need re-levelling, aborts or pseudo-heights [FrTime §3.3; DOP §6.2.1; Minsky16].
  - Cycles need special handling.
- **"Make rebuilds exactly what changed."**
  - It rebuilds what is *older than its declared prerequisites*. So it is fooled by `touch`, clock skew and restored backups, misses undeclared headers, and has no early cutoff [BSALC].
- **"Excel only recalculates what changed."**
  - It also recalculates every volatile function and its dependents on every recalculation.
  - It over-approximates `INDIRECT`/`IF` and has no early cutoff [Excel; BSALC].
- **"Lazy means nothing runs until you read it."**
  - Effects/reactions are eager by definition.
  - MobX keeps *observed* computeds up to date eagerly; laziness applies only to unobserved ones (MobX docs).
- **"Incremental is always faster than recomputing."**
  - Bookkeeping can dominate when formulas are cheap [lord20].
  - Jane Street's last rewrite gave "three times faster" applications because nearly all the time had been framework overhead [Minsky16].
  - Asymptotic gains assume changes are local (R5).
- **"Content hashing makes builds correct."**
  - Only with hermetic, deterministic tasks. Deep constructive traces break correctness for non-deterministic tasks [BSALC §4.2.4]; see also Bazel's hermeticity guide.
- **"Rx is FRP" and "Elm is FRP."**
  - ReactiveX calls the label "a misnomer".
  - Elm removed signals in 0.17 (2016).
- **"The virtual DOM is what makes React reactive" / "the virtual DOM is pure overhead."**
  - Both are slogans. The first confuses re-render-and-diff with dependency tracking. The second is Svelte's argument, not a settled result. *Treat as contested.*
- **"`useMemo` / computed are the same thing."**
  - React may discard `useMemo` caches.
  - A computed signal is a graph node with a correctness contract (cached until a dependency changes).

## 10. Watch, do or read: which medium fits which part

The evidence base here is general, not topic-specific:

- Tversky, Morrison & Bétrancourt, "Animation: can it facilitate?", *IJHCS* 2002: animation helps only when the content is itself change over time (the *congruence* principle) and is slow and segmented enough to perceive (the *apprehension* principle).
- Hundhausen, Douglas & Stasko, "A Meta-Study of Algorithm Visualization Effectiveness", *JVLC* 2002: *how* learners engage matters more than *what* the visualization shows.

The mapping below is my recommendation, not a canonical claim.

**Best watched: a narrated animation of change moving over a fixed graph**

- A dirty-marking wave going downstream, then recomputation in height order.
- The diamond glitch: var3 shows 3, then 4. Stacked diamonds doubling their work.
- Push arrows going down versus pull requests going up (push-pull: colour first, then compute on read).
- An early-cutoff node turning "unchanged" and stopping the wave.

These are temporal sequences on a spatial structure: exactly where the congruence principle favours animation, and where static diagrams need many frames.

**Best done: interactive simulation, running code, exercises**

- A sandbox spreadsheet or graph where the learner:
  - edits a cell;
  - picks a strategy (naive DFS / BFS / height order / push-pull);
  - toggles cutoff and an `IF` branch;
  - sees counters for recomputations and glitches.
- A "predict the order" quiz before each step.
- Building a ~50-line signal library ([Carniato21]; [Odersky] "A Simple FRP Implementation"), then breaking it with a diamond.
- The 7GUIs "Cells" task.
- A Make exercise: forget a header prerequisite, observe a stale build, then `touch` to fool it.

Prediction and manipulation are where misconceptions 1, 2, 3 and 6 actually surface, and Hundhausen et al. find that active engagement is what drives learning.

**Best read**

- The terminology map (§3).
- The guarantee-plus-assumption list (§4).
- The systems/mechanism table (§8), including BSALC's scheduler × rebuilder table.
- History (VisiCalc → natural order; Knockout → signals; Elm leaving FRP).
- The caveats (§9).

This is dense, comparative reference material that learners revisit and scan. Narrating it wastes time, and animation adds nothing, because nothing changes over time.
