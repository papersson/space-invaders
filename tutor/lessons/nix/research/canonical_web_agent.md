# Nix and NixOS: the canonical treatment

**Sources used throughout.** Short tags point to these.

- **[D06]** E. Dolstra, *The Purely Functional Software Deployment Model*, PhD thesis, Utrecht University, 2006. This is the primary source. Ch. 1 covers the problem, Ch. 2 the overview, Ch. 3 "Deployment as Memory Management", Ch. 4 the language, Ch. 5 the extensional model, Ch. 6 the intensional model and Ch. 7 Nixpkgs.
- **[DJV04]** Dolstra, de Jonge, Visser, "Nix: A Safe and Policy-Free System for Software Deployment", USENIX LISA 2004.
- **[DL08]** Dolstra and Löh, "NixOS: A Purely Functional Linux Distribution", ICFP 2008. An extended version with Pierron appeared in JFP 20(5–6), 2010 **[DLP10]**.
- **[Pills]** L. Bruno, *Nix Pills* (2014, now at nixos.org/guides/nix-pills).
- **[NixMan]** the Nix Reference Manual; **[NixOSMan]** the NixOS Manual; **[nix.dev]** the official tutorials.
- **[MZZ24]** Malka, Zacchiroli and Zimmermann, "Reproducibility of Build Environments through Space and Time", ICSE-NIER 2024. **[MZZ25]** the same authors, "Does Functional Package Management Enable Reproducible Builds at Scale? Yes.", MSR 2025.
- **[Courtès13]** L. Courtès, "Functional Package Management with Guix", European Lisp Symposium 2013.
- **[BSalC18]** Mokhov, Mitchell and Peyton Jones, "Build Systems à la Carte", ICFP 2018.

---

## 1. The canonical worked example

**GNU Hello is the standard example and the more common of the two.** It is a toy Autoconf program that prints "Hello, world".
- [D06] §2.2 says: "In computer science's finest tradition we will start with 'Hello World'; to be precise, a Nix expression that builds the GNU Hello package… It is representative of what one must do to deploy a component using Nix." The thesis carries `hello-2.1.1` through install, upgrade to 2.1.2, rollback, garbage collection, the store derivation and the closure (§2.2–2.4).
- [D06] §1.2 also uses an RPM `hello` package with an `xhello` front-end as the example of the imperative model being replaced.
- Nix Pills use GNU Hello in Pills 8–9 (generic builder, then runtime dependencies).
- nix.dev's "Packaging existing software" tutorial starts with `hello-2.12.1`.
- Nixpkgs still ships `pkgs/by-name/he/hello/package.nix` as the reference package.

Why Hello is the standard:
- It is small and uses the ordinary `configure; make; make install` build, so all attention goes to what Nix changes: `--prefix=$out`, declared inputs, and a hashed output path.
- Its runtime closure is tiny (glibc, plus gcc until the RPATH is shrunk), so the difference between build-time and runtime dependencies is visible. Perl is a build-only input in [D06] §2.4.

**The competing example is Subversion with OpenSSL, used in the research papers.**
- [DJV04] says outright: "As a running example for this paper we will use the Subversion version management system."
- It is used for multiple versions and variants: optional Berkeley DB, SSL, Apache (WebDAV) and zlib support, with `assert` consistency checks ([DJV04] Fig. 1–3; [D06] Fig. 2.9).
- [D06] Fig. 2.1 shows Subversion 1.1.4 and 1.2.0 side by side, each linked against a different OpenSSL. This is the standard picture of versions coexisting.

**Supporting examples that recur:**
- **Firefox**:
  - the dependency-hell graph in [D06] Fig. 1.5;
  - a GTK 2.2.4→2.4.13 change rippling through the hashes to Firefox in Fig. 2.3;
  - the Subversion and Firefox user-environment and generation figure in [D06] Fig. 2.11. That figure still appears in [NixMan] "Profiles".
- **For NixOS**:
  - a `configuration.nix` with `services.sshd.enable` and `forwardX11`, and the NTP service job ([DL08] Fig. 8, 10, 12);
  - in today's manual, `services.httpd.enable = true;` is the first configuration example ([NixOSMan] "Configuration Syntax").

---

## 2. The standard progression

