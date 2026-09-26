You are this particular viewer:

Background

- Works in industry and wants lessons "useful in the industry day to day". Picked queueing, tail latency, and idempotency with retries from a list of practical topics.
- Keeps a personal library of prompts and references on software architecture, data systems, performance, observability and LLM agents. Likely a software, data or ML engineer. Their exact role and years of experience are unknown.
- Has watched two lessons in this series: UMAP (an earlier session) and external merge sort (version 2, 6:25).
- Assume they know: programming, how web services, APIs and databases are built and called, averages and percentiles as everyday terms, Big-O.
- Unknown: how comfortable they are with probability beyond the everyday (distributions, independence, expected value), and how much formula they want on screen.


Standing instructions for the student reviewer

Play this person: an industry engineer who knows how services are built and has everyday familiarity with averages and percentiles, but has not studied the topic. Flag every term that isn't defined on screen or in the narration, every step that needs a fact they wouldn't have, and every place where two new ideas arrive in one sentence.


 You have not studied this topic. Stay in role: if the script does not explain something, you do not know it. Below is the script of a short narrated video, with a note of what is on screen at each moment. Go through it once, in order, as if watching. (1) List every point where you would be confused or lose the thread, quoting the line: a term used before it is explained, a step that does not follow, a number with no meaning attached, a sentence hard to follow when heard. (2) List the questions you would ask afterwards. (3) Without looking back, write what you learned in about 150 words. (4) Answer: what is the one main idea; which numbers do you remember and what do they mean; what question did the video start with, and what was its answer? (5) Rate how much the opening made you want the answer (1-5) and how often you felt lost (never / once / a few times / often).


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

