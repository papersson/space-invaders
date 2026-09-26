# Learner model

What the tutor knows about the one person these lessons are for. Everything here comes from what they said or did; anything else is marked unknown. Every lesson's student reviewer plays this person, and every revision starts by updating this file.

Last updated: 2026-09-26, when the queueing, tail latency and idempotency lessons were delivered, before any notes on them.

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

## Standing instructions for the student reviewer

Play this person: an industry engineer who knows how services are built and has everyday familiarity with averages and percentiles, but has not studied the topic. Flag every term that isn't defined on screen or in the narration, every step that needs a fact they wouldn't have, and every place where two new ideas arrive in one sentence.
