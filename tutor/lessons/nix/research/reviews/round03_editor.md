# Script Review — "Why the hash?"

## Test 1 — Opening question / ending callback
**PASS.** Opening: "Why is there a hash in every path? And how does that one idea deliver all of that?" Ending directly echoes it — "So why a hash in every path? Because the path names a build by everything that went into it" — and then walks the three promises in the same order they were raised. Clean callback, no fix needed.

## Test 2 — One-sentence-per-segment chain; report every "and then"
Rebuilt chain: *Install normally → /usr/bin; install with Nix → a hashed path, why, and how does it deliver reproducibility/side-by-side/rollback? **But** shared paths break. **Therefore** name outputs by a hash of inputs, known before building. **Therefore** a changed input changes its path and everything downstream, so old and new sit side by side. [Hello also needs other paths — its closure.] **Therefore** "installed" is a profile pointing at a generation, so upgrade/rollback is switching a link. **Therefore** NixOS does the same for a whole system. **But** the hash only promises inputs, not bytes, only holds pinned, and doesn't roll back data. **Therefore**, the answer.*

**"and then" count: zero.** Good — no sequence-only joins.

- **SHOULD FIX** — The join into the closure section (§4→§5) is the one non-derived link — it's an "also," not a "therefore." Quote: *"Hello needs other things to run, like the C library."* This drops in as a new topic right after "That's how two versions coexist." Rewrite: *"But an installed package isn't self-contained — Hello still needs the C library to run. Where does it find it, if not in /usr/lib?"* — turns it into a posed problem the closure then answers, matching the causal register of every other transition.

## Test 3 — Ideas announced vs. derived from a visible problem
- **SHOULD FIX** — Same spot as above: closure is *announced* ("Hello needs other things to run... its files refer to them by their full store paths") rather than raised as a question the way §2→§3 and §2→§6 are. Rewrite per Test 2 above fixes both.
- Everything else derives cleanly: §3 (hash-of-inputs) answers §2's problem; §6 (profiles/generations) answers "what does installed even mean" posed as a question; §7 extends "the same idea" by explicit analogy.

