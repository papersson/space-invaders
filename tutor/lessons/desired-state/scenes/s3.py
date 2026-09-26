from dkit import *


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("The loop")
        # 01-04: the thermostat
        self.at("01")
        dial = Circle(radius=1.25, stroke_color=TRAY_EDGE, stroke_width=3, fill_color=TRAY_FILL, fill_opacity=1)
        dial.move_to([-3.8, 0.3, 0])
        cap = label("thermostat", 15).next_to(dial, UP, 0.25)
        self.play(FadeIn(c), FadeIn(dial), FadeIn(cap), run_time=0.6)
        self.at("02")
        setv = mono("set  21°", 22, AMBER).move_to(dial.get_center() + 0.35 * UP)
        self.play(FadeIn(setv), run_time=0.4)
        self.at("03")
        room = ValueTracker(18)
        roomt = always_redraw(lambda: mono(f"room {int(round(room.get_value()))}°", 22, INK)
                              .move_to(dial.get_center() + 0.3 * DOWN))
        heat = mono("heating: on", 18, AMBER).next_to(dial, DOWN, 0.3)
        loop = Loop(("measure", "compare", "act"), center=(2.6, 0.2))
        self.play(FadeIn(roomt), FadeIn(loop), run_time=0.6)
        self.play(FadeIn(heat), loop.spin(1, 1.6), run_time=1.6)
        self.at("04")
        self.play(room.animate.set_value(21), loop.spin(1, 1.6), run_time=1.6)
        off = mono("heating: off", 18, MUTED).move_to(heat)
        self.play(Transform(heat, off), run_time=0.4)

        # 05-07: Kubernetes works the same way
        self.at("05")
        self.play(FadeOut(dial), FadeOut(cap), FadeOut(setv), FadeOut(roomt), FadeOut(heat), run_time=0.5)
        loop2 = Loop(("measure", "compare", "act"), center=(-3.3, 0.4))
        self.play(ReplacementTransform(loop, loop2), run_time=0.6)
        loop = loop2
        self.at("06")
        ctl = label("controller", 15).move_to(loop.center_pt)
        self.play(*loop.relabel(("desired", "current", "act on the difference"), size=15), FadeIn(ctl), run_time=0.8)
        code = VGroup(mono("for {", 16, INK), mono("  desired := getDesiredState()", 16, INK),
                      mono("  current := getCurrentState()", 16, INK), mono("  makeChanges(desired, current)", 16, INK),
                      mono("}", 16, INK)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        box = SurroundingRectangle(code, buff=0.3, color=DIM, stroke_width=1.5, corner_radius=0.1)
        src = mono("Kubernetes docs, \"Writing Controllers\"", 13, MUTED).next_to(box, DOWN, 0.15).align_to(box, LEFT)
        cg = VGroup(box, code, src).move_to([3.0, 0.5, 0])
        self.play(FadeIn(cg), run_time=0.7)
        self.at("07")
        self.play(loop.spin(1, 1.4), run_time=1.4)

        # 08-13: count the pods
        self.at("08")
        self.play(FadeOut(cg), run_time=0.4)
        des = mono("desired: replicas = 3", 20, AMBER).move_to([3.0, 2.2, 0])
        self.play(FadeIn(des), run_time=0.5)
        self.at("09")
        row = VGroup(*[pod([1.8 + 1.1 * i, 0.9, 0]) for i in range(3)])
        pl = mono("pod", 14, MUTED).next_to(row[0], DOWN, 0.15)
        rc = mono("replica count", 14, MUTED).next_to(des, DOWN, 0.15)
        self.play(FadeIn(row), FadeIn(pl), FadeIn(rc), run_time=0.6)
        self.at("10")
        cnt = mono("counted: 3", 18, INK).move_to([3.0, -0.3, 0])
        self.play(FadeIn(cnt), run_time=0.4)
        cases = [("11", "counted 2 → start 1", AMBER), ("12", "counted 4 → delete 1", AMBER),
                 ("13", "counted 3 → nothing to do", ICE)]
        shown = VGroup()
        for i, (cue, text, col) in enumerate(cases):
            self.at(cue)
            t = mono(text, 18, col).move_to([3.0, -1.1 - 0.5 * i, 0])
            shown.add(t)
            self.play(FadeIn(t), loop.spin(1, 1.0), run_time=1.0)

        # 14-19: three in the morning, step by step
        self.at("14")
        self.play(FadeOut(shown), FadeOut(cnt), FadeOut(row), FadeOut(pl), FadeOut(rc), FadeOut(des),
                  FadeOut(loop), FadeOut(ctl), run_time=0.5)
        x0, x1 = -5.6, 5.6
        axis = Line([x0, -0.4, 0], [x1, -0.4, 0], stroke_color=FAINT, stroke_width=2)
        def X(minute):
            return x0 + (x1 - x0) * minute / 7.0
        ticks = VGroup(*[VGroup(Line([X(m), -0.5, 0], [X(m), -0.3, 0], stroke_color=FAINT, stroke_width=2),
                                mono(f"03:{m:02d}", 14, MUTED).move_to([X(m), -0.8, 0])) for m in range(0, 8)])
        self.play(Create(axis), FadeIn(ticks), run_time=0.7)
        self.at("15")
        m0 = VGroup(Dot([X(0), -0.4, 0], color=BAD), mono("stops reporting", 15, BAD).move_to([X(0) + 0.9, 0.15, 0]))
        self.play(FadeIn(m0), run_time=0.4)
        m1 = VGroup(Dot([X(0.7), -0.4, 0], color=AMBER),
                    mono("machine loop: unreachable", 15, AMBER).move_to([X(0.7) + 1.3, 0.75, 0]))
        self.play(FadeIn(m1), run_time=0.5)
        self.at("16")
        band = Rectangle(width=X(5.7) - X(0.7), height=0.28, stroke_width=0, fill_color=AMBER, fill_opacity=0.35)
        band.move_to([(X(0.7) + X(5.7)) / 2, -0.4, 0])
        bl = mono("grace period: 5 min by default", 15, AMBER).move_to([(X(0.7) + X(5.7)) / 2 + 0.6, -1.35, 0])
        self.play(FadeIn(band), FadeIn(bl), run_time=0.6)
        self.at("17")
        m2 = VGroup(Dot([X(5.7), -0.4, 0], color=INK), mono("copy no longer counts", 15, INK).move_to([X(5.7) - 0.3, 0.15, 0]))
        self.play(FadeIn(m2), run_time=0.5)
        self.at("18")
        m3 = VGroup(Dot([X(5.9), -0.4, 0], color=ICE),
                    mono("pod controller: counted 2 → start 1", 15, ICE).move_to([X(5.9) - 1.9, 0.75, 0]))
        self.play(FadeIn(m3), run_time=0.5)
        self.at("19")
        nb = mono("nobody had to do anything", 18, MUTED).move_to([0, -2.3, 0])
        self.play(FadeIn(nb), run_time=0.4)

        # 20: the name
        self.at("20")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        loop2 = Loop(("desired", "current", "act"), center=(0, 0.1), r=1.5)
        name = T("reconciliation loop", 30, INK).next_to(loop2, DOWN, 0.5)
        self.play(FadeIn(loop2), run_time=0.5)
        self.play(FadeIn(name), loop2.spin(1, 1.5), run_time=1.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
