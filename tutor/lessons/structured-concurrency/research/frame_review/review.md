# Frame review: structured-concurrency

Scope: every frame on contact sheets s1–s8 (101 sentences). Each frame was checked against its narration line (audio/timings.json), the script's screen notes and evidence table, and data/runs.txt and data/timeline.json. All times and counts on screen match the runs: 0.10, 1.00, 1.10, 0.50, 1,000/0 tasks, Go 1,000/1,000 and 0/0. The findings below are about code, labelling, cue timing, colour and legibility.

Two claims were checked by running code in the scratchpad under Python 3.11.15, the version the evidence names. No lesson files were read for this.
- The chapter 5 code card, as shown on screen, fails to compile: `SyntaxError: 'break', 'continue' and 'return' cannot appear in an except* block`.
- A plain `except Exception as e:` around the same TaskGroup does catch the error. It reports `ExceptionGroup`.

## MUST FIX

1. **s5_01 – s5_10** (the chapter 5 code card, on screen for 10 sentences)
   - On screen: `handler_taskgroup` with `except* Exception as eg:` followed by `return "error"`.
   - Problem: this is a SyntaxError in Python 3.11 (PEP 654 forbids `return`, `break` and `continue` inside an `except*` block). I reproduced it on 3.11.15. The card can't be the code that produced the measured run, and a viewer who copies it gets a SyntaxError.
   - Fix: show exactly what sims/handler.py ran. For example, set a variable in the `except*` block and return after the `try`:
     ```
     except* Exception:
         result = "error"
     return result
     ```
     Or catch `except* ConnectionError:` and set a variable there, with no return.
   - Severity: MUST FIX

2. **s3_12 – s3_14 and s5_10** (the create_task timeline and the TaskGroup timeline where the client gives up)
   - On screen: fetch_orders runs from 0 to 0.50 s without failing. In s3_14 it goes on to 1.00 s ("runs on"). In s5_10 both bars run to 0.50 s.
   - Problem: these are the runs `cancel_create_task` and `cancel_taskgroup`, where both requests are slow and succeed. Nothing on screen says the premise changed. The viewer has been told, and has seen five times, that fetch_orders fails at 0.10 s. So these timelines contradict the setup: they seem to show fetch_orders surviving past its own failure time. Under the stated premise the task group would have acted at 0.10 s, not 0.50 s. The script's screen note says "both requests succeed after 1.0 s here", but the frames don't carry it.
   - Fix: add a scenario tag above each of these timelines, for example "this run: both requests take 1.0 s, neither fails". Or draw fetch_orders with a different, labelled duration.
   - Severity: MUST FIX

## SHOULD FIX

3. **s1_03, s1_04**
   - On screen: an empty chart with the row names, a floating "1.0 s" above the 1.0 tick, and "fails at 0.1 s" set halfway between the two rows.
   - Problem: the narration states the two durations, but no bars are drawn. "fails at 0.1 s" is the same distance from both rows, so it's unclear which row it belongs to. "1.0 s" and "0.1 s" also use a different format from "1.00 s" and "0.10 s" everywhere else.
   - Fix: draw ghost (outlined) bars, 0 to 1.00 s on fetch_user and 0 to 0.10 s on fetch_orders, with the labels inside their rows. Use two decimals.
   - Severity: SHOULD FIX

4. **s1_09 – s1_12**
   - On screen: the same fetch_user bar now ends in a "TimeoutError" cross, but "still running until 1.00 s" is still there. In s1_11–s1_12 the 1,000-request counter appears under this chart.
   - Problem: the narration is hypothetical ("if it had failed"). The frame switches to the `gather_late` run in place, with no tag, so it looks as if the real request timed out. The 1,000-request counter comes from the `gather` run, in which fetch_user succeeds, yet it sits under the TimeoutError version.
   - Fix: tag the variant ("second run: fetch_user fails at 1.00 s") or draw it dashed or ghosted. Before the counter appears, either go back to the success bar or separate the counter from the chart.
   - Severity: SHOULD FIX

5. **s3_08, s3_09** (the Python docs quote)
   - On screen: the gather docstring quote in small type. At 1080p the body is about 20 px, the attribution "Python docs, asyncio.gather:" is dimmer, and the gloss "(awaitables in the aws sequence: here, the two requests)" is about 12 px, dim grey.
   - Problem: this is the moment the video rests on ("Python's own documentation says so"), and the quote is the smallest and least prominent text on screen. The script asks for "immediately" and "won't be cancelled" to appear as they are said; neither is highlighted. The second sentence only appears at s3_09, one sentence after "doesn't cancel" is spoken.
   - Fix: enlarge the quote (at least as large as the chart labels), highlight "immediately" and "won't be cancelled", show the second sentence during s3_08, and raise the gloss's contrast.
   - Severity: SHOULD FIX

