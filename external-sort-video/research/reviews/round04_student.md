# 1. Points of confusion (quoted)

- **"This file is about twelve times bigger than the memory we'll let our programs use."** — "the memory we'll let our programs use" is odd phrasing; I don't know why it's an artificial limit yet. Fine once I see the 1GB/88MB bar, but by ear alone it's confusing.
- **"Ask the Unix sort command, with the same memory, and it just finishes."** — I don't know what `sort` is doing differently. No mechanism yet, just an assertion.
- **"treat the disk as memory, and let the operating system keep the most recently used parts in memory, fetching the rest from disk as needed."** — this is describing virtual memory/paging but never uses that word (except later cut "paging" per the log), so if I didn't already know the term I'd be lost on what this system is called.
- **"Moving one block between disk and memory is called an I/O."** — okay, defined, but then immediately: **"about three I/Os for every item it sorts"** — three I/Os per item for heapsort — I can't picture why it's specifically three and not one or ten. No visual derivation given, just a measured number.
- **"It needs less than a twentieth of the I/Os."** — a twentieth of what heapsort used? Not clearly anchored — is this a ratio or an absolute count? Confusing by ear.
- **"For a quarter of a million items, that takes eighteen passes."** — where does eighteen come from? I'd need to pause and think "log2(250000) ≈ 18" — not stated, so it feels like a magic number.
- **"For the first fourteen passes, every piece is smaller than memory."** — again, fourteen is unexplained arithmetic (piece size 2^14 = 16384 < 21760 memory size) — I would not compute this while listening.
- **"Our file is twelve memories long, so this makes twelve runs, in a single pass."** — the connection between "twelve memories long" and "twelve runs" is intuitive but stated fast; okay on rewatch.
- **"Eighteen passes become five."** — the arithmetic "1 + 4" flies by; I'd need to freeze-frame to verify 18-14+1=5.
- **"Two at a time, twelve runs become six, then three, then two, then one: those are the four passes."** — fine, but immediately followed by **"Five passes become two: one to make the runs, one to merge them."** — wait, four passes became... one merge pass? The jump from "four passes" to "one pass" via multiway merge is the crux of the video and needs a beat to land — by ear I'd feel like two different numbers (4 vs 1) are being swapped without enough transition.
- **"one run per block of memory, less one for the output"** — clear enough, but paired with **"a laptop's memory holds thousands of blocks"** with no number given for "thousands" — vague.
- **"each merge pass divides the number of runs by thousands"** — I can follow logically but there's no worked number here (unlike earlier sections), so it feels hand-wavy compared to the concrete twelve/six/three earlier.
- **End card formula**: "passes = 1 + ⌈log_{M/B − 1}(N/M)⌉" — this is dense notation dropped only visually at the very end with zero verbal walkthrough. I could not derive or verify this from what was said.

# 2. Questions for the lecturer

1. Where does "three I/Os per item" for heapsort actually come from — is that a general law or specific to this simulation's parameters?
2. Why is memory capped at 88MB / a twelfth of the file in the demo — is that an arbitrary example or does `sort` do this by default?
3. How do you compute the "eighteen passes" and "fourteen passes" numbers in general — is there a formula I should memorize, or is it just log2(N) and log2(memory size)?
4. In the multiway merge, what happens if there are MORE runs than blocks of memory (more than fifteen, since one block is reserved for output)? You said "you need more than one merge pass" — how do you decide how to group the runs across multiple merges?
5. What exactly is "GNU sort: at most 16 per merge (--batch-size)" — is 16 a hard OS/hardware limit or just sort's chosen default, and could I change it?
6. Is virtual memory (the "obvious fix") ever a reasonable choice, or is it always bad for sorting large files?
7. What does "Sort Method: external merge" mean in a PostgreSQL EXPLAIN — is that literally this same algorithm running inside the database?

# 3. In my own words (~150 words)

So there's this problem: sorting a file way bigger than your computer's RAM. Normal sorting algorithms assume everything fits in memory, so when it doesn't, the operating system starts constantly swapping data to and from disk, and disk is really slow compared to RAM — not because of one number but because every time you touch disk you grab a whole chunk of data, not just the one value you wanted. Heapsort jumps around a lot in memory, so it triggers tons of these slow disk fetches. Merge sort, on the other hand, reads and writes things in order, so it wastes way less. The trick `sort` uses: first, split the giant file into chunks that DO fit in memory, sort each chunk fully in RAM, and save each as a "run." Then merge all those sorted runs together at once (not two at a time — all of them simultaneously), using a heap to always grab the smallest next item. That way the whole file only needs to be read and written a couple of times total, instead of dozens.

# 4. Direct answers

- **One main idea:** When your data doesn't fit in memory, you should count disk I/Os (not comparisons) as your cost, and design your sort to do the fewest possible read/write passes over the file — by sorting memory-sized chunks ("runs") and then merging all of them at once instead of two at a time.
- **Numbers I remember and what they mean:** twelve — how many memory-sized "runs" the file split into (also how many temp files appeared); two — the final number of passes over the whole file (one to make runs, one to merge them); sixteen — the max number of runs `sort` merges at once by default. I do NOT confidently remember eighteen, fourteen, or the "three I/Os per item" figure — those went by too fast to stick.
- **Starting question:** Why does Python run out of memory sorting a file 12x bigger than allowed RAM, while Unix `sort` just finishes — what are those twelve mysterious temp files it creates and deletes? **Answer:** `sort` breaks the file into twelve memory-sized sorted "runs," writes them as those temp files, then merges all twelve at once in a single additional pass, so the whole file only gets read/written twice total instead of many times.

# 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — the "twelve mysterious files that appear and vanish" hook is genuinely intriguing and concrete.
- **How often I felt lost:** A few times — mainly around the unexplained arithmetic (eighteen, fourteen, "three I/Os per item," and the jump from four merge passes down to one) and the final formula card, which had no verbal walkthrough at all.
