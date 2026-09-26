# Charged twice

Status: locked after review round 4

## Argument

**Question.** A checkout page asks the payment server to charge a customer $50. The network goes quiet and the client times out. Did the charge happen? Retrying may charge twice; not retrying may lose the sale. What should the client do?

**Answer.** The client can't find out: a lost request, a slow or crashed server, and a lost reply all look the same (silence), and asking again crosses the same unreliable network. So no protocol can guarantee a request is carried out exactly once. The client retries (at least once), and the server makes repeats harmless: the client sends the same idempotency key with every attempt at one payment, and the server charges once per key and returns the saved result to repeats. At-least-once delivery plus idempotent handling gives exactly one charge.

**Takeaway.** You can't make a network deliver a request exactly once, but you can make its effect happen exactly once: retry, and make the operation idempotent with a key the server checks.

**Wrong model.** A timeout means the request failed, so it is safe to retry (or: exactly-once delivery is something the network or a library can give you).

**Objectives.**
1. Explain why a client cannot know, after a timeout, whether its request took effect.
2. Say what at-most-once and at-least-once delivery each risk, and which a payment needs.
3. Define idempotent and tell which operations are naturally idempotent.
4. Explain how an idempotency key makes a charge safe to retry, and the server-side details it depends on.

## Chain

1. The question: timeout on a $50 charge; retry or not?
2. But three different failures look the same to the client, and asking again can fail the same way. Therefore no protocol guarantees exactly once.
3. Therefore choose: at most once (may lose) or at least once (may duplicate). A payment can't be lost, so retry. Therefore the server must make repeats harmless.
4. Therefore idempotence: some operations are naturally safe to repeat; a charge isn't.
5. Therefore the idempotency key: same key on every attempt; charge once per key; return the saved result to repeats.
6. But it only works if a crash can't separate the charge from its saved result, a repeat arriving mid-charge is turned away, and a key is never reused for a different payment.
7. Therefore the answer: retry with the same key; at-least-once delivery plus idempotent handling charges exactly once.

## Format

| Chapter | Format | Why |
|---|---|---|
| 1-3 | Narrated animation | Message timing between client and server: sequence diagrams with lost messages. |
| 4 | Narrated animation | Examples side by side, repeated twice. |
| 5-6 | Narrated animation | The key table on the server filling in; a crash and a race as timelines. |
| 7 | Narrated animation | Payoff. |
| (not built) | Hands-on exercise | A toy payment server with injected message loss and concurrent retries, where the learner adds a key check and sees duplicates stop. The research names this as the best way to learn the race condition; offered, not added. |

## Ledgers

**Setups and payoffs.**
- The $50 charge and the timeout (ch. 1) are answered in ch. 7.
- The three look-alike failures (ch. 2) are why retries happen (ch. 3) and why the lost-reply case needs the saved result (ch. 5).
- "Exactly once" (ch. 2) returns as the effect, not the delivery (ch. 7).

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| timeout | ch. 1 | the client stops waiting for a reply |
| at most once / at least once / exactly once | ch. 2-3 | how many times a request may be carried out: never retried; retried until a reply arrives; exactly one time |
| idempotent | ch. 4 | doing it twice has the same effect as doing it once |
| idempotency key | ch. 5 | a unique value the client makes once per payment and sends with every attempt |

**Numbers to remember.** None beyond the example's $50; the three look-alike failures.

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
> The server might still be working on it.
> Or it might have crashed partway through.
> Or the charge went through, and the reply was lost on the way back.
> In every case, the client sees the same thing: nothing.
> It could ask the server whether the charge happened. But the question and its answer cross the same network, and can be lost the same way.
> Every confirmation is another message that can be lost, so whoever sends the last message never knows it arrived. However many messages the client sends, it can't be certain. So no protocol over an unreliable network can promise that a request is delivered exactly once.

*Screen:* three sequence diagrams side by side (client left, server right, time down): (a) request arrow stops halfway with a cross; (b) request arrives; the server is still working (a spinner), or it crashes mid-charge (two small variants); (c) request arrives, "charged $50" on the server, reply arrow stops halfway with a cross. Under all three, the client's view: the same empty timeline and "timeout". Then a "did it work?" message also crossing out.

### 3. At most once, or at least once

> That leaves two choices.
> Send the request once and never retry. Nothing is ever done twice, but a lost request is simply lost. That's called at most once.
> Or keep retrying until a reply arrives. As long as the client keeps trying, nothing is lost, but whenever only a reply was lost, the request is carried out again. That's at least once: one time or more.
> A payment can't just be lost, so the client retries.
> That means the server has to make a repeated request harmless.

