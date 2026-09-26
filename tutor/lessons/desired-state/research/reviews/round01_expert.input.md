You are a professor who has taught this material for years. Below is the script of a short narrated explainer video, with a note of what is on screen at each moment, followed by the list of numbers it uses and where each comes from. Review it for correctness and canonicity. You are the only domain expert who will see it before it is produced, so be exacting. Report every problem with: severity (BLOCKING = wrong, misleading, or non-canonical in a way a professor would object to; SHOULD FIX = imprecise, a missing caveat, non-standard terminology; NIT), the exact quote, what is wrong, and the corrected wording. Check every factual and numerical claim including arithmetic and units; that terminology and notation match the standard sources and simplifications teach nothing false; whether anything essential is missing or anything peripheral gets too much weight; and overstated claims about optimality, generality and real systems. End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> You tell Kubernetes to keep three copies of a web server running.
> At three in the morning, a machine dies, and takes one copy with it. Nobody is awake, and nobody runs a command. A minute later, there are three copies again.
> Now take Terraform. You tell it you want five servers, and it creates them. Then someone deletes one by hand.
> This time nothing happens. Terraform only notices the next time someone runs it.
> Both tools take a description of what you want, and make it real. How do they do that, and keep it that way? And why does one repair things by itself, while the other waits for you?

*Screen:* three machines, three web-server copies ("web") spread across them, a label "Kubernetes: replicas = 3". A clock "03:00"; one machine goes dark, its copy fades. A minute passes on the clock; a new copy appears on another machine: 3 again. Then five server boxes labelled "Terraform: servers = 5"; one is deleted by a hand cursor; the set stays at 4, with a caption "until the next terraform run". The question as a title card.

### 2. Say what, not how

> There are two ways to tell a machine what to do. You can list the steps: start two more servers. Or you can describe the end state: there should be five servers.
> The difference shows up when you run it twice.
> Here's a script that says "start two more servers". Run it once: two servers. Run it again: four. Every run repeats its work.
> Here's Terraform, told there should be three servers. The first run creates three. Run it again, with nothing changed, and it says: no changes; your infrastructure matches the configuration.
> Change the three to five, and it doesn't start five more. It compares what you want with what exists, and plans exactly two.
> Describing the end state is called declarative. The end state you describe is the desired state; what exists right now is the actual state. The tool's job is to make the actual state match the desired one.

*Screen:* two columns. Left: "imperative: start 2 more" with a terminal from data/terraform_run.txt: "after run 1: 2 servers", "after run 2: 4 servers" (coral on the second). Right: "declarative: servers = 3": `Plan: 3 to add`; second run `No changes. Your infrastructure matches the configuration.` (ICE). Then `servers = 5`: `Plan: 2 to add, 0 to change, 0 to destroy.` Then two labels over the columns' boxes: "desired: 5" and "actual: 3".

### 3. The loop

> A thermostat is the classic picture of how that job gets done. You set the temperature you want. The thermostat measures the room, compares, and turns the heating on or off. Then it measures again, and keeps going.
> Kubernetes works the same way. For each kind of thing it manages, a program called a controller runs a loop: look at the desired state, look at the actual state, and act on the difference. Then do it again.
> For the web server, the desired state is three copies. Kubernetes calls each running copy a pod. The controller counts the pods. If it finds two, it starts one. If it finds four, it stops one. If it finds three, it does nothing.
> That's what happened at three in the morning. Nobody had to notice the dead machine. The controller's next count came up one short, and it started a replacement.
> This loop is called reconciliation.

*Screen:* a thermostat dial: set 21°, room 18° → heating on; room rises to 21 → off; a circular arrow "measure → compare → act". The same loop re-labelled for Kubernetes: "desired: 3" / "count pods" / "start or stop the difference". The code from the Kubernetes "Writing Controllers" guide in a small box: `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }`. Then the pods: the count 2 → start one → 3.

### 4. Compare states, not events

