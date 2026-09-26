from qkit import *


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("Two ways to find the rows")
        GX, GY = 2.4, -0.35
        # 01-02: the table is pages
        self.at("01")
        grid = page_grid(w=8.0).move_to([GX, GY, 0])
        cnt = mono(f"{RELPAGES:,} pages · ~{round(2_000_000 / RELPAGES)} rows each", 16, MUTED).next_to(grid, UP, 0.2)
        self.play(FadeIn(c), FadeIn(grid), run_time=0.7)
        self.at("02")
        self.play(FadeIn(cnt), run_time=0.5)

        # 03-05: a full scan reads every page
        self.at("03")
        self.at("04")
        fs = mono("full scan", 20, AMBER).move_to([-4.6, 1.6, 0])
        sweep = Rectangle(width=grid.width, height=0.01, stroke_width=0, fill_color=AMBER, fill_opacity=0.35)
        sweep.move_to(grid.get_top(), aligned_edge=UP)
        self.play(FadeIn(fs), run_time=0.3)
        self.add(sweep)
        self.play(sweep.animate.stretch_to_fit_height(grid.height).move_to(grid.get_top(), aligned_edge=UP),
                  run_time=2.0, rate_func=linear)
        self.at("05")
        every = mono(f"{RELPAGES:,} of {RELPAGES:,} pages,\nwhoever the customer", 15, AMBER).next_to(fs, DOWN, 0.2)
        self.play(FadeIn(every), run_time=0.4)

        # 06-09: the index reads only the pages that hold the rows (customer 4242, real pages)
        self.at("06")
        self.play(FadeOut(sweep), FadeOut(every), FadeOut(fs), run_time=0.4)
        idx = VGroup(*[mono(t, 15, MUTED) for t in ("…", "4241", "4242", "4243", "…")]).arrange(DOWN, buff=0.18)
        ib = SurroundingRectangle(idx, buff=0.2, color=TRAY_EDGE, stroke_width=1.8, corner_radius=0.08)
        il = label("index: sorted customer numbers", 13).next_to(ib, UP, 0.15)
        ig = VGroup(ib, idx, il).move_to([-4.6, 0.2, 0])
        self.play(FadeIn(ig), run_time=0.6)
        self.at("07")
        self.play(idx[2].animate.set_color(ICE), run_time=0.3)
        dots = VGroup(*[Dot(page_pos(grid, p), radius=0.07, color=ICE) for p in PAGES_4242])
        arrs = VGroup(*[Line(idx[2].get_right() + 0.1 * RIGHT, d.get_center(), stroke_color=ICE, stroke_width=1.2,
                             stroke_opacity=0.6) for d in dots])
        self.play(LaggedStart(*[Create(a) for a in arrs], lag_ratio=0.1), run_time=1.2)
        self.play(FadeIn(dots), run_time=0.4)
        self.at("08")
        c10 = mono(f"customer 4242: {len(PAGES_4242)} orders, on {len(PAGES_4242)} pages", 16, ICE).move_to([GX, GY - grid.height / 2 - 0.35, 0])
        self.play(FadeIn(c10), run_time=0.4)
        self.at("09")
        c10b = mono(f"{len(PAGES_4242)} of {RELPAGES:,} pages read", 16, ICE).move_to(c10)
        self.play(Transform(c10, c10b), run_time=0.4)

        # 10-13: customer 1 is on every page
        self.at("10")
        self.play(FadeOut(arrs), FadeOut(dots), FadeOut(c10), idx[2].animate.set_color(MUTED), run_time=0.4)
        idx1 = VGroup(*[mono(t, 15, MUTED) for t in ("1", "2", "3", "…", "4242")]).arrange(DOWN, buff=0.18).move_to(idx)
        self.play(Transform(idx, idx1), run_time=0.4)
        self.play(idx[0].animate.set_color(BAD), run_time=0.3)
        self.at("11")
        arr_note = mono("stored in the order they arrived:\nabout 3 rows in 10 on every page", 14, BAD).next_to(ig, DOWN, 0.4)
        self.play(FadeIn(arr_note), run_time=0.4)
        full = page_grid(all_color=(0xE4, 0x71, 0x5F, 255), w=8.0).move_to(grid)
        full.set_opacity(0.0)
        self.add(full)
        self.play(full.animate.set_opacity(0.85), run_time=1.6)
        self.at("12")
        all_p = mono(f"customer 1: {RELPAGES:,} of {RELPAGES:,} pages", 16, BAD).move_to([GX, GY - grid.height / 2 - 0.35, 0])
        self.play(FadeIn(all_p), run_time=0.4)
        self.at("13")
        skip = mono("nothing to skip", 16, BAD).next_to(all_p, DOWN, 0.12)
        self.play(FadeIn(skip), run_time=0.4)

        # 14-15: it depends on how many rows match
        self.at("14")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        d1 = mono("does the index save work?", 24, INK).move_to([0, 0.7, 0])
        d2 = mono("it depends on how many rows match", 22, AMBER).next_to(d1, DOWN, 0.4)
        self.play(FadeIn(d1), run_time=0.4)
        self.play(FadeIn(d2), run_time=0.5)
        self.at("15")
        d3 = mono("which depends on the customer", 20, MUTED).next_to(d2, DOWN, 0.3)
        self.play(FadeIn(d3), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