6. **s3_13, s3_14**
   - On screen: the blue "cancelled" label above fetch_user.
   - Problem: the label's last letter runs into the dashed 0.50 s line and the bar's end cap. It is squeezed between "client gives up (0.50 s)" and the bar.
   - Fix: put the label to the right of the cap, as in s5_03 ("cancelled (0.10 s)"), or above it with clearance.
   - Severity: SHOULD FIX

7. **s5_04 – s5_10**
   - On screen: several labels floating inside the chart's plot area:
     - "ExceptionGroup: [ConnectionError]" and "caught with except*…", over about 0.5–1.2 s in the fetch_orders row;
     - "tasks still running: 0" and "nothing left to fail later", over about 0.6–1.1 s;
     - "both cancelled", over about 0.85–1.05 s.
   - Problem: on a time axis, text placed over 0.6–1.2 s reads as something happening then. The script puts "ExceptionGroup: ConnectionError" on the handler's line at 0.10 s. Instead that line reads "error raised in the handler", with no time. So at s5_07 ("At a tenth of a second the handler returns") nothing on screen gives 0.10 s for the handler, unlike chapter 1's "handler returned an error (0.10 s)".
   - Fix: label the dashed line "handler raised ExceptionGroup: [ConnectionError] (0.10 s)". Move the status text ("tasks still running: 0", the except* note, "both cancelled at 0.50 s") outside the plot area, to the right of the chart or below the axis.
   - Severity: SHOULD FIX

8. **s5_06 – s5_09**
   - On screen: "caught with except*, not a plain except".
   - Problem: the label implies a plain except can't catch the error. It can: `except Exception` catches the ExceptionGroup, since ExceptionGroup subclasses Exception (checked on 3.11.15). Only a typed `except ConnectionError:` would miss it. The evidence table doesn't cover the necessity claim. The narration (s5_06, "So the handler catches it with except star, not a plain except") says the same, so raise it with the script owner as well.
   - Fix: reword to what the evidence supports, for example "an ExceptionGroup: `except ConnectionError` won't match it; `except*` does". Also make the card's handler use `except* ConnectionError`, which also fixes item 1.
   - Severity: SHOULD FIX

9. **s5_12, s5_13, s6_11, s6_12, s6_13** (cues one sentence early)
   - On screen:
     - s5_12 already has the second box ticked, with its evidence line;
     - s5_13 already has the third box ticked;
     - s6_11 already shows "not covered: a plain asyncio.create_task";
     - s6_12 already shows "about lifetimes, not shared data";
     - s6_13 already shows "races and deadlocks are still possible".
   - Problem: each of these belongs to the next sentence. The script says each box is ticked "as its guarantee is said". The viewer reads guarantee 2 while hearing guarantee 1. In chapter 3 (s3_16–s3_18) the same checklist is on time, so this is a cue-sync bug.
   - Fix: re-anchor these reveals to the start of their own sentences: tick 2 and tick 3, and the create_task, lifetimes and races lines.
   - Severity: SHOULD FIX

10. **s6_06 – s6_10** (bar colour with two meanings)
    - On screen: the retrying fetch_user bar is amber from 0.10 s to 1.10 s.
    - Problem: in chapters 1, 3 and 8, amber on a bar means "running after its handler returned, with no owner". Here the handler does wait (it returns at 1.10 s), so the same amber now means "ignored the cancel but still owned". s6_09 and s6_10 are about exactly that difference ("gather: runs on after the handler returns" against "task group: the handler waits for it"), and the colour erases it.
    - Fix: use a separate treatment for "caught the cancel, still owned", for example a hatched or outlined blue bar. Keep solid amber only for work nobody waits for.
    - Severity: SHOULD FIX

