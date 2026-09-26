You are this particular viewer:

Background

- Works in industry and wants lessons "useful in the industry day to day". Picked queueing, tail latency, and idempotency with retries from a list of practical topics.
- Keeps a personal library of prompts and references on software architecture, data systems, performance, observability and LLM agents. Likely a software, data or ML engineer. Their exact role and years of experience are unknown.
- Has watched two lessons in this series: UMAP (an earlier session) and external merge sort (version 2, 6:25).
- Assume they know: programming, how web services, APIs and databases are built and called, averages and percentiles as everyday terms, Big-O.
- Unknown: how comfortable they are with probability beyond the everyday (distributions, independence, expected value), and how much formula they want on screen.


Standing instructions for the student reviewer

Play this person: an industry engineer who knows how services are built and has everyday familiarity with averages and percentiles, but has not studied the topic. Flag every term that isn't defined on screen or in the narration, every step that needs a fact they wouldn't have, and every place where two new ideas arrive in one sentence.


 You have not studied this topic. Stay in role: if the script does not explain something, you do not know it. Below is the script of a short narrated video, with a note of what is on screen at each moment. Go through it once, in order, as if watching. (1) List every point where you would be confused or lose the thread, quoting the line: a term used before it is explained, a step that does not follow, a number with no meaning attached, a sentence hard to follow when heard. (2) List the questions you would ask afterwards. (3) Without looking back, write what you learned in about 150 words. (4) Answer: what is the one main idea; which numbers do you remember and what do they mean; what question did the video start with, and what was its answer? (5) Rate how much the opening made you want the answer (1-5) and how often you felt lost (never / once / a few times / often).


---

## Script

No length target: the length follows the argument (about 150 words per minute).

### 1. The question

> Install GNU Hello, the classic tiny test program, with a normal package manager, and it lands at slash usr, slash bin, slash hello.
> Install it with Nix, and it lands somewhere stranger: a directory in slash nix, slash store, whose name starts with thirty-two characters of what looks like noise.
> That noise is a hash, and every package Nix installs has one.
> Nix, and NixOS, the Linux distribution built on it, make some unusual promises. Build the same thing twice and, as far as possible, get the same result. Keep two versions of a package side by side. Roll back an upgrade, for one program or for the whole machine.
> Why is there a hash in every path? And how does that one idea deliver all of that?

*Screen:* two terminals. Left: `/usr/bin/hello`. Right: the real path from data/nix_demo.txt, `/nix/store/hwz2l7ihv2skq7gr5l3paavs3rr9il7z-hello-2.12.1`, with the 32-character hash highlighted in amber. Three promise cards: "same build, same result", "versions side by side", "roll back: a program or a machine". The question.

### 2. The trouble with shared paths

> Most package managers put everything in shared places. Programs go in slash usr, slash bin. Libraries go in slash usr, slash lib.
> Upgrade a library, and the new version overwrites the old one in place. Every program that used the old one now gets the new one, whether it was built for it or not.
> Two programs that need different versions of the same library often can't both have what they need. Some libraries put a version number in the file name, but most things get exactly one path.
> And an upgrade that stops halfway, say the power goes out, leaves some files new and some old: a system that matches no version at all.

*Screen:* a `/usr/lib` shelf with `libssl.so` (v1). Two programs, A and B, with arrows to it. An upgrade writes v3 over v1 (the old file is replaced); program B, built for v1, turns coral. Then a second program wants v1 while A wants v3: one slot, two arrows, conflict. Briefly, the exception: `libssl.so.1.1` and `libssl.so.3` side by side ("versioned names"), then back to the single slot. Then a half-finished upgrade: a row of files, half new (ICE), half old (grey), a power symbol, "v1 and v3 files mixed".

### 3. A build is a function of its inputs

> Nix starts from a different picture. Every package is built from a recipe, which Nix calls a derivation. Nix treats that build as a pure function of its inputs, and the inputs are everything the build uses: the source code, the build script, the compiler, the libraries, and every option.
> On Linux, Nix runs each build isolated by default, so it can use only what it declared. Even a downloaded source file has to match a hash written in the recipe.
> Nix computes a hash over all of those inputs, and names the output after it: slash nix, slash store, the hash, then the package name.
> It can do that before building anything. On this machine, Nix computed Hello's path from its recipe, and the package then landed exactly there.
> So the hash is not a checksum of what came out. It's a name for everything that went in.

*Screen:* a function box "build", drawn as a closed room ("isolated"), with inputs arriving from the left: "source: hello-2.12.1.tar.gz" (tagged "hash fixed in recipe"), "build script", "compiler: gcc 13", "library: glibc 2.40", "options". A hash forms from all of them (amber) and becomes the path. A small caption under the room: "this demo's container has no sandbox; store paths don't depend on it". The real run: `nix-instantiate … hello.outPath` → the path, labelled "computed, not built"; then `nix-build` → the same path, and `Hello, world!`.

### 4. Change an input, change the path

> Now change one input. Here, one option of Hello's build: whether to run its tests.
> The recipe is different, so the hash is different, and the new Hello gets a new path.
> A small script called greet runs Hello. Its inputs include Hello's path, so greet gets a new path too. The change ripples to everything built from it.
> Cowsay doesn't use Hello, so its path stays exactly the same.
> And nothing that was already built gets touched. The old Hello and the new Hello now sit side by side in the store, each in its own directory.
> That's how two versions coexist: they can't overwrite each other, because they never share a path.

*Screen:* a small graph: hello → greet; cowsay separate. Each node shows its real path hash (first 8 characters, from data/nix_demo.txt): hello hwz2l7ih, greet 0436w8h8, cowsay bjb2xx94. The input "doCheck = false" changes on hello; hello's hash rolls to fjshijls (amber), then greet's to dwpnpr3k (amber); cowsay's stays bjb2xx94 (ICE, "unchanged"). Then a store listing: two `…-hello-2.12.1` directories side by side.

