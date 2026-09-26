## 1. Where I'd lose the thread

- **"We reach the model through Claude's command-line tool, with that tool's own tools switched off, so text is all it can give back."** — Which command-line tool? The screen just says "claude -p, tools off," which doesn't tell me what that command normally does or what "its own tools" are. I'm told they're switched off before I know what's being switched off.

- **"Most of that is fixed text: our instructions, and notes that the command-line tool we call the model through adds to every call."** — This "notes" chunk turns out to be the *majority* of the first call's tokens (≈1,180 of ≈1,400), but it's never said what these notes actually contain. I'm asked to accept a big, unexplained number.

- **"The file begins with an invisible character, called a byte order mark, glued to the front of the word 'region'."** — Fine as a plot point, but I don't know what a byte order mark is *for* or why a CSV would have one. It's presented as a fact to accept, not something I understand.

- **"The third time, it asked for the data file in a format our code didn't recognise. Our loop saw no tool call, and stopped."** — I don't follow this. How does a model's *request* come in "a format"? Isn't a tool call just JSON, as established earlier? This contradicts or complicates something I thought I already understood.

- **"Each new call re-reads everything before it, so twice the calls means more than twice the reading."** — This lands as a throwaway line, but it's actually a claim about how the cost curve bends (superlinear growth), and it goes by in one breath with no worked example the way the token numbers earlier got one.

- **"We've skipped a lot here: planning, memory that lasts between tasks, and teams of agents."** — Three unfamiliar-sounding concepts arrive back to back at the very end, right when I'm trying to hold onto the conclusion. I know they're flagged as "skipped," but they still land as loose threads.

## 2. Questions I'd ask afterward

- What exactly is "claude -p," and what do its own built-in tools normally do that got switched off?
- What's in those extra "notes" that make up most of the first call's tokens?
- Why does the sales.csv file have a byte order mark in the first place — is that a common real-world gotcha?
- What did it mean that the third run's request came in "a format our code didn't recognise" — was that a different tool-call syntax, and why would a more capable model use one?
- Is the "more capable model" a specific named model, or just "a better one" in the abstract?
- If production agents use compaction to fight context growth, does that also risk hiding the "ground truth" that made run A succeed?

## 3. What I learned (~150 words, without looking back)

An "LLM agent" is just a model in a loop: call the model, if it asks for a tool run the tool and feed the result back in, repeat until it stops asking or you hit a call limit. The model itself doesn't remember anything between calls — everything it "knows" about the task is whatever text is sent to it each time, called its context. Two runs of the same coding-fix task diverged because one had a tool to run the tests and one didn't; the one without it declared victory anyway, because nothing in its context said it was wrong — it wasn't lying, it just had no evidence against its own fix. The context also only grows over time, which gets expensive (tokens) and eventually hurts the model's recall — production systems compress it periodically, but then whatever got dropped is simply gone.

## 4. Direct answers

- **Main idea:** An agent doesn't "know" anything beyond what's currently in its context; it picks its next move from that text, not from a pre-written script. So what actually makes an agent reliable isn't how smart the model is, it's whether something in its context (like a test result) can tell it that it's wrong.
- **Numbers I remember:** Both setups were run three times each ("3 of 3"). Run A took nine model calls and read roughly 18,500 tokens total to fix two lines of code. Claude Code's own run took about 123,000 tokens over nine calls, because its first call alone was already ~11,600 tokens.
- **Starting question:** Why would taking away one tool (the ability to run the test) leave the model confidently wrong, when it was otherwise the same model doing the same task? **Answer:** Because without that tool, nothing in its context contradicted its own fix — its "Fixed" reply wasn't a lie, just an unchecked guess, whereas the version with the test tool got real feedback (a failing test) that let it catch a second bug it otherwise would have missed.

## 5. Ratings

- **Pull of the opening:** 4/5 — a concrete before/after (one passes, one silently doesn't) with a real failing-test hook made me want to know why immediately.
- **How often I felt lost:** A few times — mainly around the unexplained "notes" tokens, the byte-order-mark backstory, and the "format our code didn't recognise" moment near the end.
