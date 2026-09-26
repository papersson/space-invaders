from qkit import *

MARKS = [(0.5, 20), (0.8, 50), (0.9, 100), (0.95, 200)]


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("The curve")
        P, axes = curve_axes()
        # 01: utilization
        self.at("01")
        util = M('busy fraction = <span foreground="#8FD3FF">utilization</span>', 26, INK).move_to([2.4, 2.9, 0])
        self.play(FadeIn(c), FadeIn(axes), FadeIn(util), run_time=0.8)

        # 02-03: the simplest case
        self.at("03")
        case = VGroup(mono("one server", 18, MUTED),
                      mono("requests arriving at random (Poisson)", 18, MUTED),
                      mono("work times: mostly short, some several times longer (exponential)", 18, MUTED))
        case.arrange(DOWN, buff=0.1, aligned_edge=LEFT).move_to(P(0.03, 225), aligned_edge=LEFT)
        self.play(FadeOut(util), LaggedStart(*[FadeIn(x) for x in case], lag_ratio=0.5), run_time=1.5)

        # 04: response time = work time / spare capacity
        self.at("04")
        formula = VGroup(M('response time = <span foreground="#F2A93B">work time</span> ÷ '
                           '<span foreground="#8FD3FF">spare capacity</span>', 26, INK),
                         mono("T = S / (1 − ρ)    S: work time, ρ: utilization", 18, MUTED)).arrange(DOWN, buff=0.12)
        formula.move_to(P(0.03, 222), aligned_edge=LEFT)
        curve = mm1_curve(P)
        self.play(FadeOut(case), FadeIn(formula), run_time=0.6)
        self.play(Create(curve), run_time=2.0, rate_func=linear)

        # 05-08: the four points
        dots = VGroup()
        for i, (r, t) in enumerate(MARKS):
            self.at(f"{5 + i:02d}")
            d = Dot(P(r, t), radius=0.08, color=INK)
            lab = mono(f"{int(r * 100)}% → {t} ms", 18, INK).next_to(d, LEFT if r > 0.85 else UL, 0.12)
            self.play(FadeIn(d, scale=1.5), FadeIn(lab), run_time=0.4)
            dots.add(VGroup(d, lab))

        # 09: the simulation lands on the curve
        self.at("09")
        sims = VGroup(*[Circle(radius=0.07, stroke_color=AMBER, stroke_width=2.5).move_to(P(float(r), v))
                        for r, v in Q["mm1_sim_ms"].items() if v <= 250])
        sl = mono("circles: simulated, 20 million requests at each load", 16, AMBER).move_to(P(0.03, 180), aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(s, scale=1.4) for s in sims], lag_ratio=0.1), FadeIn(sl), run_time=1.4)

        # 10-12: flat, then steep: spare capacity halves, response time doubles
        self.at("11")
        steps = VGroup()
        for (r0, t0), (r1, t1) in ((MARKS[1], MARKS[2]), (MARKS[2], MARKS[3])):
            steps.add(Line(P(r0, t0), P(r1, t0), stroke_color=ICE, stroke_width=2),
                      Line(P(r1, t0), P(r1, t1), stroke_color=ICE, stroke_width=2))
        halves = mono("spare 20% → 10%: 50 → 100 ms", 18, ICE).move_to(P(0.03, 150), aligned_edge=LEFT)
        self.play(Create(steps[:2]), FadeIn(halves), run_time=0.8)
        self.at("12")
        halves2 = mono("spare 10% → 5%: 100 → 200 ms", 18, ICE).next_to(halves, DOWN, 0.12, aligned_edge=LEFT)
        self.play(Create(steps[2:]), FadeIn(halves2), run_time=0.8)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
