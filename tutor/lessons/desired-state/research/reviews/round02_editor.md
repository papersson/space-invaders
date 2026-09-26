# Script Review

## Test 1 — Opening question / closing callback
Opens with a compound question: "How do they do that, and keep it that way? And why does one repair things by itself, while the other waits for you?" Section 7 answers both halves explicitly and in the same vocabulary ("Kubernetes repairs things by itself... Terraform waits for you"). **Passes.**

## Test 2 — Segment chain, report "and then"
Chain as given: Q → *therefore* declare state → *therefore* need a loop → *but* why whole-state comparison → *therefore* once-vs-forever → *but* only eventual agreement → *therefore* answer. **Zero "and then"s** — every joint is causal or adversative. One joint is weak (see Finding B): step 4 (level- vs edge-triggered) doesn't actually entail step 5 (one-shot vs continuous); they're independent design facts glued together with "therefore."

## Test 3 — Announced vs. derived
Sections 2–4 derive their ideas from a shown problem (repeat-on-rerun, missed event). Section 6's three caveats are announced as a checklist ("it doesn't promise... it doesn't promise... and nothing repairs...") rather than emerging from a problem the viewer has already seen bite. Folded into Finding C below.

## Test 4 — Setups/payoffs
- "~5 minutes by default" (§1 caption) → paid off in §5 ("within minutes for a dead machine"). Good.
- "edge-triggered / level-triggered" (§4) is a setup with **no payoff** — never reused in §5–7 even though it's the exact mechanism being praised there. Candidate for a cut or a callback (Finding E).
- "Hosted Terraform... schedule" (§5) is a payoff with no setup and goes nowhere after being introduced (Finding F).

## Test 5 — Undefined terms / double names
- "autoscaler" (§6) is used cold, never explained (Finding A).
- On-screen "Kubernetes: replicas = 3" (§1) vs. spoken "three copies" (§1) vs. later "pods" (§3) — three names for close-but-not-identical concepts, never reconciled (Finding D).
- "settle" (§6) and "eventual agreement" (§7) name the same idea (convergence) with two words — minor (Finding I).