## Test 4 — Setups without payoffs / payoffs without setups
- **SHOULD FIX** — Setup without payoff: *"Old generations stay until you delete them."* (§6). This raises "so how do you delete them, and does the store just grow forever?" and never answers it — no garbage collection ever appears in the narration despite the Deviations note claiming GC "is named in one line" (it isn't, anywhere in the script as written). Either cut the line or pay it off: *"Old generations stay until you delete them — garbage collection then frees any path nothing points to anymore."*
- All other setups pay off well: §2's "half-finished upgrade" is resolved by §6/§7's atomic link-switch; §8's "as far as possible" (from the opening promise) is the setup paid off by the 69–91% stat.

## Test 5 — Terms used before explained / concepts with two names
- **NIT** — "recipe" (§3: *"Nix computed Hello's path from its recipe"*; §8: *"Nixpkgs, the collection the recipes come from"*) is used as an informal synonym for "the build's inputs" without ever being equated to it. Minor, but it's a second name for a concept the script otherwise calls "inputs." Rewrite: drop "recipe" and just say "from its inputs" / "the collection the packages are built from," or explicitly bridge it once: *"call that bundle of inputs a recipe."*
- Everything else (hash, closure, profile, generation) is defined at first use. Fine.

## Test 6 — Numbers: list, pick 2–3 to remember, flag dead ones
All numbers: 32 characters (hash length); hello-2.12.1; gcc 13 / glibc 2.40 (screen only); five paths (closure); generation 1 / 2; boot menu 42/41/40 (illustrative); ~700,000 packages; 69–91%; 2017–2023; pinned revision 50ab793786d9.

**Worth remembering:** the **32-character hash** (the hook), **five paths** (makes "closure" concrete), **69–91% bit-for-bit** (the load-bearing limit/takeaway number).

- **NIT** — "seven hundred thousand packages" does citation-credibility work, not conceptual work; the 69–91% carries the lesson on its own. Fine to keep for rigor, just don't treat it as a number to remember.
- **SHOULD FIX** — Boot menu "Configuration 42/41/40" is explicitly invented ("illustrative") while every other number in the video is pulled from a real run (`data/nix_demo.txt`, `data/nixos_demo.txt`). This is the one place fabricated numbers sit right next to real ones with nothing on screen distinguishing them. Either generate a real boot-menu screenshot from the demo machine, or visually mark it as a mockup (dashed border, "illustration" label) so it doesn't quietly break the video's real-data credibility.

## Test 7 — Abstractions before the concrete case
- **SHOULD FIX (pattern)** — §3, §6, and §7 each open the solution with the general principle before the concrete instance: §3 *"Nix... treats a build as a pure function of its inputs"* before the Hello run; §6 *"you use a profile: a link to one generation"* before installing Hello/cowsay; §7 *"you describe the system in one file... Nix builds all of it... into one store path"* before the real config diff. The problem sections (§1–2) are concrete-first and land well; the solution sections invert that. Rewrite pattern: lead with the real artifact, name the abstraction after. E.g. for §6: *"Install Hello — the store now has one path. Ask Nix what's 'installed' and it points you to a small directory of links: a generation. That's what a profile is: a link to one of these."*

## Test 8 — Wrong intuition confronted, shown failing
**PASS, and well done.** All three parts of the stated wrong model are explicitly named and shown failing, not just corrected in prose:
- "hash = checksum of contents" — refuted by showing the path computed via `nix-instantiate` *before* anything is built ("computed, not built").
- "builds are always bit-for-bit identical" — refuted with an actual byte diff (timestamp, coral) plus the 69–91% stat.
- "rollback restores the machine" — refuted visually: system link swings back but the database cylinder/`/var` stay put, labeled "data is not rolled back."

## Test 9 — Examples named but not understood
**PASS.** Hello, cowsay, greet, nginx, and all five closure entries get enough of a functional gloss for their narrative role (none need deeper explanation than given).

## Test 10 — On-screen text repeating narration / pictures not supporting the line
- **NIT** — The three promise cards in §1 and the three recap lines in §9 paraphrase the narration closely. Acceptable as chapter-marker/recap convention, but if tightened, make the cards add something the voice doesn't say (e.g., a path fragment) rather than restate it.
- **SHOULD FIX** — Two narration lines have no corresponding image at all: §2's *"Some libraries put a version number in the file name, but most things get exactly one path"* and §3's *"Nix runs each build isolated by default, with no network and nothing outside its declared inputs."* Neither appears in the shot list. Either cut (see Test 11) or give each a beat of screen support.

## Test 11 — Lines deletable without breaking anything
- **§2**: *"Some libraries put a version number in the file name, but most things get exactly one path."* — no visual, no payoff, safely cut.
- **§3**: *"And on Linux, Nix runs each build isolated by default, with no network and nothing outside its declared inputs, so nothing gets in uncounted."* — sandbox never recurs, no visual; per the Deviations note it's meant to be "mentioned in passing," but as written it's a free-floating aside. Cut, or fold into one clause: *"...and, isolated with no network access, so nothing sneaks in uncounted."*
- These are the only two genuinely cuttable lines; nothing else is filler.

## Test 12 — Hard-to-follow sentences; rushed/padded beats
- **SHOULD FIX** — §7: *"Bringing the running machine in line with it doesn't: services restart one by one, and a new kernel needs a reboot."* The elided verb after "doesn't" is hard to parse on a single listen. Rewrite: *"But bringing the running machine in line with the new generation takes longer: services restart one by one, and a new kernel needs a reboot."*
- **SHOULD FIX (pacing)** — §8 carries three distinct limits (bytes, pinning, data) in one beat, versus one idea per section everywhere else. Consider an explicit signpost — *"Three things the hash doesn't promise..."* — or split into two beats so each limit gets room to land, matching the pacing of the rest of the video.

---

**VERDICT: PASS**
