## (1) Where I'd lose the thread

- **Ch.1, "No explanation of the colours yet"** — the script itself flags this, and I felt it: cards turn blue/green/grey and I'm told "3 of 3" with no idea yet what's being counted three times or why. I just have to trust it'll be explained later.
- **Ch.2, "with that tool's own tools switched off, so text is all it can give back"** — this uses "tools" before tools are ever defined (that happens in Ch.3). On first hearing I don't know if "that tool's own tools" means the same thing as the tools added later, or something unrelated to the command-line program itself.
- **Ch.3, "the model never executes anything on its own"** — fine, but immediately after this I'm asked to track "our code" as a new box in the diagram with no time to absorb what it does before the loop appears in Ch.4.
- **Ch.5, "The file begins with an invisible character, called a byte order mark"** — introduced and explained in one breath, then immediately followed by "The code was only half the problem" and then a brand-new term, "workflow," two sentences later. Three new concepts in one short chapter.
- **Ch.7, "it asked for the data file in a format our code didn't recognise"** — I don't know what "format" means here. A different file type? A different way of writing the tool call? The screen notes mention some XML-like tags, but the narration doesn't explain what went wrong technically.
- **Ch.7, "The code around the model isn't plumbing"** — a metaphor I had to stop and unpack: I think it means "the harness makes real decisions, it's not just neutral wiring," but it's stated as a punchline, not explained.
- **Ch.8, "twice the calls means more than twice the reading"** — I believe this because I can guess it's cumulative re-reading, but the video asserts it rather than walking through why (a running total grows faster than linearly).
- **Ch.9, "planning, memory that lasts between tasks, and teams of agents"** — three unexplained terms fired off in a single clause; fine since they're explicitly out of scope, but each one made me pause for a beat wondering if I'd missed something.

## (2) Questions I'd ask afterward

1. In Chapter 2, are "that tool's own tools" the same tools introduced in Chapter 3, or something else entirely?
2. What exactly is a byte order mark, technically — why does a CSV file have one, and is this common?
3. What was the unrecognized "format" in the third strong-model run — a different tool-calling syntax?
4. Which model was the "more capable model"?
5. Is "ground truth" specifically test results, or any tool output that contradicts the model's assumption?
6. Why does re-reading grow faster than linearly with more calls — is there a simple formula?
7. Does compaction ever throw away the one detail that mattered, and how would you know?

## (3) What I learned (~150 words, written without looking back)

An LLM agent is a model plus a loop: the model reads everything so far (its "context"), and if it asks for a tool, code that we write actually runs it and feeds the result back in. The model itself never executes anything — it only asks. Two runs of the same coding-fix task diverged because one had a "run tests" tool and one didn't. The one with tests got a real failure message (a missing "region" column caused by an invisible byte order mark) fed back into its context, so it kept working until it actually fixed the bug. The one without tests had nothing to contradict its own guess, so it confidently said "Fixed" while still broken. The model keeps no memory between calls — everything is re-sent every time, which is why context size balloons the longer a task runs. The lesson: an agent is only as reliable as what checks its work, not how smart the model is.

## (4) Direct answers

- **One main idea:** An agent's reliability comes from what feeds ground truth back into its context (like test results), not from the model's intelligence — take away the check, and the model can be confidently wrong.
- **Numbers I remember:** run A took 9 model calls and read about 18,500 tokens total to fix two lines of code; Claude Code doing the same task read over 120,000 tokens because it re-sent much larger instructions every call. I don't remember the exact per-call numbers (1,400 / 2,700ish), just that they climbed each call.
- **Question the video opened with:** why does taking away one tool (the ability to run the test) leave the same model confidently declaring success on code that's still broken?
- **Its answer:** because the model only knows what's in its context, and nothing in run B's context contradicted its fix — its "Fixed" was a reasonable conclusion from incomplete evidence, not a lie or a lesser model.

## (5) Ratings

- **Pull of the opening (1–5):** 4 — the "same model, same task, one passes one fails, and it wasn't luck" setup made me want to know why immediately.
- **How often I felt lost:** a few times — mainly around the "tools switched off" line in Ch.2 before tools were defined, and the dense stretch in Ch.7 with the unexplained "format" and the "plumbing" metaphor.
