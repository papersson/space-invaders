# Watching as the student reviewer

## 1. Points where I lost the thread

- **"On a Kubernetes object, the desired state is written in a field called `spec`, and the current state is reported in one called `status`."** — two new jargon terms land in one sentence, and neither is used again until section 6. I registered them as "vocabulary to remember" but wasn't sure why I needed them at that moment.
- **"within a minute Kubernetes marked it as unreachable... its copy was given five more minutes in case the machine came back."** — two numbers, 1 minute and 5 minutes, with no explanation of where they come from. Are these fixed defaults, something the person running Kubernetes configures, or just illustrative round numbers? I can't tell if I'm supposed to remember "5 minutes" as a fact about Kubernetes or just as flavor.
- **"Acting on each change is called edge-triggered. Acting on the current state is called level-triggered."** — two named concepts back to back, right after a fairly involved two-controller timeline example. I could follow the example itself, but by the time both labels landed I had to pause and match each word back to which line on the timeline it meant.
- **"it compares its record of what it created against what actually exists, finds four, and plans one to add."** — "its record of what it created" is doing a lot of work here (this is presumably Terraform's state file) but it's never named, so I don't know if that's a real, important concept or just a turn of phrase.
- **"An autoscaler changes the number of copies to match the load."** — introduced and used to make a point (two controllers fighting) but never really explained — I know the word from job listings, not from anything the video told me.
- **"what you get is eventual agreement, not an instant guarantee"** — this sounds like it's echoing "eventual consistency," a term I already know from databases, but the video doesn't say whether that's intentional or a coincidence, so I'm left guessing whether to connect the two ideas.

## 2. Questions I'd ask afterward

- Are the "1 minute" and "5 minute" numbers Kubernetes defaults, and are they configurable?
- What actually is `spec` and `status` in practice — do I ever look at these directly, e.g. in a YAML file or `kubectl` output?
- Is "its record of what it created" the Terraform state file? Where does that live, and what happens if it gets out of sync with reality?
- How does the controller's loop actually get triggered each time — is it polling on a timer, or is it woken up by events but then re-checks everything (the video hints at both: continuous loop, but also "events are a hint to look again soon")?
- Is "eventual agreement" meant to be the same idea as "eventual consistency" in databases, or just a coincidental phrase?
- If an autoscaler and a re-applied config file fight over the replica count forever, is that considered normal/acceptable, or is it a misconfiguration people are supposed to avoid?

## 3. What I learned (written without looking back, ~150 words)

Kubernetes and Terraform both take a description of what you want and make it real, but they differ in *when* they check. You describe an end state (declarative) rather than steps to get there (imperative) — like saying "there should be 5 servers" instead of "start 2 more servers." Kubernetes runs a never-ending loop (like a thermostat): count what exists, compare to what's wanted, fix the gap, repeat forever. Because it recompares the whole state each time instead of reacting to individual events, it can't be thrown off by a missed notification — this is called level-triggered rather than edge-triggered, and it's why Kubernetes self-heals within minutes. Terraform does the same kind of compare-and-fix, but only when someone manually runs it, so a deleted server stays deleted until the next run. Neither guarantees instant success — you have to check status separately — and neither can fix things it doesn't manage.

## 4. Direct answers

- **Main idea:** Both tools reconcile a "desired" state against a "current" state, but Kubernetes does it in a continuous loop that never stops, while Terraform only does it when you invoke it — that's the whole difference between self-healing and waiting for a human.
- **Numbers I remember and what they mean:** 3 replicas / 5 servers (the example counts from the opening); "a minute" for Kubernetes to notice a dead machine and "5 more minutes" grace period before replacing its pod. I don't fully trust my memory of the 1-and-5 figures being exactly right, since the video didn't explain where they come from.
- **Question the video started with:** How do Kubernetes and Terraform turn a description into reality and keep it that way, and why does one repair itself while the other waits for you to act?
- **Its answer:** Both use a compare-desired-vs-current loop, but Kubernetes' loop runs continuously (so it repairs drift on its own), while Terraform's loop only runs when a person triggers it (so drift sits unfixed until the next run).

## 5. Ratings

- **Want-the-answer pull of the opening:** 4/5 — the 3am self-healing vs. Terraform-stays-broken contrast is concrete and made me want to know the mechanism.
- **How often I felt lost:** A few times — mainly at the `spec`/`status` naming, the 1-min/5-min numbers, and the edge-triggered/level-triggered pair landing together.
