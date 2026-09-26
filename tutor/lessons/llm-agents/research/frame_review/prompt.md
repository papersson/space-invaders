You are reviewing the frames of a finished narrated explainer video (1920x1080, dark background) before it is published. You have not seen how it was made. Everything you need is in this folder:

- pages/sN_pK.png: frames from chapter N. Each page holds up to six frames, each taken just before the end of one narrated sentence and labelled in red with that sentence's id (e.g. s3_07). Frames are downscaled to 860 px wide, so text that is barely legible here is roughly 2.2x larger in the real video.
- sentences.txt: every narrated sentence, by id.
- script_and_evidence.md: the locked script (narration, plus a *Screen:* note per chapter saying what should be on screen) and the evidence table (every claim and number, and where it comes from).
- runs.txt, overhead.txt, screen_code_check.txt: the real runs' summaries, the measured per-call overhead, and the checks that the code shown compiles and behaves as claimed.

Open and look at every page (use the Read tool on each PNG, in order s1 to s9), and read the other files. Then report findings, each with a severity (MUST FIX: wrong, misleading, contradicts the narration or evidence, unreadable, or covering what the viewer must see; SHOULD FIX: confusing, cluttered, weakly supports the line, inconsistent; NIT), the sentence id, what you see, what is wrong, and the fix. Check:
1. Every number and quoted text on screen against the narration and the evidence table (counts, token numbers, quoted replies, file names, code). Flag anything on screen that says more than, or something different from, the narration and evidence.
2. Whether the frame shows what its sentence is about, by the end of that sentence (the animation for a line should have finished or be clearly under way).
3. Layout: overlaps, text running off the frame, labels colliding with shapes, text too small to read at 1080p.
4. Text discipline: on-screen text should be names of things, real numbers and real quoted output, never sentence-length captions that repeat the narration.
5. Consistency: each colour should mean one thing throughout (grey instructions, white task, blue what the model wrote, green tool results, red a failing test, amber tokens read); the same picture should keep the same layout from chapter to chapter.
6. Anything a viewer could misread (for example a number shown beside the wrong thing, a picture that implies something the evidence does not support, a schematic that could be taken for data).
7. Any model identifier string (a "claude-..." model ID) anywhere on screen: this must never appear.

Be exacting; you are the last check before publication. End with a count of findings by severity and "FRAMES: OK" if there are no MUST FIX items, otherwise "FRAMES: FIX".
