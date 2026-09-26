from nkit import *

INPUTS = ["source: hello-2.12.1.tar.gz", "build script", "compiler: gcc 13", "library: glibc 2.40", "options"]


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("A build is a function of its inputs")
        # 01-03: a recipe, a pure function of its inputs
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        self.at("02")
        rec = mono("recipe  (Nix: a derivation)", 18, MUTED).move_to([-3.6, 2.7, 0])
        self.play(FadeIn(rec), run_time=0.4)
        self.at("03")
        room = RoundedRectangle(corner_radius=0.15, width=2.6, height=3.2, stroke_color=TRAY_EDGE, stroke_width=2.5,
                                fill_color=TRAY_FILL, fill_opacity=1).move_to([0.6, 0.2, 0])
        rl = mono("build", 22, INK).move_to(room)
        ins = VGroup(*[box(t, -4.3, 1.6 - 0.7 * i, w=4.2, h=0.5, size=15) for i, t in enumerate(INPUTS)])
        arrs = VGroup(*[arrow(b.get_right(), room.get_left() + (0.9 - 0.45 * i) * UP) for i, b in enumerate(ins)])
        fn = mono("output = f(all inputs)", 18, ICE).next_to(room, UP, 0.25)
        self.play(FadeIn(room), FadeIn(rl), FadeIn(fn), run_time=0.5)
        self.play(LaggedStart(*[AnimationGroup(FadeIn(b), GrowArrow(a)) for b, a in zip(ins, arrs)], lag_ratio=0.25),
                  run_time=2.2)

        # 04-05: isolated; even downloads are pinned by a hash
        self.at("04")
        self.play(room.animate.set_stroke(ICE, width=5), run_time=0.5)
        iso = mono("isolated: only what it declared", 15, ICE).next_to(room, DOWN, 0.2)
        note = mono("(this demo's container has no sandbox; store paths don't depend on it)", 12, FAINT)
        note.next_to(iso, DOWN, 0.12)
        self.play(FadeIn(iso), FadeIn(note), run_time=0.5)
        self.at("05")
        tag = mono("hash fixed in recipe", 13, AMBER).next_to(ins[0], UP, 0.08).align_to(ins[0], RIGHT)
        self.play(FadeIn(tag), ins[0][0].animate.set_stroke(AMBER), run_time=0.5)

        # 06: a hash over all of them names the output
        self.at("06")
        hsh = mono("hash(all inputs)", 18, AMBER).move_to([4.6, 1.2, 0])
        ha = arrow(room.get_right(), hsh.get_left())
        self.play(GrowArrow(ha), FadeIn(hsh), run_time=0.6)
        path = store_path(demo_path("hello"), 15, short=False).move_to([2.6, -2.7, 0])
        pa = arrow(hsh.get_bottom(), path[1].get_top() + 0.05 * UP)
        self.play(GrowArrow(pa), FadeIn(path), run_time=0.7)

        # 07-08: computed before building; the build lands there (real run)
        self.at("07")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        hp = demo_path("hello")
        t = terminal([("$ nix-instantiate --eval --strict -E '(import ./pkgs.nix).hello.outPath'", MUTED),
                      store_path(hp, 16), ], width=11.0).move_to([0, 1.4, 0])
        cn = mono("computed, not built", 16, AMBER).next_to(t, DOWN, 0.15).align_to(t, RIGHT)
        self.play(FadeIn(t), run_time=0.6)
        self.play(FadeIn(cn), run_time=0.4)
        self.at("08")
        t2 = terminal([("$ nix-build --no-out-link -A hello ./pkgs.nix", MUTED), store_path(hp, 16),
                       ("$ …-hello-2.12.1/bin/hello", MUTED), ("Hello, world!", GOOD)], width=11.0).move_to([0, -1.1, 0])
        self.play(FadeIn(t2), run_time=0.6)
        same = mono("same path", 16, GOOD).next_to(t2, DOWN, 0.15).align_to(t2, RIGHT)
        self.play(FadeIn(same), run_time=0.4)

        # 09-10: a name for what went in
        self.at("09")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        n1 = mono("not a checksum of what came out", 24, MUTED).move_to([0, 0.7, 0])
        self.play(FadeIn(n1), run_time=0.5)
        self.play(Create(Line(n1.get_left(), n1.get_right(), stroke_color=BAD, stroke_width=3)), run_time=0.4)
        self.at("10")
        n2 = mono("a name for everything that went in", 26, AMBER).move_to([0, -0.4, 0])
        self.play(FadeIn(n2), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
