# Script Review

## Test 1 — Opening question / ending callback
**Pass, cleanly.** Opening: "does passing messages make bugs like the vanishing deposit go away?" Ending: "So does passing messages make the vanishing deposit go away? Yes." — verbatim callback, plus the screen direction returns to the exact opening image (two deposits, now landing at $200). This is the strongest structural element in the script.

## Test 2 — Chain as one sentence, "and then" audit
Chain holds together on **but/therefore** almost throughout: race → but forgettable/deadlocking lock → therefore fixed order → therefore one owner (actor) → **[and then]** CSP channels reach the same place → but check-then-act still races → therefore make it one message → but waiting processes still deadlock → therefore break the cycle → **[and then]** real-world bug data → therefore the answer.

Two "and then" joints found:
- **Section 4→5 (actors→channels).** Channels aren't required by a "but" in the argument — they're appended as a second implementation of the same idea. NIT: harmless because the script itself labels it "same idea, different plumbing," so the additive relationship is honest rather than hidden.
- **Section 7 (deadlock fix → bug study).** The Tu et al. numbers are tacked on after the fix is already demonstrated, functioning as a citation-drop rather than a further step in the causal chain. SHOULD FIX — see Test 6.

## Test 3 — Ideas announced vs. derived
- **SHOULD FIX.** Channels are introduced by taxonomy, not from a gap the actor model just left open: *"The other message-passing family works the opposite way. It comes from Tony Hoare's communicating sequential processes, or CSP..."* Nothing in section 4 creates a question that channels answer. Rewrite to derive it: *"But an actor's send doesn't wait — so how would a machine ever know a request had been received, or get an answer back? CSP channels are built around exactly that: a send waits for a receiver."* This also better sets up why channel-deadlock (section 7) is a full replay of the lock-deadlock shape.
- **NIT.** The helper-object deadlock fix in section 7 ("an account can hand the send to a helper and keep listening") is asserted, not derived — a viewer isn't told *why* moving the send off the receive path breaks the cycle. One clause would close the gap: *"...because now nothing inside the account is ever blocked waiting to send."*

