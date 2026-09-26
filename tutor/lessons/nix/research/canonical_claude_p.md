Note: I attempted to verify a few citation details via web search but don't have search permission in this session, so the following draws on my trained knowledge. I've marked genuinely uncertain details as such rather than asserting them.

# Nix / NixOS — Canonical Treatment

## 1. Canonical worked examples
Two, serving different purposes:
- **GNU Hello** (`stdenv.mkDerivation` building the `hello` package) — the standard *hands-on/tutorial* example. Used throughout **Nix Pills** (Luca Bruno et al., nixos.org/nix-pills, pills 1–7 build it up from a raw `gcc` invocation to a full derivation) and in the official **nix.dev** "packaging existing software" tutorial. This is the one you'd show on screen for "here's what a derivation looks like."
- **Multiple coexisting variants of a package (classically Subversion/Apache/OpenSSL builds)** — the standard *motivating* example in the foundational papers, illustrating the "variability problem" (many builds of the same logical package differing in version or compile-time options, which conflict under `/usr/lib`-style managers). This is the running example in Dolstra, Visser & de Jonge, **"Nix: A Safe and Policy-Free System for Software Deployment,"** LISA '04, and in Dolstra's PhD thesis (below).

GNU Hello is the more commonly reused example in teaching material today; the Subversion/variability example is more common in the original research literature as the *problem statement*.

