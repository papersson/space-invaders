# Watching as the reviewer

## (1) Where I lost the thread or would be confused

- **"Kubernetes calls that number the replica count, and each running copy a pod."** — two new terms dropped in one breath. I now have to remember that "replica count" is the number and "pod" is the individual thing, with no time to absorb either before the next sentence moves on.
- **"a separate loop, the one that watches machines, marked it as unreachable"** — this is a *third* loop showing up (after the thermostat loop and the pod-counting loop), and it's never named. Is it also a "controller"? I can't tell if this is a detail I should track or just color.
- **"When that ran out, about six minutes after the crash"** — the previous sentence said the grace period was five minutes and the detection happened "within a minute." Nobody adds those for me — I have to do 1+5=6 myself mid-sentence, and for a second it just sounds like the numbers don't match.
- **"The first controller acts on each change; that's called edge-triggered. The second acts on the current state; that's called level-triggered."** — both technical labels land in the same sentence, attached to two different systems at once. I'd need a rewind to be sure which word goes with which behavior.
- **"An autoscaler changes the number of copies to match the load."** — "autoscaler" is used and immediately relied on for the rest of the point (two tools fighting over the same field), but it's never explained what it is or how it decides "load." I'm told it exists and just have to accept it.
- **"Terraform keeps its own record of what it created."** — this is clearly important (it's how Terraform later "finds four"), but it's described so casually ("its own record") that I wasn't sure it was a named concept versus just a turn of phrase, until it mattered again.

## (2) Questions I'd ask afterward

- Is a "pod" just one running copy, or does it mean something more specific in Kubernetes?
- What's the name of that other loop that marks a machine "unreachable," and is it a controller too?
- Where exactly does the extra minute in "six minutes" come from — is detection always about a minute, or was that just this example?
- What is an autoscaler actually looking at to decide the load, and who tells it what range of replicas is okay?
- Is Terraform's "record" the same thing people call a "state file"? What happens if that record itself gets out of sync with reality?
- Is there one controller for every kind of Kubernetes object, or one big loop for everything?

## (3) What I learned (written without looking back, ~150 words)

Tools like Kubernetes and Terraform let you describe the state you want instead of listing steps — that's called declarative versus imperative. A loop compares what you want (desired state) against what's actually there (current state) and fixes the difference, the same way a thermostat compares set temperature to room temperature. Kubernetes' loop never stops, so if something dies — a copy of an app, or a whole machine — it gets replaced automatically, though machine failures take a few minutes because of a grace period before it's declared really gone. Terraform only checks when you run it, so a manually deleted server just stays deleted until the next run. Instead of reacting to individual events (which can get lost, e.g. if the controller itself was briefly down), these systems recount everything from scratch each time, so a missed event still gets caught on the next pass.

## (4) Direct answers

- **One main idea:** these tools don't run a task once and finish — they keep a loop running that compares "what you want" to "what exists" and corrects the gap; the difference between the two tools is whether that loop runs continuously or only when triggered.
- **Numbers I remember:** five minutes (the grace period before a dead machine's copy is given up on), and six minutes (roughly how long until Kubernetes actually replaces the lost copy) — though I had to work out myself that the extra minute is detection time on top of the grace period.
- **Question it started with:** why does Kubernetes fix a dead server copy on its own at 3 a.m. with nobody awake, while Terraform just leaves a manually deleted server gone until someone runs it again?
- **Its answer:** both compare a "desired" description to what's actually there and correct the difference, but Kubernetes' comparison loop runs forever, while Terraform's only runs when a human invokes it.

## (5) Ratings

- **Want-the-answer pull of the opening:** 4/5 — the 3 a.m./nobody's-awake framing and the paired "one fixes itself, one doesn't" contrast made me want to know why immediately.
- **How often I felt lost:** a few times — mainly around the "replica count/pod" pairing, the unnamed third loop, the six-minutes arithmetic, and the edge-triggered/level-triggered pairing landing together.
