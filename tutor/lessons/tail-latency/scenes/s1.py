from tkit import *


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        # 01-03: one server: calls take about 10 ms, one in a hundred takes a full second
        self.at("01")
        axis_y = 1.6
        head = label("one backend server: each call's response time", 18, MUTED).move_to([-6.4, 2.6, 0], aligned_edge=LEFT)
        base = Line([-6.4, axis_y - 0.4, 0], [6.4, axis_y - 0.4, 0], stroke_color=DIM, stroke_width=1.5)
        self.play(FadeIn(head), FadeIn(base), run_time=0.6)
        rng = np.random.default_rng(3)
        n = 100
        slow_at = {57}
        ticks = VGroup()
        for k in range(n):
            x = -6.4 + 12.8 * (k + 0.5) / n
            h = 2.2 if k in slow_at else 0.12 + 0.05 * rng.random()
            ticks.add(Line([x, axis_y - 0.4, 0], [x, axis_y - 0.4 + h, 0], stroke_width=3,
                           stroke_color=CORAL if k in slow_at else ICE))
        self.at("02")
        typ = mono("typical: 10 ms", 20, ICE).move_to([-4.6, axis_y + 0.2, 0])
        self.play(LaggedStart(*[Create(t) for k, t in enumerate(ticks) if k < 57], lag_ratio=0.05), FadeIn(typ),
                  run_time=1.8)
        self.at("03")
        hic = mono("1 in 100: a hiccup, 1 second", 20, CORAL).next_to(ticks[57], RIGHT, 0.2).shift(0.7 * UP)
        self.play(Create(ticks[57]), FadeIn(hic), run_time=0.8)
        self.play(LaggedStart(*[Create(t) for k, t in enumerate(ticks) if k > 57], lag_ratio=0.05), run_time=1.2)

        # 05: a page calls a hundred servers at once and waits for all
        self.at("05")
        self.play(FadeOut(VGroup(head, base, ticks, typ, hic)), run_time=0.5)
        page = page_box()
        grid = server_grid()
        lines = fan_lines(page, grid)
        gl = label("100 backend servers", 18, MUTED).next_to(grid, UP, 0.15)
        self.play(FadeIn(page), run_time=0.4)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.08), FadeIn(grid, lag_ratio=0.01), FadeIn(gl),
                  run_time=1.4)
        waits = mono("waits for all 100", 18, INK).next_to(page, DOWN, 0.25)
        self.play(FadeIn(waits), run_time=0.4)

        # 06: how often is the page slow?
        self.at("06")
        q = T("How often is the page slow?", 34, ICE).to_edge(DOWN, buff=0.45)
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.until(self.end_of("06", 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title = T("The Tail at Scale", 64, INK, weight=SEMIBOLD)
        sub = T("why the slowest one percent decides", 28, MUTED)
        g = VGroup(title, sub).arrange(DOWN, buff=0.3)
        self.play(FadeIn(title, shift=0.15 * UP), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        self.until(self.dur - 0.45)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()
