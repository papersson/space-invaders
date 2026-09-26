from v2kit import *

X_LEFT, WIDTH = -5.6, 11.0
MEM_W = WIDTH * 86 / 1000
TICK_W, TICK_GAP, TICK_Y = 0.4, 0.12, 0.75


def ticks(n, color=AMBER):
    g = VGroup(*[RoundedRectangle(corner_radius=0.04, width=TICK_W, height=0.3, stroke_width=0, fill_color=color,
                                  fill_opacity=0.9) for _ in range(n)]).arrange(RIGHT, buff=TICK_GAP)
    return g.move_to([X_LEFT, TICK_Y, 0], aligned_edge=LEFT)


class V2S6(CueScene):
    SEG = "s6"

    def construct(self):
        # 01: the opening picture returns; every pass is I/O: count passes
        self.at("01")
        top = file_and_memory_bars()
        fbar, flab, mbar, mlab = top
        t18 = ticks(18)
        n18 = mono("18 passes", 24, INK).next_to(t18, RIGHT, 0.35)
        cap = mono("the simulated file, same proportions · each pass reads and writes every block", 16, FAINT).next_to(t18, DOWN, 0.15, aligned_edge=LEFT)
        self.play(FadeIn(top), run_time=0.8)
        self.play(LaggedStart(*[FadeIn(t) for t in t18], lag_ratio=0.15), FadeIn(n18), FadeIn(cap), run_time=1.4)

        # 02: in order: one sweep along the file
        self.at("02", 0.4)
        cur = Line(UP, DOWN, stroke_color=ICE, stroke_width=4).set_height(0.62).move_to(fbar.get_left())
        self.add(cur)
        self.play(cur.animate.move_to(fbar.get_right()), run_time=3.2, rate_func=linear)
        self.remove(cur)

        # 03: runs as big as memory (18 -> 5), then one wide merge (5 -> 2)
        self.at("03", 0.3)
        win = Rectangle(width=MEM_W, height=0.5, stroke_color=TRAY_EDGE, stroke_width=3).move_to(fbar.get_left(),
                                                                                                aligned_edge=LEFT)
        self.play(FadeIn(win), run_time=0.2)
        self.play(win.animate.move_to(fbar.get_right(), aligned_edge=RIGHT), run_time=1.4, rate_func=linear)
        self.play(FadeOut(win), run_time=0.2)
        t5 = VGroup(*[t.copy() for t in ticks(5)])
        t5[0].set_fill(ICE)
        n5 = mono("5 passes", 24, INK).next_to(t5, RIGHT, 0.35)
        self.play(ReplacementTransform(VGroup(*t18[:14]), t5[0]),
                  *[ReplacementTransform(t18[14 + k], t5[1 + k]) for k in range(4)],
                  ReplacementTransform(n18, n5), run_time=0.9)
        self.at("03", 3.2)
        t2 = VGroup(*[t.copy() for t in ticks(2)])
        t2[0].set_fill(ICE)
        t2[1].set_fill(ICE)
        n2 = mono("2 passes", 24, INK).next_to(t2, RIGHT, 0.35)
        self.play(ReplacementTransform(t5[0], t2[0]), ReplacementTransform(VGroup(*t5[1:]), t2[1]),
                  ReplacementTransform(n5, n2), run_time=0.9)
        trail = mono("18 → 5 → 2", 20, FAINT).next_to(n2, RIGHT, 0.4)
        self.play(FadeIn(trail), run_time=0.4)

        # 04: Python tried to hold the whole file
        self.at("04")
        py_l = mono("python", 18, MUTED).move_to([X_LEFT, -0.55, 0], aligned_edge=LEFT)
        track = Rectangle(width=WIDTH, height=0.3, stroke_color=DIM, stroke_width=1.5).move_to(
            [X_LEFT, -0.95, 0], aligned_edge=LEFT)
        want = DashedLine(track.get_left(), track.get_right(), color=CORAL, stroke_width=2, dash_length=0.1)
        cap_line = DashedLine([X_LEFT + MEM_W, -0.7, 0], [X_LEFT + MEM_W, -1.2, 0], color=TRAY_EDGE, stroke_width=2)
        py = Rectangle(width=0.01, height=0.3, stroke_width=0, fill_color=CORAL, fill_opacity=0.9).move_to(
            track.get_left(), aligned_edge=LEFT)
        self.play(FadeIn(py_l), FadeIn(track), FadeIn(cap_line), Create(want), run_time=0.6)
        self.play(py.animate.stretch_to_fit_width(MEM_W).move_to(track.get_left(), aligned_edge=LEFT), run_time=0.8)
        err = mono("MemoryError", 18, CORAL).move_to([X_LEFT + MEM_W + 0.2, -0.55, 0], aligned_edge=LEFT)
        self.play(FadeIn(err), Flash(cap_line.get_center(), color=CORAL, line_length=0.15), run_time=0.5)

        # 05: sort never held more than a memory's worth
        self.at("05")
        so_l = mono("sort", 18, MUTED).move_to([X_LEFT, -1.55, 0], aligned_edge=LEFT)
        track2 = track.copy().move_to([X_LEFT, -1.95, 0], aligned_edge=LEFT)
        sw = Rectangle(width=MEM_W, height=0.3, stroke_width=0, fill_color=ICE, fill_opacity=0.85).move_to(
            track2.get_left(), aligned_edge=LEFT)
        self.play(FadeIn(so_l), FadeIn(track2), FadeIn(sw), run_time=0.5)
        self.play(sw.animate.move_to(track2.get_right(), aligned_edge=RIGHT), run_time=1.5, rate_func=linear)

        # 06: the capture once more: pass 1, twelve runs; pass 2, one merge
        self.at("06")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not top], run_time=0.4)
        tmp = TmpFolder([-1.2, -1.05, 0], width=7.4, height=3.5)
        fold = tmp.mobject()
        self.play(FadeIn(tmp.panel), FadeIn(tmp.title), FadeIn(fold), run_time=0.3)
        p1 = mono("pass 1: twelve runs", 22, ICE).move_to([2.85, 0.1, 0], aligned_edge=LEFT)
        p2 = mono("pass 2: one merge", 22, ICE).next_to(p1, DOWN, 0.35, aligned_edge=LEFT)
        note = mono("the real run, replayed faster", 16, FAINT).next_to(tmp.panel, DOWN, 0.15, aligned_edge=LEFT)
        self.add(note)
        span = self.end_of("06", -0.4) - self.now()
        ms = merge_start_time()
        f1 = ms / SORTCAP["duration_s"]
        self.play(tmp.tt.animate.set_value(ms), FadeIn(p1, run_time=0.5), run_time=span * f1, rate_func=linear)
        self.play(tmp.tt.animate.set_value(SORTCAP["duration_s"]), FadeIn(p2, run_time=0.5), run_time=span * (1 - f1),
                  rate_func=linear)
        fold.clear_updaters()
        self.until(self.end_of("06", 0.2))

        # end card
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("External merge sort", 44, INK, weight=SEMIBOLD).move_to([0, 2.7, 0])
        f = M('passes = 1 + ⌈log<sub>(M/B) − 1</sub> ⌈N/M⌉⌉', 34, INK, font=MONO).move_to([0, 1.55, 0])
        vars_ = mono("N items · memory M items · blocks of B items", 18, MUTED).next_to(f, DOWN, 0.25)
        rg = T("Ramakrishnan & Gehrke write B for buffer pages (this video's M/B) and N for pages (this video's N/B).",
               16, MUTED).next_to(vars_, DOWN, 0.15)
        opt = VGroup(T("Asymptotically optimal: it matches the lower bound, up to constant factors,", 22, INK),
                     T("for sorts that move records as indivisible units (Aggarwal & Vitter, CACM 1988).", 22, INK))
        opt.arrange(DOWN, buff=0.12).next_to(rg, DOWN, 0.5)
        refs = VGroup(T("Further reading", 18, MUTED, weight=MEDIUM),
                      T("Ramakrishnan & Gehrke, Database Management Systems, 3rd ed., ch. 13", 18, MUTED),
                      T("Mehlhorn & Sanders, Algorithms and Data Structures: The Basic Toolbox, §5.7", 18, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(opt, DOWN, 0.5)
        self.play(FadeIn(name), FadeIn(f), run_time=0.6)
        self.play(FadeIn(vars_), FadeIn(rg), run_time=0.4)
        self.play(FadeIn(opt), run_time=0.4)
        self.play(FadeIn(refs), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
