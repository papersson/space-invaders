import math

from common import *

RACE = json.loads((DATA / "race.json").read_text())
GIB = 2 ** 30
MEM = 16 * GIB
FAN = MEM // 2 ** 20 - 1          # 16,383 runs merged at once with 1 MiB blocks


def passes(nbytes, fan):
    runs = math.ceil(nbytes / MEM)
    return 0 if runs <= 1 else math.ceil(math.log(runs) / math.log(fan) - 1e-12)


class S6Passes(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("How many passes")
        # l1: a logarithm with a different base
        self.at("l1")
        two = M('2-way merge:  passes = log<sub>2</sub>(N/M)', 34, MUTED, font=MONO)
        wide = M('wide merge:   passes = log<sub><span foreground="#8FD3FF">M/B</span></sub>(N/M)',
                 34, INK, font=MONO)
        eqs = VGroup(two, wide).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to([0, 0.7, 0])
        self.play(FadeIn(c), FadeIn(two, shift=0.1 * UP), run_time=0.7)
        self.at("l1", 2.2)
        self.play(FadeIn(wide, shift=0.1 * UP), run_time=0.7)
        base = M('M/B = 16 GB ÷ 1 MB = <span foreground="#8FD3FF">16,384</span>', 30, MUTED, font=MONO)
        base.next_to(eqs, DOWN, buff=0.7)
        self.at("l1", 5.0)
        self.play(FadeIn(base, shift=0.1 * UP), run_time=0.6)

        # l2: the chart, 16 GB of memory, sizes from 16 GB to 1 PB
        self.at("l2")
        self.play(FadeOut(VGroup(eqs, base)), run_time=0.4)
        x0, x1 = math.log10(16e9), math.log10(1e15)
        ax = Axes(x_range=[x0, x1, 1], y_range=[0, 17, 2], x_length=10.6, y_length=5.0,
                  axis_config={"color": FAINT, "stroke_width": 2, "include_ticks": False,
                               "include_tip": False}).move_to([0.4, -0.2, 0])
        xt = VGroup()
        for val, name in ((16e9, "16 GB"), (1e11, "100 GB"), (1e12, "1 TB"), (1e13, "10 TB"),
                          (1e14, "100 TB"), (1e15, "1 PB")):
            p = ax.c2p(math.log10(val), 0)
            xt.add(VGroup(Line(p, p + 0.1 * DOWN, color=FAINT, stroke_width=2),
                          T(name, 18, MUTED, font=MONO).next_to(p, DOWN, 0.18)))
        yt = VGroup()
        for v in (0, 4, 8, 12, 16):
            p = ax.c2p(x0, v)
            yt.add(T(str(v), 18, MUTED, font=MONO).next_to(p, LEFT, 0.18))
            if v:
                yt.add(DashedLine(p, ax.c2p(x1, v), dash_length=0.05, stroke_width=1, color=DIM))
        ylab = T("merge passes over the data", 20, MUTED, font=MONO).next_to(ax, UP, 0.2).align_to(ax, LEFT)
        xlab = T("file size (16 GB of memory, 1 MB blocks)", 20, MUTED, font=MONO)
        xlab.next_to(xt, DOWN, 0.15)

        def curve(fan, color, width):
            xs = np.linspace(x0, x1, 900)
            pts, prev = [], None
            for x in xs:
                y = passes(10 ** x, fan)
                if prev is not None and y != prev:
                    pts.append(ax.c2p(x, prev))
                pts.append(ax.c2p(x, y))
                prev = y
            return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(pts)

        c2 = curve(2, MUTED, 4)
        cw = curve(FAN, ICE, 6)
        l2 = T("2-way", 22, MUTED, font=MONO).next_to(c2.get_end(), UP, 0.15).shift(0.3 * LEFT)
        lw = T("wide", 22, ICE, font=MONO).next_to(ax.c2p(x1, 2), UP, 0.12).shift(0.3 * LEFT)
        self.play(FadeOut(c), Create(ax), FadeIn(xt), FadeIn(yt), FadeIn(ylab), FadeIn(xlab), run_time=0.8)
        self.play(Create(c2), FadeIn(l2), run_time=1.6, rate_func=linear)
        self.play(Create(cw), FadeIn(lw), run_time=1.2, rate_func=linear)
        # 10 TB: 10 rounds vs 1
        self.at("l2", 3.2)
        xm = math.log10(1e13)
        p10, p1 = ax.c2p(xm, passes(1e13, 2)), ax.c2p(xm, passes(1e13, FAN))
        guide = DashedLine(ax.c2p(xm, 0), ax.c2p(xm, 16), dash_length=0.06, stroke_width=1.5, color=INK)
        d10 = Dot(p10, radius=0.09, color=MUTED)
        d1 = Dot(p1, radius=0.09, color=ICE)
        t10 = T(f"{passes(1e13, 2)} rounds", 24, INK, font=MONO).next_to(d10, LEFT, 0.2)
        t1 = T("1", 24, ICE, font=MONO).next_to(d1, UR, 0.1)
        self.play(Create(guide), FadeIn(d10), FadeIn(t10), run_time=0.6)
        self.play(FadeIn(d1), FadeIn(t1), run_time=0.5)

        # l3: one pass up to ~1/4 petabyte
        self.at("l3")
        lim = math.log10(MEM * FAN)
        band = Rectangle(width=ax.c2p(lim, 0)[0] - ax.c2p(x0, 0)[0], height=ax.c2p(0, 1.6)[1] - ax.c2p(0, 0)[1],
                         fill_color=ICE, fill_opacity=0.12, stroke_width=0)
        band.move_to(ax.c2p(x0, 0), aligned_edge=DL)
        qpb = M('1 pass up to <span foreground="#8FD3FF">16 GB × 16,383 ≈ ¼ PB</span>', 24, INK,
                font=MONO).move_to(ax.c2p(x1, 4.6), aligned_edge=RIGHT)
        arrow = Arrow(qpb.get_bottom() + 0.05 * DOWN + RIGHT * 0.9, ax.c2p(lim, 1.1), buff=0.05, color=ICE,
                      stroke_width=3, max_tip_length_to_length_ratio=0.12)
        self.play(FadeIn(band), FadeIn(qpb), GrowArrow(arrow), run_time=0.9)

        # l4: optimal
        self.at("l4")
        chart = VGroup(ax, xt, yt, ylab, xlab, c2, cw, l2, lw, guide, d10, d1, t10, t1, band, qpb, arrow)
        self.play(FadeOut(chart), run_time=0.5)
        card = RoundedRectangle(corner_radius=0.2, width=12.4, height=3.2, fill_color=PANEL, fill_opacity=1,
                                stroke_color=DIM, stroke_width=2)
        f = M('Θ( N/B · log<sub>M/B</sub> N/B )  block transfers', 38, INK, font=MONO)
        sub = T("no comparison sort can do asymptotically better in this model", 26, MUTED)
        cite = T("Aggarwal and Vitter, The input/output complexity of sorting and related problems, CACM 1988",
                 18, FAINT, slant=ITALIC)
        VGroup(f, sub, cite).arrange(DOWN, buff=0.35).move_to(card)
        self.play(FadeIn(card), FadeIn(f, shift=0.1 * UP), run_time=0.8)
        self.play(FadeIn(sub), FadeIn(cite), run_time=0.6)

        # l5: the scoreboard, from the same simulation as the race
        self.at("l5")
        self.play(FadeOut(VGroup(card, f, sub, cite)), run_time=0.45)
        rows = [("heapsort", RACE["heapsort"]["trips"], AMBER),
                ("2-way merge sort", RACE["mergesort"]["trips"], AMBER),
                ("external merge sort", RACE["external_mergesort"], AMBER)]
        top = rows[0][1]
        board = VGroup()
        bars = []
        for i, (name, n, col) in enumerate(rows):
            y = 1.3 - i * 1.25
            nl = T(name, 28, INK, weight=MEDIUM).move_to([-6.2, y + 0.32, 0], aligned_edge=LEFT)
            bar = Rectangle(width=max(10.6 * n / top, 0.03), height=0.34, fill_color=col, fill_opacity=0.9,
                            stroke_width=0).move_to([-6.2, y - 0.12, 0], aligned_edge=LEFT)
            num = T(f"{n:,} trips", 28, AMBER, font=MONO, weight=MEDIUM)
            num.move_to([6.4, y + 0.32, 0], aligned_edge=RIGHT)
            board.add(nl, num)
            bars.append(bar)
        foot = T("simulated: 262,144 keys · memory holds 1/16 · blocks of 256", 18, FAINT,
                 font=MONO).move_to([0, -2.9, 0])
        self.play(FadeIn(board), FadeIn(foot), *[GrowFromEdge(b, LEFT) for b in bars], run_time=1.0)
        x = T(f"{top / rows[2][1]:.0f}× fewer trips", 30, ICE, font=MONO, weight=MEDIUM)
        x.next_to(bars[2], RIGHT, 0.4)
        self.play(FadeIn(x, shift=0.1 * LEFT), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
