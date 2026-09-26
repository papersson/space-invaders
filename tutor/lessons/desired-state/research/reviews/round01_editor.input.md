You are a script editor for educational videos. Below is the author's stated question, takeaway and objectives, and the script with a note of what is on screen. Judge the narrative, not the facts. For each finding give severity (BLOCKING / SHOULD FIX / NIT), the quote and a concrete rewrite. Tests: (1) does the opening raise one question that the ending answers, calling back to the opening; (2) write each segment as one sentence joined by "but", "therefore" or "and then", show the chain, and report every "and then"; (3) list ideas that are announced rather than derived from a visible problem; (4) list setups without payoffs and payoffs without setups; (5) list terms used before they are explained and concepts with more than one name; (6) list every number, name the two or three worth remembering, and flag numbers that do no work; (7) flag abstractions that arrive before the concrete case; (8) name the wrong intuition the video confronts and say whether it is shown failing; (9) flag examples that are named but not understood; (10) flag on-screen text that repeats the narration and pictures that do not support the line; (11) list lines that could be deleted without breaking anything; (12) flag sentences hard to follow aloud, and judge whether any beat is rushed or padded (there is no length target). End with "VERDICT: PASS" if there are no BLOCKING items, otherwise "VERDICT: REVISE".


---

## Argument

**Question.** You tell Kubernetes to keep three copies of a web server running. At three in the morning a machine dies and takes one copy with it; nobody runs a command, and a minute later there are three again. You tell Terraform you want five servers; someone deletes one by hand, and Terraform doesn't notice until the next time someone runs it. How do these tools turn a description into reality and keep it that way, and why does one repair things by itself while the other waits?

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

