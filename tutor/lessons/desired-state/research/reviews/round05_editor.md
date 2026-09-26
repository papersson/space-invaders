# Script Review

## 1. Opening question ↔ ending payoff
Passes, and passes well. Opening: *"How do they do that, and keep it that way? And why does one repair things by itself, while the other waits for you?"* Ending: *"Kubernetes repairs things by itself because its loops never stop. Terraform's command-line tool waits for you because it compares only when you run it."* Near-verbatim callback on both clauses ("repair things by itself" / "waits for you"). No finding.

## 2. Segment chain (but / therefore / and then)
1. Cold open raises the question **therefore**
2. declare end state, not steps (re-run test) **therefore**
3. that needs a loop — thermostat/reconciliation **but**
4. compare states not events, because events get lost **therefore**
5. once (Terraform) vs forever (Kubernetes) — drift **but**
6. even continuous loops only promise eventual agreement **therefore**
7. the answer

**"and then" count: 0.** Entirely causal, matches the author's own chain. No finding.

## 3. Ideas announced vs. derived
Everything is earned by a visible problem *except* the spec/status naming in §6, which lands before the problem it explains — see the combined finding under test 7 below.

## 4. Setups / payoffs
Clean. "3 in the morning" → 03:06 pays off exactly against "1 minute to unreachable + 5‑minute grace period" in §3. Hand-deleted server in §1 pays off in full in §5. Script-picture wrong model (§2) gets a second, sharper payoff in §5 ("That's what the script picture gets wrong"). No missing payoffs found.

## 5–7. Terminology and abstraction-before-concrete

**BLOCKING — "state" is reused for a third, colliding meaning.**
Quote: *"Terraform keeps its own record of what it created, called its state."* (§5)
By this point "state" has been trained for two whole sections to mean *desired state* / *current state* — the reality-vs-target dichotomy that's the spine of the video. Naming Terraform's bookkeeping file "its state" plants a third, different referent on the same word at the exact moment you're demonstrating drift, the most important beat in the video.
Rewrite: *"Terraform keeps its own record of what it created."* — drop "called its state" entirely; the label does no work no objective needs it, and cutting it removes the collision for free.

**SHOULD FIX — spec/status: new jargon before the concrete case, and a second name for concepts already named.**
Quote: *"Kubernetes keeps both states on the object itself: what you want in a field called spec, and what it has observed in a field called status."* (§6)
This breaks the pattern the rest of the script follows correctly (concrete case, then the term — see §2, §3, §4). It also quietly renames "desired state"/"current state" to "spec"/"status" without tying the two pairs together.
Rewrite: *"Run kubectl apply, and it answers at once: configured. But that only means it recorded what you want. Whether it's actually running is separate, and slower: one of three copies ready. Then two. Then three."* — cut spec/status by name; nothing downstream depends on the field names.

## 8. Wrong intuition confronted and shown failing
Named cleanly: *"it's tempting to picture apply like running a script: once it has run, the job is done."* It's shown failing twice — once on idempotence (re-run does nothing, §2) and once, more decisively, on persistence (the hand-deleted server stays deleted until the next run, §5, with an explicit callback: *"That's what the script picture gets wrong"*). Passes.

## 9. Named-but-not-understood examples
None of real weight — Operators/GitOps/ReplicaSet are deliberately left out per the Deviations note, and "autoscaler" gets its one sentence of explanation. Minor: the on-screen `local_file.server[1]` (§5) is Terraform address syntax never decoded, but it's peripheral screen dressing, not a taught concept — NIT only if you want to sand it down.

## 10. On-screen text vs. narration
**NIT** — redundant caption: *"caption: 'nobody touched anything'"* (§1) just restates *"Nobody is awake, and nobody runs a command."* Rewrite: swap it for information the narration hasn't given yet, e.g. *"03:06 — self-healed."*

**SHOULD FIX** — unclear relabeling: §4's screen starts labeled *"event-driven"/"counts pods"* and ends labeled *"edge-triggered"/"level-triggered"* with no direction that one becomes the other. As written it reads as two floating name-pairs for the same two ideas.
Rewrite (direction only): *"the label 'event-driven' morphs into 'edge-triggered'; 'counts pods' morphs into 'level-triggered'"* — one concept, watched acquiring its technical name.

## 11. Deletable lines
- *"called its state"* (§5) — delete; see BLOCKING finding above.
- Everything else earns its place; no other line is inert.

## 12. Hard to read aloud / pacing
**SHOULD FIX** — apparent self-contradiction: *"A tool that keeps re-applying your file sets it back to a fixed number."* (§6) Two sections earlier the video's central claim was that Terraform *only* checks when run — this line, unqualified, sounds like it reverses that.
Rewrite: *"Imagine some automation that re-runs terraform apply on a schedule, resetting the count to a fixed number every time."*

**NIT** — dense sentence: *"a controller has to get it right from the desired and current state alone, no matter how many updates it missed."* Rewrite: *"a controller must reach the right answer from the desired and current state alone — even if it missed every update in between."*

**NIT** — pacing: §6 carries four distinct sub-claims (apply ≠ done, moving target, fighting controllers, unmanaged drift) in the space §4 used for one worked example. It's the full content of objective 5 but gets the thinnest treatment in the script; the "fighting controllers" beat in particular would benefit from the same one-scenario treatment §4 gives edge- vs. level-triggered.

## Numbers
Every number: 3 replicas; 03:00 → ~03:06; 5 servers; imperative demo 2→4; declarative demo Plan 3‑to‑add / Plan 2‑to‑add; 5-minute grace period; ~1 minute to unreachable; timeline seconds 10/20/22/26/27/29; 5 servers → delete 1 → 4, Plan 1‑to‑add; status 1/3→2/3→3/3; moving target 3→5→4→6; fighting-controllers 3→6→3→6.

**Worth remembering:** 3 (the replica count that threads the whole video), the 5‑minute grace period (it's the answer to the cold open's "a few minutes later"), and the exact Plan diffs (3‑to‑add / 2‑to‑add) that make idempotence concrete rather than asserted.

**NIT** — doing no work: the second-by-second timeline markers (t=10, 20, 22, 26, 27, 29) in §4's screen direction are production detail; fine as invisible chart data, but if rendered as readable on-screen numbers they add clutter with nothing to remember.

---

VERDICT: REVISE
