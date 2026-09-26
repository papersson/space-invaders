from qkit import *
from s2 import UNIT


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("The answer")
        # 01-02: the forty milliseconds were waiting; spare capacity halved, response time doubled
        self.at("01")
        b80 = response_bar(40, 0.9, unit=0.075, x0=-3.0, h=0.45)
        b90 = response_bar(90, -0.4, unit=0.075, x0=-3.0, h=0.45)
        n80 = mono("80% busy: 50 ms", 22, INK).next_to(b80, LEFT, 0.3)
        n90 = mono("90% busy: 100 ms", 22, AMBER).next_to(b90, LEFT, 0.3)
        w80 = mono("40 ms waiting", 18, INK).move_to(b80[0])
        w90 = mono("90 ms waiting", 18, INK).move_to(b90[0])
        self.play(FadeIn(c), FadeIn(VGroup(b80, b90, n80, n90)), run_time=0.7)
        self.play(Indicate(b80[0], color=MUTED, scale_factor=1.05), FadeIn(w80), FadeIn(w90), run_time=0.8)
        self.at("02")
        sp = VGroup(mono("spare 20%", 18, ICE).next_to(b80, RIGHT, 0.3), mono("spare 10%", 18, ICE).next_to(b90, RIGHT, 0.3))
        dbl = mono("half the spare capacity → twice the response time", 20, AMBER).move_to([0, -1.6, 0])
        self.play(FadeIn(sp), run_time=0.5)
        self.play(FadeIn(dbl), run_time=0.5)

        # 03-04: burstier traffic or more variable work: the curve is higher
        self.at("03")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        P, axes = curve_axes()
        base = mm1_curve(P)
        bursty = DashedVMobject(mm1_curve(P, color=CORAL, width=3, factor=(Q["bursty"]["ca2"] + 1) / 2), num_dashes=60)
        bdots = VGroup(*[Circle(radius=0.07, stroke_color=CORAL, stroke_width=2.5).move_to(P(float(r), v))
                         for r, v in Q["bursty"]["sim_ms"].items() if v <= 250])
        bl = VGroup(mono("burstier arrivals (3× as variable)", 16, CORAL),
                    mono("circles: simulated · dashed: Kingman's approximation", 16, CORAL)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        bl.move_to(P(0.03, 205), aligned_edge=LEFT)
        self.play(FadeIn(axes), Create(base), run_time=1.0)
        self.play(Create(bursty), LaggedStart(*[FadeIn(d) for d in bdots], lag_ratio=0.15), FadeIn(bl), run_time=1.2)
        self.at("05")
        more = mono("same response time → needs more spare capacity", 18, CORAL).next_to(bl, DOWN, 0.15)
        self.play(FadeIn(more), run_time=0.5)

        # 06-09: headroom: a first estimate of the load limit, read off the curve
        self.at("07")
        self.play(FadeOut(VGroup(bursty, bdots, bl, more)), run_time=0.4)
        h = DashedLine(P(0, 50), P(0.8, 50), color=AMBER, stroke_width=2)
        v = DashedLine(P(0.8, 50), P(0.8, 0), color=AMBER, stroke_width=2)
        self.play(Create(h), run_time=0.6)
        self.play(Create(v), run_time=0.6)
        self.at("08")
        rule = mono("average ≤ 5 × work time (50 ms) → at most 80% busy", 20, AMBER).move_to(P(0.03, 88), aligned_edge=LEFT)
        self.play(FadeIn(rule), run_time=0.5)
        self.at("09")
        real = mono("real systems: usually more headroom than this curve", 18, MUTED).next_to(rule, DOWN, 0.15)
        self.play(FadeIn(real), run_time=0.5)

        # 10-11: averages hide the slowest requests
        self.at("10")
        avg = mono("these are averages: some requests take several times longer", 18, MUTED).move_to(P(0.03, 165), aligned_edge=LEFT)
        self.play(FadeIn(avg), run_time=0.5)

        # 12-13: never plan for 100%
        self.at("12")
        wall = DashedLine(P(1.0, 0), P(1.0, 250), color=CORAL, stroke_width=3)
        wl = mono("100%: no spare capacity, the queue keeps growing", 18, CORAL).move_to(P(0.03, 225), aligned_edge=LEFT)
        self.play(Create(wall), run_time=0.6)
        self.at("13")
        self.play(FadeIn(wl), run_time=0.5)

        # end card
        self.until(self.end_of("13", 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("Why Busy Servers Get Slow", 40, INK, weight=SEMIBOLD).move_to([0, 2.7, 0])
        f = M('T = S / (1 − ρ)', 40, INK, font=MONO).move_to([0, 1.6, 0])
        f2 = mono("mean response time T, average work time S, utilization ρ", 18, MUTED).next_to(f, DOWN, 0.2)
        f3 = T("One server, Poisson arrivals, exponential work times (the M/M/1 queue; derived in Harchol-Balter ch. 13).",
               18, MUTED).next_to(f2, DOWN, 0.2)
        f4 = T("Many servers sharing one queue stay flat for longer, then eventually turn up much the same way (M/M/c).",
               18, MUTED).next_to(f3, DOWN, 0.12)
        refs = VGroup(T("Further reading", 18, MUTED, weight=MEDIUM),
                      T("Harchol-Balter, Performance Modeling and Design of Computer Systems: Queueing Theory in Action (2013)", 18, MUTED),
                      T("Kleinrock, Queueing Systems, Volume I: Theory (1975)", 18, MUTED)).arrange(DOWN, buff=0.1)
        refs.next_to(f4, DOWN, 0.6)
        self.play(FadeIn(name), FadeIn(f), run_time=0.6)
        self.play(FadeIn(VGroup(f2, f3, f4)), run_time=0.5)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