11. **s6_10 against s8_01 – s8_07, plus s2_09, s3_13, s5_10, s6_07 and s4_08 – s4_10** (colour roles inverted and overloaded)
    - On screen:
      - in s6_10, "task group: the handler waits for it" is amber and the gather line is grey;
      - in chapter 8, "gather" is amber and "task group" is blue;
      - handler and error lines are white in chapters 1 and 5 but amber in s2_09 ("error at 1.10 s") and s6_07 ("handler returns (1.10 s)");
      - the client's timeout line is amber;
      - the task group's inner boundary in the block diagram (chapter 4) is amber.
    - Problem: amber is the video's colour for "escaped or unowned work". Here it also marks the task group itself, the handler's return, the client's timeout and a highlighted code line. Between chapters 6 and 8 the gather and task-group colours swap.
    - Fix: keep amber for work that nobody waits for, and blue or neutral for the task group and its boundary. Draw all handler-return lines one colour (white dashed, as in chapters 1 and 5). Give the client-timeout line its own neutral style.
    - Severity: SHOULD FIX

12. **All timeline frames** (s1_03 – s1_12, s2_08 – s2_10, s3_08 – s3_14, s5_02 – s5_10, s6_06 – s6_10, s8_01 – s8_07)
    - On screen: axis tick labels "0.0 s … 1.4 s".
    - Problem: at 1080p they are about 14 px, dark grey on near-black (contrast roughly 2:1). They are hard to read, and they are the only scale for the bars.
    - Fix: raise the tick labels to about 18–20 px at 1080p, with contrast of at least 4.5:1.
    - Severity: SHOULD FIX

13. **s7_03 – s7_06**
    - On screen: in the dashed box, "handler: already returned"; under the leaked-goroutine picture, "Go: no task group in the language" (s7_04–s7_05) and "context: Go's standard way of passing cancellation (and deadlines) to goroutines" (s7_06).
    - Problem:
      - "handler: already returned" is the key half of the picture ("waiting to hand its result to a handler that has already returned"). At 1080p it is about 14 px and very dim, which makes it nearly invisible.
      - The two definition lines sit in the diagram's caption slot, so they read as captions of the picture. The "context:" line runs a few pixels under the amber "goroutine" label, and the frame is crowded, with two code cards, the diagram, a definition and a counter.
    - Fix: make "handler: already returned" as bright as "channel" or brighter. Move the definition lines out of the diagram area, or clear the diagram when the error-group card appears.
    - Severity: SHOULD FIX

14. **s7_07 – s7_11**
    - On screen: two counter lines, "1,000 requests · goroutines left over: 1,000 · 1.2 s later: 1,000" (amber) and "1,000 requests · goroutines left over: 0 · 1.2 s later: 0" (blue).
    - Problem: once the bare-goroutine code card leaves (s7_07), nothing says which line is which. Colour is the only key. The script specifies "bare goroutines: …" and "errgroup + context: …".
    - Fix: prefix the lines "bare goroutines:" and "errgroup + context:".
    - Severity: SHOULD FIX

15. **s8_06, s8_07**
    - On screen: "still running: 1,000" inside the gather chart, over about 0.95–1.35 s, and "still running: 0" inside the task-group chart.
    - Problem:
      - The charts show one request each, so "1,000" next to a single-request timeline has no referent.
      - Placed over 1.0–1.35 s on the time axis, it also reads as "1,000 still running at about 1.3 s". The run says the opposite: the count of 1,000 was taken at 0.12 s, and 1.2 s later it was 0.
    - Fix: move both counters outside the plot area and give them context: "1,000 requests, when all handlers returned (0.12 s): 1,000 still running" against "… 0".
    - Severity: SHOULD FIX

## NIT

16. **s1_01 – s1_15**
    - On screen: no chapter title. Every other chapter has one ("WHAT A CALL PROMISES" and so on).
    - Fix: add "THE QUESTION" for consistency.
    - Severity: NIT

17. **s1_05, s1_06**
    - On screen: the fetch_user bar ends flush at the 0.10 s line.
    - Problem: until s1_07 it looks just like a request that stopped at 0.10 s, the same shape as the cancelled bars in chapter 5, minus the cap.
    - Fix: give the bar an open, fading or arrowed end while it is still growing.
    - Severity: NIT

18. **s1_10 – s1_12**
    - On screen: the arrow from "TimeoutError" to an empty circle.
    - Problem: the circle has no label, and it sits inside the plot area at about x = 1.35 s, where it can read as an event on the time axis.
    - Fix: label it "not raised · not logged" and place it clear of the axis range.
    - Severity: NIT

19. **s1_12**
    - On screen: "all handlers returned   tasks still running: 1,000". The "1,000 requests at once" line has gone.
    - Problem: the counter loses its "1,000 requests" context, and its format differs from chapter 5 ("1,000 requests · tasks still running: 0"), which is the line it will be compared with.
    - Fix: use one format, "1,000 requests · all handlers returned · tasks still running: 1,000".
    - Severity: NIT

