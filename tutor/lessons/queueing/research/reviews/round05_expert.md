Reviewed the script against Kleinrock/Harchol-Balter M/M/1 theory and re-derived every number (arrival rates, utilizations, T = S/(1−ρ) at 50/80/90/95%, the D/D/1 no-wait case, the M/M/8 Erlang-C sanity check, Kingman's G/G/1 approximation). The core model, all arithmetic, and the "80%→90%→95%" doubling logic all check out exactly. Findings below.

**1. SHOULD FIX — unverified chapter citation**
Quote: *"T = S / (1 − ρ): mean response time for one server with Poisson arrivals and exponential work times (the M/M/1 queue; derived in Harchol-Balter ch. 13)"*
Issue: I cannot confirm from memory that Chapter 13 of *Performance Modeling and Design of Computer Systems* (2013) is where the M/M/1 mean-response-time result is derived. A specific, wrong chapter number on an end card is exactly the kind of checkable error a knowledgeable viewer will catch, and it costs nothing to verify against the actual table of contents before locking the video.
Fix: Confirm the chapter/section against the physical book (or its published TOC) before finalizing. If verification isn't possible before the deadline, drop the chapter number and cite the book only: *"derived in Harchol-Balter, Performance Modeling and Design of Computer Systems (2013)."*

**2. SHOULD FIX — capacity-planning advice generalizes past the model**
Quote: *"That's why capacity plans leave headroom. Decide how slow requests may get, and read the load limit off the curve."*
Issue: The curve is exact only for one bottleneck resource with Poisson arrivals and exponential, memoryless service in steady state. The only caveat given ("Burstier traffic needs more headroom") addresses variability, but real capacity planning also has to contend with multiple contended resources (CPU/disk/downstream calls), non-stationary load (diurnal peaks, incidents), and finite queues/timeouts — none of which "read the load limit off the curve" warns against. As written, a viewer could reasonably take this as a literal sizing procedure rather than a first-order intuition.
Fix: *"...read the load limit off the curve — as a first-order estimate for one bottleneck resource under steady traffic. Real systems usually need more headroom than this idealized curve gives."*

**3. NIT — "spare capacity" is a coined term, not standard vocabulary**
Quote: *"Call that twenty percent the spare capacity: it's what clears the queue."*
Issue: Neither Kleinrock nor Harchol-Balter use this phrase — they just work with ρ and 1−ρ directly. It's a fine teaching device and it's clearly self-defined on screen, so this isn't an error, but a viewer who goes to the cited textbooks looking for "spare capacity" won't find it.
Fix: On its first appearance on screen, add the standard-notation gloss: *"spare capacity (1 − ρ)"* so the mapping is explicit.

**4. NIT — stability condition (ρ < 1) stated late**
Quote: formula first appears in §5 (*"T = S / (1 − ρ)"*) but the requirement that this only holds for ρ < 1 isn't said until §6's closing line about 100% utilization.
Issue: Minor sequencing point — the formula is shown as unconditionally exact before its validity condition is given.
Fix: Add *"(valid for ρ < 1)"* to the on-screen formula in §5, not just as the closing warning in §6.

Nothing else — the Kingman/G/G/1 backing for "burstier traffic makes this worse," the D/D/1 zero-wait argument, the M/M/8 pooling numbers (I cross-checked all four against an Erlang-C estimate and they land within simulation noise), and the Kleinrock/Lazowska citations for utilization and the wait/response-time split are all correct and appropriately hedged.

VERDICT: PASS
