# Make It So

Status: locked after review round 6

## Argument

**Question.** You tell Kubernetes to keep three copies of a web app running. At three in the morning a machine dies and takes one copy with it; nobody runs a command, and a few minutes later there are three again. You tell Terraform you want five servers; someone deletes one by hand, and Terraform doesn't notice until the next time someone runs it. How do these tools turn a description into reality and keep it that way, and why does one repair things by itself while the other waits?

**Answer.** You declare the end state, not the steps. The tool observes what actually exists, compares it with what you declared, and acts on the difference: a reconciliation loop, like a thermostat. Because the target is absolute ("five servers"), running it again with nothing changed does nothing, while a step ("start two more") repeats its work. Because each pass compares whole states rather than reacting to individual events, a controller that missed an event still catches up on its next pass. Terraform runs that comparison once, each time you run it; Kubernetes controllers run it forever, so they repair drift on their own. Neither promises more than eventual agreement: applying records what you want, not that it happened; if the target keeps moving, or two controllers fight over the same field, it may never settle; and anything no tool manages drifts unseen.

**Takeaway.** Declare the state you want; a loop keeps comparing it with what exists and fixes the difference. Compare states, not events, and run the loop continuously, and the system repairs itself; run it on demand, and it repairs only when you ask.

**Wrong model.** A declarative tool executes your file, like a script; once `apply` succeeds, the system is in that state and stays there.

**Objectives.**
1. Contrast a declared end state with a list of steps, and say why re-running a declaration is harmless.
2. Describe the reconciliation loop: observe, compare, act, repeat.
3. Explain why controllers compare whole states instead of reacting to events (level- vs edge-triggered).
4. Contrast one-shot reconciliation (Terraform) with continuous reconciliation (Kubernetes), and what each means for drift.
5. Say what a reconciler doesn't promise: immediate results, convergence under a moving target or fighting controllers, and anything unmanaged.

## Chain

1. The question: Kubernetes replaces a lost copy by itself; Terraform notices a deleted server only when run. How do they work, and why the difference?
2. Therefore: declare the end state, not the steps. A step repeats its work when re-run; a target doesn't (a real run: "start 2 more" twice makes 4; "3 servers" twice changes nothing; 3 → 5 plans exactly 2).
3. Therefore the tool needs a loop: observe, compare, act, repeat, like a thermostat. That's reconciliation.
4. But why compare whole states instead of reacting to "a pod died"? Because events get lost: a controller that was restarting misses one and never recovers; one that counts pods catches up on its next pass.
5. Therefore the difference in the question: Terraform runs the comparison when you run it; Kubernetes runs it forever. Drift waits for the next run, or gets repaired by itself.
6. But even a continuous loop promises only eventual agreement: apply isn't done; a moving target or fighting controllers may never settle; unmanaged things drift unseen.
7. Therefore the answer.

Deviations from the canonical progression: Operators, GitOps and the chain of controllers (Deployment → ReplicaSet → Pod) are left out; the research lists them as common extras. Idempotence is taught through the re-run, and convergence is named only as "eventual agreement".

## Format

| Chapter | Format | Why |
|---|---|---|
| 1 | Narrated animation | A cluster losing a machine and a copy reappearing; a server vanishing from a Terraform-managed set. |
| 2 | Narrated animation with a real terminal | The re-run contrast is clearest as two real runs side by side. |
| 3-4 | Narrated animation | The loop is a cycle over time; the missed event is a timeline with a gap, run by two controllers side by side. The research names these as the parts to animate. |
| 5 | Narrated animation with a real terminal | Drift over time: nothing happens until `terraform plan`. |
| 6-7 | Narrated animation | A short list of limits, then the payoff. |
| (not built) | Hands-on exercise | Delete a pod in a local cluster (kind or minikube) and watch it return; change a resource by hand and run `terraform plan`; write a 20-line reconciler and inject lost events. The research names doing as the way the "apply means done" misconception is corrected; offered, not added. |
| (not built) | Reading | Exact guarantees (Kubernetes' list of what it does not provide; Terraform's no-rollback rule), and the tool-by-tool mechanisms. |

