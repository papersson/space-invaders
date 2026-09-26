# Make It So

Status: in review round 2

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
2. Therefore: declare the end state, not the steps. A step repeats its work when re-run; a target doesn't (a real run: "start 2 more" twice makes 4; "5 servers" twice changes nothing; 3 → 5 plans exactly 2).
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

*Screen:* three machines, three web-app copies ("web") spread across them, a label "Kubernetes: replicas = 3". A clock "03:00"; one machine goes dark, its copy fades. The clock runs to about 03:06 (caption: "first, Kubernetes waits to be sure the machine is gone: about 5 minutes by default"); a new copy appears on another machine: 3 again. Then five server boxes labelled "Terraform: servers = 5"; one is deleted by a hand cursor; the set stays at 4, with a caption "until the next terraform run". The question as a title card.

### 2. Say what, not how

> There are two ways to tell a machine what to do. You can list the steps: start two more servers. Or you can describe the end state: there should be five servers.
> The difference shows up when you run it twice.
> Here's a script that says "start two more servers". Run it once: two servers. Run it again: four. Every run repeats its work.
> Here's Terraform, told there should be three servers. The first run creates three. Run it again, with nothing changed, and it says: no changes; your infrastructure matches the configuration.
> Change the three to five, and it doesn't start five more. It compares what you want with what exists, and plans exactly two.
> Describing the end state is called declarative. The end state you describe is the desired state; what exists right now is the current state. The tool's job is to make the current state match the desired one.

*Screen:* two columns. Left: "imperative: start 2 more" with a terminal from data/terraform_run.txt: "after run 1: 2 servers", "after run 2: 4 servers" (coral on the second). Right: "declarative: servers = 3": `Plan: 3 to add`; second run `No changes. Your infrastructure matches the configuration.` (ICE). Then `servers = 5`: `Plan: 2 to add, 0 to change, 0 to destroy.` Then two labels over the columns' boxes: "desired: 5" and "current: 3".

### 3. The loop

> A thermostat is the classic picture of how that job gets done. You set the temperature you want. The thermostat measures the room, compares, and turns the heating on or off. Then it measures again, and keeps going.
> Kubernetes works the same way. For each kind of thing it manages, a program called a controller runs a loop: look at the desired state, look at the current state, and act on the difference. Then do it again.
> For the web app, the desired state is three copies. Kubernetes calls each running copy a pod. The controller counts the pods. If it finds two, it starts one. If it finds four, it stops one. If it finds three, it does nothing.
> That's what happened at three in the morning. Once Kubernetes was sure the machine was gone, its copy no longer counted. The controller's next count came up one short, and it started a replacement. Nobody had to do anything.
> A loop like this is called a reconciliation loop.

*Screen:* a thermostat dial: set 21°, room 18° → heating on; room rises to 21 → off; a circular arrow "measure → compare → act". The same loop re-labelled for Kubernetes: "desired: 3" / "count pods" / "start or stop the difference". The code from the Kubernetes "Writing Controllers" guide in a small box: `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }`. Then the pods: the count 2 → start one → 3.

### 4. Compare states, not events

> Why count the pods every time? It would seem cheaper to react to events: when a pod dies, the system sends a "pod died" event, so start one pod.
> But events get lost. Here are two controllers keeping three pods running, on the same timeline.
> At second ten, a pod crashes. Both controllers see it, and both start a replacement.
> At second twenty, each controller is restarted, say for an upgrade, and is down for a few seconds. While it's down, another pod crashes.
> The first controller only reacts to events. The "pod died" event arrived while it was down, so it never saw it. It never starts a replacement, and stays at two pods for good.
> The second controller doesn't care about events. When it comes back, it counts two pods, wants three, and starts one.
> Acting on each change is called edge-triggered. Acting on the current state is called level-triggered. Kubernetes' design principles require the second: a controller must do the right thing from the desired and current state alone, however many updates it missed. Events are only a hint to look again soon.