> Why count the pods every time? It would seem cheaper to react to events: when a pod dies, the system sends a "pod died" event, so start one pod.
> But events get lost. Here are two controllers keeping three pods running, on the same timeline.
> At second ten, a pod crashes. Both controllers see it, and both start a replacement.
> At second twenty, each controller is restarted, say for an upgrade, and is down for a few seconds. While it's down, another pod crashes.
> The first controller only reacts to events. The "pod died" event arrived while it was down, so it never saw it. It never starts a replacement, and stays at two pods for good.
> The second controller doesn't care about events. When it comes back, it counts two pods, wants three, and starts one.
> Acting on each change is called edge-triggered. Acting on the current state is called level-triggered. Kubernetes' design rules require the second: a controller must do the right thing from the desired and actual state alone, however many updates it missed. Events are only a hint to look again soon.

*Screen:* two timelines (data/controller.json), "event-driven" above and "counts pods" below, 0 to 40 seconds, each with a pod-count line starting at 3. At t=10 both dip to 2 and recover (2 s start delay). A grey band t=20-26 "controller down". At t=22 a crash on both lines; an event envelope falls into the grey band on the top line and vanishes ("lost"). Top line stays at 2 to the end (coral "2 for good"); bottom line: at t=27 "counted 2, want 3 → start one", back to 3 at t=29. Labels at the end: "edge-triggered" and "level-triggered".

### 5. Once, or forever

> That also answers the question. Both tools reconcile. The difference is when.
> Terraform compares the desired and actual state when you run it, and then stops.
> Here it is managing five servers. Someone deletes server one by hand. Terraform isn't running, so nothing happens, and it stays deleted.
> The next time someone runs terraform plan, Terraform reads what exists, finds four, and plans one to add.
> A Kubernetes controller never stops. It compares again and again, so a change nobody asked for is repaired on its own, usually within seconds.
> The actual state moving away from the desired state is called drift. With Terraform, drift waits for the next run. With a continuous loop, it's repaired as soon as the loop notices.

*Screen:* the real run (data/terraform_run.txt): five files web-0 … web-4; `rm servers/web-1`; the listing shows four; a clock runs, nothing changes (caption "Terraform isn't running"). Then `terraform plan`: `# local_file.server[1] will be created`, `Plan: 1 to add, 0 to change, 0 to destroy.` (the servers are local files standing in for machines: caption "servers simulated as files"). Beside it, the Kubernetes loop from chapter 3 turning continuously, repairing a removed pod. Label "drift".

### 6. What it doesn't promise

> A reconciling system doesn't promise that you get what you asked for right away.
> When you apply a change in Kubernetes, it records what you want. The pods come later, if they can start at all. To know the change took effect, you look at the reported status, not at the apply.
> It doesn't promise to settle, either. If the desired state keeps changing, the loop chases a moving target. And if two controllers want different values for the same field, say an autoscaler and your own configuration both setting the number of copies, they can undo each other's work over and over.
> Terraform doesn't undo a half-finished apply. If one step fails, the steps before it stay done, and the next run starts from there.
> And nothing repairs what no tool manages. A setting changed by hand on something outside the configuration is simply invisible to it.

*Screen:* four short beats. (1) `kubectl apply` → "recorded"; a status line "ready: 1/3 … 2/3 … 3/3" filling over time. (2) a target number flickering 3 → 5 → 4 → 6 with a count line chasing it; then two controllers pulling a "replicas" field between 3 and 6 ("autoscaler" vs "your file"). (3) a Terraform apply of three steps, the third failing (coral), the first two staying done. (4) a box outside the managed set, greyed: "unmanaged: invisible".

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
| Kubernetes controllers reconcile continuously; Terraform runs on demand; HCP drift detection only reports | Kubernetes docs, "Controllers"; Terraform docs; HCP Terraform "health assessments" |
| Apply records intent; actuation is asynchronous and eventual; check status | Kubernetes resource model doc ("Desired state is updated immediately but actuated asynchronously and eventually"); `kubectl rollout status` |
| Convergence only if the desired state stops changing; controllers can fight (HPA vs apply over replicas) | Sun et al., "Anvil", OSDI 2024 (eventually stable reconciliation); Kubernetes HPA docs (don't set .spec.replicas with an HPA; "thrashing or flapping") |
| Terraform does not roll back a partially completed apply | Terraform docs, `apply` |
| Unmanaged state is invisible to the tool | Traugott & Brown, "Why Order Matters", LISA 2002; Morris, "ConfigurationSynchronization" (2013); CloudFormation drift detection covers explicitly set properties only |

