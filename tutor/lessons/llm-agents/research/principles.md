# Design principles for this lesson (a checklist)

The requester asked this lesson to apply what makes 3Blue1Brown's videos work. These are design
requirements, checked at three points: when the script is drafted (before review round 1), when the
script locks, and on the contact sheets after the first full render. The Review log in SCRIPT.md says
how each one was met, and where it fell short.

| # | Principle | Test (what must be true of the finished video) |
|---|---|---|
| 1 | Open with a question the viewer wants answered | The first 30 seconds show a concrete, surprising result from a real run, before any explanation or definition. The question is spoken plainly, and nothing answers it until later. |
| 2 | Discovery order, not textbook order | The agent is built up from a bare model. Each new piece appears only after the previous version visibly fails, so the viewer could almost have invented it. At least one explicit "pause and predict" moment, with a hold long enough to think. |
| 3 | One central visual idea | One picture carries the argument and persists across chapters, with its geography unchanged. The animation is the argument: removing it would lose the point, not decoration. |
| 4 | Continuity | Objects morph and move rather than cut away, so the viewer sees what stays the same. Each term has one colour, bound to one part of the picture, in every chapter. |
| 5 | Minimal on-screen text | Labels name things or give real numbers. No sentence-length captions, no status lines that repeat the narration. Prefer showing a transformed object to writing what happened. |
| 6 | Concrete before abstract | One small real case with real numbers first, then the general rule. The tempting wrong intuition is named and shown failing on screen, not only argued against. |
| 7 | Room to breathe, and honesty | Conversational narration; holds after each reveal (narration.json `holds`). Say plainly what the lesson skips. End on the bigger picture, not a recap list. |

Series strengths to keep: every number on screen comes from a real run recorded in `sims/` and `data/`;
one question, answered at the end with the opening's own evidence; each step derived from the one before.

## Checks against the draft, the lock and the render

Filled in as the build goes: see SCRIPT.md, "Review log", section "Principles".