**Thesis and papers ([D06] Ch. 1–2; [DJV04]; [DL08] §2–5):**
1. **The problem with the imperative model.** RPM or dpkg install into global paths (`/usr/bin/hello`). Dependencies are *nominal* ("hello >= 1.0"). Upgrades are destructive and non-atomic. There is DLL or dependency hell and incomplete deployment ([D06] §1.2).
2. **The Nix store.** Each package lives in `/nix/store/<hash>-name-version`, where the hash covers *all build inputs*. This gives non-interference and exact dependency identification ([D06] §2.1).
3. **Nix expressions.** A package is a *function* of its dependencies (Hello). It has a builder script, and a separate *composition* calls the function ([D06] §2.2).
4. **Package management.** `nix-env -i`, upgrade, `--rollback`, user environments (profiles and generations as symlinks) and garbage collection ([D06] §2.3).
5. **Store derivations.** Evaluation is two-stage: instantiate to a `.drv`, then realise to an output. Closures follow ([D06] §2.4).
6. **Deployment policies and channels**, then **transparent source/binary deployment** through substitutes ([D06] §2.5–2.6).
7. **Foundations.** The memory-management analogy (Ch. 3), the language (Ch. 4), the extensional (input-addressed) model (Ch. 5) and the intensional (content-addressed) model (Ch. 6).
8. **NixOS** ([DL08] §5). Configuration files are derivations. Services and `/etc` are built too. The whole system is one derivation plus an activation script. `configuration.nix` drives `nixos-rebuild switch`, the system profile and the GRUB menu of generations. The paper ends with an evaluation of purity and of mutable state.

**Nix Pills (the canonical tutorial):**
- Order: why Nix → install → profiles and environment → language → functions and imports → **Pill 6**, a raw `derivation` with a fake builder → **Pill 7**, a working builder (`echo foo > $out`, then compiling a `.c` file) → **Pill 8**, GNU Hello with a generic builder → **Pill 9**, automatic runtime dependencies (hash scanning, `patchelf --shrink-rpath`) → `nix-shell` → the garbage collector → inputs, callPackage and override patterns → **Pill 18**, how store paths are computed → stdenv.
- Simpler versions come first. The raw `derivation` built-in comes before `stdenv.mkDerivation`. A hand-written builder comes before the generic builder. Input-addressed paths come before fixed-output paths.

**nix.dev:**
- "First steps": `nix-shell -p cowsay lolcat` → reproducible scripts → declarative shells → **pinning Nixpkgs**.
- Then language basics → packaging (hello, then icat) → callPackage → the module system → NixOS VMs and tests.

**Common simplifications, taught before the full version:**
- an imperative profile (`nix-env`) before declarative configuration (NixOS or flakes);
- a single package before the whole OS;
- the input-addressed model before content addressing;
- source builds before binary caches ("binary deployment is an optimisation of source deployment", [D06] §2.6).

---

## 3. The models and their terminology

**The imperative or destructive deployment model** (RPM, dpkg/APT, Portage):
- Files go into shared global locations (FHS).
- Dependencies are nominal (name plus version range) and may be incomplete.
- Upgrades overwrite files in place and are not atomic.
- Only one version per path.
- [DL08] §2 describes the filesystem as "mutable global variables … no referential transparency."

**The purely functional deployment model** ([D06] §2.1):
- A package is the output of a build function whose inputs are all declared.
- The output is stored under a path derived from a hash of those inputs and is never modified afterwards (read-only).
- [D06]: "the contents of a component depend exclusively on the build inputs. Therefore we call this a purely functional model."
- **What it guarantees by construction:**
  - different inputs give different paths, so installing one thing cannot overwrite another;
  - an undeclared store dependency fails *deterministically* at build time.
- **What it assumes:** builders are deterministic enough.

**Extensional model = input-addressed** ([D06] Ch. 5, §5.7):
- The path is computed from the derivation *before* building. It is SHA-256 over the `.drv` with the output field blank, truncated to 160 bits and printed as 32 base-32 characters ([Pills] 18).
- The outputs of the same derivation are *assumed* interchangeable: "two … components are considered extensionally equal if they behave the same way" (timestamps are tolerated).
- This is still the default today.

**Intensional model = content-addressed** ([D06] Ch. 6):
- The path is the hash of the output *contents*, found by hash-rewriting self-references.
- It is motivated by securely sharing a store and by trusting substitutes. It was only a prototype in 2006.
- Today it exists as *content-addressed (floating CA) derivations*. This is RFC 0062, experimental since Nix 2.4 (the `ca-derivations` flag). It adds "early cutoff": if a rebuilt dependency is bit-identical, its dependents are not rebuilt.

