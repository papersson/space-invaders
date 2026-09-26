## Watching through, in order

**1. The question (Kubernetes/Terraform intro)** — clear, no confusion. Good concrete hook: dead machine at 3am vs. deleted server nobody notices.

**2. Say what, not how** — clear. "Imperative" / "declarative" / "desired state" / "current state" all get defined right where they're introduced.

**3. The loop** — mostly fine, but one spot where I lost the thread doing math in my head: *"within a minute Kubernetes marked it as unreachable. Kubernetes gave its copy a five-minute grace period... When that ran out, the copy no longer counted."* I had to add 1 + 5 = 6 minutes myself to reconcile this with the opening's "a few minutes later, there are three copies again" (which the screen note pins at 03:06). It's consistent, but the video never says "six minutes total" out loud, so I was doing arithmetic instead of listening.

**4. Compare states, not events** — *"Acting on each change is called edge-triggered. Acting on the current state is called level-triggered."* Two new labels in back-to-back sentences, right after a fairly involved two-controller timeline example. I had the concept from the example but had to pause to pin which word went with which behavior.

**5. Once, or forever** — *"Terraform keeps its own record of what it created, called its state."* This reuses the word "state" for a third meaning — I'd already got "desired state" and "current state" from section 2, and now "state" means a specific file/record Terraform keeps. Briefly confusing which "state" is meant.

**6. What it doesn't promise** — *"what you want in a field called spec, and what it has observed in a field called status."* Two new terms in one sentence again. Also, *"Run kubectl apply"* — this is the first time the name "kubectl" appears; nothing tells me it's "the Kubernetes command-line tool" (I only inferred that by analogy with the Terraform CLI mentioned earlier).

**7. The answer** — clear recap. *"What you get is eventual agreement, not an instant guarantee"* — I wasn't sure if this is the same thing as "eventual consistency," a phrase I've heard elsewhere, or a deliberately different, looser idea.

## Questions I'd ask afterward
- Is "eventual agreement" the same as "eventual consistency"?
- When Terraform says its "state" is out of date, is that stored in a file I could look at, or is it internal/hidden?
- Is `spec` writable by both a human and an autoscaler, or does only `status` get written by Kubernetes itself?
- Does every Kubernetes controller use the same 1-minute-unreachable + 5-minute-grace-period timing, or was that specific to this example?
- Is level-triggered vs. edge-triggered a Kubernetes-specific idea, or something from general systems design I'd hear elsewhere (electronics? circuits?)?

## What I learned (written without looking back, ~150 words)
Kubernetes and Terraform both work by declaring an end state rather than a sequence of steps — you say what you want, not how to get it. Kubernetes runs a "controller" in a loop, forever, that repeatedly counts what currently exists (e.g., how many copies of an app are running) and compares it to what you asked for, fixing any gap. Because it re-checks the whole state rather than reacting to individual events, it can't be fooled by a missed notification — if it comes back online after being down, it just recounts and corrects. Terraform does something similar, but only when you actually run it; if someone deletes a server by hand in between runs, Terraform doesn't notice until the next time you run it. So Kubernetes self-heals continuously, and Terraform self-heals only on demand. Neither guarantees the fix is instant or even guaranteed to succeed — you have to check status separately from just running the command.

## Direct answers
- **One main idea:** Both tools work by continuously (or periodically) comparing "what you want" against "what exists" and closing the gap, rather than executing a fixed sequence of one-time commands — the difference between them is just *how often* that comparison happens (always, vs. only when you run it).
- **Numbers I remember:** 3 replicas / 5 servers from the opening example; roughly 1 minute for Kubernetes to mark a dead node unreachable, plus a 5-minute grace period before replacing its pod.
- **Question it started with:** How do Kubernetes and Terraform turn a description of "what you want" into reality and keep it that way — and why does one fix problems on its own while the other waits for you to act?
- **Its answer:** Both use a compare-and-correct loop against a declared desired state; Kubernetes' loop never stops, so it heals itself continuously, while Terraform's loop only runs when you invoke it, so it waits for you.

## Ratings
- **Pull of the opening (how much it made me want the answer):** 4/5 — the paired 3am/deleted-server scenario was concrete and made me want to know the mechanism immediately.
- **How often I felt lost:** a few times — mainly the grace-period arithmetic, the edge/level-triggered pairing, the overloaded word "state," and the unexplained "kubectl."
