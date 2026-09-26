You are a professor who has taught this material for years. Below is the script of a short narrated explainer video, with a note of what is on screen at each moment, followed by the list of numbers it uses and where each comes from. Review it for correctness and canonicity. You are the only domain expert who will see it before it is produced, so be exacting. Report every problem with: severity (BLOCKING = wrong, misleading, or non-canonical in a way a professor would object to; SHOULD FIX = imprecise, a missing caveat, non-standard terminology; NIT), the exact quote, what is wrong, and the corrected wording. Check every factual and numerical claim including arithmetic and units; that terminology and notation match the standard sources and simplifications teach nothing false; whether anything essential is missing or anything peripheral gets too much weight; and overstated claims about optimality, generality and real systems. End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

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
> Every confirmation is another message that can be lost, so whoever sends the last message never knows it arrived. However many messages the client sends, it can't be certain. So no protocol over an unreliable network can promise that a request is carried out exactly once.

*Screen:* three sequence diagrams side by side (client left, server right, time down): (a) request arrow stops halfway with a cross; (b) request arrives; the server is still working (a spinner), or it crashes mid-charge (two small variants); (c) request arrives, "charged $50" on the server, reply arrow stops halfway with a cross. Under all three, the client's view: the same empty timeline and "timeout". Then a "did it work?" message also crossing out.

### 3. At most once, or at least once

> That leaves two choices.
> Send the request once and never retry. Nothing is ever done twice, but a lost request is simply lost. That's called at most once.
> Or retry until a reply arrives. Nothing is lost, but whenever only a reply was lost, the request is carried out again. That's at least once: one time or more.
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
> Before its first attempt, the client makes up a key for this payment: a random string so long that two payments picking the same one is practically impossible. It sends that same key with every attempt at this payment.
> The first time the server sees the key, it charges the card, and saves the result under that key.
> When a retry arrives with the same key, the server doesn't charge again. It looks up the saved result and sends that back.
> So in the lost-reply case, the retry gets the reply that was lost, and the customer pays once.
> Payment APIs such as Stripe's work this way. The client puts the key in a request header called Idempotency-Key.

*Screen:* the client makes "key: 7f3a…c91" once; the request carries it. The server has a table "key → result". First request: table empty for the key → "charge $50" → row "7f3a…c91 → charged, receipt #1042". Reply lost (case c). Retry with the same key → row found → "receipt #1042" returned; the card shows $50 once. A header line: "Idempotency-Key: 7f3a…c91".

### 6. Where it can still go wrong

> A few details decide whether this works.
> First, a crash must never leave a charge without its saved result, or the retry finds no record and charges again. When the charge and the result live in the server's own database, it saves them in one transaction. When charging the card means calling another company's service, the server sends that call its own idempotency key, so repeating that call can't charge twice either.
> Second, a retry can arrive while the first attempt is still running. The server marks the key as in progress, and turns the retry away with "still in progress, try again", instead of starting a second charge.
> Third, a key belongs to one payment. A request that reuses a key with a different amount is rejected, not answered with the old receipt.

*Screen:* (1) a timeline: "charge card" → crash before "save key → result"; retry finds nothing → second charge (coral). Then the two fixes: one box around "charge + save" labelled "one transaction"; and a call from the server to the card network carrying its own "Idempotency-Key". (2) two requests with the same key arriving 5 ms apart; the first marks the key "in progress"; the second gets "409: in progress, try again". (3) the same key with "$50" then "$80": the second is rejected ("422: key reused with a different request").

### 7. The answer

> So after a timeout, the client should retry, with the same idempotency key.
> The network can't deliver a request exactly once. But delivering it at least once, to a server that makes repeats harmless, charges the customer exactly once.

*Screen:* the chapter 1 scene replayed: timeout → retry with the same key → one charge, receipt returned. "at least once delivery + idempotent handling = charged exactly once". End card: references: Kleppmann, Designing Data-Intensive Applications (2017), ch. 8 and 11; Stripe API reference, Idempotent requests; RFC 9110 §9.2.2 (idempotent methods); Helland, "Idempotence Is Not a Medical Condition", ACM Queue (2012).


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

