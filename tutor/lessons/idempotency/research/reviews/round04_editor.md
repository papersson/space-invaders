# Script Review — "Charged Twice"

Overall this is a strong, tightly-argued script: the causal chain holds without a single filler "and then," the ending replays the opening scene, and every objective is actually covered. Findings below are mostly polish; nothing breaks the argument, so this is a REVISE-for-polish, not a structural rewrite.

## 1. Opening question / ending callback
**Pass.** Opening: "Did the charge go through?... So what should the client do?" over "charged? 0 times? 1? 2?". Ending: "the client should retry, with the same idempotency key" over "the chapter 1 scene replayed: timeout → retry with the same key → one charge, receipt returned." Direct, literal callback — no note needed.

## 2. One-sentence chain, report every "and then"
1. A $50 charge times out — retry or not?
2. **But** three different failures look identical to the client, and asking again crosses the same network, **therefore** no protocol guarantees exactly-once delivery.
3. **Therefore** the client must choose at-most-once (may lose) or at-least-once (may duplicate); a payment can't be lost, so it retries, **therefore** the server must absorb repeats.
4. **Therefore** some operations are naturally idempotent, **but** a charge isn't, so it must be made so.
5. **Therefore** attach an idempotency key to every attempt; the server charges once per key and replays the saved result.
6. **But** this only holds if the charge and its saved result can't be split by a crash, a concurrent retry is turned away, and a key is never reused for a different payment.
7. **Therefore**: retry with the same key — at-least-once + idempotent handling = exactly one charge.

**"And then" count: zero.** Every joint is causal. Nothing to fix here.

## 3. Ideas announced vs. derived
- **SHOULD FIX** — "A few details decide whether this works." (opening of §6). This announces three fixes as a checklist rather than letting each failure surface first. The screen direction *does* show the crash-before-save failure, but the narration states the rule before the reader feels the break.
  - Rewrite: *"Suppose the charge succeeds, then the server crashes before it saves the result. The retry arrives, finds nothing under the key, and charges again. So the charge and the saved result can't be allowed to come apart —"* then proceed to the transaction fix.
- **NIT** — "The standard way is an idempotency key." This names the mechanism before deriving why a *key* (vs. some other dedup scheme) is the natural fix. One clause would ground it: *"...since the server needs some way to tell 'this is the same attempt as before' from 'this is a new charge.'"*

## 4. Setups without payoffs / payoffs without setups
- **SHOULD FIX** — On-screen note: *"in HTTP, PUT and DELETE are meant to be idempotent; POST is not."* Never voiced, never connected back to why a payment `POST` needs a key while `PUT`/`DELETE` don't. It's a dangling fact.
  - Rewrite (fold into §4 narration): *"...which is why HTTP builds this in for some methods — PUT and DELETE are supposed to be idempotent — but not for POST, which is what a charge request is."*
- **Worth flagging, not fixing**: the Two Generals Problem is the exact argument in §2 (the regress of unconfirmable acks) but is only named in the end-card references, never in narration. Reasonable as an Easter egg for further reading, but consider naming it once at the point of use (see §8 below) so the citation isn't orphaned.

## 5. Terms used before explained / concepts with two names
- **SHOULD FIX** — "This is often called effectively-once processing" arrives in the very last lines, after the takeaway is already delivered. It reads as a *new* concept when it's just a synonym for what was just said, risking a "wait, is there more?" beat right at the close.
  - Rewrite: either cut it, or move the naming earlier and mark it explicitly as a label: *"People call this effectively-once processing — not exactly-once delivery, which is impossible, but an exactly-once effect, which isn't."*
- No other unexplained-before-use terms; "idempotent," "idempotency key," "at-most/least-once" are all defined at first use.

## 6. Numbers
Full list: $50 (charge amount), "0? 1? 2?" (charge-count stakes), "a few seconds" (timeout), $50→$100 (duplicate-charge illustration), 7f3a…c91 (example key, reused consistently — good continuity), receipt #1042 (reused — good), 5 ms (race window), $80 (mismatched-amount reuse example), citation years (backmatter only).

**Worth remembering: $50** (the anchor case) and **0 / 1 / 2** (the charge-count question the whole video resolves down to exactly 1).

