You are reviewing the frames of a finished narrated explainer video, "From LLM to Agent", for a non-technical to somewhat technical audience. You have not seen it before. The files are in the current folder:

- `script.md`: the narration, chapter by chapter, with a note of what should be on screen at each moment ("Screen:"), followed by the evidence table (every number and claim, and where it comes from).
- `sheets/`: contact sheets from the 1080p render, one frame near the end of every narrated sentence, labelled with the sentence id (for example s5_14) and the time. Several sheets per chapter (s1_1.png, s1_2.png, ...). Read every sheet.
- `data/`: the data the video draws on: `trace.json` (the replayed agent run: every request and the result excerpt shown), `next_word.json` (the model's real next-word probabilities), `compound.json` (the compounding arithmetic), `runs.txt` (the three runs of the example agent), `screen_code_check.txt` (the code shown on screen, replayed and run).
- `timings.json`: every sentence's id, text and start and end time.

Check every frame against the narration sentence it belongs to (the sentence with that id in timings.json) and against the evidence:
1. Every on-screen text and number matches the narration and the evidence table, and never says something stronger than the narration or something the evidence doesn't cover.
2. Nothing overlaps, is cut off, or runs off the frame; every label is legible at 1080p.
3. The thing the viewer must watch for that sentence is visible, and each animation has finished (or is clearly under way) by the frame for its sentence; nothing the sentence talks about is missing, and nothing on screen belongs to a different sentence.
4. The same thing keeps the same name and colour throughout (blue: the model and what it writes; mint green: the program, its tools and the results it pastes back; coral: a failing test; lime: a passing one; amber: numbers).
5. Anything that would confuse this audience, or anything that looks like a rendering glitch.

Report findings grouped as MUST FIX (wrong, contradicts the narration or evidence, unreadable, or broken), SHOULD FIX (confusing, cluttered, mistimed), and NIT. For each: the sentence id, what you see, what is wrong, and the fix. End with a line "FRAMES: PASS" if there are no MUST FIX items, otherwise "FRAMES: FIX".
