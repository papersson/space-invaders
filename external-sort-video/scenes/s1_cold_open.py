from common import *
from s4_runs import STRIP, strip_images

SORTCAP = json.loads((CAPTURES / "gnu_sort_tmp.json").read_text())
PYCAP = json.loads((CAPTURES / "python_memoryerror.json").read_text())
CORAL = "#E4715F"      # errors only
GAUGE_MAX_KB = 600_000  # Python's cap; both gauges share this scale


def terminal(w, h, title):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=DIM, stroke_width=2,
                         fill_color="#0B0F13", fill_opacity=1)
    t = label(title, 16, FAINT).next_to(r.get_corner(UL), DR, buff=0.14)
    return VGroup(r, t)


def mono(s, size=20, color=INK):
    return T(s, size, color, font=MONO)


class Gauge(VGroup):
    def __init__(self, width, anchor, color, cap_label=None):
        super().__init__()
        self.kb = ValueTracker(0)
        self.w = width
        self.track = Rectangle(width=width, height=0.16, stroke_color=DIM, stroke_width=1.5,
                               fill_color=PANEL, fill_opacity=1).move_to(anchor, aligned_edge=LEFT)
        self.name = mono("memory", 16, FAINT).next_to(self.track, UP, 0.08, aligned_edge=LEFT)
        self.cache = {}

        def fill():
            f = self.kb.get_value() / GAUGE_MAX_KB
            r = Rectangle(width=max(self.w * min(f, 1), 0.001), height=0.16, stroke_width=0,
                          fill_color=color, fill_opacity=0.9)
            return r.move_to(self.track.get_left(), aligned_edge=LEFT)

        def num():
            mb = int(round(self.kb.get_value() / 1000))
            if mb not in self.cache:
                self.cache[mb] = mono(f"{mb:,} MB", 16, MUTED)
            return self.cache[mb].copy().next_to(self.track, UP, 0.08, aligned_edge=RIGHT)
        self.add(self.track, self.name, always_redraw(fill), always_redraw(num))
        if cap_label:
            capx = self.track.get_right()[0]
            self.add(DashedLine([capx, self.track.get_y() - 0.16, 0], [capx, self.track.get_y() + 0.16, 0],
                                color=CORAL, dash_length=0.04, stroke_width=2))