- **NIT** — the $50→$100 duplicate-charge screen direction is ambiguous: it could read as "the second charge was for $100" rather than "two $50 charges, now totaling $100."
  - Rewrite: label it explicitly — *"$50 charged. $50 charged again. Total: $100."*
- "5 ms" and "a few seconds" do no independent work beyond "concurrently" / "eventually" — fine as flavor, not worth trimming.

## 7. Abstraction before the concrete case
- **SHOULD FIX** — §4 opens with the general definition ("An operation is idempotent if doing it any number of times has the same effect as doing it once") *before* any example. This is the clearest abstraction-first moment in the script.
  - Rewrite: *"Set the shipping address to this — do it twice, nothing changes. Delete order seven — do it twice, it's just already gone. Charge fifty dollars — do it twice, and the card is charged twice. The first two have a name: idempotent. Doing them any number of times has the same effect as doing them once."*
- §5's "The standard way is an idempotency key" is a milder version of the same pattern (name before walkthrough) — acceptable given the immediate concrete trace that follows.

## 8. Wrong intuition — confronted, and shown failing?
Two wrong beliefs per the brief:
- *"Timeout means the request failed"* — **shown failing** concretely: diagram (c), charge succeeds, only the reply is lost. Solid.
- *"Exactly-once delivery is something a protocol/library can give you"* — **refuted by argument, never voiced as a belief.** The regress ("every confirmation is another message that can be lost") is correct and is visually backed by the crossed-out "did it work?" message, but the script never states the misconception aloud before knocking it down, so a viewer who holds this belief may not recognize it's being addressed.
  - **SHOULD FIX rewrite** (insert before the regress): *"You might think: just make the protocol smarter — have it ask 'did it work?' and wait for a real answer. But that question can get lost too—"*

## 9. Examples named but not understood
- The HTTP PUT/DELETE/POST aside (already flagged in #4/#9) is the one true instance — named, not woven in.
- Stripe and "Idempotency-Key" header are named *and* functionally understood (the header matches exactly what's just been taught) — fine, not a violation.
- UUID is named only as flavor for "long random ID" — acceptable, not load-bearing.

## 10. On-screen text vs. narration / picture-line mismatch
- **NIT** — §7's on-screen equation ("at least once delivery + idempotent handling = charged exactly once") closely restates the narration's closing sentence. Acceptable as a deliberate "screenshot-this" summary card, but flagging in case that wasn't the intent.
- **SHOULD FIX** — the HTTP methods on-screen note (again) introduces unvoiced new information competing with the narration's own examples for attention — either voice it or cut it.

## 11. Lines deletable without breaking anything
- "This is often called effectively-once processing..." — deletable; the takeaway sentence immediately before it already lands the point.
- On-screen-only HTTP PUT/DELETE/POST note — deletable (or should be promoted into narration; see above).

## 12. Hard-to-follow-aloud sentences / rushed or padded beats
- **SHOULD FIX** — *"Every confirmation is another message that can be lost, so whoever sends the last message never knows it arrived. However many messages the client sends, it can't be certain."* This is the single most important inferential step in the video (it's what makes Objective 1 land — *why*, not just *that*, the client can't know) and it's also the densest, most abstract sentence in the script, with no concrete count to hang onto.
  - Rewrite: *"Say the client asks 'did it work?' The answer can get lost too. It could ask again — that answer can get lost too. There's no message in the chain that's guaranteed to arrive, no matter how many the client sends."*
- §6 is the densest section per minute (atomic transaction, concurrent-retry lock, key-scope check, plus a nested aside about the server's own idempotent call to the card network) — not padded, but worth a beat of breathing room, e.g., a half-second pause title card between the three sub-points, given each is a distinct real mechanism.
- No padding found elsewhere; pacing (~150 wpm target) otherwise matches the argument's density.

---

### Summary of severities
- **BLOCKING:** none.
- **SHOULD FIX (7):** §6 checklist framing; HTTP PUT/DELETE/POST orphaned aside (×2 instances — narration + on-screen); "effectively-once processing" introduced too late; §4 definition-before-examples ordering; wrong intuition #2 never voiced before refutation; the regress sentence in §2 is under-illustrated for its importance.
- **NIT (4):** idempotency-key introduction as "the standard way"; $50→$100 screen ambiguity; §7 on-screen equation redundancy; minor double-negative phrasing in §6 point 1.

VERDICT: PASS