**Fixed-output derivation (FOD):** the output hash is declared in advance (for example `fetchurl { hash = … }`). The path depends only on that hash, and the builder is given network access ([NixMan] glossary; [Pills] 18).

**NixOS model** ([DL08] abstract):
- "All static parts of a system (such as software packages, configuration files and system startup scripts) are built by pure functions and are immutable."
- A *configuration* is a closure in the store. An *activation* step performs the necessary side effects: starting and stopping services, creating users and linking `/etc`.

**Glossary.** Definitions follow [NixMan] "Glossary".

| Term | Meaning | Divergences and pitfalls |
|---|---|---|
| **derivation** | "can be thought of as a pure function that produces new store objects from existing store objects"; a *store derivation* is the `.drv` file | Nix jargon for a build action. [D06] says "component" and the Nix manual says "package" or "store object"; Guix also says derivation |
| **instantiate / realise** | expression → `.drv` / `.drv` → valid output, by building or substituting | British spelling "realise" is the official term |
| **store path, store object** | `/nix/store/<hash>-<name>` and its contents plus references | Guix uses `/gnu/store` |
| **reference, closure** | "the closure of the path under the references relation" | *Not* a lambda closure. It is the transitive closure of the dependency graph, a frequent confusion |
| **profile, generation, user environment** | a symlink chain `~/.nix-profile` → `profiles/default` → `default-43-link` → a store "user-env" tree of symlinks ([D06] §2.3) | NixOS: the system profile `/nix/var/nix/profiles/system-N-link`, plus `/run/current-system` |
| **substitute, substituter, binary cache** | prebuilt outputs fetched instead of built | Bazel's analogue is the remote cache |
| **purity** | [NixMan] glossary: "The *assumption* that equal Nix derivations when run always produce the same output" | Two different purities: *language purity* (evaluation has no side effects) and *build purity* (output determined by declared inputs, enforced by isolation). The manual's wording is "assumption", not "guarantee" |
| **reproducible** | Nix community: same inputs give the same build environment and path. reproducible-builds.org: "bit-by-bit identical copies of all specified artifacts" | [MZZ24] explicitly separates reproducible *build environments* from *bitwise* reproducibility |
| **hermetic** (Bazel) | builds see only declared inputs | roughly Nix "pure" plus sandboxing |
| **channel vs. pinning vs. flake lock** | a moving URL of Nixpkgs vs. a fixed revision vs. `flake.lock` | Flakes (RFC 0049) are still an *experimental* feature in upstream Nix. Determinate Nix 3.0 (Mar 2025) declared them stable. Treat current status as uncertain |
| **build-system theory** | [BSalC18] §5.4 classifies Nix as using *deep constructive traces* with a suspending, monadic scheduler | Connects input addressing to the build-systems literature |

---

## 4. Key results and guarantees: assumptions and where they stop holding

1. **Non-interference; multiple versions and variants coexist** ([D06] §2.1; [DJV04]).
   - Why it holds: any input change, applied recursively, gives a new path, and nothing is overwritten.
   - Assumes: builders write only to `$out` (enforced because builders run as unprivileged `nixbld` users, [DL08] §6.2), and the hash is collision-resistant.
   - Stops holding:
     - *Inside one process or one environment.* Two versions of a library loaded into the same process still clash. [D06] Fig. 2.9 adds `assert httpServer -> httpd.expat == expat` precisely because Apache and Subversion would otherwise load two Expats: "a runtime link error will ensue."
     - A profile cannot contain two packages that provide the same file (a collision).
     - Coexistence on disk is not coexistence of mutable user data. A newer app may migrate `~/.config` in a way the older version cannot read.

2. **Complete build-time dependencies** ([D06] §2.1, §7.1.3).
   - Why it holds: nothing sits in `/usr/lib` and the like. The builder starts with an empty environment (`PATH=/path-not-set`, `HOME=/homeless-shelter`, [Pills] 7).
   - Assumes: no access *outside* the store. [D06] §7.1.3: "there is no way that we can prevent a builder from calling /usr/bin/gcc … the main threat to the validity of the Nix approach."
   - Fixed since: the build sandbox. It became the default on Linux in Nix 2.2 (2019) and is **off by default on macOS** ([NixMan] `sandbox` setting and release notes 2.2).
   - Escape hatches: FODs (network access), `--impure`, `sandbox = false`.

