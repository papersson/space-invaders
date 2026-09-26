## 1. Points of confusion

- **"By comparisons alone, heapsort would be at most about twice as slow."** — Twice as slow as what, exactly, and where does "twice" come from? It's stated before any math backs it up.
- **"Heapsort compares items that sit far apart in its array."** — Heard aloud, this doesn't explain *why* they're far apart. The screen apparently shows positions "i and 2i," but that's not said out loud, so on audio alone I'd be lost on the mechanism.
- **"For the first fourteen passes, every piece is smaller than memory."** — Where does "fourteen" come from? I can guess it's related to memory size and doubling, but no formula or reasoning is spoken.
- **"Eighteen passes become five."** — This requires me to do 18 − 14 + 1 in my head in real time; it flew by.
- **"a laptop's memory still holds about sixteen thousand of those."** — Sixteen thousand blocks of what size of memory? The 16 GB assumption is apparently only on-screen, not spoken, so by ear this number has no source.
- The final formula, **"passes = 1 + ⌈log_{(M/B) − 1} ⌈N/M⌉⌉"** — dropped at the very end with zero walkthrough. I don't know what base of log to use or why it's structured that way.

## 2. Questions for the lecturer

- How do you actually calculate the "fourteen passes fit in memory" number — is there a formula?
- Where does the "heapsort ~2x more comparisons" figure come from, mathematically?
- Is GNU sort's "16 runs at a time" a hard limit, a tuning default, or based on something like open file limits?
- Why is 1 MB a "typical" block size — is that a hardware fact or a software choice?
- Can this technique (runs + multiway merge) be used with heapsort somehow, or is heapsort just fundamentally unfit for external sorting?
- Can I derive that end-card formula myself from what was taught, or does it need more background?

## 3. What I learned (in my own words)

When a file is too big for RAM, what matters isn't how many comparisons your sort does, it's how many times you have to go to disk, because disk access is way slower and happens in whole chunks ("blocks"), not single values. Heapsort jumps around unpredictably in memory, so under virtual memory it constantly needs blocks that aren't loaded — brutal for disk. Merge sort, though, reads and writes in straight sequential sweeps, so every disk block it touches gets fully used. The trick "sort" uses: first, sort chunks that individually fit in memory and write each out as a "run" (that's what those mysterious temp files were). Then, instead of merging two runs at a time repeatedly, merge ALL runs at once, using one memory block per run plus a small heap to track the smallest fronts. This collapses many merge passes into one, so huge files sort in just two or three total disk passes.

## 4. Main idea, numbers, question/answer

- **Main idea:** When data doesn't fit in memory, minimize *disk passes* (sequential reads/writes), not comparisons — do this by making memory-sized sorted "runs," then merging all of them at once instead of two-at-a-time.
- **Numbers I remember:** 12 (file is 12x memory size, and 12 runs get created), 16 (GNU sort's default max runs merged at once), and 2 (the total number of passes sort ends up needing — one to make runs, one to merge them all).
- **Opening question:** What are the twelve temp files sort creates and deletes, and how does it sort a huge file without running out of memory?
- **Answer:** They're "runs" — memory-sized sorted chunks. Sort makes 12 of them (one pass), then merges all 12 at once in a single multiway merge (second pass) — two passes total instead of Python's "try to hold it all at once and crash."

## 5. Ratings

- **Pull of the opening (1–5):** 4 — the "twelve mysterious files that appear then vanish" framing is a genuinely good hook, I wanted to know what they were.
- **How often I felt lost:** A few times — mainly around the "fourteen passes" number, the unexplained "twice as slow" claim, and the unspoken 16 GB assumption behind "sixteen thousand blocks."
