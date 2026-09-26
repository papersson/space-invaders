Here's my pass through the script, staying in character as someone who knows sorting/heaps but nothing about disks or external memory.

## 1. Points of confusion (quoted)

- **"While it works, twelve files appear in a temporary folder, and then they vanish."** — Fine as a hook, but I had no way to guess what these were, and I wasn't sure yet whether "twelve" was a meaningful number or just whatever happened in that particular run.

- **"Here's heapsort on a file twelve times bigger than memory..."** — Is this the *same* file as the "quarter of a million items" file mentioned two sections later, or a different demo file? Never told explicitly, so I was mentally trying to reconcile "12x bigger," "250,000 items," and later "twelve runs" as if they must all be the same example, without being sure.

- **"On our file of a quarter of a million items, that takes eighteen passes."** — I can guess this is log₂(250,000) ≈ 18 since I know merge sort's depth, but the script never says that out loud, so it feels like a number dropped from nowhere if I'm not doing the mental math in real time.

- **"But look at the first fourteen."** — Where does fourteen come from? I don't know the memory size or block size at this point in the video, so I can't derive it myself — it just has to be trusted.

- **"That's one pass instead of fourteen. Eighteen passes become five."** — This requires me to hold four numbers in my head at once (18, 14, 1, 5) and do 18 − 14 + 1 = 5 while listening, not reading. By the time I worked it out I'd missed a second of narration.

- **"Two at a time, that's four more passes."** — Again, why four? Presumably log₂(12) rounded up, but that's never stated, and I'm still not 100% sure "twelve runs" here is the same twelve from the very first scene.

- **"Five passes become two."** — Another number collapse (1 run-building pass + 1 merge pass = 2) that's easy to lose track of by ear.

- **"the number of passes grows as a logarithm of N over M, in base M over B."** — This is the moment I lost the thread hardest. A log with a fractional base spoken aloud is very hard to hold in your head without seeing it written down.

- **"Aggarwal and Vitter proved in 1988..."** — Not confusing exactly, just a name and date with zero context — I don't know who they are or why their proof matters beyond "trust me."

## 2. Questions for the lecturer

- Is the "twelve times bigger than memory" heapsort demo the same file as the "quarter-million items" merge-sort example, or two separate examples?
- How exactly did you get fourteen passes that fit in memory, and four passes for merging twelve runs two-at-a-time? Can you show the arithmetic instead of just stating the result?
- Could you write the pass formula on screen for a beat longer, or show a worked example with actual numbers plugged in?
- Why is a disk fetch "about a thousand times slower" specifically — is that a hardware constant or does it vary a lot by device?
- What would happen if memory could only hold, say, 3 runs at once instead of enough for a 12-way merge — would you just do multiple rounds of multiway merging?

## 3. What I learned (writing this without looking back)

If a file is too big to fit in memory, you can't just sort it normally — you have to think about how many times you touch the disk, since disk reads happen in big chunks and are hugely slower than RAM. Regular sorts like heapsort jump around the file randomly, so they touch the disk constantly. The trick "external merge sort" uses is: first, split the file into chunks that each fit entirely in memory, sort each chunk in RAM, and write it back out — these are called "runs." Then, instead of merging pairs of runs many times, you merge ALL the runs together at once, using one small block of memory per run and a heap to always grab the smallest current item. Because you only ever read and write each block once, this whole process takes just two total passes over the disk, no matter how big the file is, as long as memory can hold enough runs at once.

## 4. Direct answers

- **One main idea:** When data doesn't fit in memory, count disk I/Os instead of comparisons, and design the algorithm to do a few large sequential passes — build memory-sized sorted runs, then merge all of them in a single multiway pass — instead of many small random ones.
- **Numbers I remember:** disk I/O is about **1000x** slower than memory access; the example ended up with **12 runs**; the whole external sort finished in **2 passes**; a 16 GB machine with 1 MB blocks can merge roughly **16,000 runs** at once, enough for files of "hundreds of terabytes."
- **Starting question:** Why does Unix `sort` finish on a file too big for memory (spitting out twelve mystery temp files that vanish), while Python's naive sort just runs out of memory? **Answer:** those files were sorted "runs" — `sort` filled memory 12 times, sorted and saved each chunk, then merged all 12 at once in a single final pass.

## 5. Ratings

- **Desire to know the answer after the opening:** 4/5 — a real side-by-side terminal race plus mysterious vanishing files is a strong hook.
- **How often I felt lost:** a few times — mostly around the pass-count arithmetic (18→14→5→2, and the "four more passes" step) and the spoken log formula near the end.
