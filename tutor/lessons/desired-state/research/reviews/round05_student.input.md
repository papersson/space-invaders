You are this particular viewer:

Background

- Works in industry and wants lessons "useful in the industry day to day". Picked queueing, tail latency, and idempotency with retries from a list of practical topics.
- Keeps a personal library of prompts and references on software architecture, data systems, performance, observability and LLM agents. Likely a software, data or ML engineer. Their exact role and years of experience are unknown.
- Has watched two lessons in this series: UMAP (an earlier session) and external merge sort (version 2, 6:25).
- Assume they know: programming, how web services, APIs and databases are built and called, averages and percentiles as everyday terms, Big-O.
- Unknown: how comfortable they are with probability beyond the everyday (distributions, independence, expected value), and how much formula they want on screen.


Standing instructions for the student reviewer

Play this person: an industry engineer who knows how services are built and has everyday familiarity with averages and percentiles, but has not studied the topic. Flag every term that isn't defined on screen or in the narration, every step that needs a fact they wouldn't have, and every place where two new ideas arrive in one sentence.


 You have not studied this topic. Stay in role: if the script does not explain something, you do not know it. Below is the script of a short narrated video, with a note of what is on screen at each moment. Go through it once, in order, as if watching. (1) List every point where you would be confused or lose the thread, quoting the line: a term used before it is explained, a step that does not follow, a number with no meaning attached, a sentence hard to follow when heard. (2) List the questions you would ask afterwards. (3) Without looking back, write what you learned in about 150 words. (4) Answer: what is the one main idea; which numbers do you remember and what do they mean; what question did the video start with, and what was its answer? (5) Rate how much the opening made you want the answer (1-5) and how often you felt lost (never / once / a few times / often).


---

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
> That's what happened at three in the morning. The dead machine stopped reporting, and within a minute Kubernetes marked it as unreachable. Kubernetes gave its copy a five-minute grace period, in case the machine came back. When that ran out, the copy no longer counted. The controller's next count came up one short, and it started a replacement. Nobody had to do anything.
> A loop like this is called a reconciliation loop.

*Screen:* a thermostat dial: set 21°, room 18° → heating on; room rises to 21 → off; a circular arrow "measure → compare → act". The same loop re-labelled for Kubernetes: "desired: 3" / "count pods" / "start or stop the difference". The code from the Kubernetes "Writing Controllers" guide in a small box: `for { desired := getDesiredState(); current := getCurrentState(); makeChanges(desired, current) }`. Then the pods: the count 2 → start one → 3.

### 4. Compare states, not events

> Why count the pods every time? It would seem cheaper to react to events: when a pod dies, the system sends a "pod died" event, so start one pod.
> But events get lost. Here are two controllers keeping three pods running, on the same timeline.
> At second ten, a pod crashes. Both controllers see it, and both start a replacement.
> At second twenty, each controller is restarted, say for an upgrade, and is down for a few seconds. While it's down, another pod crashes.
> The first controller only reacts to events. The "pod died" event arrived while it was down, so it never saw it. It never starts a replacement, and stays at two pods for good.
> The second controller doesn't care about events. When it comes back, it counts two pods, wants three, and starts one.
> Acting on each change is called edge-triggered. Acting on the current state is called level-triggered. Kubernetes' design principles require the second: a controller has to get it right from the desired and current state alone, no matter how many updates it missed. Events are only a hint to look again soon.

*Screen:* two timelines (data/controller.json), "event-driven" above and "counts pods" below, 0 to 40 seconds, each with a pod-count line starting at 3. At t=10 both dip to 2 and recover (2 s start delay). A grey band t=20-26 "controller down". At t=22 a crash on both lines; an event envelope falls into the grey band on the top line and vanishes ("lost"). Top line stays at 2 to the end (coral "2 for good"); bottom line: at t=27 "counted 2, want 3 → start one", back to 3 at t=29. Labels at the end: "edge-triggered" and "level-triggered".