3. **Complete runtime closure** ([D06] §2.1, §3.4). Runtime references are found by scanning outputs for the hash parts of input paths, which is conservative scanning like a conservative GC.
   - Assumes: there is no "pointer hiding" (compressed files, UTF-16, paths assembled at runtime). [D06] §6.8 lists the assumptions explicitly. §7.1.5 reports no instance of pointer hiding found in Nixpkgs.
   - Failure modes:
     - False positives make closures bigger (gcc in the RPATH, [Pills] 9).
     - Deliberately impure runtime paths exist, for example NixOS's `/run/opengl-driver` ([DL08] §6.2) and `/bin/sh`.
   - Formal statement: the *closure invariant*, "the set of valid paths is closed under the references relation" ([D06] §5.2.3, Invariant 3). Safe garbage collection and "copy the closure, and it runs" both rest on it.

4. **Determinism / reproducibility.**
   - Guaranteed: the same expression and the same Nixpkgs revision give the same `.drv` and the same output path.
   - *Not* guaranteed: identical output bytes (the extensional assumption, [D06] §5.7).
   - Evidence:
     - [DL08] §6.2 built 485 derivations twice. 3.4% of files differed, almost all due to timestamps, and only 42 files (0.03%) differed in size.
     - [MZZ25] rebuilt 709,816 packages from Nixpkgs 2017–2023. Bitwise reproducibility was 69%→91%, rising over time, and rebuildability was over 99%. Embedded dates caused about 15% of failures.
     - [MZZ24] rebuilt 99.94% of about 14k packages from a 6-year-old revision.
   - Requires: pinning the Nixpkgs revision, and upstream sources still being fetchable (FODs).

5. **Atomic upgrades and rollbacks** ([D06] §2.3; [NixMan] "Profiles").
   - Mechanism: build the new user environment on the side, then atomically replace the profile symlink. Nix creates a temporary symlink and `rename(2)`s it over the old one (`replaceSymlink` in the Nix source). Rollback flips it back.
   - Assumes: the old generation still exists. `nix-env --delete-generations old` or `nix-collect-garbage -d`, followed by GC, removes the ability to roll back ([D06] §2.3).
   - Covers only the *store closure and the symlinks*. It does not cover data.

6. **NixOS whole-system rollback** ([DL08] §5; [NixOSMan] "Rolling Back Configuration Changes").
   - Each `nixos-rebuild switch` makes a system generation, and every non-GC'd generation appears in the boot menu. `nixos-rebuild switch --rollback` is equivalent to `…/system-N-link/bin/switch-to-configuration switch`.
   - The build is pure and atomic. *Activation is not*: services are stopped, started or restarted one by one according to whether their unit file's store path changed ([DL08] §5).
   - Kernel and initrd changes take effect only on reboot.
   - `nixos-rebuild test` activates without adding a boot entry, so a reboot recovers.
   - **State is out of scope.** [DL08] §6.2: "NixOS does not have any mechanism to deal directly with mutable state, such as the contents of /var… the running of a system (as opposed to the configuration) is inherently stateful."
   - `system.stateVersion` exists for exactly this reason: a newer default database version "may no longer be compatible, causing applications to fail, or even leading to data loss" (nixpkgs `nixos/modules/misc/version.nix`).

7. **Transparent source/binary deployment** ([D06] §2.6). Because the path identifies the build, a binary download is a pure optimisation, and local modifications "degrade" to source builds.
   - Assumes: you trust the cache's claim that the output belongs to the derivation.
   - How that trust is handled:
     - it is the motivation for the intensional model ([D06] Ch. 6);
     - it is enforced today by signatures (`require-sigs = true`, the `cache.nixos.org-1` key, [NixMan] conf-file);
     - content-addressed paths need no signature.

8. **Safe, automatic garbage collection** ([D06] §2.3, §5.6). Only paths unreachable from GC roots (profiles, `result` links, `gcroots`) are deleted. Its safety rests on (3).

---

## 5. Standard concrete examples as they appear in the sources

**Hello as a function of its dependencies** ([D06] Fig. 2.6):
```nix
{stdenv, fetchurl, perl}:
stdenv.mkDerivation {
  name = "hello-2.1.1";
  builder = ./builder.sh;
  src = fetchurl {
    url = http://ftp.gnu.org/pub/gnu/hello/hello-2.1.1.tar.gz;
    md5 = "70c9ccf9fac07f762c24f2df2290784d";
  };
  inherit perl;
}
```

