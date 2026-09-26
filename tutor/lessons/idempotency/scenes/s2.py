from ikit import *

TOP, BOT = 2.2, -1.3
COLS = [-4.5, 0.0, 4.5]          # centres of the three diagrams
HALF = 1.5                       # client lane at centre - HALF, server at centre + HALF


def diagram(cx, title):
    xc, xs = cx - HALF, cx + HALF
    return VGroup(mono(title, 16, MUTED).move_to([cx, TOP + 0.75, 0]), lanes(xc, xs, TOP, BOT)), xc, xs


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("Silence looks the same")
        self.at("01")
        diags = [diagram(cx, t) for cx, t in zip(COLS, ("request lost", "server slow or crashed", "reply lost"))]
        self.play(FadeIn(c), *[FadeIn(d[0]) for d in diags], run_time=0.8)

        # 02: (a) the request is lost on the way
        self.at("02")
        _, xc, xs = diags[0]
        ra = message([xc, TOP - 0.3, 0], [xs, TOP - 0.7, 0], "charge $50", lost_at=0.55)
        self.play(Create(ra[0]), FadeIn(ra[1]), FadeIn(ra[2]), run_time=0.9)
        na = mono("nothing happened", 14, MUTED).move_to([xs, TOP - 1.3, 0])
        self.play(FadeIn(na), run_time=0.3)

        # 03-04: (b) still working, or crashed partway
        self.at("03")
        _, xc, xs = diags[1]
        rb = message([xc, TOP - 0.3, 0], [xs, TOP - 0.7, 0], "charge $50")
        self.play(GrowArrow(rb[0]), FadeIn(rb[1]), run_time=0.7)
        work = Rectangle(width=0.3, height=1.4, stroke_width=0, fill_color=ICE, fill_opacity=0.5)
        work.move_to([xs, TOP - 0.7, 0], aligned_edge=UP)
        wl = mono("still working…", 14, ICE).next_to(work, LEFT, 0.1)
        self.play(GrowFromEdge(work, UP), FadeIn(wl), run_time=0.6)
        self.at("04")
        crash = lost_mark(np.array([xs, TOP - 2.35, 0]))
        cl = mono("or: crashed partway", 14, CORAL).next_to(crash, LEFT, 0.1)
        self.play(FadeIn(crash), FadeIn(cl), run_time=0.5)

        # 05: (c) charged, but the reply is lost
        self.at("05")
        _, xc, xs = diags[2]
        rc = message([xc, TOP - 0.3, 0], [xs, TOP - 0.7, 0], "charge $50")
        self.play(GrowArrow(rc[0]), FadeIn(rc[1]), run_time=0.6)
        ch = mono("charged $50", 14, AMBER).move_to([xs + 0.1, TOP - 1.0, 0]).shift(0.45 * LEFT)
        self.play(FadeIn(ch), run_time=0.3)
        rep = message([xs, TOP - 1.3, 0], [xc, TOP - 1.7, 0], "ok", color=INK, lost_at=0.5)
        self.play(Create(rep[0]), FadeIn(rep[1]), FadeIn(rep[2]), run_time=0.7)

        # 06: the client sees the same thing in every case
        self.at("06")
        views = VGroup(*[VGroup(Rectangle(width=2.6, height=0.55, stroke_color=DIM, stroke_width=1.5),
                                mono("client sees: nothing, then timeout", 13, CORAL))
                         for _ in COLS])
        for v, cx in zip(views, COLS):
            v[1].move_to(v[0])
            v.move_to([cx, BOT - 0.45, 0])
        self.play(LaggedStart(*[FadeIn(v) for v in views], lag_ratio=0.2), run_time=0.8)

        # 07-10: asking again crosses the same network; the last message is never confirmed
        self.at("07")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        lanes2 = lanes(-2.2, 2.2, 2.4, -2.6)
        self.play(FadeIn(lanes2), run_time=0.4)
        m1 = message([-2.2, 2.0, 0], [2.2, 1.6, 0], "did my charge go through?")
        self.play(GrowArrow(m1[0]), FadeIn(m1[1]), run_time=0.7)
        self.at("08")
        m2 = message([2.2, 1.3, 0], [-2.2, 0.9, 0], "yes", color=INK, lost_at=0.5)
        self.play(Create(m2[0]), FadeIn(m2[1]), FadeIn(m2[2]), run_time=0.7)
        self.at("09")
        m3 = message([-2.2, 0.5, 0], [2.2, 0.1, 0], "got your answer?")
        m4 = message([2.2, -0.2, 0], [-2.2, -0.6, 0], "got it", color=INK)
        m5 = message([-2.2, -0.9, 0], [2.2, -1.3, 0], "…", lost_at=0.6)
        self.play(GrowArrow(m3[0]), FadeIn(m3[1]), run_time=0.5)
        self.play(GrowArrow(m4[0]), FadeIn(m4[1]), run_time=0.5)
        self.play(Create(m5[0]), FadeIn(m5[1]), FadeIn(m5[2]), run_time=0.5)
        last = mono("the last message is never confirmed", 18, CORAL).move_to([0, -1.9, 0])
        self.play(FadeIn(last), run_time=0.4)
        self.at("11")
        no = T("No protocol can promise exactly-once delivery.", 28, ICE).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(no), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