## 2. Standard progression
Consistent across the thesis, LISA'04 paper, Nix Pills, and Dolstra's conference talks:
1. **Motivate with "dependency/DLL hell"** — imperative package managers (APT/RPM, or Windows DLL replacement) overwrite shared, mutable paths, so upgrading a shared library breaks unrelated programs.
2. **Introduce content-addressed store paths** — `/nix/store/<hash>-name-version`, hash derived from build inputs. Simpler version shown first: just hashing the *name+version*; then generalized to hashing the *entire input closure* (source, dependencies, build script).
3. **Introduce the derivation as a "pure function"** — a build action (inputs → output path) is deterministic given its inputs, drawing an explicit analogy to pure functions in functional programming (this is the "purely functional" in the model's name).
4. **Show atomic upgrade via symlink switching** — profiles/generations are just symlinks repointed atomically (`rename(2)`), giving atomic upgrade and instant rollback "for free," without new machinery.
5. **Explain garbage collection as the dual operation** — old generations are just unreferenced store paths; GC is reachability analysis from GC roots (profiles), explicitly analogized to a language runtime's garbage collector (heap = store, roots = profiles).
6. **Generalize to the whole OS (NixOS)** — same model applied one level up: the entire system configuration (kernel, systemd units, `/etc`) is itself one derivation graph, so system upgrades/rollbacks reuse the identical mechanism.

Source for this exact ordering: Dolstra's PhD thesis, **"The Purely Functional Software Deployment Model,"** Utrecht University, 2006 (Ch. 1–2 for 1–4, later chapters for GC and generalization), and Dolstra & Löh, **"NixOS: A Purely Functional Linux Distribution,"** ICFP 2008 (journal version: *Journal of Functional Programming* 20(5–6), 2010; a third co-author, possibly Nicolas Pierron, on the journal version — **uncertain**, please verify before citing in the video).

## 3. Models and terminology
- **Nix store**: the immutable repository of store paths, `/nix/store/<hash>-<name>`.
- **Derivation**: a build action, represented as a `.drv` file produced by evaluating a Nix expression; roughly "a Makefile rule, but pure and hashed."
- **Store path hash**: by default **input-addressed** — the hash is a function of the *declared inputs* to the derivation, not of the actual output bytes. Nix later added experimental **content-addressed derivations** (hash of actual output content) — see Nix RFC 62; still an experimental feature as of my knowledge, treat as an "extra," not core.
- **Closure**: the full transitive set of a store path's dependencies. Note the term clashes with "closure" in functional programming (function + captured environment) — worth a one-line disambiguation in the video.
- **Generation / profile**: a versioned, named symlink tree representing one point-in-time configuration (per-user profile or whole-system generation).
- **GC roots**: live references (profile symlinks, running processes) that keep store paths from being collected.
- **"Purely functional"**: describes the *deployment model* (builds as pure functions of declared inputs), not a claim that the packaged software itself is pure or that builds are bit-reproducible.
- **Cross-source terminology**: **GNU Guix** uses the same core vocabulary (store, derivations) but expressed in Guile Scheme rather than the Nix language — see Ludovic Courtès, **"Functional Package Management with Guix,"** 2013 (ELS 2013 / arXiv:1305.4584), and the GNU Guix Reference Manual.

## 4. Key results/guarantees and where they stop holding
- **Distinct configurations get distinct, non-conflicting paths** — holds as long as the store is treated as read-only (enforced by filesystem permissions) and all build inputs are actually declared (undeclared/impure inputs, e.g. absolute-path leakage, break this — discussed as a known limitation in the thesis).
- **Safe caching/substitution**: because the store path is a hash of declared inputs, a binary cache (e.g. `cache.nixos.org`) can serve a pre-built output instead of rebuilding — this assumes the *build itself* is deterministic; Nix does not enforce this by default, it only sandboxes builds (network access blocked) to reduce nondeterminism.
- **Fixed-output derivations** are the explicit escape hatch: for things that must fetch from the network (`fetchurl`), the *output hash* is declared and verified instead of derived from inputs — this is a commonly-tested exam-style nuance.
- **Atomic upgrade/rollback**: guaranteed by `rename(2)` atomicity of the profile/generation symlink swap; this covers *activation* of a new generation, not the state of already-running stateful services (a rolled-back database schema is not automatically reverted).
- **GC safety**: never deletes anything reachable from a GC root; breaks down if a program has an "impure runtime dependency" not captured in its closure (e.g. `dlopen`/`exec` of a path outside the closure) — flagged explicitly in the thesis's limitations discussion.
- **NixOS whole-system guarantee**: the entire OS config (minus stateful data) is reproducible/rollback-able the same way; **explicitly does not cover user/application data** (databases, `/home`) — repeatedly stated caveat in the NixOS manual.

## 5. Standard concrete examples as they appear canonically
- The GNU Hello derivation built up incrementally (Nix Pills #1–7).
- A store path shown literally, e.g. `/nix/store/b6gvzjyb2pg0kjfwrknmuz0z9roxu2vk-glibc-2.31`, to teach the `hash-name-version` structure (Nix manual / nix.dev).
- Two versions of the same library (canonically OpenSSL 1.0 vs 1.1, or two versions of GCC) installed and used simultaneously via `nix-shell -p`.
- The rollback demo: `nixos-rebuild switch` creating `/nix/var/nix/profiles/system-N-link` generations, boot-menu entries per generation, then rolling back with `nixos-rebuild switch --rollback` or selecting an older boot entry — this exact demo appears in nearly every canonical NixOS conference talk.
- A minimal `configuration.nix` (`environment.systemPackages = [ pkgs.hello ];`) as the standard first NixOS example.

## 6. Common misconceptions and how the canonical treatment corrects them
- *"Nix guarantees bit-reproducible builds by default."* — No: it guarantees deterministic **store paths as a function of declared inputs**; actual byte-for-byte output determinism is a separate, harder property (see the Reproducible Builds project, reproducible-builds.org). The thesis is careful to distinguish these.
- *"The Nix language is Haskell."* — It's a small, lazy, dynamically-typed DSL, Haskell-inspired but distinct (nix.dev "Nix language basics" addresses this directly).
- *"Declarative means nothing gets executed."* — Building the closure still runs arbitrary bash builder scripts; "declarative" describes specifying the desired end-state, not the absence of imperative execution underneath.
- *"Old generations are free."* — Rollback requires keeping old store paths around; disk usage grows until `nix-collect-garbage` runs (a standard FAQ item).
- *"Purely functional" describes the software, not the model.* — It describes treating builds as pure functions in the deployment model itself (Dolstra's own framing in the thesis title/intro).

## 7. For a short lesson
- **Essential**: dependency-hell motivation; hash-of-inputs store paths; derivation-as-pure-function; version coexistence; atomic symlink-swap upgrade/rollback; GC-as-reachability; one NixOS demo (switch + rollback) as the "same idea, one level up" payoff.
- **Common extra** (include if time allows): binary caches/substituters exploiting the hash to skip rebuilds; a one-line mention of flakes as the modern reproducible-inputs interface.
- **Leave out**: content-addressed derivations/RFC 62 (still experimental); full Nix language semantics (laziness, attribute sets); Guix comparison in depth; the thesis's formal operational-semantics chapter; NixOps/home-manager ecosystem tooling.

## 8. Real systems and mechanisms, canonically cited
- **Nix/NixOS**: content-addressed `/nix/store`, Linux-namespace sandboxed builders (Dolstra thesis; nix.dev).
- **GNU Guix**: same model, Guile Scheme front-end, transactional upgrades for Guix System (Courtès 2013; GNU Guix Reference Manual).
- **Docker/OCI images** (contrast case): mutable layered filesystem, tag-addressed not input-hash-addressed — routinely used in talks to contrast with Nix's content addressing.
- **Bazel** (convergent, not derived from Nix): hermetic build actions keyed by action hash for remote caching — cited as an independently-arrived-at similar idea in industry build systems (Bazel docs on remote caching/hermeticity).
- **APT/RPM** (the negative example): shared mutable paths, the "dependency hell" Nix was built to fix — the explicit foil in the LISA'04 paper.

## 9. Overstated or subtly wrong claims
- "Nix eliminates dependency conflicts entirely" — it eliminates *path* conflicts for declared dependencies; undeclared/impure runtime dependencies can still break the model.
- "NixOS is stateless" — only the system closure is; application/user data is explicitly out of scope.
- "A Nix hash proves the software is safe" — it proves the build is a faithful, repeatable function of specific inputs, not that those inputs are trustworthy.
- "Nix replaces containers/VMs" — it solves dependency versioning on one kernel; it doesn't provide network/cgroup isolation unless combined with those tools.
- "Rollback restores your data" — false; a very common newcomer assumption directly addressed in the NixOS manual/FAQ.

## 10. Animation vs. hands-on vs. reading
- **Narrated animation**: the store/hash concept, the dependency closure graph, and the symlink-swap for atomic upgrade/rollback — these are spatial "boxes and arrows" mental models, and this is literally how Dolstra's own conference slides present them.
- **Hands-on/interactive**: writing a derivation, running `nix-build`, inspecting `/nix/store`, running `nixos-rebuild switch` and rolling back, running two versions side-by-side with `nix-shell -p` — the state changes are concrete and the CLI feedback is what cements "coexisting versions" and "instant rollback" as real, not theoretical.
- **Reading**: Nix language syntax/semantics, the precise caveats (fixed-output derivations, content-addressed derivations, sandbox exceptions), and up-to-date CLI syntax (the Nix CLI has changed substantially with flakes) — these need precise, re-checkable text rather than a one-pass narration, so point viewers to nix.dev/NixOS manual for current commands rather than trusting a script frozen at recording time.