### 5. Once, or forever

> That explains how a loop stays right when it misses something. It doesn't say how often the loop runs, and that's where the two tools part ways.
> Both tools reconcile. The difference is when.
> Terraform's command-line tool compares the desired and current state when you run it, and then stops.
> Here it is managing the five servers from before. Someone deletes server one by hand. Terraform isn't running, so nothing happens, and it stays deleted.
> Terraform keeps its own record of what it created, called its state. The next time someone runs terraform plan, it refreshes that record against what actually exists, finds four, and plans one to add.
> That's what the script picture gets wrong. Applying didn't hold the system in that state. Terraform only checks it when you ask.
> A Kubernetes controller's loop has no end. It runs all the time, comparing again and again, so a change nobody asked for is repaired on its own: within seconds for a deleted copy, and a few minutes for a dead machine, because of that grace period.
> The current state moving away from the desired state is called drift. With Terraform, drift waits for the next run. With a continuous loop, drift is repaired as soon as the loop notices.

*Screen:* the real run (data/terraform_run.txt): five files web-0 … web-4; `rm servers/web-1`; the listing shows four; an idle clock runs, nothing changes. Then `terraform plan`: `# local_file.server[1] will be created`, `Plan: 1 to add, 0 to change, 0 to destroy.` (the servers are local files standing in for machines: caption "servers simulated as files"). Beside it, the Kubernetes loop from chapter 3 turning continuously, repairing a removed pod. Label "drift".

### 6. What it doesn't promise

> Kubernetes keeps both states on the object itself: what you want in a field called spec, and what it has observed in a field called status.
> Run kubectl apply, and it answers at once: configured. But status says one of three copies ready. A moment later, two. Then three.
> Applying records what you want. Getting there is separate, and slower. Sometimes it never happens, if a copy can't start at all. To know a change took effect, you look at the status, not at the apply.
> The loop doesn't promise to settle, either. If the desired state keeps changing, it chases a moving target.
> And two controllers can want different values for the same field. An autoscaler changes the number of copies to match the load. A tool that keeps re-applying your file sets it back to a fixed number. They can undo each other's work over and over.
> And nothing repairs what no tool manages. A setting changed by hand on something outside the configuration is simply invisible to it.

*Screen:* three short beats. (1) `kubectl apply` → "configured" at once; a status line under it "ready: 1/3 … 2/3 … 3/3" filling over time. (2) a target number flickering 3 → 5 → 4 → 6 with a count line chasing it; then two controllers pulling a "replicas" field between 3 and 6 (the field's value flipping: replicas 3 → 6 → 3 → 6). (3) a box outside the managed set, greyed: "unmanaged: invisible".

### 7. The answer

> So how do these tools turn a description into reality and keep it there? You declare the state you want. A loop keeps comparing it with what exists, and fixes the difference, like a thermostat.
> It compares whole states instead of reacting to events: level-triggered, not edge-triggered. So a missed event is caught on the next pass. And it aims at an absolute target, so running it again does no harm.
> Kubernetes repairs things by itself because its loops never stop. Terraform's command-line tool waits for you because it compares only when you run it.
> Either way, what you get is eventual agreement, not an instant guarantee: check the status, and watch for things no tool is managing.

*Screen:* the thermostat loop and the pod loop side by side, turning. Two lines: "Kubernetes: continuous" and "Terraform: when you run it". End card with the takeaway and references: Kubernetes documentation, "Controllers"; Kubernetes design principles and API conventions (level-based logic); Burns, Grant, Oppenheimer, Brewer & Wilkes, "Borg, Omega, and Kubernetes", ACM Queue (2016); Brikman, Terraform: Up & Running (3rd ed., 2022), ch. 1-3; Terraform documentation, "plan" and "apply"; Åström & Murray, Feedback Systems (2008), ch. 1.

