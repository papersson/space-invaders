# Script Review

## 1. Opening question ↔ ending callback
**Pass.** Opening: "Did the charge go through? ... So what should the client do?" Ending explicitly replays the scene ("the chapter 1 scene replayed: timeout → retry with the same key → one charge, receipt returned") and answers in the same terms ("retry, with the same idempotency key... charges the customer exactly once"). Clean callback, both verbal and visual.

## 2. Chain test (but/therefore/and then)
Rebuilding the chain independently from the script's seven sections:

1. A $50 charge times out — did it happen? **But** three failure modes look identical and a follow-up question can be lost the same way, **therefore** no protocol can guarantee exactly-once delivery. **Therefore** the client must pick at-most-once (may lose the sale) or at-least-once (may duplicate the charge), and since losing a sale is worse, it retries, **therefore** the server must absorb repeats harmlessly. **Therefore** some operations are naturally repeat-safe (idempotent) but charging isn't one of them, **therefore** the client attaches an idempotency key and the server charges once per key, returning the saved result to repeats. **But** this only holds if the charge and its saved result can't be split by a crash, an in-flight retry is turned away rather than started twice, and a key can't be reused for a different amount, **therefore** the answer: retry with the same key — at-least-once delivery plus idempotent handling yields exactly-once effect.

**"and then" count: zero.** Every join is causal (but/therefore); nothing is glued on by mere sequence. This is a real strength — flag it as something to preserve, not fix.

## 3. Ideas announced vs. derived
- **SHOULD FIX** — *"The standard way is an idempotency key."* (Section 5 opener) — the mechanism is named before the problem forces it. Section 4 ends on "the charge has to be made safe to repeat," which motivates *that something* is needed but not *why a key specifically*. Rewrite: "So the server needs to tell 'this is the same payment I already handled' apart from 'this is a new one.' The client can hand it exactly that: an idempotency key."
- Everything else derives cleanly from the preceding beat (idempotence from "repeats must be harmless," the key's failure modes from "make it actually work").

## 4. Setups/payoffs
- No orphaned setups or payoffs found. The one borderline case — the on-screen-only note "*in HTTP, PUT and DELETE are meant to be idempotent; POST is not*" (Section 4) — is a payoff with no verbal setup and no later callback; see Test 9/10 below, it's really a comprehension issue more than a structural one.

## 5. Terms before explanation / duplicate naming
Clean. "idempotent," "at most/at least once," and "idempotency key" are each defined at first use. No concept acquires a second name later (the HTTP header "Idempotency-Key" matches the spoken term rather than introducing a synonym).

## 6. Numbers
All numbers: $50, "a few seconds," three failure modes, 0/1 (at-most-once), "1 or more" (at-least-once), order "seven," $50→$100 (coral), random key "7f3a…c91," "receipt #1042," "5 ms apart," $50 vs $80, HTTP 409, HTTP 422.

**Worth remembering:** $50 (the anchor case), the 0-or-1 vs. 1-or-more contrast (this *is* the whole delivery-semantics idea in miniature), and $50→$100 (the visceral cost of getting it wrong).

- **NIT** — "receipt #1042," "7f3a…c91," "5 ms apart," and the HTTP codes 409/422 do no independent work — the accompanying plain-English text already carries the meaning. Fine as production flavor, but don't expect a viewer to retain them; no rewrite needed, just don't quiz on them.

## 7. Abstraction before the concrete case
- **SHOULD FIX** — *"An operation is idempotent if doing it any number of times has the same effect as doing it once."* (Section 4, first line) — definition precedes any example. Rewrite: lead with "Setting the shipping address to the same value twice leaves it exactly where it was. Deleting order seven twice leaves it deleted once. There's a name for that: idempotent." Then generalize.
- **NIT** — same pattern in Section 5's "The standard way is an idempotency key" (see Test 3) — also an abstraction-first move, same fix resolves both.

## 8. Wrong intuition
Named implicitly: "a timeout means the request failed, so retrying is safe." **Shown failing** twice — verbally in the opening ("If it did and the client tries again, the customer pays twice") and visually in Section 4 ("card charged $50, then $100 in coral"). The second wrong model ("exactly-once is something the network/library gives you") is directly refuted by the Section 2 impossibility argument. Both handled well.

## 9. Named-but-not-understood examples
- **SHOULD FIX** — *"in HTTP, PUT and DELETE are meant to be idempotent; POST is not"* — on-screen only, never narrated or unpacked. A viewer who doesn't already know REST verbs gets three names and no mechanism. Either narrate one sentence tying it to the charge example ("This is why REST calls this operation a POST, not a PUT — it's not naturally repeatable") or cut it — it doesn't currently pay for its own confusion.
- Stripe reference is fine — it's attribution, not an example that needs unpacking.

## 10. On-screen text vs. narration / picture-line mismatch
- **NIT** — Section 3's on-screen labels ("at most once: never retry" / "at least once: retry until a reply") closely mirror the narration almost verbatim. Acceptable as a recap label, but consider trimming to just the outcome ("0 or 1 charges" / "1+ charges") so the screen adds information rather than transcribing speech.
- **NIT** — the closing card equation echoes the final line almost word-for-word. Standard for an end card; leave as is.
- No pictures found that contradict or fail to support their line.

## 11. Deletable lines
- **NIT** — *"Payment APIs such as Stripe's work this way. The client puts the key in a request header called Idempotency-Key."* (Section 5) — the argument doesn't need this to hold together; it's a credibility anchor. Worth keeping for grounding, but flagged per the test as removable without breaking the chain.
- Nothing else is deletable — every other line in the seven sections carries a link in the causal chain from Test 2.

## 12. Hard-to-follow-aloud / pacing
- **SHOULD FIX** — *"Every confirmation is another message that can be lost, so whoever sends the last message never knows it arrived. However many messages the client sends, it can't be certain."* (Section 2) — this is the general Two Generals argument compressed into two dense clauses, asked to land purely by ear right after three concrete scenarios. Rewrite for the ear: "And asking again doesn't fix it — that question can get lost too. You could ask about the answer to your question, but that can get lost as well. There's no message so far down the chain that its arrival is guaranteed."
- **NIT** — *"Nothing is lost, but whenever only a reply was lost, the request is carried out again."* (Section 3) — "whenever only a reply was lost" is an awkward aloud parse. Rewrite: "Nothing is lost — except that when just the reply goes missing, the request runs a second time."
- Section 6 packs three distinct failure modes (atomicity, in-flight races, key reuse) into one beat, but it's explicitly framed as an itemized "a few details" caveat section with matching numbered visuals, so the density reads as intentional, not rushed. No fix needed.

---

VERDICT: PASS
