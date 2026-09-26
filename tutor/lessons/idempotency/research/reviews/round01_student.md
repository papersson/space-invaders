Playing the role of the student reviewer, here's my pass through the script.

## (1) Where I'd lose the thread

- **"The server might still be working on it, or have crashed partway through."** — that's two different situations bundled into one sentence (still processing vs. actually dead). I had to stop and mentally split them apart, and the diagram doesn't distinguish them either — it's one box that "stalls or shows a crash."

- **"However many messages the client sends, it can never be certain. So no protocol over an unreliable network can promise that a request is carried out exactly once."** — this is a big universal claim ("no protocol... can promise") dropped right after one specific example (asking "did it work?" and having *that* get lost too). It reads like a proof but I only saw one case of it. I'd want to know why adding acks or retrying the *status check* forever doesn't eventually pin it down — TCP seems to manage reliability somehow, so why not this?

- **"a long random string that no other payment will share"** — how do we know no other payment will ever pick the same string? Nothing about how the key is generated or why collisions won't happen is said. It's asserted as a guarantee, not explained.

- **"the charge and the saved result must succeed or fail together"** — this is the line I got stuck on longest. Charging a card is an external action on Stripe's servers; saving the result is a local database write. Saying they must happen "together" and then just drawing a box around them labeled "together" doesn't tell me *how* that's actually done. This feels like the hardest part of the whole problem and it's the one place the script waves its hands.

- **"the server has to see that the key is already in progress, and hold the retry back"** — plausible, but "hold back" isn't defined — does it block the second request until the first finishes, queue it, reject it? The screen note says "wait (or rejected)" which is two different behaviors offered as if interchangeable.

## (2) Questions I'd ask afterward

- How do you actually make "charge the card" and "save the key→result row" atomic when one is a call to an external company's server and the other is your own database?
- If the server crashes *after* charging but *before* saving (the exact failure the video names), isn't that still an unsolved case? What actually prevents it in practice?
- How are idempotency keys generated so they're guaranteed unique — is this a UUID, and is "essentially never collides" good enough for money?
- If two retries arrive "5 ms apart" and one is told to wait, wait *how long*, and what happens if the first one also times out?
- Does the client just keep the same key forever for that checkout attempt, or does something eventually give up and refund?

## (3) What I learned (written without looking back, ~150 words)

When a payment request times out, the client can't tell if the charge happened — the request could've been lost, the server could still be working (or have crashed), or the reply could've been lost on the way back. Since payments can't just be dropped, the client has to retry, which risks charging twice. The fix is making the charge itself safe to repeat: an idempotent operation. The client generates a random idempotency key before the first attempt and sends it with every retry. The server checks if it's seen that key before; if so, it returns the saved result instead of charging again. Stripe's API actually uses a header called Idempotency-Key for this. There are still edge cases — like the server crashing between charging and saving the key — that need the charge-and-save step to happen as one unit, and concurrent retries need to be held back rather than both processed.

## (4) Direct answers

- **One main idea:** you can't stop a network from possibly delivering a request twice, so instead you make the *server's handling* of a repeated request harmless (idempotent), typically via a client-generated idempotency key.
- **Numbers I remember:** $50 (the charge amount, just a running example — not meaningful on its own), and the key format like "7f3a…c91" plus "receipt #1042" — also just illustrative labels, not numbers with actual content. The "5 ms apart" for concurrent retries is the only number that felt like it was trying to convey something real (that retries can race each other), but it's not explained further.
- **Starting question:** after a payment request times out with no reply, should the client retry or not, given that retrying risks a double charge and not retrying risks losing the sale?
- **Answer given:** retry (because losing a sale is worse than an ambiguous state), but pair every retry with the same idempotency key so the server only ever actually charges the card once.

## (5) Ratings

- **Pull of the opening (1-5): 4.** "Did the charge go through? ...charged twice" is a concrete, relatable stake — I've personally worried about double-tapping a "pay now" button, so I wanted the resolution.
- **How often I felt lost: a few times** — mainly at the "no protocol can promise exactly once" jump, and more seriously at the "must succeed or fail together" step, which felt like it named the hardest sub-problem and then didn't solve it.
