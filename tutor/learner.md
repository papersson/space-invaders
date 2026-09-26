# Learner model

What the tutor knows about the one person these lessons are for. Everything here comes from what they said or did; anything else is marked unknown. Every lesson's student reviewer plays this person, and every revision starts by updating this file.

Last updated: 2026-09-26, when the queueing, tail latency, idempotency, reactive, concurrency, desired-state, Nix, query-planner, structured-concurrency and LLM-agents lessons were delivered, before any notes on them.

## Background

- Works in industry and wants lessons "useful in the industry day to day". Picked queueing, tail latency, and idempotency with retries from a list of practical topics.
- Keeps a personal library of prompts and references on software architecture, data systems, performance, observability and LLM agents. Likely a software, data or ML engineer. Their exact role and years of experience are unknown.
- Has watched two lessons in this series: UMAP (an earlier session) and external merge sort (version 2, 6:25).
- Assume they know: programming, how web services, APIs and databases are built and called, averages and percentiles as everyday terms, Big-O.
- Unknown: how comfortable they are with probability beyond the everyday (distributions, independence, expected value), and how much formula they want on screen.

## How they learn, in their words

- Asks for lessons because they don't know the subject, so they cannot check the content: it must be canonical, established knowledge.
- The story matters most: "coherent, pedagogic, and just extremely high quality". Setups must pay off; a detail raised and never used again ("the temp files are the whole trick") is noticed and disliked. Material that doesn't serve the question feels "shoehorned".
- No fixed length. "The important thing is that the story is good."
- Wants only the video on the page, with chapters and a captions toggle. The script, sources and process notes on the page were "too busy".
- "Not every topic is learnable effectively through these types of visual presentations": choose the format per chapter.
- Expects to learn iteratively: the tutor's picture of their understanding is imperfect, so lessons get revised from their feedback.

## Evidence of understanding

| Lesson | Evidence | What it tells the tutor |
|---|---|---|
| External merge sort v2 | "There are still things that I didn't quite follow." Which parts: not yet known. The page now has a "Lost me here" button. | Some step in a 6-minute, six-chapter lesson moved too fast or assumed too much. Until the notes arrive, keep each step visibly derived from the one before, and don't stack two new ideas in one sentence. |
| Queueing ("Why Busy Servers Get Slow", v1, 4:53) | Delivered; no notes yet. Predicted, not confirmed: the final student reviewer lost the "work fills ninety percent of the gap, so a new one arrives about every eleven milliseconds" step (10 / 0.9 done in the head) and the leap to "twice as long to clear". | Spoken division is a risk; show it on screen as it is said. |
| Tail latency ("The Tail at Scale", v1) | Delivered; no notes yet. Predicted, not confirmed: the student reviewer lost the converse, "each server slow only one time in ten thousand", and the multiply-the-probabilities step before it; the sentence with Google's measured results is dense. | Probability steps need their arithmetic on screen. If notes land here, the unknown about comfort with probability is answered. |
| Idempotency ("Charged Twice", v1) | Delivered; no notes yet. Predicted, not confirmed: the jump from "the last message is never confirmed" to "no protocol can promise exactly-once delivery", and the in-progress, check-and-mark-in-one-step detail. | Impossibility arguments and concurrency details compress badly into one sentence. |
| Reactive ("What the Spreadsheet Knows", v1, 7:35) | Delivered; no notes yet. Predicted, not confirmed: the doubling leap in the stacked diamonds (1024 for ten), the cluster of names in chapter 3 (glitch, topological order, height), and early cutoff and laziness arriving back to back. | Growth claims need each doubling shown, not just the endpoint; one new mechanism per chapter. |
| Concurrency models ("Share Memory, or Pass Messages?", v1, 10:20) | Delivered; no notes yet. Predicted, not confirmed: "only two orders of the six steps are safe" (asserted, not shown), race condition and data race named one sentence apart, "C and C++ promise nothing" (undefined behaviour is never named), and whether the study's "hangs" means deadlocks. | Counting claims need the enumeration on screen; two neighbouring terms need a contrast before the second name. |
| Desired state ("Make It So", v1, 7:36) | Delivered; no notes yet. Predicted, not confirmed: replica count and pod arriving together, which loop marks a dead machine unreachable, and edge/level-triggered landing back to back; chapter 6's moving target and fighting tools are faster and more abstract than the rest. | When two mechanisms share one story (the node loop and the pod loop), name both or show both. |
| Nix ("A Hash in Every Path", v1, 7:24) | Delivered; no notes yet. Predicted, not confirmed: the closure's list of libraries, and the compiler being both excluded and (as its runtime library) included; chapter 3 carries four ideas (recipe and derivation, pure function, isolation, the hash computed before the build). | Lists of names need a picture of how they connect; a named exception needs its own label on screen. |
| Query planner ("Same Query, Different Plan", v1, 6:58) | Delivered; no notes yet. Predicted, not confirmed: the join chapter's cluster of numbers and two join names, and the 1.4 million rows the stale plan walks past; "cost" was the most-flagged word across rounds (now shown with real numbers). | Abstract units need one real value on screen; a scan's mechanism (walk order numbers, check each row) needs saying before its cost. |
| Structured concurrency ("Where Did That Task Go?", v1, 7:46) | Delivered; no notes yet. Predicted, not confirmed: `except*` and the exception group (the student reviewer was lost there in rounds 7 and 8), the Go terms (goroutine, error group, context) arriving close together, and chapter 4's names and dates. The first lesson in this series checked frame by frame after the first render; that pass found a code card that didn't compile and a narration line that was wrong. | A syntax detail on screen needs to be run, not recalled; three new terms in one beat need a picture or a line each. |
| LLM agents ("It Said It Was Fixed", v1, 10:52) | Delivered; no notes yet. The longest lesson so far. Predicted, not confirmed: the workflow distinction (no student retelling in six review rounds carried it); the command-line tool's notes inside the token counts (the student reviewer tripped on them in rounds 4 and 5, before chapter 2 named the tool); chapter 7's density (run B, the first way agents break down, compounding errors, then a more capable model's three runs and a parser failure); the pile of token numbers across chapters 6 and 8 (1,423 to 2,745 and 18,537, then 11,597 and 123,192). The student reviewers rated the opening 4 of 5 in every round. | A second example in the same chapter (the more capable model) competes with the chapter's own point, even when it earns its place; a tool detail that changes the numbers (the CLI's notes) needs its setup the first time it is on screen. If notes land in chapters 6-8, the numbers budget was too high for this learner. |

## Standing instructions for the student reviewer

Play this person: an industry engineer who knows how services are built and has everyday familiarity with averages and percentiles, but has not studied the topic. Flag every term that isn't defined on screen or in the narration, every step that needs a fact they wouldn't have, and every place where two new ideas arrive in one sentence.
