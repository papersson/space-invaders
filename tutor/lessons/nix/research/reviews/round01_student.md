Playing the reviewer, going through the script once as if watching:

## 1. Points where I'd be confused (quoting the line)

- **"A build is a function of its inputs."** — I know "function" from programming, but here it's suddenly applied to a whole build process (source, compiler, libraries, options). It took me a beat to realize this is a metaphor for "pure function," not literal code — the video doesn't pause to make that mapping explicit.
- **The terminal screen with `nix-instantiate … hello.outPath` and `nix-build`** — these two commands flash by with no narration distinguishing what each does differently. I can guess "one computes the path, one builds it," but that's inference on my part, not something I was told.
- **"Nix finds those references by scanning the build's output for store paths."** — this is a step that doesn't fully follow for me. Scanning output files for hash-looking strings and treating them as real dependencies sounds fragile — how does it avoid false positives (e.g., a string that happens to look like a store path but isn't actually used)? Not addressed.
- **"You use a profile: a link to one generation, which is a small directory of links into the store."** — two new terms, "profile" and "generation," land in the same sentence, and "generation" is defined circularly in terms of the thing it's supposed to explain ("a directory of links"). I had to reread this mentally to keep the two straight.
- **"There's no moment when the profile is half old and half new"** vs. later **"the services restart one by one, and a new kernel needs a reboot."** These feel like they contradict each other. The first says switching is atomic; the second says switching isn't a single step. I get that the *link swap* is atomic while the *effects* roll out gradually, but the video doesn't flag that these are different claims about different things — it reads as a walk-back.
- **"Between sixty-nine and ninety-one percent came out bit-for-bit identical, rising over the years."** — "rising over the years" with no years spoken aloud (they're only on screen). Heard without watching, this is a number with no timeframe.
- **"To get the same inputs next year, pin the exact revision."** — revision of *what*? I inferred "Nixpkgs" from context, but the sentence itself doesn't say it, and "pin" is used as if pre-defined.

## 2. Questions I'd ask afterward

- Is the atomic "switch one link" the actual mechanism (a symlink rename), or is that my own inference? The video never quite says *why* it's atomic.
- How does closure-scanning avoid mistaking coincidental hash-like strings for real dependencies?
- If old generations "stay until you delete them," doesn't the store just grow forever until you remember to garbage-collect? What's the operational cost of that?
- Is "pinning a revision" basically the same idea as a lockfile in npm/pip, just applied to the whole package set?
- When a config switch needs a reboot (new kernel), is the system considered "switched" before or after that reboot?

## 3. What I learned (~150 words, without looking back)

Nix installs packages into paths that include a hash, and that hash isn't a checksum of the built output — it's computed from everything that goes into the build (source, compiler, build script, options), before building even starts. Because the path depends on inputs, changing any input produces a new path, so old and new versions can sit side by side without overwriting each other. Programs reference their dependencies by exact store paths rather than shared system locations, which is why builds are reproducible and exact. Installing/upgrading works by switching a symlink-like pointer ("profile") from one "generation" to another, which is why rollback is just switching that pointer back rather than uninstalling things. NixOS extends this to entire system configurations. The hash guarantees identical inputs, not necessarily identical output bytes, and rollback affects software/config only, not your data.

## 4. Direct answers

- **One main idea:** every Nix package's path is a name derived from all of its build inputs, and that one fact (input-derived, collision-free paths) is what makes reproducibility, side-by-side versions, and atomic rollback all possible.
- **Numbers I remember:** the closure of Hello was **5 paths**; a 2025 study rebuilt about **700,000 packages** and found **69–91%** bit-for-bit reproducible. I don't remember the exact hash strings (they were long and not meant to be memorized).
- **Question the video started with:** why does every Nix package path contain a hash, and how does that single detail deliver reproducible builds, side-by-side versions, and rollback?
- **Its answer:** because the hash names a build by everything that went into it — so nothing gets overwritten, dependencies are exact, and upgrading/rolling back is just switching one link.

## 5. Ratings

- **Want-the-answer pull from the opening: 4/5** — the two contrasting file paths and the three concrete promises (reproducible, side-by-side, rollback) made me want to know the mechanism.
- **How often I felt lost: a few times** — mainly at the profile/generation double-introduction, the closure-scanning step, and the "atomic switch" vs. "restarts one by one" moment that read as a contradiction.