**Builder** ([D06] Fig. 2.7): `source $stdenv/setup; PATH=$perl/bin:$PATH; tar xvfz $src; cd hello-*; ./configure --prefix=$out; make; make install`

**Composition** ([D06] Fig. 2.8): `rec { hello = (import ../applications/misc/hello) { inherit fetchurl stdenv perl; }; perl = …; … }`

**Store path** ([D06] §2.1): `/nix/store/bwacc7a5c5n3qx37nz5drwcgd2lv89w6-hello-2.1.1/bin/hello`. The hash covers the sources, the build script, its arguments and environment, and all build-time dependencies.

**Upgrade and rollback session** ([D06] §2.3):
```
$ nix-env -f .../all-packages.nix -i hello   # upgrading `hello-2.1.1' to `hello-2.1.2'
$ nix-env --rollback                         # hello -v  → GNU hello 2.1.1
$ nix-env --remove-generations old; nix-store --gc
deleting `/nix/store/bwacc7a5c5n3...-hello-2.1.1'
```

**Two-stage build and closure** ([D06] §2.4):
- `nix-instantiate foo.nix` gives `…-hello-2.1.1.drv`, then `nix-store --realise` builds it.
- `nix-store -qR …-hello-2.1.1` prints glibc, linux-headers, hello and gcc. Perl is absent because it is build-only.

**Minimal raw derivation** ([Pills] 6–7): `derivation { name = "foo"; builder = "${bash}/bin/bash"; args = [ ./builder.sh ]; system = builtins.currentSystem; }` with a builder that runs `echo foo > $out`.

**Modern Hello** (nixpkgs `pkgs/by-name/he/hello/package.nix`): `stdenv.mkDerivation (finalAttrs: { pname = "hello"; version = "2.12.3"; src = fetchurl { url = "mirror://gnu/hello/hello-${finalAttrs.version}.tar.gz"; hash = "sha256-…"; }; … })`

**Variants** ([D06] Fig. 2.9 / [DJV04] Fig. 1): the Subversion function takes `sslSupport ? false, openssl ? null, …` together with `assert sslSupport -> openssl != null`. Laziness means that unused optional dependencies are never built.

**NixOS configuration** ([DL08] Fig. 12):
```nix
{ boot = { grubDevice = "/dev/sda"; };
  fileSystems = [ { mountPoint = "/"; device = "/dev/sda1"; } ];
  services = { sshd = { enable = true; forwardX11 = true; };
               xserver = { enable = true; videoDriver = "nvidia"; sessionType = "kde"; }; }; }
```
- A generated `ssh_config` references `xauth` only if `forwardX11` is set ([DL08] Fig. 8). So a configuration file carries a GC-safe dependency on a package.
- The NTP service passes `ntpd -c ${config}` a config path in the store rather than `/etc/ntp.conf`, which lets multiple instances coexist ([DL08] Fig. 10).
- Today's manual begins with `services.httpd.enable = true; services.httpd.adminAddr = …;` and then `nixos-rebuild switch | test | boot | build | build-vm` ([NixOSMan]).

**Hash propagation** ([D06] Fig. 2.3): a GTK source change produces a new GTK path and a new Firefox path, while glibc and gcc are unchanged.

---

## 6. Misconceptions practitioners bring, and the canonical correction