## Ledgers

**Setups and payoffs.**
- The 3 a.m. machine failure (ch. 1) is repaired by the loop (ch. 3) and explained by continuous reconciliation (ch. 5).
- The server deleted by hand (ch. 1) is the Terraform drift run (ch. 5).
- "Start two more" vs "five servers" (ch. 2) returns as "compare states, not events" (ch. 4): both are about absolute targets over deltas.
- The thermostat (ch. 3) returns in the answer (ch. 7).

**Vocabulary.**
| Term | First use | Meaning |
|---|---|---|
| desired state | ch. 2 | what you declared: the end state you want |
| current state | ch. 2 | what exists right now (Kubernetes' term) |
| declarative / imperative | ch. 2 | describing the end state / listing the steps |
| reconciliation loop | ch. 3 | observe the current state, compare with the desired state, act on the difference, repeat |
| controller | ch. 3 | a program that runs a reconciliation loop for one kind of thing |
| pod | ch. 3 | one running copy of an app in Kubernetes |
| level- / edge-triggered | ch. 4 | acting on the current state / acting on each change event |
| drift | ch. 5 | the current state moving away from the desired state |

**Numbers to remember.** Two runs of "start 2 more" make 4; two applies of "5 servers" change nothing. In the simulation, the event-driven controller stays at 2 pods for good; the state-comparing one is back to 3 one pass after it restarts.

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> You tell Kubernetes to keep three copies of a web app running.
> At three in the morning, a machine dies, and takes one copy with it. Nobody is awake, and nobody runs a command. A few minutes later, there are three copies again.
> Now take Terraform. You tell it you want five servers, and it creates them. Then someone deletes one by hand.
> This time nothing happens. Terraform only notices the next time someone runs it.
> Both tools take a description of what you want, and make it real. How do they do that, and keep it that way? And why does one repair things by itself, while the other waits for you?

*Screen:* three machines, three web-app copies ("web") spread across them, a label "Kubernetes: replicas = 3". A clock "03:00"; one machine goes dark, its copy fades. The clock runs to about 03:06; a new copy appears on another machine: 3 again (caption: "nobody touched anything"). Then five server boxes labelled "Terraform: servers = 5"; one is deleted by a hand cursor; the set stays at 4, with a caption "until the next terraform run". The question as a title card.

### 2. Say what, not how

> There are two ways to tell a machine what to do. You can list the steps: start two more servers. Or you can describe the end state: there should be three servers.
> The difference shows up when you run it twice.
> Here's a script that says "start two more servers". Run it once: two servers. Run it again: four. Every run repeats its work.
> Here's Terraform, told there should be three servers. The first run creates three. Run it again, with nothing changed, and it says: no changes; your infrastructure matches the configuration.
> Change the three to five, and it doesn't start five more. It compares what you want with what exists, and plans exactly two.
> Listing the steps is called imperative. Describing the end state is called declarative. The end state you describe is the desired state; what exists right now is the current state. The tool's job is to make the current state match the desired one.
> So it's tempting to picture apply like running a script: once it has run, the job is done. But running it again did nothing at all. That wasn't "already ran". It was "already matches".

*Screen:* two columns. Left: "imperative: start 2 more" with a terminal from data/terraform_run.txt: "after run 1: 2 servers", "after run 2: 4 servers" (coral on the second). Right: "declarative: servers = 3": `Plan: 3 to add`; second run `No changes. Your infrastructure matches the configuration.` (ICE). Then `servers = 5`: `Plan: 2 to add, 0 to change, 0 to destroy.` Then two labels over the columns' boxes: "desired: 5" and "current: 3".

### 3. The loop

> A thermostat is the classic picture of how that job gets done. You set the temperature you want. The thermostat measures the room, compares, and turns the heating on or off. Then it measures again, and keeps going.
> Kubernetes works the same way. For each kind of thing it manages, a program called a controller runs a loop: look at the desired state, look at the current state, and act on the difference. Then do it again.
> For the web app, the desired state is three copies. Kubernetes calls that number the replica count, and each running copy a pod. The controller counts the pods. If it finds two, it starts one. If it finds four, it deletes one. If it finds three, it does nothing.
> That's what happened at three in the morning. The dead machine stopped reporting, and within a minute a separate loop, the one that watches machines, marked it as unreachable. Its copy then got a grace period, five minutes by default, in case the machine came back. When that ran out, about six minutes after the crash, the copy no longer counted. The controller counting pods came up one short, and started a replacement. Nobody had to do anything.
> A loop like this is called a reconciliation loop.

*Screen:* a thermostat dial: set 21°, room 18° → heating on; room rises to 21 → off; a circular arrow "measure → compare → act". The same loop re-labelled for Kubernetes: "desired: 3" / "count pods" / "start or stop the difference". The code from the Kubernetes "Writing Controllers" guide in a small box: `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }`. Then the pods: the count 2 → start one → 3.

### 4. Compare states, not events

> Why count the pods every time? It would seem cheaper to react to events: when a pod dies, the system sends a "pod died" event, so start one pod.
> But events get lost. Here are two controllers keeping three pods running, on the same timeline.
> At second ten, a pod crashes. Both controllers see it, and both start a replacement.
> At second twenty, each controller is restarted, say for an upgrade, and is down for a few seconds. While it's down, another pod crashes.
> The first controller only reacts to events. The "pod died" event arrived while it was down, so it never saw it. It never starts a replacement, and stays at two pods for good.
> The second controller doesn't care about events. When it comes back, it counts two pods, wants three, and starts one.
> The first controller acts on each change; that's called edge-triggered. The second acts on the current state; that's called level-triggered. Kubernetes' design principles require the second: a controller has to get it right from the desired and current state alone, no matter how many updates it missed. Events are only a hint to look again soon.

*Screen:* two timelines (data/controller.json), "event-driven" above and "counts pods" below, 0 to 40 seconds, each with a pod-count line starting at 3. At t=10 both dip to 2 and recover (2 s start delay). A grey band t=20-26 "controller down". At t=22 a crash on both lines; an event envelope falls into the grey band on the top line and vanishes ("lost"). Top line stays at 2 to the end (coral "2 for good"); bottom line: at t=27 "counted 2, want 3 → start one", back to 3 at t=29. At the end each line's label turns into its name: "event-driven" becomes "edge-triggered", "counts pods" becomes "level-triggered".

### 5. Once, or forever

> That explains how a loop stays right when it misses something. It doesn't say how often the loop runs, and that's where the two tools part ways.
> Both tools reconcile. The difference is when.
> Terraform's command-line tool compares the desired and current state when you run it, and then stops.
> Here it is managing the five servers from before. Someone deletes one of them by hand. Terraform isn't running, so nothing happens, and it stays deleted.
> Terraform keeps its own record of what it created. The next time someone runs terraform plan, it refreshes that record against what actually exists, finds four, and plans one to add.
> That's what the script picture gets wrong. Applying didn't hold the system there. Terraform only checks it when you ask.
> A Kubernetes controller's loop has no end. It runs all the time, comparing again and again, so a change nobody asked for is repaired on its own: within seconds for a deleted copy, and a few minutes for a dead machine, because of that grace period.
> The current state moving away from the desired state is called drift. With Terraform, drift waits for the next run. With a continuous loop, drift is repaired as soon as the loop notices.

*Screen:* the real run (data/terraform_run.txt): five files web-0 … web-4; `rm servers/web-1`; the listing shows four; an idle clock runs, nothing changes. Then `terraform plan`: `# local_file.server[1] will be created`, `Plan: 1 to add, 0 to change, 0 to destroy.` (the servers are local files standing in for machines: caption "servers simulated as files"). Beside it, the Kubernetes loop from chapter 3 turning continuously, repairing a removed pod. Label "drift".

### 6. What it doesn't promise

> Change the web app from three copies to five, and apply it with kubectl, Kubernetes' command-line tool. It answers at once: configured. But only three of the five copies are ready. A moment later, four. Then five.
> That count comes from a field called status, where Kubernetes reports the current state it has observed.
> Applying records what you want. Getting there is separate, and slower. Sometimes it never happens, if a copy can't start at all. To know a change took effect, you look at the status, not at the apply.
> The loop doesn't promise to settle, either. If the desired state keeps changing, it chases a moving target.
> And two tools can want different values for the same field. An autoscaler changes the number of copies to match the load. Meanwhile, a job that re-applies your file every few minutes sets it back to the number written there. They can undo each other's work over and over.
> And nothing repairs what no tool manages. A setting changed by hand on something outside the configuration is simply invisible to it.

*Screen:* three short beats. (1) the file's `replicas: 3` edited to `5`; `kubectl apply` → "configured" at once; a status line under it "ready: 3/5 … 4/5 … 5/5" filling over time. (2) a target number flickering 3 → 5 → 4 → 6 with a count line chasing it; then two controllers pulling a "replicas" field between 3 and 6 (the field's value flipping: replicas 3 → 6 → 3 → 6). (3) a box outside the managed set, greyed: "unmanaged: invisible".

