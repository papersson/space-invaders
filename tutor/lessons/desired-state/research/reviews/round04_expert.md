# Review of "Say What, Not How" explainer script

Overall this is a well-constructed script — the two numerical anchors I could independently verify (node-monitor-grace-period = 40s, taint tolerationSeconds = 300s, giving the "≈03:06" callback in ch.1; and the HPA "thrashing/flapping" warning in ch.6) check out exactly against current Kubernetes docs. Note: I could not reach github.com/community's "Writing Controllers" guide or developer.hashicorp.com during this review (network/tool permissions blocked the fetch), so the two flags below about verifying quoted source text are precautionary, not confirmed errors — treat them as "confirm before it airs," not "this is wrong."

No BLOCKING issues survive scrutiny. Findings below are SHOULD FIX / NIT, aimed at tightening precision to the level the rest of the script already holds itself to.

---

**SHOULD FIX — Ch.5, Terraform's core mechanism is described without its name**
> "The next time someone runs terraform plan, Terraform checks its record of what it created against what actually exists, finds four, and plans one to add."

The script is precise enough elsewhere to name the exact K8s fields (`spec`/`status`) but never names the Terraform analog: the **state file**. "Its record of what it created" *is* the state file, and it's the concept that makes the desired/current-state framing in ch.2 actually parallel between the two tools. Right now a viewer gets an exact field name for one tool and a vague periphrasis for the other. Suggested fix: one clause, e.g. "Terraform keeps its own record — the state — of what it created; it refreshes that record against real infrastructure, finds four, and plans one to add."

**SHOULD FIX — Ch.2, numbers don't match between setup and demo**
> "Or you can describe the end state: there should be five servers." … "Here's Terraform, told there should be three servers."

The declarative example is introduced with "five servers" and then immediately demonstrated with three. Not factually wrong, just a continuity slip that costs a beat of confusion. Fix: make the setup line say "there should be three servers" (or run the demo at five, matching the later 3→5 plan later in the same section, which would also tighten the callback).

**SHOULD FIX — Ch.5 & Ch.7, "Terraform" overgeneralized where "Terraform CLI" is meant**
> "Terraform's command-line tool compares the desired and current state when you run it, and then stops." (ch.5) … "Terraform waits for you because it compares only when you run it." (ch.7, no longer scoped to "command-line tool")

Ch.5 correctly scopes the claim to the CLI. Ch.7's recap drops the scoping and says "Terraform" generally, which slightly overstates generality — HCP Terraform can run scheduled drift *checks* (they still only report, never auto-remediate, so the substantive claim survives, but the wording implies no automation exists at all). Fix: keep "the Terraform CLI" in the ch.7 recap line too, for consistency with ch.5's own careful scoping.

**SHOULD FIX / NIT — Ch.3, "grace period" is used for two different named parameters**
> "within a minute Kubernetes marked it as unreachable. Its copy was given five more minutes in case the machine came back." (ch.3) … "a few minutes for a dead machine, because of that grace period." (ch.5)

These are actually two distinct mechanisms with two distinct names: `node-monitor-grace-period` (≈40s, node→unreachable) and the pod's `tolerationSeconds` on the `unreachable` taint (300s, pod→evicted). Calling both "grace period" colloquially isn't wrong, but ch.5's "that grace period" is ambiguous about which one it's referring back to. A precise but still plain-language fix: "...five more minutes — a toleration — in case the machine came back," then ch.5 can say "because of that toleration window."

**NIT — Ch.3, informal term presented without flagging it as informal**
> "Kubernetes calls that number the replica count"

The field is literally named `replicas` (`spec.replicas`); "replica count" is common shorthand, not Kubernetes's own name for it. Given the script is careful to give the *actual* field names for `spec`/`status` two paragraphs earlier, this one reads as slightly less rigorous by contrast. Fix (optional): "Kubernetes calls that number `replicas`" mirrors the spec/status treatment.

**NIT — Ch.2, missing the standard word for the property being demonstrated**
The whole beat (script that repeats work vs. Terraform that says "no changes") is a textbook demonstration of **idempotency**, but the term is never used, even though it's the standard vocabulary a course on this material would want a learner to leave with. Not wrong to omit, but worth a half-sentence: "declarative tools converge to a target, so re-running them is idempotent — it does nothing once you're already there."

**NIT — Ch.3/Ch.4, unverified literal quotes to double-check before final render**
The on-screen `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }` (attributed to the Kubernetes "Writing Controllers" guide) and the design-principles quote about edge-triggered behavior being "just an optimization" both match my recollection of the source docs, but I was unable to re-fetch either primary source live in this review pass. Since both appear as verbatim on-screen citations, have someone diff them against the current source text before publishing — a misquoted literal citation is the one class of error that would actually be embarrassing here.

---

Everything else checked out: the imperative/declarative contrast, spec/status, thermostat analogy, reconciliation-loop framing, edge- vs level-triggered terminology and its sourcing to Kubernetes' own design principles, the drift/eventual-repair framing, and the ch.6 caveats (apply is not the same as converged, controllers can fight each other, unmanaged state is invisible) are all accurate, appropriately hedged, and don't overclaim optimality or guarantees anywhere. The 03:00→"about 03:06" timing is arithmetically correct (40s + 300s = 5m40s, rounds to 6 min).

VERDICT: PASS
