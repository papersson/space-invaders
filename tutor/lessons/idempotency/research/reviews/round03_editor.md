# Script Review

## 1. Opening question / ending callback
**Pass.** Opens on "what should the client do?" after the $50 timeout; closes with "the client should retry, with the same idempotency key" and the screen direction explicitly replays the chapter-1 scene (timeout → retry → one charge). Clean callback.

## 2. Chain (but/therefore/and then)
1. Timeout on $50 charge — retry or not?
2. **But** three failures look identical, and asking again risks the same loss. **Therefore** no protocol guarantees exactly-once delivery.
3. **Therefore** choose at-most-once (may lose) or at-least-once (may duplicate); a payment can't be lost, so retry. **Therefore** the server must neutralize repeats.
4. **Therefore** idempotence: some ops are naturally safe to repeat; a charge isn't.
5. **Therefore** the idempotency key: same key every attempt, charge once per key, replay the saved result.
6. **But** it only works if a crash can't split charge-from-record, a concurrent retry can't sneak in, and a key can't be reused for a different payment.
7. **Therefore** retry + idempotent handling = exactly one charge.

No "**and then**" anywhere — the whole thing is causal, not a list of events. This is a strength; flag nothing here.

## 3. Announced vs. derived ideas
Mostly derived. One soft spot:
- **NIT** — "An operation is idempotent if doing it any number of times has the same effect as doing it once." This is handed to the viewer as a definition rather than surfaced from the problem just stated ("the server has to make a repeated request harmless" → *how?*). It's earned by the preceding line, so this is minor, not a real violation — see also Test 7.

## 4. Setups/payoffs
All major setups pay off: UUID → collision improbability; one DB transaction → both-or-neither; card-network call → server sends its own idempotency key (nice recursive echo); check-and-mark → race turned away; key-scoped-to-payment → mismatched retry rejected.

- **NIT** — Payoff without setup: the screen-only aside "in HTTP, PUT and DELETE are meant to be idempotent; POST is not" arrives with no narrated setup and nothing later depends on it. It's inert trivia riding on the idempotence beat.

## 5. Terms defined before use / duplicate naming
Idempotent, at-most-once, at-least-once, idempotency key — all defined before use. One inconsistency:
- **SHOULD FIX** — The payment record is called "the saved result" in narration (twice: section 5 and section 6) but shown on screen as "receipt #1042" / "receipt returned." Two names for one concept. 
  **Rewrite:** either say "saves a receipt under that key" in the section 5 narration to match the screen, or relabel the screen artifact "saved result: charged" to match the narration. Pick one term and use it in both channels.

## 6. Numbers
All numbers: $50, "a few seconds," $100 (doubled charge), UUID "7f3a…c91," "receipt #1042," 5 ms, $80, plus end-card citation years.

**Worth remembering:** $50 (the running example) and $100 (the visual proof of what a duplicate charge looks like). Everything else is disposable.

- **NIT** — "receipt #1042" does no work; it's flavor, not information. Fine to keep as texture but don't expect anyone to retain it (they won't, and shouldn't).
- **NIT** — "5 ms apart" is precise but arbitrary; "milliseconds apart" would communicate "concurrent" just as well without implying the exact gap matters.

## 7. Abstraction before the concrete case
- **SHOULD FIX** — Section 4 states the idempotence definition first, then gives three examples. Given the rest of the script's discipline (three failure modes *shown* before the "no protocol" conclusion in section 2), this section breaks the pattern.
  **Rewrite:** Lead with the address/delete/charge trio, then land the definition: *"Set the shipping address to this" — do it twice, address is the same. "Delete order seven" — do it twice, still gone. "Charge fifty dollars" — do it twice, charged twice. The first two don't care how many times you do them. That's called idempotent: doing it any number of times has the same effect as doing it once. A charge isn't idempotent, so it has to be made safe to repeat.*

## 8. Wrong intuition — confronted and shown failing
Wrong model: "timeout = failure, safe to retry" / "exactly-once is something the network/library gives you." Both are directly dismantled: section 2's three-indistinguishable-outcomes argument kills the first ("the charge went through, and the reply was lost" looks identical to "nothing happened"), and the recursive confirmation-message regress ("whoever sends the last message never knows it arrived") kills the second by demonstration, not assertion. **Pass.**

## 9. Named but not understood
- **SHOULD FIX** — "in HTTP, PUT and DELETE are meant to be idempotent; POST is not" (screen-only). It names a real-world mapping but never explains *why* PUT/DELETE qualify, so a viewer who doesn't already know HTTP gets a label with no mechanism. Either cut it (see Test 11) or give it one clause: *"PUT replaces a resource wholesale — same effect every time — which is why HTTP calls it idempotent by design."*
- Stripe mention is fine — it's grounded with the concrete header name, not just name-dropped.

## 10. On-screen text vs. narration; pictures vs. line
- **NIT** — End card: "at least once delivery + idempotent handling = charged exactly once" is a near-verbatim restatement of the final narration line. That's acceptable as a takeaway card (it's meant to be the one thing that lingers after the video ends), but if the intent was for the *visual replay* to carry the payoff, the redundant text competes with it.
  **Rewrite (optional):** drop to just "at-least-once + idempotent = exactly once" (shorter, functions as a formula/memory aid rather than a restated sentence).
- No pictures found that contradict or fail to support their line — the sequence diagrams, the two-lane comparison, and the key/table mechanics are all doing real explanatory work.

## 11. Deletable lines
- **NIT** — "Payment APIs such as Stripe's work this way. The client puts the key in a request header called Idempotency-Key." Doesn't advance the argument (the mechanism was already fully explained) — but it's the moment the video proves this isn't a toy abstraction, so I'd keep it despite it being technically prunable.
- **NIT** — The screen-only HTTP PUT/DELETE/POST note (see Tests 4 and 9) is the cleanest candidate for outright deletion — remove it or expand it; as written it neither pays off nor teaches.

## 12. Hard-to-say-aloud / pacing
- **SHOULD FIX** — "However many messages the client sends, it can't be certain." Grammatically fine on the page but easy to trip over aloud (dangling "it," ambiguous referent). 
  **Rewrite:** *"No matter how many messages go back and forth, someone is always left not knowing if the last one arrived."*
- **SHOULD FIX (pacing)** — Section 6's first sub-point is rushed relative to the rest of the script. It compresses three distinct ideas — transactional atomicity, *and* the recursive move of the server becoming its own idempotent client toward the card network — into four sentences, right after two sections (4 and 5) that gave comparably sized ideas much more room. The recursive-idempotency point is arguably the most conceptually interesting beat in the whole script (the pattern nests) and it goes by in one sentence: *"So the server does what the client did: it sends that call with an idempotency key of its own, and can safely repeat it."* 
  **Rewrite (give it a breath):** *"And charging the card usually means calling another company's payment network — another request, over another unreliable connection, with the exact same problem. So the server treats that call the same way the client treated its own: it attaches an idempotency key, and it's safe to retry."*

---

**VERDICT: PASS**
