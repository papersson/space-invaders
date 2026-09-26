from tkit import *


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("One in a hundred, a hundred times")
        page = page_box()
        grid = server_grid()
        lines = fan_lines(page, grid)
        self.play(FadeIn(c), FadeIn(page), FadeIn(grid), FadeIn(lines), run_time=0.5)

        # 01-03: fast only if all 100 are fast; independent calls, like separate die rolls
        self.at("01")
        rule = mono("page fast ⇔ all 100 calls fast", 18, INK).next_to(page, DOWN, 0.3)
        self.play(FadeIn(rule), run_time=0.5)
        self.at("03", 2.0)
        ind = mono("independent: one server's hiccup\ndoesn't make another's more likely", 16, MUTED)
        ind.next_to(rule, DOWN, 0.3)
        self.play(FadeIn(ind), run_time=0.5)

        # 04-06: twenty pages play; the tally of slow pages climbs; 0.99^100
        self.at("04")
        tally = Counter(0, title="SLOW PAGES", size=40, anchor=[6.6, 3.35, 0], color=CORAL)
        of = mono("of 0 pages", 18, MUTED)
        of_cache = {}

        def of_text(n):
            if n not in of_cache:
                of_cache[n] = mono(f"of {n} pages", 18, MUTED)
            return of_cache[n].copy().next_to(tally, DOWN, 0.1).align_to(tally, RIGHT)
        seen = ValueTracker(0)
        of = always_redraw(lambda: of_text(int(seen.get_value())))
        self.play(FadeIn(tally), FadeIn(of), run_time=0.3)
        per = (self.start_of("05") - self.now() - 0.2) / 20
        for p, row in enumerate(F["grid"]):
            slow = any(row)
            color_grid(grid, row)
            page[0].set_stroke(CORAL if slow else TRAY_EDGE)
            seen.set_value(p + 1)
            if slow:
                tally.tracker.set_value(tally.value() + 1)
            self.wait(max(per, 1 / 15), frozen_frame=False)
        of.clear_updaters()
        math1 = M('0.99 × 0.99 × … (100 times) = 0.99<sup>100</sup> ≈ <span foreground="#8FD3FF">0.37</span>', 24, INK,
                  font=MONO).to_edge(DOWN, buff=0.9)
        self.at("05")
        self.play(FadeIn(math1), run_time=0.6)
        self.at("07")
        math2 = M('1 − 0.37 = <span foreground="#E4715F">63% of pages slow</span>', 24, INK, font=MONO)
        math2.next_to(math1, DOWN, 0.2)
        self.play(FadeIn(math2), run_time=0.6)

        # 08-09: rare for one server, usual for the page
        self.at("08")
        one = mono("one server: 1% slow", 20, INK).move_to([-4.6, 2.3, 0])
        self.play(FadeIn(one), run_time=0.4)
        self.at("09")
        pg = mono("the page: 63% slow", 20, CORAL).next_to(one, DOWN, 0.15)
        self.play(FadeIn(pg), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