| Misconception | Correction (source) |
|---|---|
| "The hash in the path is a checksum of the package's contents." | By default it is the hash of the *inputs* (the `.drv`), known before building ([D06] §2.1, §2.4; [Pills] 18). Content hashes apply only to sources, FODs and CA derivations. |
| "Nix builds are bit-for-bit reproducible." | Nix guarantees identical *inputs and environment*. Identical bits are an assumption and an empirical 69–91% ([D06] §5.7; [NixMan] "purity" is an "assumption"; [MZZ25]). |
| "Rollback undoes everything." | It flips symlinks to an older closure. `/var`, databases, home directories and schema migrations are not touched ([DL08] §6.2; `system.stateVersion`; Christensen, "Erase your darlings", 2020, on state accumulating in `/etc` and `/var`). |
| "Multiple versions coexist, so any mix works." | They coexist *on disk and in separate closures*. Within one process or environment you still need consistent choices ([D06] Fig. 2.9 expat and openssl assertions). |
| "A declarative configuration is automatically reproducible." | Only if Nixpkgs is pinned. Channels move ([nix.dev] "Towards reproducibility: pinning Nixpkgs"; flakes' `flake.lock`). |
| "Nix = NixOS" / "Nix = the language". | There are four things: the Nix language, the Nix tool and store, the Nixpkgs collection, and NixOS. Nix runs on other Linux distributions and on macOS ([NixMan] Introduction). |
| "Nix is like Docker." | Nix isolates at *build* time and on disk (store paths). It provides no runtime isolation. Docker images are snapshots of imperative steps. Nix can *produce* images (nix.dev "Building and running Docker images"). |
| "`nixos-rebuild switch` is atomic." | Only the profile switch and the bootloader entry are. Activation restarts services sequentially, and the kernel needs a reboot ([DL08] §5). |
| "Closure = lambda closure." | Here it means the transitive closure over references ([D06] §3.3). |
| "Builds never touch the network." | Fixed-output derivations do, and they are checked against a declared hash ([NixMan] glossary). |
| "GC might delete something I use." | GC deletes only what is unreachable from roots. But deleting old generations and then running GC removes your rollback targets ([D06] §2.3). |

The canonical corrective device is the analogy in [D06] Ch. 3, Fig. 3.1:
- memory ⇔ disk; objects ⇔ components; addresses ⇔ paths; dangling pointer ⇔ a reference to an absent component;
- conservative GC ⇔ hash scanning;
- "typical Unix-style deployment" ⇔ assembler with no pointer discipline;
- Nix ⇔ C-level discipline, just enough for conservative GC.

---

## 7. For a short lesson

**Essential:**
- The problem: global mutable paths, destructive upgrades, nominal and incomplete dependencies.
- The store: `/nix/store/<hash-of-all-inputs>-name`, immutable.
- A package as a pure function of its inputs (Hello). A change ripples through hashes to all dependents.
- Closures: a package plus everything it references.
- Profiles and generations: an atomic symlink flip gives upgrade and rollback. Garbage collection frees what no generation references.
- NixOS: one `configuration.nix` → one system derivation → a new generation and a boot-menu entry → `switch` or `--rollback`.
- The honest limits: mutable state is not rolled back, and reproducibility means "same inputs", with bitwise reproducibility high but not guaranteed.

**Common extras:**
- binary caches and substitution;
- the build sandbox and fixed-output derivations;
- runtime-dependency scanning;
- pinning, flakes and `nix-shell`/`nix develop`;
- Subversion-style variants;
- a comparison with Guix.

**Leave out:**
- Nix language minutiae (`rec`, `with`, `inherit`, laziness semantics);
- stdenv phases and hooks, callPackage, overrides and overlays;
- module-system internals (option types, priorities);
- the exact store-path fingerprint format;
- the intensional model and CA-derivation mechanics (hash rewriting);
- the multi-user daemon and `nixbld` users; cross-compilation; Hydra;
- the politics of flake stabilisation.

---

## 8. Systems canonically cited, with their mechanisms

| System | Model | Specific mechanism |
|---|---|---|
| **RPM / dpkg-APT / Portage** | imperative (the contrast case) | FHS global paths; nominal `Requires:`; maintainer scripts; overwrite on upgrade ([D06] §1.2; [DL08] §2) |
| **Nix** | purely functional, input-addressed | hashed store paths from `.drv`; clean env and sandbox; `patchelf`/RPATH to pin libraries; reference scanning; symlink profiles; GC roots; signed substituters ([D06]; [NixMan]) |
| **NixOS** | purely functional system configuration | system toplevel derivation; `/etc` built in the store and symlinked (optionally an overlay, "atomically replaced during system switch"); `switch-to-configuration` diffs units; system profile and bootloader generations; `/bin/sh` (and today `/usr/bin/env`) as the only FHS concessions ([DL08] §5–6; [NixOSMan]) |
| **GNU Guix / Guix System** | same model, Scheme DSL | "builds upon the low-level build and deployment layer of the Nix package manager" ([Courtès13]); `/gnu/store` names contain "a hash of all the inputs"; transactional upgrades and roll-backs; `guix challenge` to verify substitutes (Guix Manual, "Features") |
| **Spack** | hash-versioned installs (HPC) | installs each concretised spec in a unique hashed prefix and RPATHs; multiple builds coexist; not a sandboxed pure-build model ([Gamblin et al., SC15]) |
| **Bazel / Buck** | hermetic build systems | declared inputs, action cache and CAS. Buck and Nix are both "deep constructive traces" in [BSalC18] |
| **OSTree / rpm-ostree (Fedora Silverblue)** | image-based atomic OS | "git for operating system binaries"; atomic deployment of whole filesystem trees and rollback, with no per-package dependency model (ostreedev docs) |
| **Docker** | runtime container images | layered filesystem snapshots from imperative Dockerfile steps; runtime isolation (often contrasted; Nix `dockerTools` builds images) |

---

## 9. Claims that are commonly overstated or subtly wrong

- **"Nix gives reproducible builds."**
  - True for inputs and environments. Not guaranteed bitwise.
  - [MZZ25] frames bitwise reproducibility as an empirical 69–91%.
  - Malka's blog "Is NixOS truly reproducible?" notes that nixos.org used "Reproducible builds and deployments" as a headline until about 2023. This comes from a secondary source, so the exact date is **uncertain**.
- **"Store paths are content hashes."** This is false for normal derivations, which are input-addressed.
- **"Dependencies are guaranteed complete."**
  - At build time this depends on the sandbox, which macOS lacks by default.
  - At runtime it depends on scanning finding references, and on no deliberate impure paths.
- **"Atomic OS upgrades."** The generation switch is atomic. Activation (services, users, `/etc` side effects) is not ([DL08] §5).
- **"Rollback restores the previous machine."** It does not restore data or state, and not after the generation has been garbage-collected.
- **"You can install any version of anything side by side."** The store allows it, but a single Nixpkgs revision usually offers one version of most packages. Old versions come from old revisions or explicit variants, and a single process or environment still needs one consistent choice.
- **"Two machines with the same `configuration.nix` are identical."** Only with the same Nixpkgs pin, the same hardware configuration and the same state.
- **"Nix is purely functional all the way down."**
  - Builders are arbitrary shell scripts. Purity is *enforced by isolation*, not by the language.
  - Escape hatches exist: FODs, `--impure`, `builtins.currentTime` outside pure-eval mode ([NixMan] `pure-eval`).
- **"Old builds are rebuildable forever."**
  - Rebuildability is over 99% in the studies above ([MZZ24] and [MZZ25]), but it depends on upstream sources still being fetchable.
  - Cache retention of old binaries is policy-dependent. Its current scope is **uncertain**.
- **"Flakes are stable" or "Flakes are experimental."** Both are true depending on the distribution: experimental upstream, stable in Determinate Nix since 2025. Mark as **uncertain or in flux**.

---

## 10. Which modality suits which part

| Content | Best learned by | Why |
|---|---|---|
| Imperative vs. functional install (overwriting `/usr/bin/hello` vs. adding a new hashed directory) | **narrated animation** | a spatial before-and-after contrast; the canonical figures ([D06] Fig. 2.1, 1.5) are already diagrams |
| Hash propagation (change GTK, and Firefox's path changes while glibc's does not) | **animation**, then **doing** | a ripple through a DAG is a temporal process ([D06] Fig. 2.3). Then change one attribute yourself and watch `nix-instantiate` print a new `.drv` path |
| Profiles, generations, atomic symlink flip, rollback, GC from roots | **animation** | pointer-chain and mark-sweep dynamics ([D06] Fig. 2.11); mirrors the GC analogy |
| NixOS: `configuration.nix` → system derivation → generation → boot menu | **animation** plus **doing** | watch it once, then run `nixos-rebuild build-vm` and `switch --rollback` in a VM, where it is safe to break |
| Building Hello, inspecting `result`, `nix-store -qR`, `nix derivation show`, the sandbox rejecting an undeclared dependency | **doing** (running code) | the mechanisms become concrete only by seeing real paths and `.drv` files ([Pills] 7–9; nix.dev packaging tutorial) |
| Store-path hash computation | **doing** (an exercise) | [Pills] 18 has you reproduce the hash by hand; a small interactive "which paths change?" simulator works well |
| Guarantees vs. assumptions, the extensional model, pointer hiding, the trust model, reproducibility statistics, what rollback does not cover | **reading** | these are careful qualifications and numbers; narration tends to flatten them into overclaims ([D06] §5.7, §6.8; [DL08] §6.2; [MZZ25]) |
| Terminology (derivation, closure, realise, profile; the two meanings of "reproducible") | **reading** (a glossary table) | reference material that is revisited, not watched |
