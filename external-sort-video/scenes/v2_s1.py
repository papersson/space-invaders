from v2kit import *


class Gauge(VGroup):
    """Memory use against the 86 MB cap, replayed from a capture."""

    def __init__(self, width, anchor, color):
        super().__init__()
        self.mb = ValueTracker(0)
        self.w = width
        self.track = Rectangle(width=width, height=0.16, stroke_color=DIM, stroke_width=1.5,
                               fill_color=PANEL, fill_opacity=1).move_to(anchor, aligned_edge=LEFT)
        self.name = mono("memory used", 16, FAINT).next_to(self.track, UP, 0.08, aligned_edge=LEFT)
        cap = DashedLine(self.track.get_corner(UR) + 0.08 * UP, self.track.get_corner(DR) + 0.08 * DOWN,
                         color=CORAL, dash_length=0.04, stroke_width=2)
        caplab = mono("cap 86 MB", 14, CORAL).next_to(cap, DOWN, 0.06)
        self.cache = {}

        def fill():
            f = self.mb.get_value() / 86
            return Rectangle(width=max(self.w * min(f, 1), 0.001), height=0.16, stroke_width=0,
                             fill_color=color, fill_opacity=0.9).move_to(self.track.get_left(), aligned_edge=LEFT)

        def num():
            v = int(round(self.mb.get_value()))
            if v not in self.cache:
                self.cache[v] = mono(f"{v} MB", 16, MUTED)
            return self.cache[v].copy().next_to(self.track, UP, 0.08).align_to(self.track, RIGHT).shift(0.9 * LEFT)
        self.add(self.track, self.name, cap, caplab, always_redraw(fill), always_redraw(num))


class V2S1(CueScene):
    SEG = "s1"

    def construct(self):
        # 01: the file and the memory, to scale
        self.at("01")
        top = file_and_memory_bars()
        fbar, flab, mbar, mlab = top
        self.play(FadeIn(flab), GrowFromEdge(fbar, LEFT), run_time=1.2)
        self.play(GrowFromEdge(mbar, LEFT), FadeIn(mlab), run_time=0.8)
        ratio = mono("1,000 MB ÷ 86 MB ≈ 11.6", 18, MUTED).next_to(mlab, RIGHT, 0.5)
        self.play(FadeIn(ratio), run_time=0.4)

        # 02: a simple Python script runs out of memory just reading the file in
        self.at("02")
        self.play(Group(top, ratio).animate.scale(0.62).to_edge(UP, buff=0.35).shift(1.9 * LEFT), run_time=0.6)
        lt = terminal(6.6, 2.3, "python").move_to([-3.45, 0.95, 0])
        cmd1 = mono("$ python3 -c \"lines = sorted(open('records.txt'))\"", 14, INK)
        cmd1.next_to(lt[0].get_corner(UL), DR, buff=0.45).shift(0.1 * DOWN)
        g1 = Gauge(5.9, lt[0].get_corner(DL) + np.array([0.35, 0.3, 0]), CORAL)
        foot = VGroup(mono("real runs, this machine:", 16, FAINT),
                      mono("Python under an 86 MB cap", 16, FAINT),
                      mono("GNU coreutils sort 9.4, -S 86000000b", 16, FAINT)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        foot.move_to([-6.6, -2.5, 0], aligned_edge=LEFT)
        self.play(FadeIn(lt), FadeIn(foot), run_time=0.4)
        self.play(AddTextLetterByLetter(cmd1), run_time=0.8)
        self.add(g1)
        s = PYCAP["samples"]
        rss = [(x["t"], x["rss_kb"] * 1024 / 1e6) for x in s]
        dur = PYCAP["duration_s"]

        def py_upd(m, a):
            t = a * dur
            v = 0
            for tt, mb in rss:
                if tt <= t:
                    v = mb
            m.set_value(86 if a >= 0.999 else max(v, 86 * a))
        self.play(UpdateFromAlphaFunc(g1.mb, py_upd, rate_func=linear), run_time=2.0)
        tb = VGroup(*[mono(l, 14, CORAL if l.startswith("MemoryError") else MUTED)
                      for l in PYCAP["stderr"].strip().splitlines()])
        tb.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(cmd1, DOWN, 0.2, aligned_edge=LEFT)
        self.play(FadeIn(tb), run_time=0.3)
        self.play(Indicate(tb[-1], color=CORAL, scale_factor=1.15), run_time=0.6)

        # 03: sort, same memory, just finishes
        self.at("03")
        rt = terminal(6.6, 2.3, "shell").move_to([3.45, 0.95, 0])
        cmd2 = mono("$ sort -S 86000000b records.txt -o sorted.txt", 14, INK)
        cmd2.next_to(rt[0].get_corner(UL), DR, buff=0.45).shift(0.1 * DOWN)
        budget = mono("memory budget (-S): 86 MB, the same cap", 14, MUTED).next_to(cmd2, DOWN, 0.25, aligned_edge=LEFT)
        self.play(FadeIn(rt), run_time=0.4)
        self.play(AddTextLetterByLetter(cmd2), run_time=0.7)
        self.play(FadeIn(budget), run_time=0.4)

        # 04: the temp folder fills and empties (the capture, replayed at about real speed)
        tmp = TmpFolder([3.45, -2.12, 0], height=3.5)
        fold = tmp.mobject()
        self.play(FadeIn(tmp.panel), FadeIn(tmp.title), FadeIn(fold), run_time=0.4)
        t0 = self.now()
        t1 = self.start_of("05") - 0.2
        self.play(tmp.tt.animate.set_value(SORTCAP["duration_s"]), run_time=t1 - t0, rate_func=linear)
        done = mono("$", 14, INK).next_to(budget, DOWN, 0.18, aligned_edge=LEFT)
        self.add(done)

        # 05: what are those files?
        self.at("05")
        tmp.tt.set_value(peak_time())
        ghost = tmp.draw(rows_only=True).set_opacity(0.5)
        tmp.tt.set_value(SORTCAP["duration_s"])
        q = T("?", 120, ICE, weight=SEMIBOLD).next_to(ghost, LEFT, 0.6)
        self.play(FadeIn(ghost), FadeIn(q, scale=0.8), run_time=0.7)

        # title
        self.until(self.end_of("05", 0.3))
        fold.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title = T("Bigger Than Memory", 72, INK, weight=SEMIBOLD)
        sub = T("sorting a file that doesn't fit", 30, MUTED)
        g = VGroup(title, sub).arrange(DOWN, buff=0.3)
        self.play(FadeIn(title, shift=0.15 * UP), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        self.until(self.dur - 0.45)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()