*Screen:* two timelines (data/controller.json), "event-driven" above and "counts pods" below, 0 to 40 seconds, each with a pod-count line starting at 3. At t=10 both dip to 2 and recover (2 s start delay). A grey band t=20-26 "controller down". At t=22 a crash on both lines; an event envelope falls into the grey band on the top line and vanishes ("lost"). Top line stays at 2 to the end (coral "2 for good"); bottom line: at t=27 "counted 2, want 3 → start one", back to 3 at t=29. Labels at the end: "edge-triggered" and "level-triggered".

### 5. Once, or forever

> That also answers the question. Both tools reconcile. The difference is when.
> Terraform's command-line tool compares the desired and current state when you run it, and then stops.
> Here it is managing five servers. Someone deletes server one by hand. Terraform isn't running, so nothing happens, and it stays deleted.
> The next time someone runs terraform plan, Terraform reads what exists, finds four, and plans one to add.
> A Kubernetes controller never stops. It compares again and again, so a change nobody asked for is repaired on its own: within seconds for a deleted copy, within minutes for a dead machine, which Kubernetes first has to be sure of.
> The current state moving away from the desired state is called drift. With Terraform, drift waits for the next run. Hosted Terraform can run that check on a schedule, but it only reports the drift; it doesn't fix it. With a continuous loop, drift is repaired as soon as the loop notices.

*Screen:* the real run (data/terraform_run.txt): five files web-0 … web-4; `rm servers/web-1`; the listing shows four; a clock runs, nothing changes (caption "Terraform isn't running"). Then `terraform plan`: `# local_file.server[1] will be created`, `Plan: 1 to add, 0 to change, 0 to destroy.` (the servers are local files standing in for machines: caption "servers simulated as files"). Beside it, the Kubernetes loop from chapter 3 turning continuously, repairing a removed pod. Label "drift".

### 6. What it doesn't promise

> The loop doesn't promise that you get what you asked for right away.
> When you apply a change in Kubernetes, it records what you want. The pods come later, if they can start at all. To know the change took effect, you look at the reported status, not at the apply.
> It doesn't promise to settle, either. If the desired state keeps changing, the loop chases a moving target. And if two controllers want different values for the same field, say an autoscaler and a tool that keeps re-applying your configuration, both setting the number of copies, they can undo each other's work over and over.
> And nothing repairs what no tool manages. A setting changed by hand on something outside the configuration is simply invisible to it.

*Screen:* three short beats. (1) `kubectl apply` → "recorded"; a status line "ready: 1/3 … 2/3 … 3/3" filling over time. (2) a target number flickering 3 → 5 → 4 → 6 with a count line chasing it; then two controllers pulling a "replicas" field between 3 and 6 ("autoscaler" vs "re-applied config"). (3) a box outside the managed set, greyed: "unmanaged: invisible".

### 7. The answer

> So how do these tools turn a description into reality and keep it there? You declare the state you want. A loop keeps comparing it with what exists, and fixes the difference, like a thermostat.
> It compares whole states instead of reacting to events, so a missed event is caught on the next pass. And it aims at an absolute target, so running it again does no harm.
> Kubernetes repairs things by itself because its loops never stop. Terraform waits for you because it compares only when you run it.
> Either way, what you get is eventual agreement, not an instant guarantee: check the status, and watch for things no tool is managing.

*Screen:* the thermostat loop and the pod loop side by side, turning. Two lines: "Kubernetes: continuous" and "Terraform: when you run it". End card with the takeaway and references: Kubernetes documentation, "Controllers"; Kubernetes design principles and API conventions (level-based logic); Burns, Grant, Oppenheimer, Brewer & Wilkes, "Borg, Omega, and Kubernetes", ACM Queue (2016); Brikman, Terraform: Up & Running (3rd ed., 2022), ch. 1-3; Terraform documentation, "plan" and "apply"; Åström & Murray, Feedback Systems (2008), ch. 1.

## Evidence