class S1ColdOpen(CueScene):
    SEG = "s1"

    def construct(self):
        # l1: the file and the memory, to scale
        self.at("l1")
        _, noise = strip_images(STRIP["states"][0], strip_h=10)
        fbar = ImageMobject(noise).stretch_to_fit_width(11.0).stretch_to_fit_height(0.42)
        fbar.move_to([-5.6, 2.95, 0], aligned_edge=LEFT)
        flab = mono("records.txt · 100 GB", 20, INK).next_to(fbar, UP, 0.1, aligned_edge=LEFT)
        mbar = Rectangle(width=11.0 * 16 / 100, height=0.42, stroke_color=TRAY_EDGE, stroke_width=2.5,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([-5.6, 1.95, 0], aligned_edge=LEFT)
        mlab = mono("laptop memory · 16 GB", 20, INK).next_to(mbar, RIGHT, 0.25)
        self.play(FadeIn(flab), GrowFromEdge(fbar, LEFT), run_time=1.2)
        self.play(GrowFromEdge(mbar, LEFT), FadeIn(mlab), run_time=0.8)
        top = Group(fbar, flab, mbar, mlab)

        # l2: Python tries to hold it all
        self.at("l2")
        self.play(top.animate.scale(0.62).to_edge(UP, buff=0.35).shift(1.9 * LEFT), run_time=0.6)
        foot = VGroup(mono("real runs, scaled down 100×:", 16, FAINT),
                      mono("a 1 GB file · sort -S 160M", 16, FAINT),
                      mono("Python capped at 600 MB", 16, FAINT)).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        foot.move_to([-6.6, -2.5, 0], aligned_edge=LEFT)
        lt = terminal(6.6, 2.5, "python").move_to([-3.45, 0.75, 0])
        cmd1 = mono("$ python3 -c \"lines = sorted(open('records.txt'))\"", 14, INK)
        cmd1.next_to(lt[0].get_corner(UL), DR, buff=0.45).shift(0.1 * DOWN)
        g1 = Gauge(5.9, lt[0].get_corner(DL) + np.array([0.35, 0.3, 0]), CORAL, cap_label=True)
        self.play(FadeIn(lt), FadeIn(foot), run_time=0.4)
        self.play(AddTextLetterByLetter(cmd1), run_time=0.6)
        self.add(g1)
        samples = PYCAP["samples"]
        peak = max(s["rss_kb"] for s in samples)
        t_py = 1.6

        def py_upd(m, a):
            t = a * PYCAP["duration_s"]
            v = 0
            for s in samples:
                if s["t"] <= t:
                    v = s["rss_kb"]
            m.set_value(v if t < 0.46 else peak)
        self.play(UpdateFromAlphaFunc(g1.kb, py_upd, rate_func=linear), run_time=t_py)
        tb = VGroup(*[mono(l, 14, CORAL if l.startswith("MemoryError") else MUTED)
                      for l in PYCAP["stderr"].strip().splitlines()])
        tb.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(cmd1, DOWN, 0.2, aligned_edge=LEFT)
        self.play(FadeIn(tb), run_time=0.3)
        self.play(Indicate(tb[-1], color=CORAL, scale_factor=1.15), run_time=0.6)

        # l3: GNU sort
        self.at("l3")
        rt = terminal(6.6, 2.5, "shell").move_to([3.45, 0.75, 0])
        cmd2 = mono("$ sort records.txt -o sorted.txt", 14, INK)
        cmd2.next_to(rt[0].get_corner(UL), DR, buff=0.45).shift(0.1 * DOWN)
        g2 = Gauge(5.9, rt[0].get_corner(DL) + np.array([0.35, 0.3, 0]), ICE)
        self.play(FadeIn(rt), run_time=0.4)
        self.play(AddTextLetterByLetter(cmd2), run_time=0.5)
        self.add(g2)

        # the temp folder, replayed from the capture
        panel = RoundedRectangle(corner_radius=0.14, width=6.6, height=3.35, stroke_color=DIM, stroke_width=2,
                                 fill_color=PANEL, fill_opacity=1).move_to([3.45, -2.05, 0])
        plab = mono("/tmp", 16, FAINT).next_to(panel.get_corner(UL), DR, buff=0.12)
        names = []
        for s in SORTCAP["samples"]:
            for f in s["tmp_files"]:
                if f["name"] not in names:
                    names.append(f["name"])
        full = max(f["bytes"] for s in SORTCAP["samples"] for f in s["tmp_files"])
        row_y = [panel.get_top()[1] - 0.52 - 0.2 * i for i in range(len(names))]
        tt = ValueTracker(0.0)
        text_cache = {}

        def cached(key, s, color):
            if key not in text_cache:
                text_cache[key] = mono(s, 14, color)
            return text_cache[key].copy()

        def sample_at(t):
            cur = SORTCAP["samples"][0]
            for s in SORTCAP["samples"]:
                if s["t"] <= t:
                    cur = s
            return cur

        x0 = panel.get_left()[0] + 0.25

        def folder(rows_only=False):
            s = sample_at(tt.get_value())
            g = VGroup()
            present = {f["name"]: f["bytes"] for f in s["tmp_files"]}
            for i, nm in enumerate(names):
                if nm not in present:
                    continue
                y = row_y[i]
                g.add(cached(("n", nm), nm, INK).move_to([x0, y, 0], aligned_edge=LEFT))
                w = 3.2 * present[nm] / full
                g.add(Rectangle(width=max(w, 0.01), height=0.1, stroke_width=0, fill_color=MUTED,
                                fill_opacity=0.8).move_to([x0 + 1.55, y, 0], aligned_edge=LEFT))
            if rows_only:
                return g
            out = s["output_bytes"]
            yo = panel.get_bottom()[1] + 0.3
            g.add(cached(("o",), "sorted.txt", ICE).move_to([x0, yo, 0], aligned_edge=LEFT))
            g.add(Rectangle(width=max(3.2 * out / SORTCAP["input_bytes"], 0.01), height=0.1, stroke_width=0,
                            fill_color=ICE, fill_opacity=0.9).move_to([x0 + 1.55, yo, 0], aligned_edge=LEFT))
            mb = out // 10 ** 6
            g.add(cached(("om", mb), f"{mb:,} MB", MUTED).move_to([x0 + 5.0, yo, 0], aligned_edge=LEFT))
            n = len(present)
            g.add(cached(("c", n), f"{n} temp files", MUTED).move_to([panel.get_right()[0] - 0.25,
                                                                    panel.get_top()[1] - 0.2, 0],
                                                                   aligned_edge=RIGHT))
            g2.kb.set_value(s["sort_rss_kb"])
            return g
        fold = always_redraw(folder)
        self.play(FadeIn(panel), FadeIn(plab), FadeIn(fold), run_time=0.4)

        # l4: the replay (6.9 s of real time, shown in about 5.9 s)
        self.at("l3", 1.6)
        t_start = self.now()
        t_end = self.start_of("l5") + 0.1
        self.play(tt.animate.set_value(SORTCAP["duration_s"]), run_time=t_end - t_start, rate_func=linear)
        done = mono("$", 14, INK).next_to(cmd2, DOWN, 0.18, aligned_edge=LEFT)
        self.add(done)

        # l5: those files are the whole trick
        self.at("l5", 0.1)
        tt.set_value(3.85)                     # the moment all 12 runs exist
        ghost = folder(rows_only=True).set_opacity(0.45)
        tt.set_value(SORTCAP["duration_s"])
        brace = Brace(ghost, LEFT, color=ICE)
        bl = T(f"{SORTCAP['n_temp_files_max']} temp files:\nthe whole trick", 24, ICE).next_to(brace, LEFT, 0.15)
        self.play(FadeIn(ghost), GrowFromCenter(brace), FadeIn(bl), run_time=0.6)

        # l6: title
        self.at("l6")
        fold.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        title = T("Bigger Than Memory", 72, INK, weight=SEMIBOLD)
        sub = T("sorting a file that doesn't fit", 30, MUTED)
        g = VGroup(title, sub).arrange(DOWN, buff=0.3)
        self.play(FadeIn(title, shift=0.15 * UP), run_time=0.9)
        self.play(FadeIn(sub), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(FadeOut(g), run_time=0.45)
        self.finish()
