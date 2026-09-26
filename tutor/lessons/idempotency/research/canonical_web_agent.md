# Idempotency and retries: canonical treatment (research notes)

Lesson: *why a client cannot guarantee that a request over an unreliable network is carried out exactly once, and how systems such as payment APIs avoid doing an operation twice when requests are retried.*

**How to read this.** Unless marked **(uncertain)**, each claim was checked against the primary text during this research, meaning the RFC, paper, book text or vendor documentation. Where I could not read the primary source directly, I say so. Where a formula is my own derivation rather than taken from a canonical source, it is marked **(derived)**.

---

## 1. The canonical worked example

There are two standard examples: one used for motivation and one used for the definition. A third example is standard for the impossibility argument.

**A. The double charge or double transfer.** This is the most common example, and it is the backbone of any lesson about payment APIs. A client asks a server to move money, and the server does it. The reply is then lost or arrives late, so the client times out and retries, and the money moves twice.
- Tanenbaum & van Steen, *Distributed Systems* 3rd ed. (v3.02, 2017/18), §8.3 "Lost reply messages": a transfer between bank accounts is carried out, the reply is lost, and the client retransmits. "Twice the amount of money will be transferred. Transferring money is not idempotent." The contrasting case is reading the first 1024 bytes of a file. §2.3 has the same contrast: "transfer $10,000 from my bank account" versus "tell me how much money I have left." ([book site](https://www.distributed-systems.net/))
- Kleppmann, *Designing Data-Intensive Applications* (DDIA) 1st ed. (2017), Ch. 12, "The end-to-end argument for databases", **Example 12-1**: a transaction transfers $11. The client loses the connection after sending `COMMIT` and retries, and the retry can transfer $22 instead of the intended $11. **Example 12-2** fixes this with a `requests` table that has a `UNIQUE (request_id)` constraint. In the 2nd ed. (Kleppmann & Riccomini, 2026) these became Examples 13-1 and 13-2. (I verified the text and example numbering through the community translation [Vonng/ddia](https://github.com/Vonng/ddia), which reproduces the SQL. The English section titles are from memory, so DDIA claims in this file are paraphrased rather than quoted.)
- Kleppmann, *Distributed Systems* lecture notes, Cambridge 2021/22 ([PDF](https://www.cl.cam.ac.uk/teaching/2122/ConcDisSys/dist-sys-notes.pdf)). §1.3, slides 15–17, uses the `processPayment()` RPC and asks whether it is safe to retry: a retry "might cause the request to be performed more than once (e.g. charging a credit card twice)". §5.1 raises the stakes to "deducting £1,000 from your bank account".
- Stripe, "Designing robust and predictable APIs with idempotency" (Brandur Leach, 22 Feb 2017, [blog](https://stripe.com/blog/idempotency)): charging a customer "twice would lead to the customer being double-charged". This is the motivation for the `Idempotency-Key` header.
- Gray, "Notes on Data Base Operating Systems" (1978, [PDF](https://jimgray.azurewebsites.net/papers/dbos.pdf)), §5.8.3.3.1: a cash-dispensing terminal in Füssen that opens a drawer with a million marks, and a computer in Tokyo that debits the account.
- Airbnb, "Avoiding Double Payments in a Distributed Payments System" (J. Chew & N. Khisti, 16 Apr 2019, [Medium](https://medium.com/airbnb-engineering/avoiding-double-payments-in-a-distributed-payments-system-2981f6b070bb)).

**B. Incrementing a counter versus setting a value (or adding to a set).** This is the standard example for defining idempotence.
- Kleppmann's Cambridge notes, §5.1, slides 88–90: liking a post. `increment post.likes` retried takes 12,300 to 12,302. f(likeCount) = likeCount + 1 is **not** idempotent. f(likeSet) = likeSet ∪ {userID} **is** idempotent. Slide 89 shows a real 2014 Twitter profile with a negative following count, probably caused by a retried decrement.
- DDIA 1st ed. Ch. 11, "Idempotence": setting a key in a key-value store to a fixed value is idempotent, while incrementing a counter is not.
- Coulouris et al., *Distributed Systems: Concepts and Design* 5th ed., Ch. 5: adding to a set versus appending to a sequence. **(uncertain: from memory, wording not verified)**

**C. Two Generals, the example for impossibility.** Kleppmann's notes §2.1, slides 22–25, attribute it to Gray (1978) and map it onto an online shop and a payments service. They also say explicitly that the payment case "does not exactly match the two generals problem", because a payment can be refunded and its status queried later. Tanenbaum has a second impossibility illustration: a server that crashes while processing a document, shown in the table in §4, R2.

A further industry example comes from AWS: a retried `RunInstances` call launches two EC2 instances for a "singleton workload" (Featonby, [Builders' Library](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/)).

**Which is more common, and why.** A is the more common example. It appears in the textbooks (Tanenbaum, DDIA, Kleppmann, Gray) and in essentially every industry source (Stripe, Airbnb, AWS). It became the standard example for four reasons:
1. The operation is inherently non-idempotent. You cannot rewrite "charge $20" as "set x", so the example forces the request-ID or deduplication solution.
2. The harm is obvious.
3. The dangerous case, where the operation succeeded but the response was lost, is realistic.
4. The fix is exactly what payment APIs ship.

B is the usual one-slide definition. The typical structure is to motivate with A, define with B, and then return to A for the idempotency key.

---

## 2. The standard progression

**The common skeleton.** The textbooks and well-known articles below broadly follow this order:
1. An RPC or HTTP call looks like a local call but isn't one (Kleppmann slide 17; Birrell & Nelson 1984; Tanenbaum §8.3; MIT 6.5840 L2).
2. List what can go wrong. DDIA Fig. 8-1 has the request lost, the remote node down, and the response lost; the surrounding text lists six cases. Tanenbaum's five failure classes are: cannot locate the server, request lost, server crashes, reply lost, client crashes. Stripe's three are: the connection fails, the call fails midway, and the call succeeds but the connection breaks before the reply.
3. The central insight: **after a timeout the client cannot tell which of these happened.**
4. The binary choice: don't retry (at-most-once, the operation may be lost) or retry (at-least-once, the operation may be duplicated).
5. **The simpler version first:** operations that are naturally idempotent (reads, "set", PUT/DELETE, add-to-set) can simply be retried.
   - The Stripe blog shows an idempotent DNS `PUT` before the non-idempotent charge `POST`.
   - Kleppmann shows the counter first, then idempotence through a set.
   - Tanenbaum says to "structure all the requests in an idempotent way" before introducing sequence numbers.
6. **The full version:** for non-idempotent operations, the client attaches a unique ID, reuses it on every retry, and the server remembers it and replays the result.
   - Tanenbaum: per-client sequence numbers.
   - Birrell & Nelson: call identifiers.
   - DDIA: operation identifiers.
   - Stripe: idempotency keys.
   - Kleppmann's summary: "exactly-once semantics: retry + idempotence or deduplication".
7. Refinements:
   - Durable and atomic storage of the key together with the effect.
   - Retention window.
   - Parameter mismatch.
   - Concurrent duplicates.
   - End-to-end propagation (DDIA Ch. 12; Saltzer, Reed & Clark 1984).
8. Retry hygiene, in order: plain retry, then exponential backoff, then capped backoff, then jitter, then limits on retries (budgets, token buckets, retrying at a single layer). Sources: Brooker 2015; the AWS Builders' Library; Google SRE book Ch. 21–22.
9. Limits: interleaving with other clients' writes, delayed duplicates, and the boundary of "exactly-once".

**How each canonical source orders it:**
- **Kleppmann, Cambridge notes (2021/22):**
  - §1.3, RPC: payment example, "is it safe to retry?"
  - §2.1, Two Generals: applied to shop and payment.
  - §2.3, system models: "fair-loss links", with the rule that retry plus deduplication gives a reliable link. TCP does this per connection but "typically" gives up after about a minute.
  - §5.1, "Retrying state updates": likes counter; deduplication requires stable storage; idempotence; at-most-once, at-least-once and exactly-once; the limits of idempotence (add then remove); timestamps and tombstones.
- **Tanenbaum & van Steen 3rd ed.:**
  - §2.3: lost request versus lost reply; idempotence defined.
  - §4.x: DCE RPC defaults to at-most-once, and procedures can be marked idempotent in the IDL.
  - §8.3: five failure classes; lost request (timer and retransmit); server crash (at-least-once, at-most-once, no guarantee; "exactly-once… in general, there is no way to arrange this"; Note 8.9 table); lost reply (idempotence, then sequence numbers, then a "retransmission" bit); client crash (orphans).
- **Coulouris et al. 5th ed., Ch. 5:** request-reply protocol, then failure model, then timeouts, then duplicate requests, then lost replies (idempotent operations or a reply "history"), then **Fig. 5.9 "Call semantics"** (Maybe, At-least-once, At-most-once). Verified through the publisher's instructor slides ([WSU copy](https://eecs.wsu.edu/~cs464/Chap5.pdf)).
- **DDIA 1st ed.:**
  - Ch. 8: unreliable networks, Fig. 8-1, timeouts.
  - Ch. 9: 2PC and exactly-once message processing.
  - Ch. 11: exactly-once, "effectively-once" and idempotence.
  - Ch. 12: end-to-end duplicate suppression with Examples 12-1 and 12-2.
  - In the 2nd ed. (2026) the chapters are 9, 8, 12 and 13, according to the translation.
- **Industry sequence:**
  - Stripe blog (2017): failure cases, then idempotent endpoints, then idempotency keys, then exponential backoff, then jitter and the thundering herd.
  - Brandur, "Implementing Stripe-like Idempotency Keys in Postgres" (27 Oct 2017, [brandur.org](https://brandur.org/idempotency-keys)): the implementation.
  - AWS Builders' Library: Brooker's "Timeouts, retries, and backoff with jitter" comes first, then Featonby's "Making retries safe with idempotent APIs".
- **MIT 6.5840 (2025), Lecture 2 ([notes](http://nil.csail.mit.edu/6.5840/2025/notes/l-rpc.txt)):** "best-effort RPC" with the delayed-duplicate example `Put("k",10); Put("k",20)`, then at-most-once (Go RPC "never re-sends"). Lab 2 ([lab](http://nil.csail.mit.edu/6.5840/2025/labs/lab-kvsrv1.html)) builds at-most-once `Put` with version numbers over a lossy network and introduces `ErrMaybe`.

---

## 3. Model, parameters, what is measured, and terminology

**System model.** From Kleppmann §2.3, slide 33:
- **Links** are point-to-point and "fair-loss": "Messages may be lost, duplicated, or reordered. If you keep retrying, a message eventually gets through." A fair-loss link becomes a reliable link by "retry + dedup".
- **Nodes** crash, or crash and recover. Deduplicating across a crash "requires storing requests… in stable storage" (§5.1).
- **Timing** is asynchronous, with unbounded delay. DDIA Ch. 8: only if delay were bounded by *d* and processing by *r* would **2d + r** be a sound timeout.

**Parameters:**
- Per-attempt timeout *T*.
- Maximum attempts *n*. gRPC's `maxAttempts` includes the original call, and values above 5 are treated as 5 ([gRFC A6](https://github.com/grpc/proposal/blob/master/A6-client-retries.md)).
- Backoff base, cap and jitter type.
- Key retention window *W*.
- Key scope, meaning per account or user. AWS keys the idempotency "session" on "the customer identifier and their unique client request identifier". Brandur uses `UNIQUE (user_id, idempotency_key)`.
- Request fingerprint.

**What is measured:**
- **Correctness:** the number of times the effect is applied, *k* ∈ {0, 1, ≥2}.
  - Tanenbaum's Fig. 8.19 cells are OK, DUP and ZERO.
  - Spector's reliability table counts "op performed: 0,1 / ≥1 / 1" under lost packets, slave crash and master crash (Spector, Stanford TR STAN-CS-80-850, 1980; CACM 25(4), 1982; [PDF](http://i.stanford.edu/pub/cstr/reports/cs/tr/80/850/CS-TR-80-850.pdf)).
- **Availability and cost:** the probability of success within *n* attempts; attempts per logical request (load amplification); latency percentiles. AWS picks a timeout from an acceptable false-timeout rate, for example 0.1%, which means the p99.9 latency (Brooker).

**Definitions of "idempotent" differ by field:**
- **Mathematics:** f(f(x)) = f(x), a property of a function on state (Kleppmann slide 90).
- **HTTP**, [RFC 9110 §9.2.2](https://www.rfc-editor.org/rfc/rfc9110.html#section-9.2.2): "the intended effect on the server of multiple identical requests with that method is the same as the effect for a single such request."
  - It covers *intended* effect only. A server may still log each request or keep revision history.
  - The response may differ: "…same intended effect, even if the original request succeeded, though the response might differ."
  - PUT, DELETE and the safe methods (GET, HEAD, OPTIONS, TRACE) are idempotent. POST is not, and "PATCH is neither safe nor idempotent" ([RFC 5789 §2](https://www.rfc-editor.org/rfc/rfc5789.html#section-2)).
  - **Safe ≠ idempotent.** DELETE is idempotent but not safe.
- **Systems and RPC:** a request that "can safely be repeated as often as necessary with no damage being done" (Tanenbaum §8.3). Helland ([ACM Queue 10(4), 2012](https://queue.acm.org/detail.cfm?id=2187821)) defines it as "Acting as if used only once, even if used multiple times", and explicitly excludes heap fragmentation, logging and monitoring, and performance as not "semantically relevant".
- **Messaging:** "Idempotent Receiver", a receiver "that can safely receive the same message multiple times", reached either by de-duplication or by message semantics (Hohpe & Woolf, *Enterprise Integration Patterns*, 2003; [pattern page](https://www.enterpriseintegrationpatterns.com/patterns/messaging/IdempotentReceiver.html)). Kafka's "idempotent producer" is a separate use of the word.
- **Deduplication versus idempotence.** Kleppmann separates the two. Deduplication means the server remembers request IDs. Idempotence means the request is naturally repeatable: "Idempotent requests can be retried without deduplication." An idempotency key is a deduplication mechanism that makes a non-idempotent operation idempotent with respect to retries.

**Call and delivery semantics use the same words for different things:**

| Term | What it means, by source |
|---|---|
| maybe / best-effort | Coulouris Fig. 5.9 "Maybe": no retransmission. Tanenbaum's third school, "guarantee nothing": 0 to many executions. MIT "best-effort": resend a few times, then give up. |
| at-least-once | Every source: retry until acknowledged; duplicates are possible. Coulouris: retransmit and **re-execute**. |
| at-most-once | **Coulouris:** retransmit request **plus** duplicate filtering **plus** retransmit the stored reply, so retries still happen. **Tanenbaum:** "gives up immediately and reports back failure". **Kleppmann:** "send request, don't retry". **Birrell & Nelson:** "precisely once" if the call returns; if an exception is reported, "either once or not at all". AWS calls the client-token contract an "at most once commitment". |
| exactly-once | **Kleppmann:** "retry + idempotence or deduplication". **DDIA:** suggests "effectively-once" as the more descriptive name. **Spector:** "only-once-type-1/2", where type 2 needs a recoverable server. **NFSv4.1:** "EOS". **Kafka:** "processed once and only once". **SQS FIFO:** "exactly-once processing", meaning no duplicates from `SendMessage` retries within 5 minutes. |

Coulouris' "at-most-once" (retransmit, filter duplicates, replay the reply) is essentially Kleppmann's "exactly-once" once the client keeps retrying. This naming clash confuses learners, so pick one vocabulary.

**The request identifier has different names:**
- idempotency key: Stripe, Adyen, IETF draft
- `PayPal-Request-Id`
- `ClientToken` or "client request identifier": AWS EC2
- `request_id`: Google [AIP-155](https://google.aip.dev/155); DDIA Example 12-2
- `MessageDeduplicationId`: SQS
- call identifier: Birrell & Nelson
- XID: ONC RPC
- producer ID plus sequence number: Kafka
- slot ID plus sequence ID: NFSv4.1

**"Exactly-once delivery" versus "exactly-once processing" (or effect).** Tyler Treat, "You Cannot Have Exactly-Once Delivery" (25 Mar 2015, [post](https://bravenewgeek.com/you-cannot-have-exactly-once-delivery/)), argues against the first and says "the way we achieve exactly-once delivery in practice is by faking it" through idempotence or deduplication. Confluent claims the second, scoped to Kafka (see §8).

---

## 4. Key results, formulas, assumptions and limits

**R1. Two Generals: no finite protocol gives certainty.**
- Gray 1978 §5.8.3.3.1, "The Generals Paradox", pp. 465–466: "no fixed length protocol exists: Let P be the shortest such protocol. Suppose the last messenger in P gets lost. Then either this messenger is useless or one of the generals doesn't get a needed message…"
- Formalized by Halpern & Moses, JACM 37(3), 1990 ([arXiv](https://arxiv.org/abs/cs/0006009)): "in practical systems common knowledge cannot be attained."
- Earlier source: Akkoyunlu, Ekanadham & Huber, SOSP 1975 ([doi](https://doi.org/10.1145/800213.806523)). **(uncertain:** I verified only the bibliographic record. That this paper contains the result comes from secondary sources.)
- *Assumptions:* any message can be lost; the goal is simultaneous coordinated action; the protocol is finite.
- *Where it stops holding:*
  - Gray: drop the requirement of "some finite fixed maximum length" and two-phase commit (2PC) works, possibly with many messages.
  - Kleppmann: effects that can be undone or looked up later (a refund, a status query) escape the dilemma.

**R2. A client alone cannot get exactly-once.**
- DDIA Fig. 8-1: after no response, you cannot distinguish (a) request lost, (b) remote node down, (c) response lost. A timeout does not cancel work that is already queued.
- Tanenbaum Fig. 8.18 and Note 8.9. Server events are M (send completion), P (process) and C (crash). The server can order them M→P or P→M. The client can always reissue, never reissue, reissue only if the request was acknowledged, or reissue only if it was not. Every one of the 8 combinations fails for some crash ordering: "for any combination either the request is lost forever, or carried out twice." (Fig. 8.19, verified.)

| Client reissue strategy | M→P: MPC | MC(P) | C(MP) | P→M: PMC | PC(M) | C(PM) |
|---|---|---|---|---|---|---|
| Always | DUP | OK | OK | DUP | DUP | OK |
| Never | OK | ZERO | ZERO | OK | OK | ZERO |
| Only when ACKed | DUP | OK | ZERO | DUP | OK | ZERO |
| Only when not ACKed | OK | ZERO | OK | OK | DUP | OK |

- *Assumptions:* the server has no durable, atomic record linking "processed" to "request ID".
- *Where it stops holding:* when the server can commit the effect and a deduplication record atomically and durably.
  - Spector's only-once-type-2 requires a *recoverable* server.
  - RFC 8881 (NFSv4.1) §2.10.6: "true and complete EOS is not possible unless the server persists the reply cache in stable storage."

**R3. The constructive result: exactly-once effect = at-least-once + deduplication or idempotence.**
- Kleppmann slide 90.
- Birrell & Nelson, ACM TOCS 2(1), 1984, §3.1–3.2 ([doi](https://doi.org/10.1145/2080.357392)): the call ID is [machine ID, process, sequence number]. The callee keeps "the sequence number of the last call invoked by each calling activity" and discards duplicates. The state may be dropped after about five minutes.
- The conditions in the canonical sources:
  1. The client keeps retrying with the *same* ID until it gets an answer. This needs a fair-loss network and a client that persists the ID across its own crash. Airbnb: "Persist these idempotency keys to the database before calling the service."
  2. The deduplication record is committed **atomically with the effect**:
     - AWS: recording the token and "all mutating operations… must meet the properties for an… ACID operation".
     - DDIA Example 12-2: insert into `requests` in the same transaction.
     - Kafka: "store its offset in the same place as its output".
  3. Uniqueness is enforced by the store, not by check-then-insert. DDIA relies on a `UNIQUE` constraint because application-level check-then-insert can fail under non-serializable isolation.
  4. The retention window is at least as long as the retry horizon: Stripe 24 h, Birrell & Nelson about 5 min, SQS 5 min.
  5. Same key means same request. Parameters are compared; see §8.
  6. When relying on natural idempotence rather than keys, DDIA Ch. 11 requires the same messages to be replayed in the same order, processing to be deterministic, and no other node concurrently updating the same value, with fencing on failover.
- *Where it stops holding:*
  - Side effects outside the deduplication boundary. Brandur calls these "foreign state mutations" and gives email as an example. Confluent: exactly-once "is guaranteed within the scope of Kafka Streams' internal processing only".
  - Keys that expire.
  - Keys lost by a crashed client.
  - Interleaving with other writers (R4).

**R4. Idempotence does not survive interleaving.**
- Kleppmann slide 91: f(likes) = likes ∪ {id} and g(likes) = likes \ {id}. f(f(x)) = f(x), but f(g(f(x))) ≠ g(f(x)): a retried "like" arriving after an "unlike" brings the like back. Kleppmann's fix is logical timestamps plus tombstones.
- MIT 6.5840 L2: `Put("k",10); Put("k",20)`. A delayed retransmission of the first Put overwrites 20.
- RFC 8881 §2.10.6: a delayed duplicate `WRITE A` executed after `WRITE B` corrupts data. For this reason NFSv4.1 enforces EOS even for idempotent WRITEs.

**R5. Retry arithmetic.**
- **Per-attempt failures.** With independent per-attempt failure probability *p*:
  - P(all *n* attempts fail) = *p*ⁿ.
  - Expected attempts = (1 − *p*ⁿ)/(1 − *p*) ≤ *n*.
  - At 100% failure the work is *n* = 1 + N retries. Brooker 2022 ([blog](https://brooker.co.za/blog/2022/02/28/retries.html)): "the system does 1+N times as much work."
  - This is textbook probability (derived). The independence assumption fails under overload, where failures are correlated (Brooker's "because of correlation" in the AWS article).
- **Duplicate rate without deduplication (derived teaching model, not from a canonical text).** Let *b* = P(reply lost *or later than the timeout* | the server executed). With retry-until-acknowledged and no deduplication:
  - P(executed ≥ 2 times) = *b*
  - E[executions] = 1/(1 − *b*)
  - With a timeout at p99.9, *b* ≈ 0.001 from slowness alone, so about 1 in 1,000 operations would be doubled. This connects Brooker's 0.1% false-timeout rule to duplicate rates.
- **Multi-layer amplification:** attempts at the bottom layer = ∏ attempts per layer = *a*^*L*.
  - [SRE book Ch. 22](https://sre.google/sre-book/addressing-cascading-failures/): "3 retries (4 attempts)" at 3 layers gives 4³ = **64**.
  - AWS (Brooker): a 5-deep stack gives **243×** = 3⁵. See §9 for a subtlety in how this is worded.
- **Retry budgets**, [SRE book Ch. 21](https://sre.google/sre-book/handling-overload/): a per-request cap of 3 attempts allows up to about **3X** requests. Adding a per-client retry ratio below 10% reduces growth "to just **1.1x**".
- **Backoff formulas.** Brooker, "Exponential Backoff and Jitter" (AWS Architecture Blog, 4 Mar 2015, [post](https://aws.amazon.com/blogs/architecture/exponential-backoff-and-jitter/)). The formulas in the post are images; I verified them against its [simulator code](https://github.com/awslabs/aws-arch-backoff-simulator).
  - Exponential: `min(cap, base·2^n)`
  - Full Jitter: `U(0, min(cap, base·2^n))`
  - Equal Jitter: `v/2 + U(0, v/2)`, where `v = min(cap, base·2^n)`
  - Decorrelated: `sleep = min(cap, U(base, 3·sleep))`
  - *Assumptions and limits:* the model is optimistic-concurrency contention on one row. "None of these approaches fundamentally change the N² nature of the work."
- **Fan-out tail**, Dean & Barroso, "The Tail at Scale", CACM 56(2), Feb 2013 ([PDF](https://www.barroso.org/publications/TheTailAtScale.pdf)): P(request slow) = 1 − (1 − *p*)ᴺ. Hedged requests, which send the same request to a second replica, are the usual remedy. Hedging assumes the operation is safe to duplicate: the paper places it in "largely read-only, loosely consistent" settings, and gRFC A6 says hedging must be enabled only for methods "safe to execute multiple times".

---

## 5. Standard numeric examples as they appear

- **DDIA Ex. 12-1:** a $11 transfer that is retried becomes **$22**. Ex. 12-2 uses request ID `0286FDB8-…`, accounts 4321 and 1234, amount 11.00.
- **Tanenbaum §2.3:** "transfer **$10,000**". §8.3: the first **1024 bytes** of a file (idempotent). Fig. 8.19: 2 server strategies × 4 client strategies × 3 crash orderings; every row has a DUP or a ZERO.
- **Kleppmann:**
  - Likes **12,300 → 12,301 → 12,302**; a negative following count (Twitter, 2014); **£1,000** debit.
  - The `processPayment(card, 3.99, GBP)` RPC.
  - TCP gives up after "on the order of one minute".
- **Gray 1978:** "a cash drawer with **a million marks**" in Füssen, with the debit in Tokyo.
- **Stripe:**
  - Blog: `amount=2000` (amounts are in cents, so $20) with `Idempotency-Key: AGJ6FJMkGQIpHUTX`; backoff ∝ **2ⁿ**.
  - API docs: keys up to **255** characters; V4 UUIDs recommended.
  - [Error handling docs](https://docs.stripe.com/error-low-level): retries are safe within **24 hours**, and "keys expire out of the system after 24 hours". SDK example `Stripe.max_network_retries = 2`.
- **Brandur (2017):**
  - The Rocket Rides ride-plus-charge example.
  - Recovery points `started`, `ride_created`, `charge_created`, `finished`.
  - Recycle keys after "say 24 hours"; the reaper uses about **72 hours**; concurrent use of a key returns **409 Conflict**.
- **Birrell & Nelson 1984:** callee deduplication state is discarded after "say, after **five minutes**"; 32-bit conversation identifier.
- **AWS (Brooker, Builders' Library):**
  - Timeout set at the downstream **p99.9** for **0.1%** false timeouts.
  - An anecdote about a **20 ms** timeout that caught TLS connection setup.
  - A 5-layer stack gives **243×** load.
  - A token bucket limits retries; added to the AWS SDK in **2016**.
- **Brooker, jitter blog:**
  - A simulated network with a mean delay of **10 ms**.
  - With **100** contending clients, jitter "reduced our call count by more than half".
  - Total work grows as **N²**.
- **Brooker 2022:** the token-bucket example deposits **0.1 token per success** and spends **1 per retry**. It behaves like N retries below about **10%** failure and like "0.1 retries" above that.
- **Google SRE book:**
  - **4³ = 64**.
  - A server-wide budget example of **60 retries per minute**.
  - A per-request limit of **3 attempts**, giving ~**3X**; a per-client ratio of **10%**, giving **1.1x**.
  - A backend at **10,200 QPS**, of which 200 QPS are retries of failed requests.
- **Tail at Scale:**
  - A server with 10 ms typical and 1 s p99 latency: at fan-out **100**, **63%** of requests are slower than 1 s.
  - A 1-in-10,000 slow server at fan-out **2,000** makes almost **1 in 5** requests slow.
  - Hedging after **10 ms** cut p99.9 latency from **1,800 ms to 74 ms** for **2%** more requests.
  - Deferring the hedge until p95 adds about **5%** load.
- **gRPC A6:** `maxAttempts` is capped at **5**; example `hedgingDelay` of **0.5s**.
- **SQS FIFO:** **5-minute** deduplication interval. **EC2** `ClientToken`: up to **64** ASCII characters. **Adyen** keys: max **64** characters, valid **7–14 days**. **Confluent:** the idempotent or transactional producer costs about **3%** throughput (1 KB messages, 100 ms transactions); Streams costs 15–30%.

---

## 6. Misconceptions practitioners bring, and the canonical correction

1. **"TCP is reliable, so my request arrives exactly once."**
   - DDIA Ch. 12: TCP suppresses duplicates only within one connection. Once the client reconnects and retries, TCP's duplicate suppression no longer applies.
   - Kleppmann: TCP gives up after about a minute.
   - Helland: HTTP can resend a request over a new connection, "for this reason, most HTTP requests are idempotent".
2. **"A timeout or error means the operation didn't happen."**
   - DDIA Fig. 8-1.
   - Kafka docs: a producer "cannot be sure if this error happened before or after the message was committed".
   - Stripe: treat **500** responses as "indeterminate".
3. **"Just retry."** Retries are "selfish" and multiply load across layers (Brooker; SRE Ch. 22: 64×). The fix is backoff with jitter, caps and budgets, and retrying at one layer.
4. **"Generate a fresh key on each attempt."** The key must be created once per logical operation, persisted, and reused on every retry.
   - Airbnb: "reuse the same idempotency key for retries".
   - The AWS SDK and CLI generate the token once and reuse it on retry.
5. **"Derive the key by hashing the payload."**
   - AWS warns that a caller may really want two identical EC2 instances, so a parameter hash can wrongly merge distinct requests.
   - DDIA does mention hashing the form fields as one option, and Stripe suggests keys derived from an object such as a cart ID. Present this as a trade-off.
6. **"Check whether the key exists, then insert it."** This is a race. Use a unique constraint (DDIA) or locking: Brandur returns 409 on a locked key, and Airbnb uses row-level lock "leases" with expiration.
7. **"PUT/DELETE are idempotent, so retries are always safe."**
   - The property holds only if the server implements it. gRFC A6 describes a non-idempotent delete.
   - Delayed duplicates can still clobber later writes (R4).
   - RFC 9110 lets a client retry idempotent requests automatically "if that request fails due to connection failure". It also says a client "SHOULD NOT automatically retry a failed automatic retry" and a proxy "MUST NOT automatically retry non-idempotent requests".
8. **"Idempotent means I get the same response."**
   - RFC 9110: the effect is the same but "the response might differ".
   - AWS: the response is "semantically equivalent" (for example, the instance state goes from pending to running).
   - Stripe replays the stored status and body, including 500s, and marks a replayed response with `Idempotent-Replayed: true`.
9. **"Distributed transactions or 2PC solve it."** DDIA Ch. 12: 2PC does not stop an end user from resubmitting a POST. That needs an end-to-end request ID passed all the way from the end-user client to the database. This follows Saltzer, Reed & Clark 1984 ([PDF](https://web.mit.edu/Saltzer/www/publications/endtoend/endtoend.pdf)), section "Duplicate message suppression": "suppression must be accomplished by the application itself".
10. **"Kafka, SQS or some framework gives me exactly-once end to end."** The guarantees are scoped (§8, §9).
11. **"An idempotency key protects forever."** It protects only within the retention window. Stripe: "We generate a new request if a key is reused after the original is pruned."

---

## 7. For a short lesson

**Essential:**
- The three failure points and the client's indistinguishability after a timeout (DDIA Fig. 8-1).
- Don't retry → at-most-once (may be lost). Retry → at-least-once (may be duplicated). No client-only strategy gives exactly-once (Tanenbaum Fig. 8.19 in miniature).
- The idempotence definition as "intended effect of N identical requests = effect of 1", with increment-versus-set and POST-versus-PUT examples.
- The idempotency-key pattern:
  - The client generates a random key (UUIDv4) once and reuses it on every retry.
  - The server stores key, request fingerprint and result **in the same transaction as the effect**, with a unique constraint.
  - A retry replays the stored result.
- The equation "exactly-once" = at-least-once + deduplication ("effectively-once"), valid only within the boundary where the deduplication record lives.

**Common extras:**
- Exponential backoff with jitter, and the thundering herd.
- Retry amplification across layers, and retry budgets.
- In-flight duplicates (409 Conflict) and payload mismatch (422 in the IETF draft; errors at Stripe and AWS).
- Key expiry windows.
- HTTP method semantics (RFC 9110).
- The Two Generals as a short teaser.
- Kafka's idempotent producer as a second real system.
- Delayed duplicates and interleaving (R4).

**Leave out:**
- FLP and consensus, Byzantine generals.
- 2PC internals, Kafka transaction internals.
- Orphan extermination and reincarnation.
- CRDTs and tombstones, NFSv4.1 slot tables.
- The formal common-knowledge proof.
- Hedged requests and fan-out tail math (mention them only if latency is a theme).
- Circuit-breaker debates.

---

## 8. Real systems canonically cited, and their mechanisms

| System | Mechanism (source) |
|---|---|
| **Stripe** | `Idempotency-Key` header on all POSTs. Saves the first status code and body "regardless of whether it succeeds or fails", including 500s. Compares parameters and "errors if they're not the same". Keys up to 255 characters, pruned after ≥24 h. Results are not saved for validation failures or conflicting concurrent requests. 429s are not cached because "rate limiters run before the API's idempotency layer". `Idempotent-Replayed: true` header. SDKs retry automatically with an auto-generated key ([API docs](https://docs.stripe.com/api/idempotent_requests); [error docs](https://docs.stripe.com/error-low-level)). |
| **IETF `Idempotency-Key` header draft** | [draft-ietf-httpapi-idempotency-key-header-07](https://www.ietf.org/archive/id/draft-ietf-httpapi-idempotency-key-header-07.txt) (Jena & Dalal, 15 Oct 2025). An Item Structured Header whose value is a String; a UUID is recommended; an optional payload "fingerprint". Status codes: **400** if the key is missing, **422** if a key is reused with a different payload, **409** if a retry arrives while the original is still processing. **Status: expired 18 Apr 2026. Not an RFC as of Sep 2026** ([datatracker](https://datatracker.ietf.org/doc/draft-ietf-httpapi-idempotency-key-header/)). The draft lists Stripe, Adyen, Dwolla, Interledger, WorldPay, Yandex, http4s, Finastra and Datatrans as implementers. |
| **Adyen** | `idempotency-key` header; UUIDv4; max 64 characters; valid 7–14 days. Concurrent duplicates return a transient error (HTTP 409 or 422, error code 704) ([docs](https://docs.adyen.com/development-resources/api-idempotency/)). |
| **PayPal** | `PayPal-Request-Id` header. A retry "returns the latest status of the previous request", not a replay of the original response. Retention varies by API ([docs](https://developer.paypal.com/api/rest/reference/idempotency/)). |
| **AWS EC2 / SDK** | `ClientToken` of up to 64 ASCII characters. The same token with different parameters fails with `IdempotentParameterMismatch` ([EC2 docs](https://docs.aws.amazon.com/ec2/latest/devguide/ec2-api-idempotency.html)). The SDK and CLI auto-generate a token and reuse it on retry. The token is stored atomically (ACID) with the effect, and the response is "semantically equivalent". Retention is the resource lifetime plus a margin for late arrivals. A late retry after the resource was deleted still gets the original response, following the "principle of least astonishment" (Featonby). |
| **Google APIs** | [AIP-155](https://google.aip.dev/155): an optional `string request_id` in UUID4 format. It "must guarantee idempotency". A duplicate "should return the response for the previously successful request"; retention is "any reasonable timeframe". |
| **Airbnb "Orpheus"** | An idempotency library. It splits each request into three phases: Pre-RPC (record the request in the DB), RPC (the network call), and Post-RPC (record the result and whether it is retryable). "No service interaction over networks in Pre and Post-RPC phases." Errors are classified: 5xx retryable, 4xx not. Row-lock "leases" with expiration longer than the RPC timeout. Reads and writes go to the primary (master) database. Keys can be request-level or entity-level (e.g. `payment-1234-refund`). |
| **Brandur / Rocket Rides** | Postgres `idempotency_keys` table (`locked_at`, `request_params`, `response_code`, `response_body`, `recovery_point`). "Atomic phases" sit between "foreign state mutations"; a "completer" process finishes abandoned requests; a "reaper" deletes old keys. |
| **Kafka** | Idempotent producer since 0.11: "the broker assigns each producer an ID and deduplicates messages using a sequence number" ([design docs](https://kafka.apache.org/documentation/#semantics)). Confluent adds that the sequence number is persisted in the replicated log, so it survives leader failover ([Confluent 2017](https://www.confluent.io/blog/exactly-once-semantics-are-possible-heres-how-apache-kafka-does-it/)). Transactions write consumer offsets and outputs atomically. For external sinks, store the offset "in the same place as its output". Enabled by default since 3.0 per KIP-679, fully effective from 3.2 after a config-validation bug fix (KAFKA-13598). **(Only moderately verified:** from the KIP and Jira search results.) |
| **Amazon SQS FIFO** | `MessageDeduplicationId`, or content-based deduplication using SHA-256 of the body. No duplicates from `SendMessage` retries "within the 5-minute deduplication interval" ([docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/FIFO-queues-exactly-once-processing.html)). On the consumer side delivery is still at-least-once: a message not deleted before the visibility timeout reappears ([docs](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)). |
| **TCP** | Sequence numbers for reordering and duplicate removal *within one connection* (DDIA Ch. 12; Kleppmann §2.3). |
| **Cedar RPC** (Birrell & Nelson 1984) | Call ID of [machine, process, sequence]; the callee keeps a last-sequence table; at-most-once semantics. |
| **DCE RPC, Go RPC** | DCE defaults to at-most-once, and procedures can be marked idempotent in the IDL (Tanenbaum §4.x). Go RPC "never re-sends a request" (MIT 6.5840). |
| **NFS** | Older versions used a duplicate-request cache keyed on the ONC RPC XID, with LRU eviction. NFSv4.1 sessions provide EOS through a bounded slot table and a sequence ID per slot, enforced even for idempotent requests ([RFC 8881 §2.10.6](https://www.rfc-editor.org/rfc/rfc8881.html#section-2.10.6)). The usual 1989 citation for the NFS duplicate-request cache is Juszczak, USENIX. **(uncertain: not verified)** |
| **gRPC** | Retry policy with `maxAttempts` ≤ 5; hedging only for methods that are safe to repeat; retry throttling on the failure ratio. Transparent retries happen only when the request "has never been seen by the server application logic". "gRPC retries do not provide a mechanism to specifically mark a method as idempotent" ([gRFC A6](https://github.com/grpc/proposal/blob/master/A6-client-retries.md)). |
| **Web browsers** | The "Are you sure you want to submit this form again?" prompt. Post/Redirect/Get avoids it in normal use, but not when the POST times out (DDIA Ch. 12). |

---

## 9. Claims that are commonly overstated or subtly wrong

- **"Exactly-once is impossible"** and **"exactly-once is solved"** are both overstated. The precise statement:
  - Exactly-once *delivery*, or client-only exactly-once, is impossible under message loss and crashes.
  - Exactly-once *effect* is achievable when a durable, atomically committed deduplication record exists, retries continue long enough, and the effect stays inside the deduplication boundary.
  - Kafka's own docs warn that many "exactly-once" claims "don't translate to the case where consumers or producers can fail".
- **"Two Generals proves you can't have exactly-once."** This conflates two problems. Two Generals concerns *simultaneous agreement* (common knowledge) with a finite protocol. Kleppmann notes the payment case "does not exactly match". The direct argument for request semantics is indistinguishability plus server crashes (Tanenbaum Fig. 8.19). Treat (2015) also invokes FLP; FLP is about consensus with crash failures in asynchronous systems, and it is not needed to make this point.
- **"Idempotent means f(f(x)) = f(x), so retries are safe."** The property is about repeating one operation *in isolation*. It fails under interleaving (R4) and with delayed duplicates. It also fails if the key record and the effect are not atomic.
- **"Retries at three layers means 3³ times the load."** Watch retries versus attempts. SRE: 3 retries = 4 attempts, so 4³ = 64. AWS says "three retries at each layer" but computes with "first three tries, then nine tries", i.e. 3 attempts per layer, giving 3⁵ = 243. With 3 *retries* the 5-layer figure would be 4⁵ = 1,024.
- **"Exponential backoff solves thundering herds."** Without jitter, the calls still cluster. Jitter reduces work but does not change the N² nature of contention (Brooker 2015).
- **"Retrying makes failure probability pⁿ."** Only if failures are independent. Under overload they are correlated, and retries add load.
- **"Kafka gives exactly-once."** Only within Kafka read-process-write, or Streams. Confluent: if a Streams app makes an RPC to update a remote store, "the resulting side effects would not be guaranteed exactly once".
- **"SQS FIFO is exactly-once processing."** The documented guarantee is deduplication of *sends* within 5 minutes. Consumers still see redelivery after a visibility timeout, so consumers must be idempotent.
- **"Stripe idempotency makes any retry safe."** It needs the same parameters and the 24 h window. Requests that are rate-limited or fail validation are not cached. Replayed 500s remain indeterminate.
- **"HTTP says POST must never be retried."** RFC 9110 says a client SHOULD NOT *automatically* retry a non-idempotent request *unless* it knows the semantics are idempotent or can detect the request was never applied. An idempotency key provides exactly that.
- **"Idempotency-Key is an HTTP standard."** It is a widely implemented convention. The IETF draft expired in April 2026.

---

## 10. Animation, doing, or reading

The canonical sources teach this material through sequence diagrams: Kleppmann's slides, DDIA Fig. 8-1, Tanenbaum Figs. 8.18–8.19. They teach it through labs with lossy networks (MIT 6.5840 Lab 2) and through simulators (Brooker's backoff simulator). The split below is my recommendation based on that.

**Narrated animation.** These are ideas about timing and hidden state, where a split screen of "what the client sees" versus "what actually happened" carries the insight.
- The three failure cases collapsing into one identical "timeout" from the client's side.
- The double charge.
- The idempotency-key flow: first request, then retry after completion (replayed response), then a concurrent retry (409), then the same key with a different payload (422).
- Why the key must be written in the same transaction as the charge: an animated crash between the two writes.
- A thundering herd versus jittered retries on a time axis.

**Doing: an interactive simulation, running code, or an exercise.** These parts involve rare interleavings and probabilities that learners only believe once they have seen the frequencies.
- **Tanenbaum's crash game:** pick a client and a server strategy, inject crashes, and tally OK, DUP and ZERO.
- **A lossy-network slider:** vary request and reply loss and the timeout percentile, and watch the duplicate rate track *b* and the attempts per request grow. This tests p, pⁿ and aᴸ intuitions.
- **Coding:** implement idempotency-key middleware. First use check-then-insert and break it with concurrent requests, then fix it with a `UNIQUE` constraint in the same transaction.
- **Backoff:** a full-jitter versus no-jitter simulation, as in the AWS simulator.
- **MIT-style exercise:** versioned `Put`, where the learner must discover the `ErrMaybe` case.

**Reading.** These parts need precise wording or are reference material.
- The RFC 9110 definition and its retry rules.
- The terminology table (Coulouris Fig. 5.9 and Spector's table).
- The list of preconditions for exactly-once effect (R3).
- Provider-specific parameters (24 h, 64 characters, 5 minutes, status codes).
- Edge cases such as late-arriving requests and key retention.
- The scope caveats for Kafka and SQS.

---

## Items I could not verify

- The exact wording of Coulouris' definition of idempotence and its set-versus-sequence example. Only Fig. 5.9 was verified.
- Whether Tanenbaum's 2nd ed. (2007) framed the crash example as a print server, and its figure number. The 3rd-ed. text is about document processing but still says "text printed".
- The English chapter title of DDIA 2nd-ed. Ch. 13; its content was verified through the translation.
- The content of Akkoyunlu et al. 1975 (only the bibliographic record was verified), and the Juszczak 1989 NFS citation.
- PayPal's retention periods.
- Details of Hohpe & Woolf's pattern beyond its problem and solution statements.
- The Kafka idempotence default version history (3.0 versus 3.2), which comes from secondary search results about KIP-679 and KAFKA-13598.
