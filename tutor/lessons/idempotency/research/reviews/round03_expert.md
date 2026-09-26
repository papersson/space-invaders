# Review

I read this as a domain expert would — checking every claim against the standard sources (Kleppmann, RFC 9110, Stripe docs, Helland, the Two Generals literature) and for internal logical consistency. The script is unusually careful for something this short: the failure-mode taxonomy in §2, the idempotence definition in §4, and the resolution in §7 (delivery vs. effect) are all textbook-accurate and correctly cited. I did not find anything that is factually wrong or non-canonical enough to block production. I did find precision gaps a professor would flag before signing off.

## Findings

**SHOULD FIX** — §3, quote: *"Or retry until a reply arrives. Nothing is lost, but whenever only a reply was lost, the request is carried out again."*
"Nothing is lost" is only true under the idealized definition of at-least-once delivery (retransmit indefinitely over a channel that isn't *permanently* broken). It's in tension with §1, where the client already gave up once ("a timeout"). A real client's retry budget is finite, so a permanently unreachable server still loses the sale. This is the standard idealization used in the literature (e.g., a "fair-loss link" model), so it's fine to use — but it should be flagged as an idealization, not stated flatly.
Fix: *"Or retry — keep resending until a reply arrives. As long as the client keeps trying, nothing is lost; but whenever only a reply was lost, the request is carried out again."*

**SHOULD FIX** — §7, quote: *"But delivering it at least once, to a server that makes repeats harmless, charges the customer exactly once."*
This is exactly the concept the literature calls **effectively-once semantics** (Kleppmann's own term, in ch. 11 — one of the two chapters already cited in the end card). The script proves the idea correctly but never names it, which weakens the tie back to the cited source and gives viewers nothing to search for afterward.
Fix: add the term, e.g. *"...charges the customer exactly once. This is sometimes called effectively-once processing: exactly-once delivery is impossible, exactly-once effect isn't."*

**NIT** — §5, quote: *"the retry gets the reply that was lost"*
Imprecise: the original lost packet is gone; the retry gets back an equivalent cached result, not "the" reply.
Fix: *"the retry gets back the same result that the lost reply would have carried."*

**NIT** — §6, quote: *"it sends that call with an idempotency key of its own, and can safely repeat it"*
This only holds if the downstream service also implements idempotency-key handling (true of Stripe, not guaranteed of an arbitrary "another company's service"). One clause would prevent over-generalizing a Stripe-specific pattern (the Rocket Rides parable, per the evidence table) into a universal guarantee.
Fix: *"...it sends that call with an idempotency key of its own — provided that service also honors one — and can safely repeat it."*

**NIT (optional)** — §5/§6, no quote — omission.
Stripe idempotency keys expire (currently 24h) and are scoped per-account; the script implies they're permanent. This is peripheral to the argument (which only needs the key to outlive one retry cycle after a timeout) and can reasonably be left out of a ~5-minute video, but worth a conscious decision rather than an oversight.

## What's correctly handled (no action needed, noted since it's easy to get wrong here)
- The idempotence definition and the PUT/DELETE-vs-POST note match RFC 9110 §9.2.2 exactly, including the subtle point that DELETE's *response* can differ (404 on retry) while the *state effect* stays idempotent.
- §2's argument for why exactly-once delivery is impossible is a genuinely correct proof sketch (uncertainty about the last message → any fixed retry policy can produce 0 or 2+ effective deliveries in some execution), not just a hand-wave citation of Two Generals.
- The Two Generals attribution (Akkoyunlu/Ekanadham/Huber 1975, named by Gray 1978) is the standard historical account, not a garbled version of it.
- The three-part fix in §6 (DB transaction for the local write; a forwarded idempotency key for the external call; atomic check-and-mark for concurrent retries; key-scoped-to-payload rejection) matches Helland (2012) and the Stripe/Brandur Leach "recovery points" pattern precisely, including correctly *not* claiming a single DB transaction can cover the external card-network call.
- All arithmetic/units check out ($50 → $100 on double charge, UUID collision reasoning, RFC/DDIA chapter and section numbers).

## Peripheral content
Nothing gets disproportionate screen time relative to the argument. Retry backoff policy and idempotency-key expiry are reasonably left out as implementation detail beyond this video's scope.

VERDICT: PASS
