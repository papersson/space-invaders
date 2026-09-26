# Script Review

## Test 1 — Opening question / closing callback
Passes, and does so cleanly. Opening: *"How do they do that, and keep it that way? And why does one repair things by itself, while the other waits for you?"* Closing: *"Kubernetes repairs things by itself because its loops never stop. Terraform waits for you because it compares only when you run it."* The callback is near-verbatim on the exact phrases ("repair things by itself" / "waits for you"), which is the strongest structural element in the script.

## Test 2 — One-sentence chain, report every "and then"
The author's own Chain section already does this and it holds up against the actual script:
1. Q: why does one self-heal, the other wait? **Therefore**
2. declare end state, not steps (idempotence demo). **Therefore**
3. that requires a loop: observe/compare/act (thermostat). **But**
4. why compare states not events — events get lost (timeline demo). **Therefore**
5. that's the actual difference: one-shot vs continuous compare. **But**
6. even continuous only promises eventual agreement, not instant/guaranteed settling. **Therefore**
7. the answer, calling back to the cold open.

Zero instances of "and then" — the chain is pure causal/contrastive, not a list. Good.

## Test 3 — Ideas announced vs. derived
Mostly derived correctly: "declarative" is named only after the re-run demo shows the difference; "reconciliation" only after the thermostat/loop is shown; "edge-/level-triggered" only after the two-controller timeline fails/succeeds; "drift" only after the Terraform deletion sits unrepaired. One weak spot: section 6 states each promise-gap as a flat claim ("doesn't promise... right away," "doesn't promise to settle either") *before* its example, reversing the pattern the rest of the script uses. Minor (NIT) — see below.

## Test 4 — Setups/payoffs
- **Payoff without setup:** "eventual agreement" appears for the first time in the closing line, naming a concept the script spent all of section 6 demonstrating but never labeled. Small but real — a viewer can't call back to a term that was never given to them.
- **Setup without payoff:** "Terraform doesn't undo a half-finished apply" (section 6) introduces a fourth caveat (atomicity) that isn't one of the three the Argument/Chain/objectives promise (immediate results, moving-target/fighting controllers, unmanaged drift), and it's never picked up again. See finding below.

## Test 5 — Terms before explanation / double-naming
- "copy" → "pod" is handled well (explicitly bridged: *"Kubernetes calls each running copy a pod"*).
- "level-/edge-triggered," "desired/actual state," "drift" are each introduced once and reused consistently. Good.
- Two issues, listed as findings: "server" is overloaded across the two running examples, and "reconciling system" (section 6) quietly renames "controller"/"the loop."

## Test 6 — Numbers
All numbers used: 3 (K8s replicas), 03:00, 5 (Terraform servers), 2→4 (imperative demo), 3→5 plans exactly 2, thermostat 21°/18°, pod counts 2/3/4, timeline seconds 10/20/22/26/27/29 + "2s start delay," status 1/3→2/3→3/3, flicker 3→5→4→6, tug-of-war 3/6.

**Worth remembering: 3, 5, and 2.** Three and five are the two anchors that run through the entire video and get paid off in the closing card. Two is the best number in the script — "3 → 5 plans exactly 2" is the single cleanest proof that the tool is comparing states, not replaying commands.

**Numbers doing no work:** the precise timeline seconds in section 4 (10/20/22/26/27/29, "2s delay") — no one is meant to remember them, they only stage an animation; the thermostat's 21°/18° (flavor only); the 3→5→4→6 flicker in section 6 (flavor only). None of these are wrong, just replaceable by relative language ("later," "while it's down") without losing anything.

## Test 7 — Abstraction before the concrete case
Generally fine — "There are two ways to tell a machine what to do" (section 2) and "A thermostat is the classic picture" (section 3) are both mild abstractions stated a sentence before their grounding example, but each is grounded within one beat. Not a violation.

## Test 8 — Wrong intuition
Wrong model: *"apply succeeds → the system is now in that state and stays there, like a finished script."* It **is** shown failing — the cold open's Terraform beat ("someone deletes one by hand... nothing happens... stays deleted") is the wrong intuition failing in the very first 30 seconds, and section 6 reinforces it ("apply isn't done"). But it's never *voiced* as an assumption before being corrected — it's shown, not named. That's a legitimate choice (show-don't-tell), but worth a NIT.

