## 1. Points of confusion (quoted)

- **"twelve files appear in a temporary folder, and then they vanish"** — no idea what these are yet; just a mystery hook, which is fine, but I'm holding onto it waiting for payback.
- **"treat the disk as memory, and let the operating system move data in and out as needed"** — I don't really know how virtual memory works under the hood, so I have to take this on faith rather than picture it.
- **"even on a fast SSD, hundreds of times slower than memory"** — hundreds of times slower than what unit? Per byte? Per access? I can't picture the actual gap.
- **"Heapsort jumps all over the file"** — I know heapsort swaps around in an array, but why does that translate to jumping around *the file on disk*? The connection between "heap operations reorder indices" and "which disk blocks get touched" isn't spelled out.
- **"about three I/Os for every item it sorts"** vs **"less than a twentieth of the I/Os"** — these numbers come from "a simulation," but I don't know the simulation's setup well enough to sanity-check them; they just land as assertions.
- **"A quarter of a million is about two to the eighteenth, so that's eighteen passes."** — I can follow the log2 math, but the leap from "doubling pieces each pass" to "one pass = one read+write of the whole file" needed a beat to land; on first listen I might miss why doubling implies passes = log(N).
- **"Fill memory with the start of the file, sort it right there, and write it back as one sorted piece, called a run."** — okay, but this is introduced as if it's an obvious next move; I wouldn't have derived on my own *why* stopping the merge process early and pre-sorting chunks is allowed/equivalent.
- **"each run is about 86 MB, because sort also keeps a pointer to every line in its memory"** — this footnote flew by; I don't understand why a per-line pointer shrinks the run size, since I don't know how sort represents data in memory.
- **"give every run its own block of memory, and merge them all at once... a heap picks the smallest item"** — I know heaps, so the mechanic makes sense, but visualizing "twelve blocks in memory simultaneously, one heap over all twelve fronts" purely from audio is hard without pausing the screen.
- **"a laptop with sixteen gigabytes of memory holds about sixteen thousand one-megabyte blocks... two passes can sort hundreds of terabytes"** — the jump from "16k blocks fit" to "hundreds of terabytes in two passes" is a big leap in the numbers; I can't verify or really picture it in the moment.
- **"the number of passes grows like a logarithm with an enormous base"** — I get logs, but "enormous base" is described qualitatively with no example number, so it's abstract.
- **"Aggarwal and Vitter, who defined this I/O model, proved that no sort that treats items as indivisible can do asymptotically better."** — total black box to me; I don't know who they are or what "the I/O model" or "indivisible" precisely means here, just have to accept it as an authority claim.
- **the silent formula card** `passes ≈ 1 + ⌈log_{M/B}(N/M)⌉` — since it's silent and on-screen only, if I were just *listening* (as instructed) I'd miss it entirely; I can't evaluate a formula I never heard explained.

## 2. Questions for the lecturer

1. Why exactly does heapsort's access pattern cause 3 I/Os per item — what is it about heap indices that scatters disk access?
2. When you say "hundreds of times slower," slower per what — per byte, per random access, compared to sequential RAM access?
3. Why does keeping a pointer per line shrink usable memory enough to make runs 86 MB instead of a full 160 MB / 12?
4. In the multiway merge, what happens if there are more runs than memory has blocks for — is that the "merge in rounds" case, and how do you pick which runs to merge first?
5. What does "indivisible" mean in the Aggarwal–Vitter result, and does it rule out any clever trick (like compression) from beating this bound?
6. Is the formula on screen (log base M/B) exactly what predicts "hundreds of terabytes in two passes," and could I plug in my own laptop's numbers?

## 3. What I learned (in my own words, ~150 words)

Normal sorting algorithms count comparisons, but that's the wrong thing to optimize once your data is too big for memory — what actually matters is how many times you have to fetch a chunk of data from disk, since disk is way slower than memory. Heapsort bounces around unpredictably, so it wastes a ton of these fetches. Merge sort, though, reads and writes in order, so it wastes nothing. The trick to make merge sort fast on huge files: first, sort as much as fits in memory at once and dump it back as a "run" — do that repeatedly until the whole file is chopped into sorted runs. Then merge all the runs together in one go, using a heap to always pick the smallest next item across all of them, as long as memory has room for one chunk from every run. That's basically two total passes over the disk instead of many, and it's literally what the Unix `sort` command does.

## 4. Direct answers

- **One main idea:** When data is bigger than memory, don't count comparisons — count disk fetches (I/Os), and design your algorithm (sequential runs + one big multiway merge) to minimize those.
- **Numbers I remember:** twelve runs / two passes (the headline result); "three I/Os per item" for heapsort vs "under a twentieth" for merge sort; sixteen thousand blocks fitting in 16GB memory letting two passes sort "hundreds of terabytes." I don't remember the exact formula, and the 86 MB/run detail didn't stick with meaning attached.
- **Starting question:** How does the Unix `sort` command sort a file bigger than allowed memory without running out, and what are those twelve temporary files it creates and deletes? **Answer:** It splits the file into twelve memory-sized sorted "runs," then merges all twelve at once in a single multiway pass — so the whole job takes just two total passes over the disk.

## 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — the "twelve files appear then vanish" mystery, paired with "Python crashes but sort just finishes" on the same memory budget, is a genuinely hooky, concrete puzzle.
- **How often I felt lost:** A few times — mainly around the heapsort-I/O explanation, the 86 MB footnote, and the jump to "hundreds of terabytes," where numbers or mechanisms were asserted faster than I could build a mental picture from audio alone.
