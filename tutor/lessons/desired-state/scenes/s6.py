from dkit import *


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("What it doesn't promise")
        # 01-02: an update, applied; kubectl answers at once
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        f = VGroup(mono("web.yaml", 14, MUTED), mono("replicas: 3", 20, INK)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        fb = SurroundingRectangle(f, buff=0.25, color=DIM, stroke_width=1.5, corner_radius=0.08)
        fg = VGroup(fb, f).move_to([-4.2, 1.6, 0])
        self.play(FadeIn(fg), run_time=0.4)
        f5 = mono("replicas: 5", 20, AMBER).move_to(f[1], aligned_edge=LEFT)
        self.play(Transform(f[1], f5), run_time=0.5)
        cmd = terminal([("$ kubectl apply -f web.yaml", MUTED)], width=6.4).move_to([2.2, 1.6, 0])
        self.play(FadeIn(cmd), run_time=0.4)
        self.at("02")
        out = mono("deployment.apps/web configured", 17, ICE).next_to(cmd, DOWN, 0.15).align_to(cmd, LEFT).shift(0.25 * RIGHT)
        self.play(FadeIn(out), run_time=0.3)
        at_once = mono("(at once)", 14, MUTED).next_to(out, RIGHT, 0.2)
        self.play(FadeIn(at_once), run_time=0.3)

        # 03-06: status catches up
        self.at("03")
        bar_bg = Rectangle(width=5.0, height=0.3, stroke_color=DIM, stroke_width=1.5, fill_color=PANEL, fill_opacity=1)
        bar_bg.move_to([0.6, -0.4, 0])
        segs = VGroup(*[Rectangle(width=1.0, height=0.3, stroke_width=0, fill_color=ICE, fill_opacity=0.8)
                        .move_to(bar_bg.get_left() + (0.5 + i) * RIGHT) for i in range(5)])
        ready = mono("ready: 3/5", 20, INK).next_to(bar_bg, LEFT, 0.4)
        self.play(FadeIn(bar_bg), FadeIn(segs[:3]), FadeIn(ready), run_time=0.5)
        self.at("04")
        self.play(FadeIn(segs[3]), Transform(ready, mono("ready: 4/5", 20, INK).move_to(ready)), run_time=0.4)
        self.at("05")
        self.play(FadeIn(segs[4]), Transform(ready, mono("ready: 5/5", 20, ICE).move_to(ready)), run_time=0.4)
        self.at("06")
        st = VGroup(ready, bar_bg, segs)
        sb = SurroundingRectangle(st, buff=0.2, color=ICE, stroke_width=1.8, corner_radius=0.08)
        sl = mono("status: the current state, as observed", 15, ICE).next_to(sb, DOWN, 0.15)
        self.play(Create(sb), FadeIn(sl), run_time=0.6)

        # 07-10: applying records; getting there is separate
        self.at("07")
        rec = mono("apply: records what you want", 17, INK).move_to([-2.6, -2.3, 0])
        self.play(FadeIn(rec), run_time=0.4)
        self.at("08")
        slow = mono("getting there: separate, slower", 17, MUTED).move_to([2.9, -2.3, 0])
        self.play(FadeIn(slow), run_time=0.4)
        self.at("09")
        never = mono("sometimes never: a copy that can't start", 16, BAD).move_to([0, -2.85, 0])
        self.play(FadeIn(never), run_time=0.4)
        self.at("10")
        self.play(Indicate(sb, color=ICE, scale_factor=1.03), run_time=0.8)

        # 11-12: a moving target
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        x0, x1, base = -5.0, 1.0, -1.2
        def X(t):
            return x0 + (x1 - x0) * t / 12
        def Y(n):
            return base + 0.45 * (n - 3)
        target = [3, 3, 5, 5, 5, 4, 4, 6, 6, 6, 5, 5]
        actual = [3, 3, 3, 4, 5, 5, 4, 4, 5, 6, 6, 5]
        tp = VMobject(stroke_color=AMBER, stroke_width=3).set_points_as_corners(
            [p for t, n in enumerate(target) for p in ([X(t), Y(n), 0], [X(t + 1), Y(n), 0])])
        ap = VMobject(stroke_color=ICE, stroke_width=3).set_points_as_corners(
            [p for t, n in enumerate(actual) for p in ([X(t), Y(n) - 0.05, 0], [X(t + 1), Y(n) - 0.05, 0])])
        kt = VGroup(mono("desired", 14, AMBER), mono("current", 14, ICE)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        kt.move_to([X(12) + 0.8, Y(5), 0])
        mt = mono("never settles while the target moves", 16, MUTED).move_to([X(6), Y(3) - 0.8, 0])
        self.play(FadeIn(kt), run_time=0.3)
        self.at("12")
        self.play(Create(tp), Create(ap), run_time=2.4, rate_func=linear)
        self.play(FadeIn(mt), run_time=0.4)

        # 13-16: two tools pulling one field
        self.at("13")
        fld = VGroup(mono("replicas", 15, MUTED), mono("3", 30, INK)).arrange(DOWN, buff=0.1)
        fbx = SurroundingRectangle(fld, buff=0.25, color=TRAY_EDGE, stroke_width=2, corner_radius=0.08)
        fgp = VGroup(fbx, fld).move_to([4.6, 0.6, 0])
        self.play(FadeIn(fgp), run_time=0.4)
        self.at("14")
        auto = mono("autoscaler: follows the load", 15, AMBER).move_to([4.6, 2.2, 0])
        self.play(FadeIn(auto), run_time=0.4)
        v6 = mono("6", 30, AMBER).move_to(fld[1])
        self.play(Transform(fld[1], v6), run_time=0.4)
        self.at("15")
        job = mono("job: re-applies the file", 15, ICE).move_to([4.6, -1.0, 0])
        self.play(FadeIn(job), run_time=0.4)
        v3 = mono("3", 30, ICE).move_to(fld[1])
        self.play(Transform(fld[1], v3), run_time=0.4)
        self.at("16")
        for v, col in (("6", AMBER), ("3", ICE), ("6", AMBER), ("3", ICE)):
            self.play(Transform(fld[1], mono(v, 30, col).move_to(fld[1])), run_time=0.35)
            self.wait(0.15)

        # 17-18: what no tool manages
        self.at("17")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        managed = RoundedRectangle(corner_radius=0.15, width=6.2, height=3.0, stroke_color=ICE, stroke_width=2).move_to([-2.0, 0.2, 0])
        ml = mono("managed by the configuration", 15, ICE).next_to(managed, UP, 0.12)
        inside = VGroup(*[server(f"web-{i}", -4.1 + 1.45 * i, 0.2, w=1.2, h=0.7) for i in range(4)])
        self.play(Create(managed), FadeIn(ml), FadeIn(inside), run_time=0.7)
        self.at("18")
        out = server("db-old", 3.9, 0.2, color=FAINT)
        out[0].set_stroke(FAINT)
        hand = mono("setting changed by hand", 14, BAD).next_to(out, UP, 0.2)
        inv = mono("unmanaged: invisible", 16, MUTED).next_to(out, DOWN, 0.25)
        self.play(FadeIn(out), FadeIn(hand), run_time=0.5)
        self.play(FadeIn(inv), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
