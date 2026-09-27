You are reviewing the frames of a finished narrated explainer video, "Find, Rank, Measure", a primer on search engineering for a technical viewer new to the field (like an undergraduate in a first information retrieval course). You have not seen it before. The files are in the current folder:

- `script.md`: the narration, chapter by chapter, with a note of what should be on screen at each moment ("Screen:"), followed by the evidence table (every number and claim, and where it comes from).
- `sheets/`: contact sheets from the 1080p render, one frame near the end of every narrated sentence, labelled with the sentence id (for example s4_12). Several sheets per chapter (s1_1.png, s1_2.png, ...). Read every sheet.
- `data/`: the data the video draws on (results.json: every stage's metrics over the 50 topics; topic1.json: the opening query's ten results, grades, precision/recall by cutoff and the NDCG worked example; topic4.json: the vocabulary-mismatch topic; dense_stats.json: the approximate nearest-neighbour search and reranker measurements; timing.json: the scan and index timings).
- `captures/`: real output of the search library (posting lists, analyzer output, BM25 explanations) that the screens replay.
- `timings.json`: every sentence's id, text and start and end time.

Check every frame against the narration sentence it belongs to (the sentence with that id in timings.json) and against the evidence:
1. Every on-screen text, number and formula matches the narration, the evidence table and the data, and never says something stronger than the narration or something the evidence doesn't cover. Check the arithmetic shown on screen.
2. Nothing overlaps, is cut off, or runs off the frame; every label is legible at 1080p.
3. The thing the viewer must watch for that sentence is visible, and each animation has finished (or is clearly under way) by the frame for its sentence; nothing the sentence talks about is missing, and nothing on screen belongs to a different sentence.
4. The same thing keeps the same name and colour throughout (ice blue: the query and the current selection; amber: costs and measured numbers; the grade chips 2 / 1 / 0 keep their colours; coral: a failure).
5. Anything that would confuse this audience, or anything that looks like a rendering glitch.

Report findings grouped as MUST FIX (wrong, contradicts the narration or evidence, unreadable, or broken), SHOULD FIX (confusing, cluttered, mistimed), and NIT. For each: the sentence id, what you see, what is wrong, and the fix. End with a line "FRAMES: PASS" if there are no MUST FIX items, otherwise "FRAMES: FIX".