## Test 9 — Examples named but not understood
"Autoscaler" (section 6) is named as the other party in a controller fight but never explained — a viewer with no prior Kubernetes exposure gets a label, not a mechanism. Everything else named (thermostat, pods, files-as-servers) is explained enough to use.

## Test 10 — On-screen text vs. narration; pictures vs. line
The closing section's text cards ("Kubernetes: continuous" / "Terraform: when you run it") simply retype the line just spoken, adding no new information at the moment the video most needs its strongest visual (the two loops, which are already on screen). Section 6's second beat crams two distinct ideas (moving target *and* fighting controllers) into one busy visual, which risks blurring exactly the two things the line is trying to keep separate.

## Test 11 — Deletable lines
*"Terraform doesn't undo a half-finished apply. If one step fails, the steps before it stay done, and the next run starts from there."* — cuttable. It's not one of the three promised caveats, isn't in the Chain, and isn't returned to.

## Test 12 — Hard to say aloud / pacing
- *"Kubernetes' design rules require the second: a controller must do the right thing from the desired and actual state alone, however many updates it missed."* — one sentence carrying a rule plus a qualifier clause; reads better split.
- Section 6 is the most rushed beat in the script: five distinct ideas (not-instant, moving target, fighting controllers, partial-apply, unmanaged) each get about one sentence, versus a full section apiece for the concepts in 2–5. Nothing is padded.

---

## Findings

**SHOULD FIX** — `data/script.md`, section 6
> "Terraform doesn't undo a half-finished apply. If one step fails, the steps before it stay done, and the next run starts from there."
Introduces a fourth, unplanned caveat that isn't in the Argument's three promises, isn't in the Chain, and is never revisited — dilutes the tightest section in the script.
Rewrite: delete the two sentences; let the beat run not-instant → moving-target/fighting-controllers → unmanaged, matching the objectives exactly.

**SHOULD FIX** — cold open, section 1
> "keep three copies of a web server running" ... "a machine dies" ... "you want five servers"
"Server" is used for two different things: the app copies running on a Kubernetes machine, and the Terraform-managed resources that *are* the machines. This risks a mixed model of what a "server" is in each half of the analogy.
Rewrite: "You tell Kubernetes to keep three copies of a web app running" in the K8s beat, reserving "server(s)" exclusively for the Terraform half.

**SHOULD FIX** — section 6
> "A reconciling system doesn't promise that you get what you asked for right away."
Quietly renames the "controller" / "the loop" established in sections 3–5.
Rewrite: "A controller doesn't promise you get what you asked for right away."

**NIT** — closing, section 7
> On-screen: "Kubernetes: continuous" / "Terraform: when you run it" over narration saying almost the same words.
Rewrite: drop the text cards and let the two spinning loops (already specified) carry the point, or replace the cards with "3" / "5" to complete the numeric callback instead of repeating prose.

**NIT** — section 6
> "say an autoscaler and your own configuration both setting the number of copies"
Names a mechanism it doesn't explain.
Rewrite: "say a tool that adds copies under load, and your own configuration, both fighting over the same field" — or cut the aside; it's a caveat, not a taught concept.

**NIT** — section 4
> "Kubernetes' design rules require the second: a controller must do the right thing from the desired and actual state alone, however many updates it missed."
Rewrite: "Kubernetes' design rules require the second. A controller must do the right thing from the desired and actual state alone — no matter how many updates it missed."

**NIT** — closing line
> "what you get is eventual agreement, not an instant guarantee"
First use of this exact term; everything before it argued the *idea* but never named it. Consider seeding the phrase once in section 6 so the finale reuses rather than introduces it.

**NIT** — section 4 numbers
The precise seconds (10/20/22/26/27/29, "2s start delay") are staging detail, not memorable content; narration could say "early on... then later, while it's restarting" and let the screen carry the exact timestamps.

VERDICT: PASS