## Test 6 — Numbers
Roughly 18 numeric beats. Worth remembering: **3/5** (the declared targets), **~5 minutes vs. seconds** (why K8s healing isn't instant), and **2 vs. 0** (the idempotent-rerun proof). Everything else (timeline seconds 10/20/22/26/27/29/40, thermostat 21°/18°, status 1/3→3/3) is screen-only choreography and does its job without needing to be memorized. One friction point: the *same* digits recur across unrelated referents — 3am and 3 copies; 5 servers and 5 minutes — risking cross-talk (Finding J).

## Test 7 — Abstraction before the concrete case
§2–4 consistently show the concrete demo, *then* name the abstraction. §6 flips this: each caveat is stated abstractly first ("it doesn't promise X"), then illustrated. Breaks the pattern the rest of the script trained the viewer on (Finding C).

## Test 8 — Wrong intuition
Named wrong model: "apply executes your file like a script; once it succeeds, the system stays there." It's **shown failing** twice — the idempotent no-op rerun (§2) and the Terraform drift-after-delete (§1/§5) — but it is never **stated** as the belief being corrected. The refutation is implicit only (Finding G).

## Test 9 — Examples named but not understood
"Autoscaler" (Finding A) and "Hosted Terraform" (Finding F) are both named and dropped without enough for the viewer to reconstruct why they matter.

## Test 10 — Redundant on-screen text / unsupported pictures
- Caption "Terraform isn't running" (§5) exactly repeats the line just spoken (Finding H).
- The Terraform-as-local-files demo (§5) needs its caption to do all the translation work — the picture alone (rm'ing a file) doesn't read as "someone deletes a server" without the text (Finding K).

## Test 11 — Deletable lines
- "Hosted Terraform can run that check on a schedule, but it only reports the drift; it doesn't fix it." — accurate but load-bearing for nothing; cuttable (Finding F).
- "Acting on each change is called edge-triggered. Acting on the current state is called level-triggered." — if not given a payoff, this is also a deletion candidate (Finding E).

## Test 12 — Hard-to-follow-aloud / pacing
- The autoscaler sentence (§6) stacks a compound subject, an aside, and a restatement in one breath — hard to parse by ear (Finding A).
- §2's three back-to-back definitions (declarative / desired state / current state) are a dense definitional dump with no room to breathe (Finding L).
- §6 covers three distinct failure modes (no instant result, no convergence, unmanaged drift) in roughly the screen time §3 spends on one thermostat — feels rushed relative to the rest of the video (folded into Finding C).

---

## Findings

**A. BLOCKING — unexplained term collides with a dense sentence, undermining Objective 5**
> "And if two controllers want different values for the same field, say an autoscaler and a tool that keeps re-applying your configuration, both setting the number of copies, they can undo each other's work over and over."

"Autoscaler" is never explained, and the sentence is a run-on by ear. This is the sole illustration of "fighting controllers" (an explicit objective) — if it doesn't land, that objective silently fails.
Rewrite: *"It doesn't promise the controllers agree with each other, either. Say an autoscaler — something that watches load and picks its own replica count — decides you need six copies. Meanwhile a separate tool keeps re-applying a config file that says three. Neither is wrong by its own rule, so the count flips back and forth: six, three, six, three."*

**B. SHOULD FIX — chain step 4→5 "therefore" doesn't follow**
Level- vs. edge-triggered (§4) explains robustness to *missed* events within a running loop; it doesn't explain *why* Terraform stops running and Kubernetes doesn't — that's a separate fact (CLI tool vs. long-running process) asserted, not derived.
Rewrite: open §5 with an explicit bridge — *"That explains how a loop stays right even when it misses something. But it doesn't say how often the loop runs — and that's where Terraform and Kubernetes actually part ways."*

**C. SHOULD FIX — §6 breaks the concrete-before-abstract pattern and reads as an announced checklist**
> "The loop doesn't promise that you get what you asked for right away... It doesn't promise to settle, either... And nothing repairs what no tool manages."
Every other section shows the demo first and names the concept after; §6 states the claim first, three times in a row, then illustrates. It also isn't motivated by a problem the viewer has just seen fail — it's a list of caveats.
Rewrite: lead with the visual — *"Run kubectl apply and it answers instantly: configured. But look at the status line underneath — 1/3, still 1/3 a second later, 2/3... Applying only records what you want; reaching it is a separate, slower fact."* Then name the principle.

**D. SHOULD FIX — "replicas" (screen) vs. "copies" (narration) never reconciled**
> Screen: "Kubernetes: replicas = 3" / Narration: "keep three copies of a web app running"
Two labels for one thing, introduced simultaneously, with no line ever saying they're the same. A viewer who later hears "replica count" (if they read docs) may not connect it back.
Rewrite: either change the on-screen label to "copies = 3" for consistency, or add to §3: *"Kubernetes calls the number you want the replica count, and each running copy a pod."*

**E. SHOULD FIX / candidate cut — "edge-triggered"/"level-triggered" set up, never paid off**
These terms are defined at the end of §4 and then never used again, even though §5–7 are describing exactly the level-triggered behavior. Either cut the terminology (the concept survives fine without the labels) or make one callback.
Rewrite for a callback, in §7: *"It compares whole states instead of reacting to events — level-triggered, not edge-triggered — so a missed event is caught on the next pass."*

**F. NIT — "Hosted Terraform" is a dangling named example**
> "Hosted Terraform can run that check on a schedule, but it only reports the drift; it doesn't fix it."
Introduces a specific product/feature the viewer can't place, purely to dismiss it. Deletable without loss.
Rewrite: cut the line entirely, or fold into the prior sentence: *"With Terraform, drift waits for the next run — even a scheduled check only reports it, it doesn't fix it."*

**G. SHOULD FIX — the wrong model is refuted but never named**
The misconception ("apply is like running a script; once it succeeds you're done") is disproved by demonstration (idempotent rerun, drift persisting) but never stated as a belief being corrected, so a viewer who holds it may not notice it was challenged.
Rewrite, added to §2: *"It's tempting to picture apply like running a script — once it succeeds, the job's done. Run it again with nothing changed, though, and it does nothing at all. That's not 'already ran'; it's 'already matches.'"*

**H. NIT — redundant caption**
> Narration: "Terraform isn't running, so nothing happens" / Screen caption: "Terraform isn't running"
Pure repeat. Cut the caption or make it add information, e.g. a literal clock/timer instead of restating the sentence.

**I. NIT — "settle" and "eventual agreement" name the same thing**
§6 says the loop "doesn't promise to settle"; §7 calls the same idea "eventual agreement." Pick one term and reuse it both places.

**J. NIT — recycled digits across unrelated referents**
3am/three copies, five servers/five minutes — no single instance is confusing, but four separate uses of "3" and "5" for unrelated things in one script invites cross-talk. Consider shifting the clock to a different hour (e.g., "two in the morning") to free up the number.

**K. NIT — picture needs its caption to mean anything**
The Terraform-as-local-files demo (`rm servers/web-1`) doesn't read as "a server got deleted" without the caption doing the translation. Consider establishing the file-stand-in convention back in §1 when Terraform's five servers are first shown, so §5's demo doesn't need the caption crutch.

**L. NIT — definitional crowding in §2**
Three terms (declarative, desired state, current state) land in three consecutive sentences with no example between them. Consider splitting: give "desired/current state" its own beat with a one-line concrete tie-back ("desired: 5, current: 3 — that's the gap Terraform just planned for").

---

VERDICT: REVISE