20. **s2_03 – s2_07**
    - On screen: the caption stack "one way in, one way out / returned = finished / error → back to the caller / …".
    - Problem: "returned = finished" is set tighter to the line above than the other lines are to each other, so it looks crowded.
    - Fix: use even line spacing.
    - Severity: NIT

21. **s2_07**
    - On screen: "a black box" sits under the code card.
    - Problem: the black box is the handler, which is drawn as the box diagram on the right.
    - Fix: put the label on or next to the handler box.
    - Severity: NIT

22. **s2_08, s4_01**
    - On screen: s2_08 ("But it's slow.") shows an empty timeline with row names only. s4_01 is an empty frame with only the chapter title.
    - Fix: start the sequential bars during s2_08. Optionally put a small visual in s4_01.
    - Severity: NIT

23. **s2_09, s2_10**
    - On screen: the "error at 1.10 s" label and its dashed line start directly under the "one way in, one way out" caption.
    - Problem: the dashed line almost lines up with the handler's control arrow above, so the arrow seems to continue into the chart.
    - Fix: add vertical space between the diagram and the chart, or shift the chart.
    - Severity: NIT

24. **s3_02, s3_03**
    - On screen: "start a task" is left-aligned under its box, while "call a function" is centred under its box.
    - Fix: centre it.
    - Severity: NIT

25. **s3_12**
    - On screen: both bars are already drawn from 0 to 0.50 s and stop flush.
    - Problem: the timeout marker that explains the stop only appears in s3_13.
    - Fix: hold the bars short of 0.50 s, or show the timeout line at the same moment.
    - Severity: NIT

26. **s4_02 – s4_10**
    - On screen: the attributions "Dijkstra, 1968" and "Smith, 2018" are about 12 px at 1080p and very dim. The fourth diagram is labelled "block"; the script asks for "task group".
    - Fix: raise the contrast. Label the fourth diagram "block (task group)".
    - Severity: NIT

27. **s4_12**
    - On screen: the bracket label "tasks can't outlive this block" and the names line "Dijkstra 1968 · Sústrik 2016 · Smith 2018 · asyncio.TaskGroup: Python 3.11" are small and dim, about 15 px at 1080p.
    - Fix: enlarge both a little and brighten them.
    - Severity: NIT

28. **s5_12 – s5_14**
    - On screen: the blue evidence lines under each ticked box (for example "fetch_user cancelled at 0.10 s · ExceptionGroup: [ConnectionError]").
    - Problem: they are about 15 px at 1080p, small for the measured proof of each guarantee.
    - Fix: enlarge them a step.
    - Severity: NIT

29. **s6_06 – s6_10**
    - On screen: fetch_user changes from blue to amber at 0.10 s.
    - Problem: the script asks for "the cancellation arrow hits fetch_user at 0.10 s". There is no arrow or marker, so the colour change is the only cue for the cancel.
    - Fix: add a short arrow or tick from fetch_orders' cross to fetch_user at 0.10 s.
    - Severity: NIT

30. **s6_09, s6_10**
    - On screen: "gather: stubborn work runs on after the handler returns", placed directly under the TaskGroup retry timeline.
    - Problem: the chart above shows the handler waiting, and no gather-plus-retry run exists. The line refers back to chapter 1.
    - Fix: "before (gather, ch. 1): the work ran on after the handler returned".
    - Severity: NIT

31. **s8_03**
    - On screen: the stacked timelines only.
    - Problem: the script asks for the block diagram from chapter 4 here, where the narration says "a block that can't end until its tasks have". Nothing on screen shows the block or the owner.
    - Fix: reprise the chapter 4 block diagram, even small, beside the charts.
    - Severity: NIT

32. **s8_05 – s8_07**
    - On screen: "caller cancelled → its tasks too" next to the task-group timeline.
    - Problem: that timeline is the fetch_orders-fails run and doesn't show caller cancellation.
    - Fix: add "(ch. 5: both cancelled at 0.50 s)", or keep the line away from this chart.
    - Severity: NIT

33. **After s8_07**
    - On screen: s8_07 shows the takeaway under the charts. None of the sampled frames shows the script's end card with references (Smith 2018, Sústrik 2016, Dijkstra 1968, Python docs, JEP 533/543, Kotlin docs, SE-0304).
    - Fix: confirm the references card is rendered after the last sentence. It can't be verified from sentence-end frames.
    - Severity: NIT

Counts: MUST FIX 2 · SHOULD FIX 13 · NIT 18

FRAMES: FIX
