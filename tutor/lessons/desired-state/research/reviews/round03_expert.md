Verified the on-screen numbers against the actual simulation files (`data/terraform_run.txt`, `data/controller.json`, `sims/controller.py`) — every quoted number and log line in chapters 2, 4, and 5 matches its source exactly. No web access was available to cross-check the Kubernetes/Terraform doc citations, so those are assessed from domain knowledge; I flag confidence explicitly where relevant.

## Findings

**1. SHOULD FIX — Node condition terminology conflates "not ready" (False) with "unreachable" (Unknown)**

Quote: *"the machine stops reporting → marked not ready in under a minute → its copies get 5 more minutes in case it comes back"* (Ch.1 screen) and *"within a minute Kubernetes marked it as not ready. Its copy was given five more minutes in case the machine came back."* (Ch.3)

What's wrong: Kubernetes distinguishes two `Ready` condition values that lead to two different taints — `Ready: False` → `node.kubernetes.io/not-ready`, versus `Ready: Unknown` (kubelet stopped reporting entirely, i.e. "the machine dies") → `node.kubernetes.io/unreachable`. The scenario described is squarely the second case, so "not ready" is the wrong condition name — the correct one is "unreachable" (Ready: Unknown). This matters here specifically because the segment cites exact numbers from the "Taints and Tolerations" doc, whose entire point is this distinction. (Caveat, in the script's favor: `kubectl get nodes` does render both False and Unknown as `NotReady` in the STATUS column, so "not ready" isn't unheard-of as end-user shorthand — that's why I'm not calling this BLOCKING.)

Corrected wording: "the machine stops reporting → marked unreachable in under a minute → its copies get 5 more minutes in case it comes back" / "within a minute Kubernetes marked the node unreachable. Its copies were given five more minutes..."

**2. SHOULD FIX — Terraform's "current state" elides the state file**

Quote: *"It compares what you want with what exists"* (Ch.2); *"Terraform reads what exists, finds four, and plans one to add"* (Ch.5)

What's wrong: This isn't false, but it skips Terraform's actual mechanism: `plan`/`apply` refresh each managed resource against the real infrastructure and reconcile that against the recorded **state file**, then diff against the config. Terraform's model is three-way (config / state / real infrastructure), not the two-way (desired/current) model borrowed from Kubernetes' spec/status. For this specific demo (local files via the `local_file` provider) the simplification happens to cause no visible discrepancy, but since the whole video is built on the desired/current-state vocabulary, one sentence acknowledging the state file would prevent viewers from thinking Terraform has no persisted record of its own.

Corrected wording (Ch.5, one added clause): "Terraform refreshes its recorded state against what actually exists, finds four, and plans one to add."

**3. NIT — "stops one" for pod removal**

Quote: *"If it finds four, it stops one."*

What's wrong: Kubernetes Pods aren't paused/stopped and resumed; the controller deletes the excess Pod object. "Stops" is colloquially understandable but not the terminology Kubernetes docs use.

Corrected wording: "If it finds four, it deletes one."

**4. NIT — controller loop pseudocode could misread as literal busy-polling**

Quote: `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }`

What's wrong: This is the real, canonical pseudocode from the "Writing Controllers" guide, so it's not wrong to show — but without a caveat, a viewer could conclude real controllers hammer the API server in a tight loop. Actual controllers use watch-fed informer caches and a work queue; the loop is a conceptual model, not literal implementation. Chapter 4's "events are only a hint to look again soon" gestures at this but never says outright that the reconciliation itself reads from a local cache rather than polling the API server.

Corrected wording: add a brief caption, e.g. "(conceptually — in practice triggered by watch events, not by polling)."

**5. NIT — confirm "HCP Terraform" is still the current product name at air date**

Quote: *"HCP Terraform, HashiCorp's hosted service"*

What's wrong: This was the correct name as of my training data (renamed from Terraform Cloud in 2024), but HashiCorp's post-IBM-acquisition branding may have shifted again by the time this ships; I have no way to check current naming without web access. Worth a final check before publishing rather than a script change now.

## What's not a problem (checked and confirmed correct)

- All Terraform CLI output text and plan/apply arithmetic (3→5 plans "2 to add"; 5 minus 1 deleted → "finds four" → "1 to add") match `data/terraform_run.txt` exactly.
- The edge- vs. level-triggered controller simulation timeline (crash at t=10 recovered by both; crash at t=22 during t=20–26 outage lost by the edge controller, caught by the level controller at t=27, ready at t=29) matches `controller.json`/`controller.py` exactly, including the "stays at two for good" / "back to 3 at t=29" captions.
- node-monitor-grace-period (≈40s, "under a minute") and default `tolerationSeconds` (300s, "five more minutes") are correct current defaults, and the arithmetic (03:00 + 40s + 300s ≈ 03:06) is correct.
- Kubernetes design-principles quote on edge-triggered behavior as "just an optimization," the spec/status vocabulary, the thermostat framing, `kubectl apply` → "configured" immediately vs. asynchronous status convergence, the HPA-vs-reapplied-manifest conflict, and the HCP Terraform drift-detection-reports-but-doesn't-fix claim are all accurate and appropriately hedged — no overstated optimality or generality claims anywhere in the script.
- Citations (Burns et al. ACM Queue 2016, Åström & Murray, Brikman TUR 3rd ed.) are correctly attributed.

VERDICT: PASS
