# Watching as the student reviewer

## 1. Points where I lost the thread or need more

- **"This is the observer pattern"** (§3) — dropped in as a name with only "each value tells its readers" as the gloss. I can follow the mechanism, but I don't know if this is a term I'm expected to already recognize from OOP design patterns, or a term the video is defining for me. Feels assumed rather than taught.

- **"Which does it tell first? Whichever subscribed first; nothing in the pattern decides."** — this is asserted without grounding. Why would subscription order be the tiebreaker? I don't have a mental model of "subscribing" yet at this point, so this reads as an arbitrary rule rather than a consequence of something I understand.

- **"A value like that, built from a mix of new and old inputs, is called a glitch."** — fine as a definition, but it lands right after the observer-pattern explanation and right before "diamond" two sentences later. Three new vocabulary words (observer pattern, glitch, diamond) inside about 30 seconds of narration.

- **"Two diamonds in a row make the last value run four times. Three make it eight."** (§4) — I saw *one* diamond cause the total to run twice. I don't see why *stacking* diamonds multiplies rather than adds. The jump from "1 diamond → 2 runs" to "2 diamonds → 4 runs" is stated as fact, not derived — I'd need a beat showing the second diamond's inputs each doubling to buy the doubling claim.

- **"the last value runs one thousand and twenty-four times... over a million"** — numbers with no unit I can hold onto beyond "big." I believe it's 2^10 and 2^20, but the script never says that explicitly, so I'm trusting arithmetic I can't verify from what's shown.

- **§6 early cutoff and laziness arrive back to back** — two distinct optimizations, each demonstrated once, in the same short section. I processed early cutoff fine but laziness felt like a second concept bolted on before the first one settled.

- **§7 is the densest stretch** — dynamic tracking (spreadsheets/UI frameworks), static declaration (Makefiles), a staleness bug demo, *and* circular references, all in one section. By the time "Excel calls this a circular reference" arrives, I'm still digesting the Makefile bug and don't have spare attention for a fourth new idea.

- **"By default it warns instead of computing, though it can be told to iterate toward an answer."** — "iterate toward an answer" is unexplained; I don't know what iterating on a circular formula means numerically (is it like a fixed-point loop? how does it stop?).

## 2. Questions I'd ask afterward

- Why does one diamond's *doubling* turn into *multiplying* across a chain instead of adding? Can I see the second diamond's effect drawn out like the first was?
- Is "height" always well-defined, or can normal (non-circular) graphs still have ties or ambiguity in height assignment?
- When a framework "records what each formula reads, every time it runs" — does that mean it re-derives the whole graph on every single recompute? Isn't that expensive?
- For circular references, what does "iterate toward an answer" actually compute — some kind of average that converges, or something else?
- Is the observer pattern's ordering problem (glitches) a real bug people hit in production code, or purely a spreadsheet/UI-framework concern?

## 3. What I learned (written without looking back, ~150 words)

Spreadsheets, build tools, and reactive UI frameworks all solve the same problem: when one value changes, which other values need recomputing, and in what order? They build a dependency graph — arrows from each value to the formulas that read it. Naively, letting each changed value directly notify its readers (the "observer pattern") can produce a wrong intermediate value, called a glitch, because a value with two paths to it (a "diamond") gets recomputed before all its inputs are current. Diamonds chained together make this exponentially worse. The fix: first mark everything reachable from the change as stale, then recompute in order of "height" (distance from the inputs), so nothing is computed before its own inputs are ready — each value computes exactly once. Extra tricks (stopping early when a value doesn't change, deferring unwatched values) cut work further. Build tools like Make need the graph declared explicitly, or it goes stale.

## 4. Direct answers

- **One main idea:** correct, efficient recomputation requires knowing the dependency graph and processing it in dependency order (lowest "height" first), not just letting each change eagerly notify the next thing downstream.
- **Numbers I remember:** the cart total going to a wrong intermediate value of $64 (should have been $66); a chain of ten diamonds causing 1,024 recomputations naively vs. one in order; five recomputations total for the ordered version of the full example.
- **Opening question:** how does a system decide what to recompute and in what order when something changes, and what goes wrong if it gets that wrong? **Answer:** mark everything downstream of the change as stale, then recompute in height order (each value's inputs are ready before it runs), computing each value exactly once and stopping wherever a value turns out unchanged.

## 5. Ratings

- **Want-the-answer pull of the opening:** 4/5 — the stale $44 total and the spreadsheet-just-works contrast is a genuinely relatable, well-chosen hook.
- **How often I felt lost:** a few times — mainly around the diamond-doubling leap in §4, the vocabulary cluster in §3, and the density of §7.
