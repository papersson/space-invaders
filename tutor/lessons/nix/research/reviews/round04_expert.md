Reviewed the script against the evidence table and my own knowledge of the Nix/NixOS literature (Dolstra's thesis, the LISA 2004 and ICFP 2008 papers, the Nix manual, and the MSR 2025 paper). The numbers, hashes, and closure contents all check out against `data/nix_demo.txt` / `data/nixos_demo.txt` as cited, and I found no arithmetic or unit errors. The remaining issues are precision/terminology/framing problems, not outright falsehoods.

## Findings

**1. SHOULD FIX — Section 3, sandbox depiction**
> "On Linux, Nix runs each build isolated by default, so it can use only what it declared."
> *Screen:* "a function box 'build', drawn as a closed room ('isolated')"

The evidence table itself notes: *"this lesson's demo ran with the sandbox off, since the container has no namespaces."* The claim about Nix's default behavior is correct, but the screen immediately illustrates it with the real `nix-instantiate`/`nix-build` run from this un-sandboxed demo, visually labeled a "closed room." A viewer who reproduces the demo in a similar container and checks `sandbox` settings will find it off, and may reasonably feel the video implied otherwise. Add a one-line disclosure (e.g., a small caption: "this container has no sandbox; store paths don't depend on it") so the "isolated by default" claim isn't visually conflated with the specific run shown.

**2. SHOULD FIX — Section 7, "one file"**
> "You describe the system in one file, configuration.nix: the packages, the settings, the services to run."

This overstates the norm. A standard NixOS install has `configuration.nix` importing `hardware-configuration.nix` at minimum, and real configs are routinely split into modules. It's true of the minimal demo shown (`base.nix`), but stated as a general fact about NixOS it's misleading. Fix: "You describe the system starting from one entry point, configuration.nix, which can import other files: the packages, the settings, the services to run."

**3. SHOULD FIX — Section 5, "compiler's support library"**
> "a small part of the compiler's support library"

`libgcc` is GCC's runtime support library — it's linked into and used by *programs GCC compiles*, not a library that supports the compiler's own operation. "The compiler's support library" reads as if it helps gcc run, which invites exactly the wrong mental model (why would a runtime program need something that supports a compiler?). Fix: "a small runtime library that programs compiled by GCC depend on."

**4. SHOULD FIX — "recipe" vs. "derivation"**
The script consistently says "recipe" and never names the actual Nix term, "derivation." This is a defensible simplification for a general audience, but it's the single most load-bearing vocabulary word in the entire ecosystem — it appears in `nix-instantiate` output, `.drv` file names, every error message, and all further documentation a viewer will hit next. Add one aside at first use in Section 3, e.g.: "Nix calls this recipe a *derivation* — you'll see that word everywhere once you start using Nix." Leaving it out entirely is a real gap for a video whose job is to prepare viewers for what they'll see next.

## Nits (optional, low priority)

- **Section 3**, "the hash is not a checksum of what came out" — true for standard (input-addressed) derivations, which is what's shown and what's default; Nix also has an experimental content-addressed-derivations mode where output paths *do* depend on content. Not worth a caveat in an intro video, but flagging since it's a categorical statement.
- **Section 5**, "Nix finds those references by scanning the build's output for store paths" — more precisely, it scans for the specific 32-character hashes of each declared input, not for "store paths" as a generic pattern (it doesn't know what a store path looks like except via those hashes). Minor.
- **Section 9 references**, "Bruno, Nix Pills" — full name is Luca Bruno; fine as a terse citation but easy to complete.
- **Section 8**, the MSR 2025 study also reports >99% of packages were rebuildable at all (build succeeded), separate from the 69–91% that were bit-identical. Not required, but it would round out the claim rather than leaving "69–91%" looking like the study's only headline number.

## What's solid
The core arc — build as pure function of inputs, input-addressed paths, ripple/no-ripple on rebuild, closures, atomic profile/generation switching, NixOS generations, and the reproducibility caveats (timestamps, pinning, no data rollback) — is all canonical, correctly hedged, and matches Dolstra's thesis and the cited papers. The hash counts, closure membership, and percentages all match the evidence table with no arithmetic errors.

VERDICT: REVISE
