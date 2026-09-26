Note: I attempted to verify these with a live search, but web search permission wasn't granted in this session, so this is from trained knowledge — I've flagged confidence levels below and you should check primary sources for the granular numbers before citing them yourself.

## 1) Optimal/max length of lecture videos — Guo, Kim & Rubin (2014)

**Citation:** Guo, P. J., Kim, J., & Rubin, R. (2014). "How Video Production Affects Student Engagement: An Empirical Study of MOOC Videos." *Proceedings of the First ACM Conference on Learning @ Scale (L@S '14)*, pp. 41–50.

**Design:** Analyzed engagement logs from **6.9 million video-watching sessions** across **4 HarvardX/MITx edX courses**, using both session duration and interaction data (pauses, skips, drop-off points).

**Headline finding (high confidence):** Engagement — measured as how long students actually watched relative to video length — **drops off sharply once videos exceed about 6 minutes**, essentially independent of the video's total length. Beyond that point, median watch time plateaus rather than scaling with video length, so a 20-minute video does not get proportionally more watch-time than a 6-minute one — it just gets a similar absolute amount of attention followed by a much lower completion percentage.

**Practical conclusion drawn by the authors and widely cited since:** keep videos to **roughly 6 minutes, and generally under ~9–12 minutes**, chunking longer material into multiple short videos rather than one long one.

**Secondary finding (high confidence):** Production style also mattered — videos with an informal, "talking head + tablet drawing" (Khan Academy-style) feel, and instructors speaking relatively fast/enthusiastically, sustained engagement better than highly polished studio lecture recordings, but this effect was smaller than the length effect.

**⚠️ Uncertain / not verified here:** I recall the paper presenting a table of median-engagement-percentage by length bucket (e.g., very short videos watched close to 100%, tapering into the 30–40% range for very long videos), but I can't vouch for the exact percentages without checking the paper directly — treat any specific percentage figure as approximate until confirmed against the source.

This finding was later synthesized into practitioner/academic guidance by:
**Brame, C. J. (2016). "Effective Educational Videos: Principles and Guidelines for Maximizing Student Learning from Video Content." *CBE—Life Sciences Education*, 15(4), es6.** — which explicitly cites Guo et al. and recommends segmenting instructional video into **chunks of 6 minutes or less**, tying the recommendation directly to Mayer's cognitive-load-based segmenting principle (see below).

## 2) Mayer's segmenting principle / cognitive load theory

**Core source:** Mayer, R. E. (2009, 2nd ed.; 2021, 3rd ed.). *Multimedia Learning*. Cambridge University Press.

Mayer's Cognitive Theory of Multimedia Learning (CTML) rests on three assumptions: dual-channel processing (visual/verbal), limited channel capacity (working memory limits, per Baddeley and Sweller), and active processing (learners must select, organize, integrate). Cognitive load theory (Sweller) partitions load into **intrinsic** (inherent material complexity), **extraneous** (poor design), and **germane** (schema-building) load.

**Segmenting principle (Mayer's own wording):** "People learn more deeply when a multimedia lesson is presented in learner-paced segments rather than as a continuous unit."

**Key supporting experiments:**
- **Mayer, R. E., & Chandler, P. (2001).** "When learning is just a click away: Does simple user interaction foster deeper understanding of multimedia messages?" *Journal of Educational Psychology*, 93(2), 390–397. Learners who clicked "continue" between meaningful segments of a narrated animation on lightning formation outperformed learners who watched the same content as one continuous unit on retention and transfer tests.
- **Mayer, R. E., Dow, G. T., & Mayer, S. (2003).** "Multimedia Learning in an Interactive Self-Explaining Environment." *Journal of Educational Psychology*, 95(4), 806–813. Extended the segmenting/interactivity result.
- **Spanjers, I. A. E., van Gog, T., & van Merriënboer, J. J. G. (2010).** "A Theoretical Analysis of How Segmentation of Dynamic Visualizations Optimizes Students' Learning." *Educational Psychology Review*, 22(4), 411–423. Theoretical/meta-review explaining the mechanism: pauses between meaningful segments give working memory time to finish organizing/integrating one chunk before the next arrives, preventing overload (a "transient information" cost argument).

**Effect size:** Mayer reports the segmenting principle as one of the more robust multimedia principles, with a **median effect size in the large range (Mayer cites d around ~0.9–1.0 in his summary tables across the principle's supporting studies)**. ⚠️ I'm not fully confident in the exact decimal — treat it as "large effect, consistently replicated," and verify the precise number in Mayer (2021) Table if you need to cite it exactly.

**Practical implications for splitting long explanations (well-supported by this literature):**
- Break at **conceptual/step boundaries**, not arbitrary time marks — each segment should be a complete, meaningful sub-unit (a sub-step of a procedure, one cause in a causal chain), because segmenting works by letting working memory consolidate a whole chunk, not by literally chopping runtime.
- Prefer **learner-paced** breaks (a pause, a click-to-continue, a short quiz) over forced continuous playback where possible — the *control* over pacing is part of what drove the effect in Mayer & Chandler (2001), not just the existence of a cut point.
- Related, complementary principles from the same body of work reinforce this: the **pre-training principle** (teach names/characteristics of key components before the process itself), **modality principle** (narrate over visuals rather than adding on-screen text redundant with narration, to avoid split visual attention), and **coherence principle** (cut extraneous material) — all aimed at keeping total cognitive load under working-memory capacity (~4±1 chunks; Cowan, N. (2001), *Behavioral and Brain Sciences*, 24(1), 87–114, revising Miller's classic 7±2).

## 3) Typical narration speaking rate for educational video

This is much less settled by controlled experimental research than #1 and #2 — most concrete numbers here come from **speech-communication norms and e-learning production practice**, not a single canonical study on "optimal" instructional narration rate. Flagging accordingly:

- **General conversational/lecture English speech: ~150 words per minute** is the most commonly cited baseline figure in speech-communication literature (a range of roughly **120–160 wpm** is typical for extemporaneous speech and lectures).
- **Audiobook and professional narration norms: ~150–160 wpm** (industry convention, e.g., ACX/Audible narration guidelines), somewhat higher/faster than casual conversation because it's scripted and fluent.
- **E-learning/instructional voice-over practitioner guidance** (e.g., Articulate, TechSmith production guides) commonly recommends **~130–150 wpm**, i.e., slightly *slower* than general narration, on the rationale that technical/unfamiliar content needs more processing time — this is consistent with cognitive load theory's intrinsic-load argument in #2, but I don't have a controlled peer-reviewed study pinning an exact optimal wpm for comprehension of instructional content specifically.
- **Related empirical research that does exist:** studies on **sped-up lecture video playback** (not narration rate per se, but adjacent) — e.g., work by **Murphy, D. H., Hoover, M. L., Agadzhanyan, K., Kuehn, J. C., & Castel, A. D. (2022), "Learning in double time: The effect of lecture video speed on immediate and delayed comprehension," *Applied Cognitive Psychology*, 36(1), 69–82** — found comprehension held up reasonably well up to **1.5x–2x** playback speed of normally-paced lectures (typically recorded around the ~140–160 wpm baseline), with degradation becoming more apparent beyond 2x. This is evidence that effective *perceived* information rate has some headroom above normal conversational pace, but it's about playback speed, not native narration scripting rate.

**Bottom line for #3:** cite **~150 wpm** as the standard reference point for narrated speech in general, note **~130–150 wpm** as common e-learning practitioner guidance for instructional narration, but be upfront that — unlike Guo et al. and Mayer — there isn't a single well-replicated experimental study establishing one "optimal" wpm number specifically for educational video comprehension; it's converged practitioner norms plus adjacent playback-speed research.
