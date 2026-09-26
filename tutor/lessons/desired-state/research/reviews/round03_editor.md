# Review

## Test 1 — opening question / ending callback
**PASS.** Opening: "How do they do that, and keep it that way? And why does one repair things by itself, while the other waits for you?" Ending: "So how do these tools turn a description into reality and keep it there? … Kubernetes repairs things by itself because its loops never stop. Terraform waits for you because it compares only when you run it." Direct, tight callback using the same two clauses in the same order.

## Test 2 — segment chain, report every "and then"
The author's own Chain section holds up against the script: Question → Therefore (declare end state) → Therefore (needs a loop) → But (why compare states not events) → Therefore (once vs forever) → But (limits/eventual agreement) → Therefore (answer). **Zero "and then" joints anywhere** — every transition is causal, which is a real strength worth preserving in revision; don't let edits soften a "therefore" into an "and then."

## Test 3 — ideas announced vs. derived
Mostly derived well: declarative (run-it-twice demo), reconciliation loop (thermostat), level/edge-triggered (two-controller timeline) all earn their names through a shown problem before being labeled.

- **SHOULD FIX** — `"HCP Terraform, HashiCorp's hosted service, can run that check on a schedule, but it only reports the drift; it doesn't fix it."` This is announced, not derived from any problem the video raised, serves none of the five objectives, and isn't picked up again. Cut it: *"With Terraform, drift waits for the next run."* (already true without the extra sentence).

## Test 4 — setups without payoffs / payoffs without setups
- The grace-period fact is set up as an on-screen caption in section 1 and then **restated almost verbatim as narration in section 3** — see Test 10 below, this is the same defect viewed from the payoff side: the payoff arrives with nothing left to reveal.
- `spec`/`status` (section 2) is a genuine long-range setup/payoff — `status` returns in section 6 ("the status underneath says…"). But `spec` itself never returns. **NIT** — trim it: *"the current state is reported in a field called status"* (drop the spec half; it does no work).

## Test 5 — terms before explanation / double-naming
Clean overall — every term (declarative, desired/current state, reconciliation loop, level/edge-triggered, drift) is defined at or right after first use.
- **NIT** — section 2 uses "what exists" and "current state" within two sentences of each other for the same idea before settling on one term. Pick one first (*"current state"*) and let "what exists" be the plain-English gloss only once.

## Test 6 — numbers
Full list: 3 (replicas), 03:00/03:06 (clock), "under a minute" / "five more minutes" (grace period), 5→4 servers (opening + §5), 3→5 servers, "Plan: 2 to add" (§2), 2→4 (imperative script), "1 to add" (§5), timeline seconds 10/20/22/27/29 (§4), 1/3→2/3→3/3 (§6), 21°/18° (thermostat, screen only).

**Worth remembering:** 3 (the replica count that frames the whole cold open and the answer), five minutes (the grace period that resolves the opening's "a few minutes later" mystery), and the 10/20/22/27/29 timeline (the mechanism proof for level- vs edge-triggered).

**SHOULD FIX** — the script runs *two different* Terraform number sequences (5→4→5 in §1/§5 for drift; 3→5, "2 to add" in §2 for idempotence). Viewers have to track two unrelated numeric threads for "Terraform." Consider using the same five-servers case in both places (e.g., §2 uses "told there should be five… change nothing, no changes; add two more, plans exactly two" against the same five-server board from the cold open) so the number does double duty instead of adding a parallel example to remember.

**No-work number:** 03:00/03:06 clock — purely atmospheric, redundant with the spoken "five more minutes," fine to keep only if it stays silent (it does).

## Test 7 — abstraction before the concrete case
**PASS**, no violations. Every abstract label (declarative, reconciliation loop, level/edge-triggered) follows a concrete demonstration, not the reverse.
- **NIT** — section 6's "chases a moving target" and the fighting-controllers line are stated abstractly first, with the concrete visual arriving simultaneously rather than the narration describing the concrete case first. Minor since the screen carries the concreteness.

## Test 8 — wrong intuition confronted, shown failing?
Wrong model: "apply is like running a script; once it succeeds, the system stays there." The **idempotence half** is confronted explicitly: *"So it's tempting to picture apply like running a script: once it has run, the job is done. But running it again did nothing at all."* The **persistence/drift half** is only shown failing (the Terraform deletion in §1 and §5), never named as the misconception being overturned.

**SHOULD FIX** — add one explicit line tying the drift demo back to the wrong model, e.g. in §5: *"That's the piece the script picture gets wrong: apply doesn't lock the system into that state — it only checks it, and only when you ask."*

## Test 9 — examples named but not understood
- **SHOULD FIX** — HCP Terraform (see Test 3): named, given one clause, never explained or used again. Either cut or actually unpack it; as written it's a name-drop.
- Autoscaler (§6) is brief but functionally explained ("follows the load" vs "fixed number") — acceptable.

## Test 10 — on-screen text repeating narration / pictures not supporting the line
**BLOCKING** — the section 1 screen caption: *"the machine stops reporting → marked not ready in under a minute → its copies get 5 more minutes in case it comes back"* pre-delivers, almost word-for-word, the section 3 narration payoff: *"The dead machine stopped reporting, and within a minute Kubernetes marked it as not ready. Its copy was given five more minutes in case the machine came back."* This is the video's single biggest planted mystery ("a few minutes later, there are three copies again") and its resolution — spoiling it as a caption in the cold open removes the "aha" from the moment the whole first act was built to earn.

**Rewrite:** strip the mechanism from the §1 caption, keep only the unexplained fact: *"03:06 — a new copy appears. Nobody touched anything."* Let §3's narration be the first place the not-ready/five-minute timing is spoken.

- **NIT** — the end-card labels "Kubernetes: continuous" / "Terraform: when you run it" restate the closing lines verbatim. Standard for a summary card; leave unless the editor wants a less literal callback.

## Test 11 — deletable lines
- The HCP Terraform sentence (§5) — deletable outright, see Tests 3/9.
- "written in a field called spec" (§2) — deletable, see Test 4.
- Everything else earns its place; no other line is free-standing filler.

## Test 12 — hard-to-say-aloud sentences / pacing
- **NIT** — `"Kubernetes' design principles require the second: a controller must do the right thing from the desired and current state alone, however many updates it missed."` Dense for spoken delivery. Rewrite: *"Kubernetes' design rules require this: a controller has to get it right from the desired and current state alone, no matter how many updates it missed."*
- **NIT** — `"HCP Terraform, HashiCorp's hosted service, can run that check on a schedule, but it only reports the drift; it doesn't fix it."` Packs a brand name and a nuance into one breath — another reason to just cut it.
- **Pacing** — section 4 carries the densest information load (two controllers, a synchronized timeline, two new terms) in its own runtime; not necessarily rushed at 150 wpm, but worth confirming in edit that the animation holds on the t=20–29 window long enough for the "lost event" and "counted 2, want 3" beats to land before the edge/level labels appear. No other segment reads as padded.

---

**Summary of severities:** 1 BLOCKING (spoiled payoff via on-screen caption), 5 SHOULD FIX (HCP Terraform tangent, spec/status trim, dual Terraform number threads, explicit wrong-model callback, dense sentence rewrite), several NITs (terminology double-naming, abstraction-before-concrete in §6, end-card repetition, §4 pacing check).

VERDICT: REVISE