*Screen:* two lanes: "at most once: never retry" with outcomes "charged 0 or 1 times", and "at least once: retry until a reply" with outcomes "charged 1 or more times"; the second lane highlighted.

### 4. Safe to repeat

> An operation is idempotent if doing it any number of times has the same effect as doing it once.
> "Set the shipping address to this" is idempotent. Do it again, and the address is still the same.
> "Delete order seven" is idempotent too. The second time, there's nothing left to delete.
> "Charge fifty dollars" is not. Every copy charges the card again.
> So the charge has to be made safe to repeat.

*Screen:* three operations, each applied twice with the resulting state shown: address unchanged; order 7 gone (second delete: "not found", state the same); card charged $50, then $100 in coral. A small note: "in HTTP, PUT and DELETE are meant to be idempotent; POST is not".

### 5. Idempotency keys

> The standard way is an idempotency key.
> Before its first attempt, the client makes up a key for this payment: a long random ID, like a UUID, so long that two payments picking the same one is practically impossible. It sends that same key with every attempt at this payment.
> The first time the server sees the key, it charges the card, and saves the result under that key.
> When a retry arrives with the same key, the server doesn't charge again. It looks up the saved result and sends that back.
> So in the lost-reply case, the retry gets back a saved copy of the reply that was lost, and the customer pays once.
> Payment APIs such as Stripe's work this way. The client puts the key in a request header called Idempotency-Key.

*Screen:* the client makes "key: 7f3a…c91" once; the request carries it. The server has a table "key → result". First request: table empty for the key → "charge $50" → row "7f3a…c91 → charged, receipt #1042". Reply lost (case c). Retry with the same key → row found → "receipt #1042" returned; the card shows $50 once. A header line: "Idempotency-Key: 7f3a…c91".

### 6. Where it can still go wrong

> A few details decide whether this works.
> First, a crash must never leave a charge without its saved result, or the retry finds no record and charges again. When the charge and the result live in the server's own database, it saves them in one database transaction, so either both are saved or neither is. And when charging the card means calling another company's service, that call crosses an unreliable network too. So the server does what the client did: it sends that call with an idempotency key of its own, and can safely repeat it.
> Second, a retry can arrive while the first attempt is still running. The server checks the key and marks it as in progress in one step, so two attempts can't both find it unused. Then it turns the retry away with "still in progress, try again", instead of starting a second charge.
> Third, a key belongs to one payment. A request that reuses a key with a different amount is rejected, not answered with the old receipt.

*Screen:* (1) a timeline: "charge card" → crash before "save key → result"; retry finds nothing → second charge (coral). Then the two fixes: one box around "charge + save" labelled "one transaction: both saved or neither"; and a call from the server to the card network carrying its own "Idempotency-Key". (2) two requests with the same key arriving 5 ms apart; the first marks the key "in progress"; the second gets "in progress, try again" (check and mark in one atomic step). (3) the same key with "$50" then "$80": the second is rejected ("key reused with a different request").

### 7. The answer

> So after a timeout, the client should retry, with the same idempotency key.
> The network can't deliver a request exactly once. But delivering it at least once, to a server that makes repeats harmless, charges the customer exactly once. This is often called effectively-once processing: exactly-once delivery is impossible, but an exactly-once effect isn't.

*Screen:* the chapter 1 scene replayed: timeout → retry with the same key → one charge, receipt returned. "at least once delivery + idempotent handling = charged exactly once". End card: references: Kleppmann, Designing Data-Intensive Applications (2017), ch. 8 and 11; Stripe API reference, Idempotent requests; RFC 9110 §9.2.2 (idempotent methods); Helland, "Idempotence Is Not a Medical Condition", ACM Queue (2012); the Two Generals Problem (Akkoyunlu, Ekanadham & Huber, 1975; Gray, 1978).

## Evidence