## Test 4 — Setups without payoffs / payoffs without setups
- **Well-paid-off:** the Erlang/Akka aside in §4 pays off in §5 ("as in Akka") and again in §8 ("wherever the language enforces the ownership"). Keep as is.
- **SHOULD FIX — payoff without setup.** The closing duality beat — *"a lock can be built as a process: send it 'may I?'... and a Go channel is built with a lock inside"* — answers a question the script never asked. It arrives after the takeaway is essentially delivered and doesn't serve the callback to the opening question; it's the one place the ending drifts past its own landing point. Cut it, or move it earlier as a bridge between §4 and §5 where it would actually motivate why the two models can be compared at all.
- **Inconsistent rigor (setup implies a payoff-with-numbers, but two claims don't get one):** the "forgotten lock" race in §3 and the "two actors waiting on each other's replies" deadlock in §7 are both stated with no run count, unlike every sibling claim in those same sections (989→0, 482→0, 1,703→0). Not wrong, just inconsistent — a viewer may wonder why some claims get measured and others don't.

## Test 5 — Terms before explanation / duplicate names
- **NIT.** "Goroutines" (§5: *"Go also lets goroutines share memory..."*) is used without ever being introduced — the script has said "processes," "channels," "Go," but never "goroutine." One clause fixes it: *"Go also lets its goroutines — its lightweight processes — share memory..."*
- **NIT.** "One owner" and "single owner" are used interchangeably (§4 opens with "single owner," everywhere else "one owner"). Pick one term.
- Race condition vs. data race is handled deliberately and well — not a violation, this is the model of how to do test 5 correctly.

## Test 6 — Numbers
Full list: $50/$50/$100→$150/$200 (opening); 3 steps; 10,000,000×2 / 20,000,000 expected / five runs (10.2M, 10.3M, 11.7M, 11.0M, 10.1M); locked runs (20M×3); 1,000 deadlock runs (989→0); 100,000 withdrawal runs (1,703→0); 1,000 channel-deadlock runs (482→0); the study (171 bugs, 86 wrong-result [69/17], 85 hangs [36/49]).

**Worth remembering (pick 3):** $150 vs. $200 (the emblem), 1,703/100,000 → 0 (message passing still races), 17 of 86 vs. 49 of 85 (message passing causes few wrong answers but most hangs — the direct refutation of the wrong model).

- **NIT — numbers doing no work.** The five individual counter-run values (10.2M…10.1M) are more precision than the point needs; the point is "short, and different each time." Two examples would do the same job with less to track by ear.
- **SHOULD FIX — number overload at the climax.** §7's closing sentence delivers five numbers back to back (171, 86, 17, 85, 49) right at the moment the wrong model is empirically overturned — the highest-stakes beat in the script. Lead with the ratio, drop the scaffolding: *"Message passing caused only a sixth of the bugs that gave wrong answers — but nearly half of the bugs where code just hung."* Keep 171/86/85 on screen only, not spoken.

## Test 7 — Abstraction before the concrete case
No real violations. Every section leads with the concrete interleaving/scenario before naming the abstraction (lost update → data race; withdrawal race → race condition without data race). The one-owner principle in §4 is stated as the answer to a rhetorical question the concrete lock problem just raised, which is a legitimate order, not a violation.

## Test 8 — Wrong intuition
Named explicitly ("Actors and channels remove concurrency bugs...") and **shown failing** twice, with numbers: the withdrawal race (1,703/100,000 overdrawn) and the channel/actor deadlock (482/1,000 stuck; message-passing causing the majority of real-world hangs). This is the script's strongest piece of construction — no notes.

## Test 9 — Examples named but not understood
- **SHOULD FIX.** Docker, Kubernetes, etcd, CockroachDB, gRPC, BoltDB are named on screen (§7) purely for authority — none is used, none is distinguished, and the narration never engages with them individually. Either drop to "six large Go codebases" or, if the names stay, spend one clause on why they're credible evidence (e.g., "widely used, so real bugs, not toy code").
- **NIT.** Erlang and Akka get one differentiating fact each and are actually used later — these are understood at the depth needed, not a violation.
- **NIT.** "Like a cache" (final line) is a name-drop with zero elaboration — low stakes, but could be cut without loss.

## Test 10 — On-screen text vs. narration; picture/line mismatch
- **NIT.** §8: *"which steps happen as one", "no cycle of waits"* on screen is a near-verbatim restatement of the narration's own sentence. Harmless as a summary card, but it is literal duplication rather than added information.
- **NIT.** §6's label *"no data race · still a race condition"* mirrors the spoken line closely. Same verdict — acceptable as a tag, worth noting only because the brief asked for it.
- No picture found that fails to support its line — the visuals are unusually tightly bound to the argument throughout (e.g., the "forgot the lock" path literally reappearing as a wall in §4 is a good non-verbal callback).

## Test 11 — Deletable lines
- The duality passage in §8 (lock-as-process / channel-with-a-lock-inside) is the clearest candidate: removing it doesn't weaken the argument or the callback, and its absence would let the ending land more tightly on the opening question. **SHOULD FIX: cut or relocate.**
- Nothing else is safely deletable — the Erlang/Akka aside, the "sending doesn't wait" line, and "most orders of the six steps are fine" all get used later.

## Test 12 — Hard-to-follow-aloud / rushed or padded beats
- **SHOULD FIX.** §7's closing sentence (see Test 6) is the one place the script is rushed relative to its importance — five numbers in three sentences, at the point the entire wrong-model refutation lands. Give it more room: split into two beats with a pause, and lead with the ratio, not the raw counts.
- **NIT.** The Erlang/Akka sentence in §4 is a dense parenthetical-laden aside ("a message is copied to the receiver, and shared tables exist only for a process that opts in... a library for Java and Scala...") that's harder to track by ear than the rest of the script's plain declarative style. Consider shortening each clause.
- Nothing else reads as padded; the rest of the script's pacing (roughly one demonstrated claim per beat) is consistent and appropriately brisk.

---

No finding here rises to blocking: the spine (open→race→lock→deadlock→one owner→race without data race→deadlock without locks→answer) is sound, the wrong model is actually falsified on screen with numbers, and the ending calls back to the opening precisely. The fixes above are tightening, not structural surgery — mainly (a) motivate channels instead of taxonomizing them in, (b) cut or relocate the duality tangent, (c) de-densify the numbers at the §7 climax, and (d) trim the unexplained project name-drops.

**VERDICT: PASS**