### 7. The answer

> So how do these tools turn a description into reality and keep it there? You declare the state you want. A loop keeps comparing it with what exists, and fixes the difference, like a thermostat.
> It compares whole states instead of reacting to events: level-triggered, not edge-triggered. So a missed event is caught on the next pass. And it aims at an absolute target, so running it again does no harm.
> Kubernetes repairs things by itself because its loops never stop. Terraform's command-line tool waits for you because it compares only when you run it.
> Either way, what you get is eventual agreement, not an instant guarantee: check the status, and watch for things no tool is managing.

*Screen:* the thermostat loop and the pod loop side by side, turning. Two lines: "Kubernetes: continuous" and "Terraform: when you run it". End card with the takeaway and references: Kubernetes documentation, "Controllers"; Kubernetes design principles and API conventions (level-based logic); Burns, Grant, Oppenheimer, Brewer & Wilkes, "Borg, Omega, and Kubernetes", ACM Queue (2016); Brikman, Terraform: Up & Running (3rd ed., 2022), ch. 1-3; Terraform documentation, "plan" and "apply"; Åström & Murray, Feedback Systems (2008), ch. 1.

## Evidence

| Claim | Source |
|---|---|
| Kubernetes keeps a declared number of replicas; a failed instance is replaced by responding to the difference between spec and status | Kubernetes docs, "Objects in Kubernetes"; KUAR (Burns, Beda, Hightower), ReplicaSets chapter, "Reconciliation Loops" |
| Terraform reconciles only when run; drift is reported at the next plan | Terraform docs, `plan`; HashiCorp tutorial "Manage resource drift"; data/terraform_run.txt |
| Imperative "start 2 more" run twice gives 4; declarative re-apply prints "No changes. Your infrastructure matches the configuration."; 3 → 5 plans "2 to add" | sims/terraform/run.sh, data/terraform_run.txt (Terraform v1.9.8, hashicorp/local provider; servers simulated as files); Brikman, Gruntwork blog (2016) and TUR ch. 1 (10 → 15 servers vs Ansible creating 15 more) |
| Desired state / current state; declarative: describe the end state; spec holds the desired state, status the observed state | Kubernetes docs, "Controllers", "Objects in Kubernetes" and "Object Management"; KUAR ch. 1 |
| Thermostat as the picture of a control loop | Kubernetes docs, "Controllers" (opening example); Åström & Murray, Feedback Systems (2008), ch. 1 |
| Controller loop `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }` | Kubernetes community, "Writing Controllers" guide |
| Reconciliation compares desired and observed state and acts to converge them | Burns et al., "Borg, Omega, and Kubernetes", ACM Queue 14(1), 2016; OpenGitOps glossary |
| Edge-triggered controller misses a crash during a restart and stays at 2; level-triggered counts 2 and starts one at t=27 | sims/controller.py, data/controller.json (simulation written for this lesson) |
| Level-based design: "The system must operate correctly given the desired state and the current/observed state, regardless of how many intermediate state updates may have been missed. Edge-triggered behavior must be just an optimization." | Kubernetes design principles (design-proposals-archive, architecture/principles.md) |
| Kubernetes controllers reconcile continuously; the Terraform CLI runs on demand (HCP Terraform health assessments can schedule drift checks, which only report); plan refreshes the recorded state against real infrastructure, then diffs against the configuration | Kubernetes docs, "Controllers"; Terraform docs; HCP Terraform "health assessments" |
| A node that stops reporting is marked unreachable (Ready: Unknown; taint node.kubernetes.io/unreachable) after the node monitor grace period (under a minute by default); its pods tolerate the not-ready/unreachable taint for 300 s by default, then are evicted and replaced; the 300 s is a timeout that avoids rescheduling on a blip, not a check that the node is dead | Kubernetes docs, "Taints and Tolerations" (taint-based evictions; default tolerationSeconds 300) and "Nodes" (node controller, node-monitor-grace-period) |
| Apply records intent; actuation is asynchronous and eventual; check status | Kubernetes resource model doc ("Desired state is updated immediately but actuated asynchronously and eventually"); `kubectl rollout status` |
| Convergence only if the desired state stops changing; controllers can fight (the Horizontal Pod Autoscaler vs a re-applied replica count) | Sun et al., "Anvil", OSDI 2024 (eventually stable reconciliation); Kubernetes HPA docs (don't set .spec.replicas with an HPA; "thrashing or flapping") |
| Unmanaged state is invisible to the tool | Traugott & Brown, "Why Order Matters", LISA 2002; Morris, "ConfigurationSynchronization" (2013); CloudFormation drift detection covers explicitly set properties only |

## Review log

**Round 1:** editor PASS, expert REVISE, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: "a minute later" was wrong for a dead machine; by default Kubernetes waits for the node to be marked unreachable and a 300-second eviction toleration before the ReplicaSet replaces its pods. Now "a few minutes later", with the wait shown and explained in chapters 1 and 3; chapter 5 now says seconds for a deleted copy, minutes for a dead machine.
- Expert: "only when you run it" now scoped to Terraform's command-line tool, with hosted Terraform's scheduled checks that only report; the fighting controllers now need something that keeps re-applying the configuration; "design principles", not "design rules"; "reconciliation loop"; "current state" (Kubernetes' term) throughout.
- Editor: the half-finished-apply caveat is cut (not in the argument, never revisited); "web app" on the Kubernetes side and "servers" only for Terraform; chapter 6 says "the loop", not a new name.
- Student: lost at the edge/level naming and chapter 6's density; chapter 6 is now shorter by one beat.

**Round 2:** expert REVISE, editor REVISE, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: the five minutes isn't Kubernetes "being sure" a machine is dead. A node that stops reporting is marked not ready within the node monitor grace period, and its pods then tolerate that for 300 seconds by default (in case it comes back) before they are evicted and replaced. Chapter 3 now says that; the chapter 1 caption shows both steps and matches the clock (about six minutes in all).
- Expert: "never stops" contradicted the restart in chapter 4; now "its loop has no end; it runs all the time". "HCP Terraform, HashiCorp's hosted service" replaces the invented "hosted Terraform". Desired and current state are tied to Kubernetes' spec and status fields.
- Editor, blocking: the autoscaler is now explained, in short sentences (it follows the load; a re-applied file sets a fixed number).
- Editor: a bridge from chapter 4 to chapter 5 (level-triggering says how the loop stays right, not how often it runs); chapter 6 now opens with the apply-then-status demonstration; "replica count" is connected to "copies"; level/edge are called back in the answer; the wrong model (apply is like running a script) is said aloud and knocked down by the re-run.
- Student: lost at "hosted Terraform" and "autoscaler" (both fixed).

**Round 3:** expert PASS, editor REVISE, student retold the question and answer correctly (lost "a few times").
- Editor, blocking: the chapter 1 caption gave away chapter 3's explanation of the delay; it now shows only the unexplained fact ("nobody touched anything").
- Expert: a machine that stops reporting is marked unreachable (Ready: Unknown), not "not ready"; Terraform checks its record of what it created (the state file) against what exists; a controller deletes an extra pod rather than "stops" it.
- Editor: the HCP Terraform aside is cut (the command-line scoping from round 2 covers the expert's point; the evidence table keeps the detail); the drift demo is tied back to the wrong model ("applying didn't hold the system in that state"); chapter 5 uses "the five servers from before", so the Terraform numbers form one thread; the design-principles sentence is easier to say.
- Editor, not taken: cutting the spec/status line (the expert asked for it in round 2, as the link to the Kubernetes docs).

**Round 4:** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times"). The gate is passed; the should-fix items are applied once, and round 5 decides the lock.
- Expert: Terraform's state is now named ("its own record of what it created, called its state"); the chapter 2 setup says three servers, matching the demo; the recap keeps "Terraform's command-line tool"; the five-minute wait is named once as a grace period and called back by that name.
- Editor: spec and status moved from chapter 2 (where they were trivia and crowded the densest beat) to chapter 6, where status pays off; "imperative" is now said aloud; captions that restated the narration are replaced (an idle clock; the replicas value flipping 3 → 6); a stacked sentence in chapter 6 is split.
- Student: lost at spec/status (moved), the one-minute/five-minute numbers (now one named grace period), and edge/level landing together.

**Round 5 (meant as the final round):** expert PASS, editor REVISE, student retold the question and answer correctly. The gate failed, so the blocking item is fixed and round 6 runs.
- Editor, blocking: "called its state" gave "state" a third meaning next to desired and current state; the record is now just "its own record of what it created".
- Editor: chapter 6 now shows the case before the term (replicas 3 → 5, "configured" at once, ready 3/5 … 5/5) and names only status, the field that pays off; the fighting-controllers line names a job that re-applies the file on a schedule, so it no longer sounds like Terraform's command-line tool; the chapter 4 labels are shown turning into their names.
- Expert: the grace period is a default ("five minutes by default"); the machine is marked unreachable by a separate loop that watches machines, and the pod-counting controller starts the replacement; the apply is an update (three copies to five), so kubectl's "configured" is right; kubectl is introduced as Kubernetes' command-line tool.
- Student: lost adding one minute and five minutes (now "about six minutes after the crash"), at edge/level (each name is now attached to its controller), and at "state" (fixed above). The chain's step 2 now says "3 servers" twice, matching the demo.

**Round 6:** expert PASS, editor PASS, student retold the question and answer correctly (lost "a few times"). The gate holds again after the final round's blocking fix, so the script is locked. Revision candidates, not applied (final-round SHOULD FIX items):
- Expert: the five minutes is a toleration period on the unreachable taint (`tolerationSeconds`), which Kubernetes doesn't call a grace period; "idempotence" is never named; Terraform's record is never called its state (the editor had asked for the opposite in round 5, so the next revision has to settle it, perhaps as "its state file"); spec is never named beside status.
- Editor: the autoscaler arrives cold in chapter 6; "Terraform's command-line tool" is qualified without saying why; chapter 6's moving-target and fighting-tools beats are stated abstractly and faster than the rest.
- Student: lost at replica count and pod arriving together, at which loop marks a machine unreachable, and at edge/level landing together.