| Claim | Source |
|---|---|
| After a timeout the client cannot tell a lost request, a slow or crashed server, and a lost reply apart | Kleppmann, DDIA (2017), ch. 8, "Unreliable Networks" |
| No protocol over a lossy channel can give certainty (Two Generals); exactly-once delivery can't be guaranteed | Two Generals' Problem (Akkoyunlu, Ekanadham & Huber, 1975; named by Gray, 1978); Kleppmann 2017 ch. 8 |
| At-most-once / at-least-once delivery; at-least-once + idempotent processing gives exactly-once effect | Kleppmann 2017, ch. 11 ("Idempotence"); Kafka exactly-once literature |
| Idempotent: repeating has the same effect as doing it once; PUT and DELETE idempotent, POST not | RFC 9110 §9.2.2 |
| Idempotency keys: client-generated unique key per operation, sent with each retry; server saves the result of the first request and returns it for repeats | Stripe API reference, "Idempotent requests" |
| Header name Idempotency-Key | Stripe API reference |
| The dedup record and the side effect must be atomic; concurrent duplicates need a check-and-set | Helland, "Idempotence Is Not a Medical Condition", ACM Queue 10(4), 2012; Brandur Leach, "Designing robust and predictable APIs with idempotency" (Stripe blog, 2017) and "Implementing Stripe-like Idempotency Keys in Postgres" (2017): atomic phases between foreign state mutations, recovery points |
| Calls to another service carry their own idempotency key | Brandur Leach 2017 (the Rocket Rides example charges through Stripe with an idempotency key); DDIA ch. 12, end-to-end request IDs |
| Concurrent use of a key → 409 Conflict; same key with a different payload → rejected (422 in the IETF draft; an error at Stripe and AWS) | Brandur Leach 2017; IETF draft-ietf-httpapi-idempotency-key-header-07; Stripe API reference; AWS EC2 IdempotentParameterMismatch |
| At-least-once can apply an operation more than twice | Tanenbaum & van Steen, Distributed Systems 3rd ed., §8.3 |

## Review log

**Round 1:** editor PASS, expert REVISE, student retold the answer correctly (lost "a few times").
- Expert, blocking: "at least once" was shown as "charged 1 or 2 times"; retrying until a reply can apply the charge any number of times. Now "one time or more" in narration and "1 or more times" on screen.
- Expert: a key reused with a different request must be rejected; added as the third detail in chapter 6 (Stripe, AWS and the IETF draft all do this). Idempotent is now defined over "any number of times" (RFC 9110).
- Expert, declined: citing an RFC for the Idempotency-Key header. The research pass found it is still an IETF draft (draft-ietf-httpapi-idempotency-key-header-07, expired April 2026), not an RFC, so the end card keeps Stripe's documentation and the evidence table cites the draft.
- Student: "still working, or crashed" was two situations in one sentence (now two sentences and two diagram variants); the jump to "no protocol can promise" needed a reason (added: every confirmation is another message that can be lost, so the last message's sender never knows it arrived); key uniqueness was asserted (now: so long that a collision is practically impossible); "succeed or fail together" named the hardest part without saying how. Chapter 6 now says how: one transaction inside the server's own database, and the server's own idempotency key on its call to the card network.
- Expert, nit, not taken: bounded retries in real clients. The lesson's mechanism holds for any number of retries; retry policy (backoff, limits) is a separate topic.

**Round 2:** editor PASS, expert REVISE, student retold the answer correctly (lost "a few times").
- Expert, blocking: the screen showed "422" for a reused key as if Stripe returned it; 422 is the IETF draft's code and Stripe answers differently. Status codes are gone from the screen (the student also didn't know them); the outcomes are described in words.
- Expert: chapter 2's impossibility is about delivery, so it now says "delivered exactly once" (chapter 7 keeps "charged exactly once" for the effect). The in-progress check must be atomic; chapter 6 now says the server checks and marks the key in one step. Two Generals added to the end card.
- Student: "transaction" now defined (both saved or neither); the key's uniqueness is anchored to a familiar thing (a UUID); the server's own key for the card network is now framed as the same problem one level down (that call crosses an unreliable network too, so the server does what the client did).
- Not taken: calling the three failures "among the ways" (the script says they look alike, not that they are all the ways); the DELETE response-code nuance (no caption states response codes).

**Round 3:** expert PASS, editor PASS, student retold the question and the answer correctly. The gate is passed; the should-fix items are applied once, and round 4 decides the lock.
- Expert: "nothing is lost" holds only while the client keeps retrying; now said so. The closing idea now has its standard name, effectively-once processing (DDIA ch. 11). The retry gets back "a saved copy" of the lost reply, not the reply itself.

**Round 4 (final):** expert PASS, editor PASS, student retold the question and answer correctly (retry with the same idempotency key; the server charges once and replays the saved result). Locked. Should-fix items logged, not applied, per the stopping rule:
- Expert: the server's own key for the card network must stay the same across that call's retries. Covered by "the server does what the client did" (the client made one key and reused it); worth making explicit in a revision.
- Expert: "effectively-once" asserted without a source; DDIA ch. 11 uses the term (research/canonical_web_agent.md), so it stands.
- Expert: the step from "the sender can't be certain" to "no protocol can promise exactly-once delivery" is compressed. A revision candidate if the learner flags it.
- Editor: chapter 6 announces "a few details" before the failure is felt; a revision candidate.
