Reviewed the script in full against the evidence table and canonical Nix/NixOS sources (Dolstra's thesis, the LISA 2004 and ICFP 2008 papers, Nix Pills, the Nix manual). Findings below.

---

**BLOCKING**

- **Quote:** *"And on Linux, Nix runs each build isolated by default, with no network and nothing outside its declared inputs, so nothing gets in uncounted."*
  **Problem:** Stated as an unqualified rule, this is false for the most important case in the very same section: fetching source. The script's own diagram shows `source: hello-2.12.1.tar.gz` as a build input, but that tarball can only get into the store by being downloaded — and Nix permits network access during a build only for *fixed-output derivations* (e.g., `fetchurl`), precisely because their output is checked against a content hash fixed in advance rather than an input hash. This is not a minor aside; it's the mechanism that reconciles "sandboxed, no network" with "Nix can fetch sources at all," and it's covered explicitly in Dolstra's thesis (ch. 5) and every Nix Pills treatment of purity. Leaving it out lets viewers construct a mental model that collapses the first time they use `fetchurl` or ask "how did the tarball get there?"
  **Fix:** *"...Nix runs each build isolated by default: no network, nothing outside its declared inputs — with one exception. Fetching a source file is itself a build, but a special kind: one where the *output's* hash, not the inputs', is fixed in advance, so it's allowed the network access needed to fetch it."* (Or, more simply, drop "no network" as a blanket claim and instead say builds see "nothing outside their declared inputs," saving the fixed-output/network nuance for wherever `fetchurl` is discussed.)

---

**SHOULD FIX**

- **Quote:** *"It can do that before building anything. On this machine, Nix computed Hello's path from its recipe, and the package then landed exactly there. So the hash is not a checksum of what came out. It's a name for everything that went in. And on Linux, Nix runs each build isolated by default..."*
  **Problem:** Placed right after "on this machine," the sandboxing claim reads as describing *that* demo run. The evidence notes the demo actually ran with the sandbox off (the container has no namespaces) and that store paths don't depend on it. That's a defensible production choice, but as written a careful viewer could conclude the recorded build was sandboxed, which it wasn't.
  **Fix:** Decouple the two sentences, e.g. move the sandboxing sentence earlier (as a general property of Nix on Linux) or add a light qualifier: *"Nix is designed to run each build isolated by default on Linux..."* so it doesn't read as a claim about the specific machine/run just shown.

- **Quote:** *"Install cowsay: Nix builds generation two, with links to both, and then switches the profile's link to it, in a single step."*
  **Problem:** Terminology slip. A generation isn't *built* — cowsay is built (as a derivation); the generation is a directory of symlinks that Nix *creates/assembles* from already-built store paths. Using "builds" here, right after several sections that use "build" specifically to mean "run a derivation and produce a hashed output," teaches students to conflate the two distinct operations.
  **Fix:** *"Install cowsay: Nix creates generation two, with links to both, and then switches the profile's link to it, in a single step."*

---

**NIT**

- **Quote:** *"You describe the system in one file, configuration.nix"*
  **Problem:** True as the entry point, but in practice most real configurations `import` several files (hardware-configuration.nix, module files, etc.), so "one file" slightly overstates how NixOS configs actually look in the wild. Minor, and defensible as a simplification for a short explainer.
  **Fix (optional):** *"...in one file, configuration.nix, which can pull in others"* — only worth doing if there's word-budget to spare.

- **Citation check:** *"Malka, Zacchiroli & Zimmermann, 'Does Functional Package Management Enable Reproducible Builds at Scale? Yes.', MSR (2025)"* — the evidence table says this was checked against the arXiv abstract, and the author list (Julien Malka's work with Zacchiroli on Nix reproducibility is real) is consistent with what I know, so I have no basis to contradict it. I could not independently re-verify the exact title/venue live in this session (no web access), so flag only as a final pre-publication double-check, not a correction.

---

**What's done well, worth noting:** the input-addressing vs. reproducibility distinction (§3 vs §8) is kept clean and correctly hedged throughout ("as far as possible," "usually, but not always"); the closure definition, profile/generation mechanics, and the atomic-link-switch-vs-service-restart distinction in §7 are all precise and match the canonical sources; the rollback-doesn't-restore-data caveat is exactly the kind of thing that's easy to omit and is handled correctly here.

VERDICT: REVISE
