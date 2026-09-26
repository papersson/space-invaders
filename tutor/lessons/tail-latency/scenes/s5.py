from tkit import *

LANE_X = {"page": -3.4, "A": -0.2, "B": 3.3}
TOP, MS = 2.3, 0.1          # y of time 0, and scene units per millisecond (time runs down)


def ty(ms):
    return TOP - MS * ms


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("Hedged requests")
        self.at("01")
        head = T("one standard technique: the hedged request", 26, INK).move_to([0, 3.3, 0])
        self.play(FadeIn(c), FadeIn(head), run_time=0.5)

        # lanes: time runs down
        lanes = VGroup()
        for name, x in LANE_X.items():
            text = {"page": "page", "A": "server A", "B": "server B (another machine)"}[name]
            lanes.add(VGroup(mono(text, 18, INK).move_to([x, TOP + 0.35, 0]),
                             DashedLine([x, TOP, 0], [x, ty(45), 0], color=DIM, stroke_width=1.5, dash_length=0.08)))
        self.play(FadeIn(lanes), run_time=0.5)

        # 02: send to A
        self.at("02")
        p95 = F["backend"]["p95"]
        a1 = Arrow([LANE_X["page"], ty(0), 0], [LANE_X["A"], ty(2), 0], buff=0, color=ICE, stroke_width=3,
                   max_tip_length_to_length_ratio=0.06)
        self.play(GrowArrow(a1), run_time=0.6)
        stall = Rectangle(width=0.35, height=MS * 40, stroke_width=0, fill_color=CORAL, fill_opacity=0.6)
        stall.move_to([LANE_X["A"], ty(2), 0], aligned_edge=UP)
        sl = mono("stalled (hiccup)", 16, CORAL).next_to(stall, RIGHT, 0.1).align_to(stall, UP)
        self.play(GrowFromEdge(stall, UP), FadeIn(sl), run_time=0.8)

        # 03: at the 95th percentile, send a copy to B
        self.at("03", 1.0)
        timer = Line([LANE_X["page"] - 0.35, ty(0), 0], [LANE_X["page"] - 0.35, ty(p95), 0], color=AMBER, stroke_width=5)
        tl = mono(f"wait until\nthe 95th percentile\n({p95:.0f} ms here)", 16, AMBER).next_to(timer, LEFT, 0.12)
        self.play(Create(timer), FadeIn(tl), run_time=1.0)
        a2 = Arrow([LANE_X["page"], ty(p95), 0], [LANE_X["B"], ty(p95 + 2), 0], buff=0, color=ICE, stroke_width=3,
                   max_tip_length_to_length_ratio=0.05)
        cp = mono("copy", 16, ICE).next_to(a2.get_end(), UP, 0.1).shift(0.6 * LEFT)
        self.at("03", 4.5)
        self.play(GrowArrow(a2), FadeIn(cp), run_time=0.6)

        # 04: B answers first
        self.at("04")
        work = Rectangle(width=0.35, height=MS * 8, stroke_width=0, fill_color=ICE, fill_opacity=0.6)
        work.move_to([LANE_X["B"], ty(p95 + 2), 0], aligned_edge=UP)
        a3 = Arrow([LANE_X["B"], ty(p95 + 10), 0], [LANE_X["page"], ty(p95 + 12), 0], buff=0, color=INK,
                   stroke_width=3, max_tip_length_to_length_ratio=0.05)
        done = mono(f"answer at ≈{p95 + 12:.0f} ms", 18, INK).next_to([LANE_X["page"], ty(p95 + 12), 0], DOWN, 0.15)
        self.play(GrowFromEdge(work, UP), run_time=0.4)
        self.play(GrowArrow(a3), FadeIn(done), run_time=0.6)
        drop = mono("A's answer: ignored", 16, FAINT).next_to(stall, DOWN, 0.1)
        self.play(FadeIn(drop), run_time=0.4)

        # 05-06: works if the two don't stall together
        self.at("06")
        diff = mono("different machine:\nthe same hiccup is unlikely to hit both", 18, MUTED)
        diff.move_to([0.35, ty(33), 0], aligned_edge=LEFT)
        self.play(FadeIn(diff), run_time=0.5)

        # 07-08: at most 5% more requests
        self.at("08")
        load = mono("copies: only calls slower than the 95th percentile → about +5% requests", 18, AMBER)
        load.move_to([0.6, ty(49), 0])
        self.play(FadeIn(load), run_time=0.6)

        # 09: slow pages 63% -> 1% (simulated)
        self.at("09")
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (c,)], run_time=0.5)
        base = -1.2
        b1 = Rectangle(width=1.6, height=4.0 * F["sim"]["slow"], stroke_width=0, fill_color=CORAL, fill_opacity=0.85)
        b1.move_to([-2.0, base, 0], aligned_edge=DOWN)
        b2 = Rectangle(width=1.6, height=max(4.0 * F["sim"]["slow_hedged"], 0.04), stroke_width=0, fill_color=ICE,
                       fill_opacity=0.9).move_to([1.2, base, 0], aligned_edge=DOWN)
        v1 = mono(f"{F['sim']['slow'] * 100:.0f}%", 24, INK).next_to(b1, UP, 0.1)
        v2 = mono(f"{F['sim']['slow_hedged'] * 100:.0f}%", 24, INK).next_to(b2, UP, 0.1)
        n1 = mono("no hedging", 18, MUTED).next_to([-2.0, base, 0], DOWN, 0.15)
        n2 = mono("hedged at the 95th percentile", 18, MUTED).next_to([1.2, base, 0], DOWN, 0.15)
        cap = mono("slow pages (≥ 1 s), 200,000 simulated pages of 100 calls", 16, FAINT).next_to(n1, DOWN, 0.35)
        cap.set_x(-0.4)
        self.play(GrowFromEdge(b1, DOWN), FadeIn(v1), FadeIn(n1), FadeIn(cap), run_time=0.7)
        self.play(GrowFromEdge(b2, DOWN), FadeIn(v2), FadeIn(n2), run_time=0.7)

        # 10-12: Google's measurement
        self.at("10")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        g_head = T("Google, Bigtable benchmark (Dean & Barroso, 2013)", 26, INK).move_to([0, 2.5, 0])
        setup = mono("each request reads 1,000 values from 100 servers", 20, MUTED).next_to(g_head, DOWN, 0.3)
        self.play(FadeIn(g_head), run_time=0.5)
        self.at("11")
        self.play(FadeIn(setup), run_time=0.5)
        self.at("12")
        parts = VGroup(
            VGroup(label("trigger", 16, MUTED), mono("hedge after a fixed 10 ms", 24, INK)).arrange(DOWN, buff=0.15),
            VGroup(label("result, across many requests", 16, MUTED), M('99.9th percentile\n1,800 ms → <span foreground="#8FD3FF">74 ms</span>',
                                                  24, INK, font=MONO)).arrange(DOWN, buff=0.15),
            VGroup(label("cost", 16, MUTED), mono("+2% requests", 24, AMBER)).arrange(DOWN, buff=0.15),
        ).arrange(RIGHT, buff=0.8).move_to([0, 0.0, 0])
        self.play(LaggedStart(*[FadeIn(p, shift=0.1 * UP) for p in parts], lag_ratio=0.5), run_time=1.8)

        # 14-16: hedge too early: twice the load
        self.at("14")
        early = mono("hedge immediately → every call copied → 2× load → longer queues → slower", 18, CORAL)
        early.move_to([0, -1.9, 0])
        self.play(FadeIn(early), run_time=0.6)

        # 17-18: reads, not writes
        self.at("17")
        rw = mono("reads: safe to copy · writes (a payment): could happen twice", 18, MUTED).move_to([0, -2.7, 0])
        self.play(FadeIn(rw), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
