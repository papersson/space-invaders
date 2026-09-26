## Review

### BLOCKING

**Quote:** "A little more traffic halved the spare capacity, from twenty percent to ten, and doubled the time requests spend waiting for it."

**What's wrong:** This misstates which quantity doubles, and it contradicts the numbers the script itself gave in chapter 2. There, waiting time (queue delay only, excluding service) was stated as 40 ms at 80% and 90 ms at 90% — a factor of 2.25×, not 2×. What actually doubles exactly is the *response time* T = S/(1−ρ), because S is constant and 1/(1−ρ) doubles when spare capacity halves (50 ms → 100 ms). The *waiting* component Wq = ρS/(1−ρ) carries an extra factor of ρ, which also grew from 0.8 to 0.9, so it grows by more than 2×. Presenting this as a clean doubling of the wait is an arithmetic error a viewer can catch by rewinding to chapter 2's own bar chart (40+10 vs. 90+10).

**Corrected wording:** "A little more traffic halved the spare capacity, from twenty percent to ten, and doubled the response time." (If you want to keep the wait-specific framing, say instead: "and the wait grew from forty milliseconds to ninety — more than double.")

---

### SHOULD FIX

**Quote:** "if a request may take five times its work time on average, keep the server below eighty percent busy"

**What's wrong:** At exactly ρ = 0.8, T = S/(1−ρ) = 5S, i.e., the equality holds *at* 80%, not only below it. "Below eighty percent" is a stricter (safer) reading than the math requires, and it's inconsistent with the curve panel, which marks 80% itself as the point where the value is 50 ms = 5×10 ms.

**Corrected wording:** "keep the server at or below eighty percent busy."

---

**Quote:** "spare capacity" (used repeatedly from chapter 3 onward as if it were the standard name for 1 − ρ)

**What's wrong:** Neither Kleinrock nor Harchol-Balter uses "spare capacity" as a term of art; the standard object is simply 1 − ρ, sometimes described as the fraction of time the server is idle. Calling it "spare capacity" throughout without ever flagging it as a plain-language stand-in risks viewers repeating it as if it's textbook vocabulary.

**Corrected wording:** On first use (chapter 4), add a brief tag, e.g., "the other twenty percent — call it spare capacity — is time the server is idle," so it's clearly introduced as descriptive language for 1 − ρ, not a named quantity from the field.

---

**Quote:** "The same queue takes twice as long to clear, and more requests pile on while that happens."

**What's wrong:** This is presented as a direct mechanical consequence, but nothing in the script has actually derived it — it happens to be consistent with the exact result (and, not coincidentally, with the true mean busy-period length in M/M1, which is also S/(1−ρ)), but as stated it reads like a proof rather than the intuition-building heuristic it is.

**Corrected wording:** "That same queue takes roughly twice as long to clear, on average — and more requests pile on while it does." (The "on average" and "roughly" mark it as intuition, with chapter 5 supplying the exact result.)

---

### NIT

**Quote:** "a request waits forty milliseconds in a queue, four times longer than it's worked on"

**What's wrong:** "Four times longer than X" is colloquially read as 4×X, but strictly parsed it can mean X + 4X = 5X. Minor, but worth tightening since the rest of the script is arithmetically exacting.

**Corrected wording:** "four times as long as it's worked on."

**Quote:** (general) — Little's Law is never named.

**What's wrong:** Not an error, just a missed anchor point; viewers who want to look further have no bridge from "queueing theory gives the exact average response time" to how such formulas are actually derived.

**Corrected wording:** Optional — could add a half-sentence in the end card, e.g., "(derived via Little's Law, L = λW)," without adding narration time.

---

Everything else checked out: the M/M/1 formula and all its plugged-in values (20/50/100/200 ms at 50/80/90/95%), the "+12.5% traffic" arithmetic, the D/D/1 zero-wait argument and its 11.1 ms interarrival figure, the Kingman/G-G-1 burstiness claim, the instability claim at ρ=1, and both citations (Kleinrock 1975, Harchol-Balter 2013) are all correct and canonical.

VERDICT: REVISE
