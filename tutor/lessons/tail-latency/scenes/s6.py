from tkit import *


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("The answer")
        page = page_box()
        grid = server_grid()
        lines = fan_lines(page, grid)
        row = [0] * 100
        row[37] = 1
        color_grid(grid, row)
        page[0].set_stroke(CORAL)
        # 01: one slow call holds up the page
        self.at("01")
        self.play(FadeIn(c), FadeIn(page), FadeIn(grid), FadeIn(lines), run_time=0.6)
        ring = SurroundingRectangle(grid[37], buff=0.06, color=CORAL, stroke_width=3)
        held = mono("one hiccup holds up the page", 20, CORAL).next_to(grid, DOWN, 0.3)
        self.play(Create(ring), FadeIn(held), run_time=0.7)
        self.at("01", 5.0)
        self.play(grid[37].animate.set_fill(FAST), page[0].animate.set_stroke(TRAY_EDGE), FadeOut(ring),
                  FadeOut(held), run_time=0.8)
        rescued = mono("the hedge rescues it", 20, ICE).next_to(grid, DOWN, 0.3)
        self.play(FadeIn(rescued), run_time=0.4)

        # 02-03: watch the 99th percentile; tolerate the tail
        self.at("02")
        w = VGroup(mono("watch: the servers' 99th percentile (their tail latency), not their average", 20, INK),
                   mono("design the fan-out to tolerate hiccups", 20, INK)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        w.to_edge(UP, buff=0.9).set_x(0)
        self.play(FadeIn(w[0]), run_time=0.5)
        self.at("03")
        self.play(FadeIn(w[1]), run_time=0.5)

        # 04-05: all of this assumes independent hiccups
        self.at("04")
        caveat = mono("assumes independent hiccups: one cause hitting many servers\nchanges the arithmetic, and can slow the hedge's copy too", 17, CORAL)
        caveat.to_edge(DOWN, buff=0.35)
        self.play(FadeOut(rescued), FadeIn(caveat), run_time=0.6)

        # end card
        self.until(self.end_of("05", 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("The Tail at Scale", 40, INK, weight=SEMIBOLD).move_to([0, 2.5, 0])
        f = M('P(page fast) = p<sup>N</sup>', 40, INK, font=MONO).move_to([0, 1.3, 0])
        f2 = mono("p: chance one call is fast · N: calls per page · assumes independent calls", 18, MUTED)
        f2.next_to(f, DOWN, 0.25)
        f3 = mono("0.99¹⁰⁰ ≈ 0.37 → 63% of pages slow", 18, MUTED).next_to(f2, DOWN, 0.15)
        refs = VGroup(T("Further reading", 18, MUTED, weight=MEDIUM),
                      T("Dean & Barroso, \"The Tail at Scale\", Communications of the ACM 56(2), 2013", 18, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(f3, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(f), run_time=0.6)
        self.play(FadeIn(f2), FadeIn(f3), run_time=0.5)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
