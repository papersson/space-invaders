Here's my read-through as that student, going through it once in order.

## 1. Where I lost the thread

- **"let the operating system keep the most recently used parts in memory, fetching the rest from disk as needed."** — I've heard "virtual memory" as a term before but never learned how it actually decides what to keep. "Most recently used parts" of *what* — the file? A block? This goes by fast.
- **"Heapsort compares items that sit far apart in its array."** — I know heapsort works on a tree-shaped structure stored in an array, but I can't picture *why* that makes it jump around in memory more than, say, merge sort does. This one I just had to take on faith.
- **"Eighteen doublings take you from one item to a quarter of a million, so that's eighteen passes."** — I can follow "doubling gets you there in log₂ steps" if I stop and do the math, but hearing "eighteen" fly by without being able to pause and check 2¹⁸ ≈ 262,144 myself, I just had to trust the number.
- **"For the first fourteen passes, every piece is smaller than memory."** — Where does fourteen come from? It's not derived out loud — I guess it's tied to memory size, but the connection isn't spoken, only shown on screen apparently.
- **"That one pass replaces the first fourteen, and the last four stay. Eighteen passes become five."** — Three numbers (14, 4, 5) landing back to back. By the time I did 18−14+1=5 in my head, the video had moved on.

## 2. Questions for the lecturer

- Why exactly does heapsort's array access pattern jump around while merge sort's doesn't — can you show me the actual index math?
- How did you get "fourteen" passes as the cutoff where pieces are still smaller than memory? What's the formula?
- Is "virtual memory" the OS literally deciding what's "recently used," and is that decision ever wrong/costly?
- Why sixteen as GNU sort's default merge cap — is that just tuned by hand, or is there a principled reason?
- Does this "runs then merge" idea only work for sorting, or do other algorithms use the same trick when data doesn't fit in memory?

## 3. What I learned, in my own words

When a file is too big for memory, the bottleneck isn't how many comparisons you do — it's how many times you touch the disk, because each disk fetch grabs a whole chunk of data and is way slower than reading memory. Heapsort jumps around unpredictably, so it wastes tons of disk fetches. Merge sort reads and writes in order, so it wastes way fewer. The trick "external merge sort" uses: first, sort as much as fits in memory at a time and save each sorted chunk (a "run") back to disk. Then merge all those runs together in one pass, using one little slice of memory per run plus a heap to always grab the smallest next item. That turns a huge sort into just two full passes over the disk instead of many — and that's literally what the Unix `sort` command does, which is why temporary files show up and disappear while it runs.

## 4. Main idea, numbers, question/answer

- **Main idea:** when data doesn't fit in memory, minimize disk *passes* (not comparisons) by sorting memory-sized chunks first, then merging as many of those chunks at once as memory allows.
- **Numbers I remember:** twelve (the file is 12x memory, so 12 runs get made), sixteen (sort's default max runs per merge), and two (the total passes needed — one to build runs, one to merge).
- **Opening question:** what are those twelve temporary files `sort` creates, and how does it avoid running out of memory? **Answer:** they're the 12 sorted "runs" it builds because the file is 12 memory-loads long, and it finishes in just two total disk passes by merging all twelve at once.

## 5. Ratings

- **Hook pull (1–5):** 4 — the vanishing files with a literal question mark on screen made me want the answer.
- **How often I felt lost:** a few times — mainly around the heapsort-array-jump explanation and the string of numbers (18, 14, 4, 5) in section 3.