### 5. The closure

> But Hello isn't self-contained. It needs other things to run, like the C library. So where does it find them, if not in slash usr, slash lib?
> Its files refer to them by their full store paths, hashes included.
> Nix finds those references by scanning the build's output for store paths. Follow them, and the references of those, and you get the package's closure: everything it needs at run time.
> Hello's closure is five paths: Hello itself, the C library, a library the C library pulls in, another that one needs in turn, and a small runtime library that ships with the compiler and that compiled programs use.
> Copy those five paths to another machine of the same kind, and Hello runs there. And things needed only to build it, like the compiler itself, aren't in the list.

*Screen:* the hello path with arrows to its references; the real closure from data/nix_demo.txt appears as five boxes: hello-2.12.1, glibc-2.40-66, libidn2-2.3.7, libunistring-1.2, xgcc-13.3.0-libgcc. A dashed "compiler: gcc 13" box off to the side: "build-time only, not in the closure".

### 6. Installing is switching a link

> So what does it mean to have a program installed?
> In Nix, what you have installed is a generation: a small directory of links into the store. Your profile is a link to one generation.
> Install Hello: that's generation one. Install cowsay: Nix creates generation two, with links to both, and then switches the profile's link to it, in a single step.
> There's no moment when the profile is half old and half new. It points to one generation, then to the other.
> Roll back, and the link switches back to generation one. Hello is there, cowsay is gone from the profile, and nothing in the store was deleted.
> Old generations stay until you delete them. Only then can Nix's garbage collector remove the store paths nothing else uses.

*Screen:* the real run from data/nix_demo.txt: `profile -> profile-1-link` (hello). Install cowsay: generation 2 is created alongside (links to hello and cowsay), then the profile arrow swings from 1 to 2 in one move: `profile -> profile-2-link`, `bin: cowsay cowthink hello`. `nix-env --rollback`: "switching profile from version 2 to 1"; the arrow swings back; `bin: hello`. Both generations stay visible, greyed.

### 7. A whole system

> NixOS applies the same idea to an entire operating system.
> You describe the system in configuration.nix, a file that can pull in others: the packages, the settings, the services to run. Nix builds all of it, the programs, the configuration files, the start-up scripts, into one store path.
> Here's a minimal configuration, evaluated on this machine. It has one system path. Add one line, turning on the nginx web server, and the system gets a different path. Remove the line, and the path is exactly the first one again.
> Switching to a new configuration makes a new system generation, and adds it to the boot menu. If an upgrade goes wrong, you pick the previous generation when the machine starts, or roll back from the command line.
> The link to the new generation switches in one step. Bringing the running machine in line with it takes longer: services restart one by one, and a new kernel needs a reboot.

*Screen:* a configuration.nix box (the real base.nix from data/nixos_demo.txt) → one path `…l4krbrjp…-nixos-system-…`. The line `services.nginx.enable = true;` slides in → `…4dh0ybk1…-nixos-system-…` (amber); the line slides out → `…l4krbrjp…` again (ICE, "same as before"). Then a boot menu, captioned "illustration" and drawn with a dashed border (the only invented numbers in the video), listing "NixOS - Configuration 42", "Configuration 41", "Configuration 40", with the selection moving down one.

### 8. What the hash doesn't promise

> The hash promises the same inputs. It doesn't always promise the same bytes.
> Some builds stamp in the date, or vary in small ways from run to run: same path, different bytes. A 2025 study rebuilt about seven hundred thousand packages from old Nixpkgs snapshots. Between sixty-nine and ninety-one percent came out bit-for-bit identical, rising over the years.
> And the inputs are only fixed if you fix them. Nixpkgs, the collection the recipes come from, keeps moving. To get the same inputs next year, pin the exact revision.
> Rollback switches the software and its configuration. It doesn't touch your data. Say a new version of a database converted its files to a new format. Roll back, and you get the old program, but the files stay converted, and the old program may not be able to read them.

*Screen:* a build run twice → two paths identical (ICE) but a byte diff showing a timestamp (coral): "same inputs ≠ same bytes". The study (Malka, Zacchiroli & Zimmermann, MSR 2025): "709,816 packages, 2017-2023: 69% → 91% bit-for-bit reproducible". Then "nixpkgs: pinned to 50ab793786d9" (the revision used for every path in this video). Then rollback: the system arrow swings back, but a database cylinder and `/var` stay unchanged: "data is not rolled back".

### 9. The answer

> So why a hash in every path? Because the path names a build by everything that went into it.
> That's what keeps anything from being overwritten. Versions coexist because they never share a path. Dependencies are exact, because they're referred to by their paths. And an upgrade, or a rollback, is switching one link, for a program or for a whole system.
> What the hash fixes is the inputs. Pin them, and you get the same recipe again; the bytes usually, but not always, follow. And back up your data, because rollback won't.

*Screen:* the hello path once more, the hash expanding into its inputs. Three lines: "no overwriting → versions side by side", "exact paths → exact dependencies", "switch one link → upgrade, rollback". End card with the takeaway and references: Dolstra, The Purely Functional Software Deployment Model, PhD thesis, Utrecht (2006); Dolstra, de Jonge & Visser, "Nix: A Safe and Policy-Free System for Software Deployment", LISA (2004); Dolstra & Löh, "NixOS: A Purely Functional Linux Distribution", ICFP (2008); Bruno, Nix Pills; Malka, Zacchiroli & Zimmermann, "Does Functional Package Management Enable Reproducible Builds at Scale? Yes.", MSR (2025).

