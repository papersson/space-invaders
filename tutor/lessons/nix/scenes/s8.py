from nkit import *


class S8(CueScene):
    SEG = "s8"

    def construct(self):
        c = chip("What the hash doesn't promise")
        hp = demo_path("hello")
        # 01-03: same inputs, not always the same bytes
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        a = store_path(hp, 15, hash_color=GOOD).move_to([0, 2.2, 0])
        al = mono("same inputs → same path", 16, GOOD).next_to(a, DOWN, 0.2)
        self.play(FadeIn(a), FadeIn(al), run_time=0.6)
        self.at("02")
        def row(n, same, diff_bytes):
            return VGroup(mono(f"build {n}:  … {same}", 16, INK), mono(diff_bytes, 16, BAD), mono("…", 16, INK)).arrange(RIGHT, buff=0.18)
        diff = VGroup(row(1, "2d 00 32 30 32", "35 2d 30 33"), row(2, "2d 00 32 30 32", "36 2d 31 31")).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        diff.move_to([0, 0.4, 0])
        ill = mono("illustration", 13, MUTED).next_to(diff, UP, 0.12).align_to(diff, LEFT)
        self.play(FadeIn(diff), FadeIn(ill), run_time=0.6)
        self.at("03")
        mark = SurroundingRectangle(VGroup(diff[0][1], diff[1][1]), buff=0.08, color=BAD, stroke_width=2)
        dl = mono("a timestamp baked in: same path, different bytes", 16, BAD).next_to(diff, DOWN, 0.3)
        self.play(Create(mark), FadeIn(dl), run_time=0.6)

        # 04-05: the study
        self.at("04")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        st = VGroup(mono("Malka, Zacchiroli & Zimmermann, MSR 2025", 15, MUTED),
                    mono("709,816 packages rebuilt from Nixpkgs snapshots, 2017-2023", 18, INK)).arrange(DOWN, buff=0.15)
        st.move_to([0, 1.8, 0])
        self.play(FadeIn(st), run_time=0.6)
        self.at("05")
        ax = Line([-4, -1.2, 0], [4, -1.2, 0], stroke_color=FAINT, stroke_width=1.5)
        b1 = Rectangle(width=1.4, height=2.4 * 0.69, stroke_width=0, fill_color=ICE, fill_opacity=0.7)
        b1.move_to([-1.8, -1.2, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.4, height=2.4 * 0.91, stroke_width=0, fill_color=ICE, fill_opacity=0.9)
        b2.move_to([1.8, -1.2, 0], aligned_edge=DOWN)
        t1 = mono("69%", 20, INK).next_to(b1, UP, 0.1)
        t2 = mono("91%", 20, INK).next_to(b2, UP, 0.1)
        y1 = mono("oldest snapshots", 14, MUTED).next_to(b1, DOWN, 0.15)
        y2 = mono("newest", 14, MUTED).next_to(b2, DOWN, 0.15)
        cap = mono("bit-for-bit identical", 16, ICE).move_to([0, -2.3, 0]).next_to(VGroup(y1, y2), DOWN, 0.2)
        self.play(Create(ax), GrowFromEdge(b1, DOWN), GrowFromEdge(b2, DOWN), FadeIn(t1), FadeIn(t2), FadeIn(y1),
                  FadeIn(y2), FadeIn(cap), run_time=0.9)

        # 06-08: the inputs are fixed only if you pin them
        self.at("06")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        mv = mono("nixpkgs: the recipes, always moving", 20, INK).move_to([0, 1.2, 0])
        self.play(FadeIn(mv), run_time=0.5)
        self.at("07")
        revs = VGroup(*[mono(r, 15, FAINT) for r in ("older", "…", "50ab793786d9", "…", "newer")])
        revs.arrange(RIGHT, buff=0.5).move_to([0, 0.2, 0])
        self.play(LaggedStart(*[FadeIn(r, shift=0.2 * LEFT) for r in revs], lag_ratio=0.2), run_time=1.0)
        self.at("08")
        pin = mono("pinned: nixpkgs 50ab793786d9  (every path in this video)", 17, AMBER).move_to([0, -0.9, 0])
        self.play(revs[2].animate.set_color(AMBER), FadeIn(pin), run_time=0.6)

        # 09-12: rollback switches software, not data
        self.at("09")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        sysv = VGroup(box("system gen 2: db v2", 3.0, 1.6, w=3.6, size=15), box("system gen 1: db v1", 3.0, 0.2, w=3.6, size=15))
        cur = box("current", -1.4, 1.6, w=1.8, color=AMBER, edge=AMBER)
        ca = arrow(cur.get_right(), sysv[0][0].get_left(), color=AMBER)
        self.play(FadeIn(sysv), FadeIn(cur), GrowArrow(ca), run_time=0.6)
        self.at("10")
        cyl = VGroup(Ellipse(width=1.6, height=0.45, stroke_color=INK, stroke_width=2),
                     Line([-0.8, 0, 0], [-0.8, -1.1, 0], stroke_color=INK, stroke_width=2),
                     Line([0.8, 0, 0], [0.8, -1.1, 0], stroke_color=INK, stroke_width=2),
                     Arc(radius=0.8, start_angle=PI, angle=PI, stroke_color=INK, stroke_width=2).stretch(0.28, 1).shift(1.1 * DOWN))
        cyl.move_to([-3.8, -1.6, 0])
        dv = mono("/var: your data", 15, MUTED).next_to(cyl, UP, 0.15)
        self.play(FadeIn(cyl), FadeIn(dv), run_time=0.5)
        self.at("11")
        fmt = mono("files converted to v2 format", 15, AMBER).next_to(cyl, RIGHT, 0.3)
        self.play(FadeIn(fmt), run_time=0.4)
        self.at("12")
        ca1 = arrow(cur.get_right(), sysv[1][0].get_left(), color=AMBER)
        self.play(Transform(ca, ca1), run_time=0.5)
        nr = mono("data is not rolled back: v1 may not read v2 files", 16, BAD).move_to([0.6, -2.9, 0])
        self.play(FadeIn(nr), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