| Claim | Source |
|---|---|
| Kubernetes keeps a declared number of replicas; a failed instance is replaced by responding to the difference between spec and status | Kubernetes docs, "Objects in Kubernetes"; KUAR (Burns, Beda, Hightower), ReplicaSets chapter, "Reconciliation Loops" |
| Terraform reconciles only when run; drift is reported at the next plan | Terraform docs, `plan`; HashiCorp tutorial "Manage resource drift"; data/terraform_run.txt |
| Imperative "start 2 more" run twice gives 4; declarative re-apply prints "No changes. Your infrastructure matches the configuration."; 3 → 5 plans "2 to add" | sims/terraform/run.sh, data/terraform_run.txt (Terraform v1.9.8, hashicorp/local provider; servers simulated as files); Brikman, Gruntwork blog (2016) and TUR ch. 1 (10 → 15 servers vs Ansible creating 15 more) |
| Desired state / current state; declarative: describe the end state | Kubernetes docs, "Controllers" and "Object Management"; KUAR ch. 1 |
| Thermostat as the picture of a control loop | Kubernetes docs, "Controllers" (opening example); Åström & Murray, Feedback Systems (2008), ch. 1 |
| Controller loop `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }` | Kubernetes community, "Writing Controllers" guide |
| Reconciliation compares desired and observed state and acts to converge them | Burns et al., "Borg, Omega, and Kubernetes", ACM Queue 14(1), 2016; OpenGitOps glossary |
| Edge-triggered controller misses a crash during a restart and stays at 2; level-triggered counts 2 and starts one at t=27 | sims/controller.py, data/controller.json (simulation written for this lesson) |
| Level-based design: "The system must operate correctly given the desired state and the current/observed state, regardless of how many intermediate state updates may have been missed. Edge-triggered behavior must be just an optimization." | Kubernetes design principles (design-proposals-archive, architecture/principles.md) |
| Kubernetes controllers reconcile continuously; the Terraform CLI runs on demand; HCP Terraform can schedule drift checks, which only report | Kubernetes docs, "Controllers"; Terraform docs; HCP Terraform "health assessments" |
| A dead node's pods are replaced only after the node is marked unreachable and the eviction toleration (300 s by default) expires | Kubernetes docs, "Taints and Tolerations" (default tolerationSeconds 300 for not-ready/unreachable) and node controller (node-monitor-grace-period) |
| Apply records intent; actuation is asynchronous and eventual; check status | Kubernetes resource model doc ("Desired state is updated immediately but actuated asynchronously and eventually"); `kubectl rollout status` |
| Convergence only if the desired state stops changing; controllers can fight (HPA vs apply over replicas) | Sun et al., "Anvil", OSDI 2024 (eventually stable reconciliation); Kubernetes HPA docs (don't set .spec.replicas with an HPA; "thrashing or flapping") |
| Unmanaged state is invisible to the tool | Traugott & Brown, "Why Order Matters", LISA 2002; Morris, "ConfigurationSynchronization" (2013); CloudFormation drift detection covers explicitly set properties only |

## Review log

**Round 1:** editor PASS, expert REVISE, student retold the question and answer correctly (lost "a few times").
- Expert, blocking: "a minute later" was wrong for a dead machine; by default Kubernetes waits for the node to be marked unreachable and a 300-second eviction toleration before the ReplicaSet replaces its pods. Now "a few minutes later", with the wait shown and explained in chapters 1 and 3; chapter 5 now says seconds for a deleted copy, minutes for a dead machine.
- Expert: "only when you run it" now scoped to Terraform's command-line tool, with hosted Terraform's scheduled checks that only report; the fighting controllers now need something that keeps re-applying the configuration; "design principles", not "design rules"; "reconciliation loop"; "current state" (Kubernetes' term) throughout.
- Editor: the half-finished-apply caveat is cut (not in the argument, never revisited); "web app" on the Kubernetes side and "servers" only for Terraform; chapter 6 says "the loop", not a new name.
- Student: lost at the edge/level naming and chapter 6's density; chapter 6 is now shorter by one beat.
