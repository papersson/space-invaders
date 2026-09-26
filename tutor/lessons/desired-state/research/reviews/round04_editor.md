# Script Review

## 1. Opening question → ending answer
**Pass.** The opening ends on: *"How do they do that, and keep it that way? And why does one repair things by itself, while the other waits for you?"* Section 7 answers with matching language: *"Kubernetes repairs things by itself because its loops never stop. Terraform waits for you because it compares only when you run it."* Clean callback, no drift in framing.

## 2. One-sentence chain / "and then" count
Chain compresses cleanly to therefore/but links (question → declare-state → therefore-loop → but-compare-states-not-events → therefore-once-vs-forever → but-only-eventual-agreement → therefore-answer). **Zero literal instances of "and then"** anywhere in the narration — the connective tissue is causal throughout, not additive. No finding.

## 3. Ideas announced vs. derived
**SHOULD FIX** — File: Section 2. Quote: *"On a Kubernetes object, the desired state is written in a field called spec, and the current state is reported in one called status."* This is dropped in as trivia, not derived from any visible problem on screen at that moment, and (per test 4 below) half of it never pays off. Rewrite: cut `spec` entirely; introduce `status` only where it's actually used, in Section 6: *"kubectl apply answers at once: configured. But a field called status tells a different story — one of three copies ready…"*

## 4. Setups without payoffs / payoffs without setups
**SHOULD FIX** — same finding as above: `spec` (Section 2) is a setup with no payoff anywhere later in the script. `status` (Section 2) is fine — it does pay off in Section 6/7. Everything else (thermostat, edge/level-triggered, drift, script-model) sets up and pays off correctly.

## 5. Terms before explanation / duplicate names
**SHOULD FIX** — File: Section 5. Quote: *"a few minutes for a dead machine, because of that grace period."* Section 3 never actually names the five-minute wait — it just describes it (*"Its copy was given five more minutes…"*). The callback in Section 5 uses a label ("grace period") the audience never heard. Rewrite Section 3: *"Kubernetes gives it a five-minute grace period, in case the machine comes back."* — then Section 5's callback lands as a real callback.

**NIT** — screen caption *"imperative: start 2 more"* (Section 2) is never spoken; narration only names "declarative," leaving its counterpart unlabeled aloud. Rewrite: add *"That's called imperative — listing steps."* before naming declarative.

## 6. Numbers: what's worth remembering, what's dead weight
Worth remembering: **3 vs 5** (the two running examples), and the **~5-6 minute repair window** (03:00→03:06, tied explicitly to the grace period) — it's the number that makes the opening anecdote's timing checkable.

**NIT** — Section 4 screen note stacks precise, unspoken seconds (t=26, t=27, t=29, "2 s start delay") on top of the two numbers narration actually says (10, 20). They do no narrative work. Rewrite: keep only t=10 and t=20 visible; drop the rest.

**NIT** — Section 6: *"a target number flickering 3 → 5 → 4 → 6"* introduces two fresh digits (4, 6) at the least important moment. Rewrite: reuse 3 and 5, e.g. "3 → 5 → 3 → 5," so no new numbers compete for attention.

## 7. Abstraction before concrete case
**Pass, no finding.** Ordering is consistently concrete-first: imperative/declarative demoed before named (Sec. 2), thermostat is a concrete analog before being mapped onto Kubernetes (Sec. 3), the two-controller timeline runs before edge/level-triggered are named (Sec. 4).

## 8. Wrong intuition, shown failing
**Pass.** Wrong model ("apply is like running a script, and it stays done") is named in Section 2, then explicitly shown failing in Section 5 via the deleted server staying deleted, with a direct callback: *"That's what the script picture gets wrong. Applying didn't hold the system in that state."* Confronted and shown failing, not just asserted.

## 9. Examples named but not understood
**NIT** — Section 6's "autoscaler" gets exactly one clause of explanation (*"changes the number of copies to match the load"*). Adequate for its narrow job, but thin. Optional rewrite: *"a horizontal autoscaler watches load and changes the replica count to match it."* Not required.

## 10. On-screen text repeating narration
**SHOULD FIX** — Section 5 caption *"Terraform isn't running"* exactly restates the narration line spoken over it. Same problem in Section 6: captions *"autoscaler: follows the load"* / *"re-applied file: fixed number"* mirror the narration almost verbatim. Rewrite: replace with information the voiceover doesn't already give — e.g. swap the Terraform caption for a plain idle clock with no text, and swap the autoscaler captions for the actual field value oscillating on screen (`replicas: 3 → 6 → 3 → 6`) instead of restating the sentence.

## 11. Deletable lines
- The `spec` clause in Section 2 (see #3/#4) — deletable outright, nothing downstream references it.
- **NIT** — Section 4: *"each controller is restarted, say for an upgrade,"* — the reason for the restart is irrelevant to the logic and can be cut: *"each controller is restarted and is down for a few seconds."*

## 12. Hard-to-say sentences / rushed or padded beats
**SHOULD FIX** — Section 2 is the densest beat in the script: steps-vs-end-state, "declarative," desired/current state, spec/status, and the script-model correction all land in one segment. Trimming the spec/status aside (per #3) directly relieves this.

**NIT** — Section 6: *"Getting there is separate, and slower, and sometimes it never happens, if a copy can't start at all."* Three qualifiers stacked in one breath. Rewrite: *"Getting there is separate, and slower. Sometimes it never happens — if a copy can't start at all."*

**NIT** — Section 6's caveats (moving target, fighting controllers, unmanaged) each get only a single sentence with no consequence stated, reading as a checklist rather than an argument beat. Rewrite the fighting-controllers line to add a consequence clause: *"…neither one ever wins for long."*

---

VERDICT: PASS
