from tkit import *

X0, X1 = -5.8, 5.8           # log time axis from 3 ms to 3,000 ms
LO, HI = math.log10(3), math.log10(3000)
AX_Y = -0.6


def tx(ms):
    return X0 + (X1 - X0) * (math.log10(ms) - LO) / (HI - LO)


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("What the dashboard shows")
        # a thousand calls to one server, as dots on a log time axis
        rng = np.random.default_rng(11)
        sample = F["hist"][::20][:1000]
        axis = Line([X0, AX_Y, 0], [X1, AX_Y, 0], stroke_color=FAINT, stroke_width=2)
        ticks = VGroup(*[VGroup(Line([tx(v), AX_Y, 0], [tx(v), AX_Y - 0.1, 0], stroke_color=FAINT),
                                mono(lab, 16, MUTED).next_to([tx(v), AX_Y - 0.1, 0], DOWN, 0.08))
                         for v, lab in ((3, "3 ms"), (10, "10 ms"), (30, "30 ms"), (100, "100 ms"), (300, "300 ms"),
                                        (1000, "1 s"), (3000, "3 s"))])
        xl = mono("response time of 1,000 calls to one server (log scale, simulated)", 16, FAINT)
        xl.next_to(axis, DOWN, 0.6)
        dots = VGroup(*[Dot([tx(v), AX_Y + 0.2 + 1.9 * rng.random(), 0], radius=0.035,
                            color=CORAL if v > 500 else ICE).set_opacity(0.85) for v in sample])
        self.play(FadeIn(c), FadeIn(axis), FadeIn(ticks), FadeIn(xl), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.002), run_time=1.8)

        # 01-02: the average looks healthy
        self.at("01", 0.5)
        avg = F["backend"]["mean"]
        mk = lambda v, text, col, y: VGroup(DashedLine([tx(v), AX_Y, 0], [tx(v), y, 0], color=col, stroke_width=2),
                                            mono(text, 18, col).next_to([tx(v), y, 0], UP, 0.08))
        m_avg = mk(avg, "average 20 ms", INK, 1.8)
        self.play(FadeIn(m_avg), run_time=0.6)
        self.at("02")
        calc = mono("(99 × 10 ms + 1 × 1,000 ms) ÷ 100 ≈ 20 ms", 18, MUTED).move_to([0, -2.1, 0])
        self.play(FadeIn(calc), run_time=0.5)

        # 03-05: percentiles: the 99th is about a second
        self.at("04")
        m_p99 = mk(F["backend"]["p99"], "99th percentile ≈ 1 s", CORAL, 1.8)
        m_med = mk(F["backend"]["p50"], "median 10 ms", ICE, 2.3)
        self.play(FadeIn(m_med), run_time=0.5)
        self.at("05")
        self.play(FadeIn(m_p99), run_time=0.6)

        # 06-07: the long tail
        self.at("06")
        slow_dots = VGroup(*[d for d in dots if d.get_color() == ManimColor(CORAL)])
        tail = SurroundingRectangle(slow_dots, buff=0.12, color=CORAL, stroke_width=2, corner_radius=0.08)
        tl = mono("the tail", 20, CORAL).next_to(tail, RIGHT, 0.15)
        self.play(FadeOut(calc), Create(tail), FadeIn(tl), run_time=0.6)

        # 08-10: the more calls per page, the more pages hit the tail
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        ns = [1, 10, 50, 100]
        bw, base_y, hmax = 1.3, -2.4, 4.4
        bars = VGroup()
        for i, n in enumerate(ns):
            f = 1 - 0.99 ** n
            x = -3.3 + i * 2.3
            b = Rectangle(width=bw, height=max(hmax * f, 0.02), stroke_width=0, fill_color=CORAL, fill_opacity=0.85)
            b.move_to([x, base_y, 0], aligned_edge=DOWN)
            val = mono(f"{f * 100:.1f}%" if n > 1 else "1%", 20, INK).next_to(b, UP, 0.1)
            nl = mono(f"{n} call{'s' if n > 1 else ''}", 18, MUTED).next_to([x, base_y, 0], DOWN, 0.15)
            bars.add(VGroup(b, val, nl))
        head = mono("pages with at least one call from the servers' slowest 1%", 20, INK).move_to([0, 2.9, 0])
        self.play(FadeIn(head), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(b, shift=0.1 * UP) for b in bars], lag_ratio=0.35), run_time=2.0)
        self.at("09")
        typical = mono("100 calls: more than half of pages → the typical page is as slow as the 99th percentile", 17, CORAL)
        typical.next_to(head, DOWN, 0.2)
        self.play(FadeIn(typical), run_time=0.5)
        self.at("10")
        rarer = mono("more calls per page → an even rarer, slower percentile decides", 17, MUTED).next_to(typical, DOWN, 0.12)
        self.play(FadeIn(rarer), run_time=0.5)

        # 11-12: turned around: for the page to be slow 1 time in 100, each server must be slow 1 in 10,000
        self.at("11")
        self.play(FadeOut(VGroup(typical, rarer)), run_time=0.3)
        conv = VGroup(mono("page slow 1 time in 100", 24, INK),
                      Arrow(ORIGIN, 1.0 * RIGHT, buff=0, color=MUTED, stroke_width=3),
                      mono("each server slow 1 time in 10,000", 24, CORAL)).arrange(RIGHT, buff=0.3)
        conv.next_to(head, DOWN, 0.3)
        conv_l = mono("(with 100 calls per page)", 16, MUTED).next_to(conv, DOWN, 0.1)
        self.at("12")
        self.play(FadeIn(conv[0]), run_time=0.4)
        self.play(GrowArrow(conv[1]), FadeIn(conv[2]), FadeIn(conv_l), run_time=0.8)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
