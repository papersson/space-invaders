# Review

I checked every numerical, terminological, and citational claim against the standard sources (Kleppmann DDIA, RFC 9110, Stripe's docs, Helland). Overall the argument is sound and the delivery/effect distinction in the closing line is handled with real care. I found one item that must be fixed before this airs, plus several precision gaps.

---

**BLOCKING — internally inconsistent bound on duplicate charges**

> *Screen (§3):* "at least once: retry until a reply" with outcomes "**charged 1 or 2 times**"

"At-least-once," as the lane itself defines it ("retry *until* a reply arrives," i.e. an unbounded loop, not "retry once"), permits an arbitrary number of duplicate charges: if the server succeeds on attempts 1, 2, and 3 but only the reply to attempt 3 survives, the client has retried three times and the customer has been charged three times before the client ever sees a reply. Capping the outcome at "1 or 2" contradicts the lane's own description and misstates a formally named delivery semantic — a viewer who internalizes this will get the wrong answer the first time they reason about more than one retry. This is exactly the kind of error the idempotency-key mechanism in §5–6 exists to fix, so getting the "before" state's bound wrong undercuts the whole argument.

**Corrected wording:** change the outcome to "charged 1 or more times." (If you want to keep a clean "1 or 2" for the video's specific one-timeout-one-retry narrative, relabel the lane something like "at least once (this example: one retry)" and have the voiceover note that with repeated retries the count is unbounded — that's the more honest and more interesting fact anyway, since it's precisely why dedup can't be an afterthought.)

---

**SHOULD FIX — missing caveat: key reuse with mismatched request content**

> "When a retry arrives with the same key, the server doesn't charge again. It looks up the saved result and sends that back."

§6 lists two failure modes (non-atomic save, concurrent in-flight retry) but omits a third, equally standard one: a key gets reused for a *different* request (e.g. a client-side bug that recycles a key across two distinct payments, or reuses it after changing the amount). Without a check, the server would silently return the first payment's receipt for the second payment — a correctness hole, not just an edge case. Stripe's own API explicitly guards against this (a key reused with different parameters is rejected, not honored), so this isn't a hypothetical.

**Suggested addition:** a third bullet/beat in §6 — "the server also has to check that a repeated key arrives with the same request it saw the first time — otherwise a bug could hand back someone else's receipt" — with a corresponding screen beat (same key, different amount → rejected, not silently matched).

---

**SHOULD FIX — reference list is missing the now-standardized header**

The end card cites Stripe's proprietary docs as the source for the `Idempotency-Key` header while the narration calls this "the standard way." To my knowledge this has since been formalized by the IETF HTTPAPI working group as an RFC ("The Idempotency-Key HTTP Header Field") published in 2025, alongside RFC 9110's idempotent-methods section already cited. Since you're asked to check canonicity and the script leans on RFC 9110 for exactly this kind of authority, the header itself deserves the equivalent citation rather than only a vendor doc.

**Action:** verify the current RFC number (I'm recalling this from training data, not a live lookup) and add it to the reference card next to RFC 9110 §9.2.2.

---

**NIT — idempotence defined over "twice" rather than "any number of times"**

> "An operation is idempotent if doing it twice has the same effect as doing it once."

RFC 9110 §9.2.2 defines it over "multiple identical requests," not specifically two. Harmless for narration pacing, but if you want it exactly quotable: "...if doing it any number of times has the same effect as doing it once."

---

**NIT — "retry until a reply arrives" glosses over bounded retry in real systems**

Taken literally this is an infinite loop; real clients (including Stripe's own SDKs) retry a bounded number of times with backoff and then give up, at which point chapter 1's original dilemma (double charge vs. lost sale) actually resurfaces rather than being fully dissolved. A half-sentence caveat would keep the closing "exactly once" claim scoped honestly, though this is a polish item, not a correctness one, since the video's explicit scope is the mechanism, not production retry policy.

---

Everything else checks out: the three-way classification of timeout causes matches Kleppmann's treatment of unreliable networks, the Two-Generals-style argument for "no certainty" is sound (and correctly *not* overreached into "exactly-once delivery is what we're building" — the closing line's delivery/effect distinction is exactly right), the PUT/DELETE/POST idempotency claims match RFC 9110, the atomicity and in-flight-duplicate caveats in §6 are the two real ones from Helland/Stripe engineering practice, and all arithmetic ($50 → $100 on double charge) is correct.

VERDICT: REVISE
