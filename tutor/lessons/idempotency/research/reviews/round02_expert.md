## Review

**Overall**: The script's core argument (Two-Generals-style ambiguity → at-most-once/at-least-once → idempotent handling → idempotency keys) is sound, matches the cited sources, and the arithmetic checks out. One on-screen numeric claim is factually wrong for the exact system (Stripe) the script invokes, and a couple of precision/caveat issues are worth tightening.

### BLOCKING

**Quote:** *"the same key with '$50' then '$80': the second is rejected ('422: key reused with a different request')"* (Section 6, screen direction)

**What's wrong:** I checked Stripe's own API error reference (`docs.stripe.com/error-low-level`, "HTTP Status Code Reference") — it lists only `200, 400, 401, 402, 403, 409, 424, 429, 500/502/503/504`. There is no `422` anywhere in Stripe's status vocabulary. A mismatched-parameters idempotency error at Stripe is a content error, returned as `400`, not `422`. `422` is the number proposed in the IETF draft (`draft-ietf-httpapi-idempotency-key-header`) — a document the video never mentions — not what the running example (Stripe's own `Idempotency-Key` header, invoked one section earlier as "Payment APIs such as Stripe's work this way") actually does. As written, a viewer who tries this against Stripe will get a different code than the video taught, which is exactly the kind of checkable, wrong specific claim that undermines the video's credibility.

**Fix:** Either drop the numeral and just show the rejection ("`400: idempotency key reused with a different request`" if you want to stay accurate to Stripe), or if you want to keep "422," explicitly attribute it to the IETF draft rather than presenting it as what happens in the Stripe-flavored example (e.g., a caption "422 (per the IETF idempotency-key draft; Stripe returns 400 for this case)").

### SHOULD FIX

**Quote:** *"So no protocol over an unreliable network can promise that a request is carried out exactly once."* (Section 2)

**What's wrong:** "Carried out" is ambiguous between "delivered" (the message reaches the server once) and "takes effect" (the charge happens once). The impossibility result (Two Generals) is about the former; the video's whole point in Section 7 is that the latter *is* achievable via idempotent handling. Left as "carried out," a sharp viewer can read Section 2 as contradicting Section 7's "charged exactly once." Section 7 itself gets this right ("the network can't *deliver* a request exactly once") — Section 2 should use the same word.

**Fix:** "So no protocol over an unreliable network can promise that a request is *delivered* exactly once." (Keep "carried out" only for the effect-level claim in Section 7, where it's earned.)

---

**Quote:** *"The server marks the key as in progress, and turns the retry away with 'still in progress, try again'"* (Section 6, point 2)

**What's wrong:** This is the crux of the concurrency safety argument, but it skips the one detail that makes it actually correct: the check "does this key already exist" and the act of marking it "in progress" must themselves be a single atomic operation (e.g., an INSERT under a unique constraint / compare-and-set), or two simultaneous first attempts can both see "no key yet" and both proceed to charge. Point 1 explicitly calls out atomicity ("it saves them in one transaction"); point 2 doesn't, even though it's the same requirement applied to the read-then-write of the key itself. This is exactly what Helland's paper (already in your references) discusses under "check-and-set."

**Fix:** Add one clause: "...the server marks the key as in progress — checking and marking done as one atomic step, so two simultaneous first attempts can't both slip through — and turns the retry away..."

### NIT

- Section 2's four-way failure enumeration (lost request / still working / crashed / reply lost) is a compressed subset of Kleppmann's six-case list in DDIA ch. 8 (it also separately distinguishes "temporarily unresponsive but will resume" and "response delayed vs. lost"). Fine as a simplification for a 2-minute video, but if you want to be exact, call it "these are among the ways..." rather than implying it's exhaustive.
- Section 4: "'Delete order seven' is idempotent too. The second time, there's nothing left to delete." — true of the *effect*, but per RFC 9110's own note, the two responses needn't be identical (e.g., 200 vs. 404) even though server state converges. Not worth belaboring on screen, but if a caption ever states response codes match, that would need this caveat.
- The end card cites Two Generals nowhere, even though the argument in Section 2 is exactly the Two Generals Problem and it's in your evidence table. Consider adding "(cf. the Two Generals Problem)" to the references — free canonicity credit, no script change needed.

VERDICT: REVISE
