You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Argument

**Question.** A checkout page asks the payment server to charge a customer $50. The network goes quiet and the client times out. Did the charge happen? Retrying may charge twice; not retrying may lose the sale. What should the client do?

**Answer.** The client can't find out: a lost request, a slow or crashed server, and a lost reply all look the same (silence), and asking again crosses the same unreliable network. So no protocol can guarantee a request is carried out exactly once. The client retries (at least once), and the server makes repeats harmless: the client sends the same idempotency key with every attempt at one payment, and the server charges once per key and returns the saved result to repeats. At-least-once delivery plus idempotent handling gives exactly one charge.

**Takeaway.** You can't make a network deliver a request exactly once, but you can make its effect happen exactly once: retry, and make the operation idempotent with a key the server checks.

**Wrong model.** A timeout means the request failed, so it is safe to retry (or: exactly-once delivery is something the network or a library can give you).

**Objectives.**
1. Explain why a client cannot know, after a timeout, whether its request took effect.
2. Say what at-most-once and at-least-once delivery each risk, and which a payment needs.
3. Define idempotent and tell which operations are naturally idempotent.
4. Explain how an idempotency key makes a charge safe to retry, and the two server-side details it depends on.


## Chain

1. The question: timeout on a $50 charge; retry or not?
2. But three different failures look the same to the client, and asking again can fail the same way. Therefore no protocol guarantees exactly once.
3. Therefore choose: at most once (may lose) or at least once (may duplicate). A payment can't be lost, so retry. Therefore the server must make repeats harmless.
4. Therefore idempotence: some operations are naturally safe to repeat; a charge isn't.
5. Therefore the idempotency key: same key on every attempt; charge once per key; return the saved result to repeats.
6. But it only works if the key and the result are saved together, and a repeat arriving mid-charge is held back.
7. Therefore the answer: retry with the same key; at-least-once delivery plus idempotent handling charges exactly once.


## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> A checkout page asks the payment server to charge a customer fifty dollars.
> Then the network goes quiet. After a few seconds with no reply, the client gives up: a timeout.
> Did the charge go through?
> If it did and the client tries again, the customer pays twice. If it didn't and the client gives up, the sale is lost.
> So what should the client do?

*Screen:* a client (checkout page) and a payment server, a request arrow "charge $50" leaving the client; a clock on the client counting up; "timeout". A question mark over the customer's card: "charged? 0 times? 1? 2?". Title: "Charged Twice".

### 2. Silence looks the same

> From the client's side, three different failures look exactly alike.
> The request might have been lost on the way, so nothing happened.
> The server might still be working on it, or have crashed partway through.
> Or the charge went through, and the reply was lost on the way back.
> In every case, the client sees the same thing: nothing.
> It could ask the server whether the charge happened. But the question and its answer cross the same network, and can be lost the same way.
> However many messages the client sends, it can never be certain. So no protocol over an unreliable network can promise that a request is carried out exactly once.

*Screen:* three sequence diagrams side by side (client left, server right, time down): (a) request arrow stops halfway with a cross; (b) request arrives, server box stalls or shows a crash mid-charge; (c) request arrives, "charged $50" on the server, reply arrow stops halfway with a cross. Under all three, the client's view: the same empty timeline and "timeout". Then a "did it work?" message also crossing out.

### 3. At most once, or at least once

> That leaves two choices.
> Send the request once and never retry. Nothing is ever done twice, but a lost request is simply lost. That's called at most once.
> Or retry until a reply arrives. Nothing is lost, but when only the reply was lost, the request is carried out twice. That's at least once.
> A payment can't just be lost, so the client retries.
> That means the server has to make a repeated request harmless.

*Screen:* two lanes: "at most once: never retry" with outcomes "charged 0 or 1 times", and "at least once: retry until a reply" with outcomes "charged 1 or 2 times"; the second lane highlighted.

### 4. Safe to repeat

> An operation is idempotent if doing it twice has the same effect as doing it once.
> "Set the shipping address to this" is idempotent. Do it again, and the address is still the same.
> "Delete order seven" is idempotent too. The second time, there's nothing left to delete.
> "Charge fifty dollars" is not. Every copy charges the card again.
> So the charge has to be made safe to repeat.

*Screen:* three operations, each applied twice with the resulting state shown: address unchanged; order 7 gone (second delete: "not found", state the same); card charged $50, then $100 in coral. A small note: "in HTTP, PUT and DELETE are meant to be idempotent; POST is not".

### 5. Idempotency keys

> The standard way is an idempotency key.
> Before its first attempt, the client makes up a key for this payment: a long random string that no other payment will share. It sends that same key with every attempt.
> The first time the server sees the key, it charges the card, and saves the result under that key.
> When a retry arrives with the same key, the server doesn't charge again. It looks up the saved result and sends that back.
> So in the lost-reply case, the retry gets the reply that was lost, and the customer pays once.
> Payment APIs such as Stripe's work this way. The client puts the key in a request header called Idempotency-Key.

*Screen:* the client makes "key: 7f3a…c91" once; the request carries it. The server has a table "key → result". First request: table empty for the key → "charge $50" → row "7f3a…c91 → charged, receipt #1042". Reply lost (case c). Retry with the same key → row found → "receipt #1042" returned; the card shows $50 once. A header line: "Idempotency-Key: 7f3a…c91".

### 6. Where it can still go wrong

> Two details decide whether this works.
> First, the charge and the saved result must succeed or fail together. If the server charges the card and crashes before saving the result under the key, the retry finds no record, and charges again.
> Second, a retry can arrive while the first attempt is still running. The server has to see that the key is already in progress, and hold the retry back, rather than start a second charge.

*Screen:* (1) a timeline: "charge card" → crash before "save key → result"; retry finds nothing → second charge (coral). The fix drawn as one box around "charge + save" labelled "together". (2) two requests with the same key arriving 5 ms apart; the first marks the key "in progress"; the second is told to wait (or rejected with "in progress, try again").

### 7. The answer

> So after a timeout, the client should retry, with the same idempotency key.
> The network can't deliver a request exactly once. But delivering it at least once, to a server that makes repeats harmless, charges the customer exactly once.

*Screen:* the chapter 1 scene replayed: timeout → retry with the same key → one charge, receipt returned. "at least once delivery + idempotent handling = charged exactly once". End card: references: Kleppmann, Designing Data-Intensive Applications (2017), ch. 8 and 11; Stripe API reference, Idempotent requests; RFC 9110 §9.2.2 (idempotent methods); Helland, "Idempotence Is Not a Medical Condition", ACM Queue (2012).

