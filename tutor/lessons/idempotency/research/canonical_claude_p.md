# Idempotency and Retries — Canonical Treatment

## 1. Canonical worked example

**Most common real-world example: the payment API idempotency key**, specifically Stripe's `Idempotency-Key` header on `POST /v1/charges` (docs.stripe.com/api/idempotent_requests). This is the example almost every system-design course, engineering blog, and interview guide reaches for, because payments make the stakes ("don't double-charge the customer") immediately intuitive and the mechanism (client-generated key → server dedup store) is simple to state. AWS (`ClientToken` on `RunInstances`, etc.) and PayPal (`PayPal-Request-Id`) are cited as the same pattern in other domains.

**Competing canonical example (theoretical foundation): the Two Generals' Problem** — two armies must coordinate an attack via messengers who may be captured, and no protocol can give both generals certainty that the other will attack. It's the standard proof that reliable, acknowledged delivery over an unreliable channel cannot be reduced to zero uncertainty. It appears in Tanenbaum & Van Steen's *Distributed Systems* and is invoked in Kleppmann's *DDIA* (Ch. 8, "Unreliable Networks") to justify why a client can't know if its request succeeded after a timeout.

The Stripe-style example is the standard *practical* one; Two Generals is the standard *theoretical* one for "why exactly-once is impossible." Most treatments use both, in that order.

## 2. Standard progression

1. **Networks are unreliable and asymmetric-failure-prone**: a timeout doesn't tell you whether the request was lost, the response was lost, or the server is just slow (Kleppmann, *DDIA*, Ch. 8, "Unreliable Networks").
2. **Two Generals' Problem** as the formal reason no finite protocol eliminates this uncertainty.
3. **Delivery semantics taxonomy**: at-most-once (no retry, may lose messages) → at-least-once (retry until ack, may duplicate) → exactly-once (the unachievable ideal at the transport layer). Standard in messaging-systems literature (JMS spec, Kafka docs, DDIA Ch. 11).
4. **Show the failure mode concretely**: retry a non-idempotent operation (e.g., "charge the card again") → duplicate effect.
5. **Idempotence as the fix**, introduced first as a mathematical property, then applied to HTTP methods (RFC 9110 §9.2.2).
6. **Idempotency keys** as the mechanism for making an inherently non-idempotent operation (like creating a charge) safe to retry.
7. **Deeper implementation concerns**: atomic check-and-set on the server, storing the *response* alongside the key, key TTL/expiry, and race conditions between concurrent duplicate requests.
8. **(Optional, advanced) exactly-once in streaming systems**: Kafka's idempotent producer and transactions, framed as "at-least-once delivery + idempotent/transactional processing = effectively-once" (Confluent, "Exactly-once Semantics are Possible: Here's How Kafka Does It," Narkhede/Gustafson, 2017).

The simpler version always shown first is "retry causes duplication" with a single client and server; the full version adds concurrent retries, server crashes between side-effect and dedup-record write, and distributed/streaming exactly-once.

## 3. Model and notation

- **Delivery semantics** (informal taxonomy, not a formal parametrized model): *at-most-once*, *at-least-once*, *exactly-once*. Used across DDIA, Kafka docs, JMS/AMQP specs.
- **Idempotence (math origin)**: an operation *f* is idempotent if `f(f(x)) = f(x)` — borrowed from algebra (idempotent elements of a monoid/ring, e.g. idempotent matrices `A² = A`).
- **HTTP terminology (RFC 9110 §9.2, formerly RFC 7231 §4.2)**:
  - *Safe* methods (no intended state change): GET, HEAD, OPTIONS.
  - *Idempotent* methods (repeating has the same effect as doing it once): all safe methods, plus PUT and DELETE.
  - POST and PATCH are neither safe nor idempotent by default.
  - Important nuance in the spec: idempotence is about the *effect on server state*, not about the response being byte-identical (a second DELETE can legitimately return 404 instead of 200).
- **Idempotency-key model**: client generates a unique key (typically a UUID) per logical operation attempt; server keeps a durable store mapping `key → (status, stored response)`; first request executes the operation and persists the record; retries with the same key return the stored result instead of re-executing.
- **Pattern names in the literature**: "Idempotent Receiver" (Hohpe & Woolf, *Enterprise Integration Patterns*, 2003) and "Idempotent Consumer" (Chris Richardson, *Microservices Patterns*, 2018 / microservices.io) are the standard pattern-catalog names for the same server-side dedup mechanism, mostly used in messaging/microservices contexts rather than plain REST API contexts.

## 4. Key results and formulas

There's no single closed-form "theorem" here (this is a systems-design topic, not a probability-heavy one), but two formal/semi-formal results recur:

- **Two Generals' Problem impossibility result**: no finite protocol over a channel where messages can be lost can give both parties common knowledge that an action will occur. Proof is by contradiction on the last message in any hypothetical finite protocol. Holds for *any* unbounded-loss, unbounded-delay channel; it stops applying once you assume synchronous, bounded-delay, non-lossy channels (rarely true in practice).
- **Effectively-once equivalence**: `at-least-once delivery + idempotent processing ≈ exactly-once effect` (stated explicitly in DDIA Ch. 11 "Idempotence," and in the Kafka exactly-once literature). This holds only if (a) the idempotency check-and-set is atomic/durable with respect to the side effect, and (b) all downstream side effects triggered by the operation are also idempotent or covered by the same transaction — it breaks down the moment either fails.
- **Exponential backoff with jitter** (the standard retry-timing formula, Marc Brooker, AWS Architecture Blog, "Exponential Backoff and Jitter," 2015):
  `backoff = min(cap, base * 2^attempt)`, then "full jitter": `sleep = random(0, backoff)`.
  This is the canonical formula for spacing retries to avoid synchronized retry storms; assumes independent clients (ties to the audience's "independent events" background).

## 5. Standard numeric examples

This topic is mechanism-heavy rather than numeric-example-heavy, but the canonical sources do give concrete numbers:

- Stripe's docs describe idempotency keys as valid for a bounded retention window before being recycled (commonly cited as **24 hours**, per docs.stripe.com — *flag: exact current value should be verified against live docs, as vendor docs change*).
- Marc Brooker's AWS backoff-and-jitter post includes simulated request-volume charts comparing "no jitter," "equal jitter," and "full jitter" strategies under contention — the standard illustration that jitter reduces total retry load, using concrete simulated request counts over time.
- Kafka's idempotent producer uses a **producer ID (PID) + per-partition sequence number** so the broker can detect and drop duplicate writes — not really a "numeric example" in the pedagogical sense, but the standard concrete mechanism cited (KIP-98).

## 6. Misconceptions and how the canon corrects them

| Misconception | Canonical correction |
|---|---|
| "Exactly-once delivery" is achievable over the network | Provably impossible (Two Generals); what's achievable is *effectively-once* via at-least-once delivery + idempotent processing (DDIA Ch. 11; Kafka literature explicitly hedges its "exactly-once semantics" marketing this way). |
| Idempotent = "returns the same response every time" | RFC 9110 defines it in terms of *server-side effect*, not response equality — a second DELETE can 404 while still being idempotent. |
| GET/PUT/DELETE are "automatically" idempotent because the spec says so | The spec states an *intended contract*; the server must actually implement it that way. Buggy PUT handlers that append instead of replace violate it. |
| Retrying with the same idempotency key is by itself sufficient | Concurrent duplicate requests racing before the first one has stored its result is a classic bug — the server needs an atomic check-and-set (e.g., a DB unique constraint), per Pat Helland, "Idempotence Is Not a Medical Condition," *ACM Queue* 10(4), 2012. |
| Idempotency keys make the whole system exactly-once | They only make the *operation* idempotent; a crash between executing the side effect and persisting the dedup record, or non-idempotent downstream calls made from inside the handler, still break it. |

## 7. For a short lesson

**Essential**: unreliable networks → ambiguous timeouts → retries are necessary but cause duplicates for non-idempotent operations → definition of idempotence → idempotency-key mechanism → the Stripe/payment example end to end.

**Common extra** (include if time allows): the HTTP safe-vs-idempotent method table; exponential backoff with jitter.

**Leave out**: the formal Two Generals proof (state the conclusion, skip the induction argument); Kafka transactional internals (sequence numbers, epochs, producer fencing); distributed consensus (Paxos/Raft) — it's adjacent but not required to explain idempotency.

## 8. Real systems canonically cited

- **Stripe API** — `Idempotency-Key` header on charge/payment creation endpoints; server-side dedup store keyed by the header value (Stripe docs).
- **PayPal API** — `PayPal-Request-Id` header, same pattern.
- **AWS APIs** — `ClientToken` parameters (EC2 `RunInstances`, etc.); AWS Lambda Powertools "idempotency" utility for at-least-once event sources (SQS, Kinesis).
- **Apache Kafka** — idempotent producer (PID + per-partition sequence number, KIP-98/101) to dedupe on the broker; transactional API layered on top for exactly-once stream processing (Confluent engineering blog, 2017).
- **TCP** — sequence numbers used to detect and discard duplicate segments, often used as the lower-layer analogy in DDIA's discussion.
- **HTTP infrastructure** (browsers, load balancers) — will auto-retry idempotent methods (GET) on failure but not POST, a direct consequence of the RFC classification.

## 9. Overstated or subtly wrong claims

- "Exactly-once delivery is impossible, full stop" overstates it slightly — delivery is impossible to guarantee exactly-once, but *processing effect* can be made exactly-once via idempotency; conflating the two is the single most common confusion in the field, and it's exactly why Kafka's "exactly-once semantics" phrase is controversial among practitioners.
- "Idempotent operations require no extra server logic" — false for business operations like charging a card; idempotence there is *engineered* via a dedup store, not free.
- "Idempotency keys guarantee no duplicate side effects under all failure modes" — false if the dedup-record write and the side effect aren't atomic, or if downstream calls made inside the handler aren't themselves idempotent.
- "PUT is always idempotent in practice" — the spec describes intended semantics; real APIs sometimes violate it (e.g., a PUT that also fires a notification on each call).

## 10. Best learning modality per part

- **Narrated animation**: message-timing diagrams (request/response/ack loss scenarios causing ambiguity), the Two Generals' Problem narrative, and the idempotency-key check-and-set sequence — these are fundamentally about *timing and message flow*, which animation conveys far better than text.
- **Hands-on / interactive**: simulate packet loss and retries against a toy payment endpoint, watch duplicate charges occur, then add an idempotency-key middleware and watch it get fixed; a race-condition exercise (two concurrent identical requests) makes the "needs atomic check-and-set" lesson concrete in a way reading can't.
- **Reading**: exact definitions (RFC 9110 §9.2), the real header/TTL details of Stripe/AWS/PayPal APIs, Pat Helland's paper, and DDIA's chapters for the deeper conceptual scaffolding — these are precise, referenceable technical facts better absorbed as text than narration.
