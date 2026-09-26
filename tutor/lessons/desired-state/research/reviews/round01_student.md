## (1) Where I lost the thread

- **"The end state you describe is the desired state; what exists right now is the actual state."** — this lands right after "declarative" is introduced, so that's three new terms (declarative, desired state, actual state) in one breath. I had to mentally rewind to pin down which word meant which.

- By the end of section 3 I've been handed **"controller," "pod,"** and **"reconciliation"** all in the same short passage — no single one is hard, but they arrive stacked.

- **"Acting on each change is called edge-triggered. Acting on the current state is called level-triggered."** — two jargon words dropped back to back with zero explanation of where the metaphor comes from. They sound like electronics terms; I can't tell if I'm supposed to already know them.

- **"At second twenty, each controller is restarted... and is down for a few seconds. While it's down, another pod crashes."** — this asks me to track a restart, a vague "few seconds," and a second, separately-timed crash, all in my head, with only the on-screen caption (not the narration) giving the actual second (t=22). Hard to follow by ear alone.

- **"Kubernetes' design rules require..."** — "design rules" is stated like it's a known, citable spec, but whose rules, and where they live, isn't said.

- Section 6 opener: **"The pods come later, if they can start at all. To know the change took effect, you look at the reported status, not at the apply."** — three separate claims (delay / possible failure / status≠apply) compressed into two sentences, with no worked example like every earlier section had.

- **"say an autoscaler and your own configuration both setting the number of copies"** — "autoscaler" is used as if already defined; I only half-know the word from general cloud talk, not from anything this video told me.

- The reveal that Terraform's servers were **"simulated as files"** came after I'd already pictured real machines — a late correction to my mental model.

- **"eventual agreement, not an instant guarantee"** — this echoes "eventual consistency" from databases; I don't know if that's deliberate or just a similar-sounding phrase.

## (2) Questions I'd ask afterward

1. Is "level-triggered" literally borrowed from hardware/interrupt terminology? What's the actual metaphor?
2. When Kubernetes "records what you want," where does that go, and roughly how long before pods actually show up?
3. Is an autoscaler itself running its own reconciliation loop — is that why it can fight with my config?
4. How often does the Kubernetes loop actually run — is it continuous polling, or triggered by something, and what does "usually within seconds" really mean?
5. For Terraform, is there any way to detect drift automatically, or does it truly require a human to remember to run `plan`?

## (3) What I learned (written cold, ~150 words)

Kubernetes and Terraform both take a description of what you want and try to make it real, but they differ in *when* they check. You say what you want (declarative), not the steps to get there (imperative) — running a declarative tool twice does nothing extra if nothing changed. Kubernetes runs a never-ending loop, like a thermostat: measure, compare to what you want, fix the gap, repeat — so if a server dies at 3am, it just gets replaced automatically. Terraform only checks when a person runs it, so a manually deleted resource stays gone until someone runs it again. Kubernetes prefers comparing full current state over reacting to individual events, because events can get lost (e.g., during a restart) while a fresh state comparison always catches the problem. Neither tool guarantees instant success — you have to check status, and changes made outside the tool's awareness are invisible to it.

## (4) Main idea, numbers, question/answer

- **Main idea:** both tools reconcile desired vs. actual state, but Kubernetes checks continuously so it self-heals, while Terraform only checks when run, so it waits for a human.
- **Numbers I remember:** "3 replicas" for the web server; "5 servers" in Terraform, dropping to "4" after a manual deletion; a timeline around "second 10" and "second 20" for the crash/restart example. I don't remember exact recovery times other than "a minute later" and "usually within seconds."
- **Opening question:** how do Kubernetes and Terraform turn a description into reality and keep it that way, and why does one self-heal while the other waits for you?
- **Answer given:** both use a "compare desired vs. actual, fix the difference" loop; the difference is that Kubernetes' loop never stops, while Terraform's only runs when invoked.

## (5) Ratings

- **Pull of the opening:** 4/5 — the 3am dead-machine vs. silently-deleted-Terraform-server contrast is concrete and made me want the mechanism.
- **How often I felt lost:** a few times — mainly around the edge-triggered/level-triggered naming and the compressed "what it doesn't promise" section.
