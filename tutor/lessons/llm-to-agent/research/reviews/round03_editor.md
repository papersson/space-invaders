# Script Review

## 1. Opening question → ending callback
**Pass.** One question: *"How do you get from a model that writes text, to an agent that fixes a bug?"* The dashed "?" box is planted in Ch.1 and explicitly returns in Ch.8, "now filled in with the word 'harness.'" Clean, single-question bookend — no fix needed.

## 2. Segment chain (but/therefore/and then)
Reconstructing the chain from the script confirms the author's own "Chain" section: every transition is a genuine **but** (turn) or **therefore** (consequence) — e.g., Ch.2→3 "*Two facts follow... But text doesn't do anything*," Ch.5→6 "*a pass. But if the loop is that simple, why did 2023's agents get stuck?*" 
**Finding:** zero literal instances of "and then" in the narration — the connective tissue is causal throughout, not just sequential. No fix needed.

## 3. Ideas announced vs. derived from a visible problem
- SHOULD FIX — **Quote:** *"A real harness also checks permission before an edit or a command, sometimes by asking you. And since a context has a size limit, it trims the context when it fills up..."* Nothing earlier shows a risky action or an overflowing context, so both ideas arrive as assertions, not fixes to a shown problem. **Rewrite:** cut both sentences, or ground one: *"Imagine a prompt popping up before that 'edit file' step — a real harness checks with you first."*

Everything else (the request format, the three "why now" fixes) is reasonably tied to a problem already on screen.

## 4. Setups without payoffs / payoffs without setups
- The same permission-check/context-trimming lines are **payoffs without a setup** — features introduced with no earlier planted need. (Same SHOULD FIX as above; don't double-fix.)
- Everything else pays off cleanly: "knows only its context" (Ch.2) → paid off twice (Ch.4); the dashed "?" (Ch.1) → filled (Ch.8); Ben's failing test (Ch.5) → resolved via the discount fix.

## 5. Terms before explanation / concepts with two names
- SHOULD FIX — **Quote:** *"it wrote that it would explore the project, and even wrote out a command to do it. But nothing was there to run the command"* — followed shortly by *"give the model a format for **requests**."* "Command" and "request" name the same kind of thing without ever being equated, risking a viewer thinking they're different. **Rewrite:** *"it wrote out the kind of instruction we're about to call a request — but nothing was there to carry it out."*
- NIT — the "LLM" box is labelled on screen in Ch.1, before the term is narrated/defined in Ch.2. **Rewrite:** label it generically ("the model") in Ch.1 and switch the on-screen label to "LLM" exactly when Ch.2 names it.
- "Agent" is used loosely in Ch.1 before its Ch.5 definition — but this is the naive/intuitive sense the video is questioning, not a technical term jumping ahead. Not a fix, just worth noting it's intentional.

## 6. Numbers: which 2–3 matter, which do no work
Worth remembering: **95%→99% per-step reliability** (the pivot statistic), **$37 vs. $39.50** (Ben's bill — the concrete bug), **twelve requests** (nobody planned them).
- NIT — **Quote (screen):** "soup 1.5%, the 1.3%, this 1.2%" and "and" 18%, "I" 8%" — never spoken, add decorative precision with no payoff. **Rewrite:** show shorter, unlabeled bars for the unspoken candidates.

## 7. Abstraction before the concrete case
Mostly well-ordered — "tool" is named only after a tool is used; "harness" is named only after all its parts have already appeared. The one exception is the same permission-check/trimming pair (test 3/4): abstractions with no concrete instance from the run shown.

## 8. Wrong intuition — named and shown failing
**Pass.** Ch.3 explicitly stages it: *"You might picture the model reaching into the files itself... it wrote that it would explore the project, and even wrote out a command... But nothing was there to run the command, and the tests still failed."* Confronted and shown failing on screen, then reinforced at the close ("An agent is still talking. The difference is the harness").

## 9. Examples named but not understood
- SHOULD FIX — **Quote (screen):** *"2023 · early agents (AutoGPT and others)"* — named on screen only, never explained in narration, adds an unexplained brand name for a non-technical audience. **Rewrite:** drop the name ("2023 · early agents") or add one narrated clause: *"People tried, in 2023 — tools with names like AutoGPT..."*
- Claude Code and GPT-2 are both adequately grounded (behavior + reason given).

## 10. On-screen text vs. narration; unsupported pictures
- NIT — **Quote (screen):** *"edit file: prices.py (a change of blank lines only; shown, not narrated)"* — an on-screen event with nothing in the narration to anchor it. **Rewrite:** cut it from the montage, or add a half-second tag ("no real change") so it doesn't read as a mystery edit.
- The rest (equation card, glossary, numeric callouts) reinforces rather than pads — acceptable repetition.

## 11. Deletable lines
- The permission-check/context-trimming sentences (test 3) are the cleanest candidates — deletable without breaking the chain to "agent = LLM + harness."
- Minor/optional: *"Real agents use a stricter format, but the idea is the same"* — an honest hedge, harmless if kept, deletable if trimming for time.

## 12. Hard-to-follow lines / rushed or padded beats
- NIT — **Quote:** *"So it edits the lookup, so that 'gadget' finds 'Gadget.'"* — double "so" reads awkwardly aloud. **Rewrite:** *"So it edits the lookup: now 'gadget' finds 'Gadget.'"*
- NIT — Chapter 3 stacks five new ideas (bare-model failure, program, format, first request, "tool" definition) with heavy simultaneous screen choreography. Not broken, but tightest beat in the script — consider a half-beat pause after "the tests still failed" before introducing the fix.
- NIT — Chapter 5's full-run replay restarts at request #1, re-showing the same two steps already dramatized in Ch.3–4. **Rewrite:** open the montage at step 3 ("search: price_of") with a one-line recap ("...same first two steps as before, then—") to avoid retreading ground.
- The 95%→99% statistical walkthrough is dense by ear alone, but the parallel dot-row visual carries it — acceptable as designed, not a fix.

---

**Summary of fixes recommended:** unify "command"/"request" terminology; cut or ground the permission-check/context-trimming aside; drop or explain the "AutoGPT" name-drop; small phrasing/pacing polish (the double "so," the unnarrated blank-line edit, the Ch.5 recap overlap).

None of these break the throughline, the callback, or the takeaway.

VERDICT: PASS
