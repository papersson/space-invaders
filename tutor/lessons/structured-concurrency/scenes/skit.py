"""Pieces shared by the structured-concurrency scenes: request timelines replayed from the real
runs (data/timeline.json), code cards, the control-flow arrow pictures, and a counter line."""
import json
from common import *

TL = json.loads((DATA / "timeline.json").read_text())
RUNS = (DATA / "runs.txt").read_text()
GOOD = ICE
BAD = CORAL


def code_card(lines, size=17, title=None, width=None):
    """Lines of code, each (indent_level, text, color); Text drops leading spaces, so indent by hand."""
    rows = VGroup()
    for lvl, s, col in lines:
        t = mono(s, size, col)
        rows.add(t)
    rows.arrange(DOWN, buff=0.12, aligned_edge=LEFT)
    step = mono("xxxx", size).width          # four characters of the monospace font
    for (lvl, _, _), t in zip(lines, rows):
        t.shift(lvl * step * RIGHT)
    box = RoundedRectangle(corner_radius=0.1, width=max(width or 0, rows.width + 0.6), height=rows.height + 0.5,
                           stroke_color=DIM, stroke_width=1.5, fill_color="#0B0E12", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(0.3 * RIGHT)
    g = VGroup(box, rows)
    if title:
        g.add(label(title, 13).next_to(box, UP, 0.12).align_to(box, LEFT))
    return g


def events(run, who):
    return [e for e in TL[run] if e["who"] == who]


def when(run, who, what):
    """Time of the first event of `who` whose text starts with `what`."""
    return next(e["t"] for e in TL[run] if e["who"] == who and e["what"].startswith(what))


class Timeline(VGroup):
    """Two task bars (fetch_user, fetch_orders) on a time axis, drawn from one real run."""

    def __init__(self, run, x0=-4.2, x1=5.6, y=0.0, t_max=1.4, rows=("fetch_user", "fetch_orders"), gap=0.75):
        super().__init__()
        self.run, self.x0, self.x1, self.t_max = run, x0, x1, t_max
        self.ys = {r: y + gap * (len(rows) - 1) / 2 - gap * i for i, r in enumerate(rows)}
        self.axis_y = y - gap * (len(rows) - 1) / 2 - 0.6
        ax = Line([x0, self.axis_y, 0], [x1, self.axis_y, 0], stroke_color=FAINT, stroke_width=1.5)
        ticks = VGroup()
        t = 0.0
        while t <= t_max + 1e-9:
            ticks.add(Line([self.X(t), self.axis_y - 0.06, 0], [self.X(t), self.axis_y + 0.06, 0], stroke_color=FAINT, stroke_width=1.5),
                      mono(f"{t:.1f} s", 12, FAINT).move_to([self.X(t), self.axis_y - 0.28, 0]))
            t += 0.2
        self.axis = VGroup(ax, ticks)
        self.names = VGroup(*[mono(r, 16, INK).move_to([x0 - 0.2, yy, 0], aligned_edge=RIGHT) for r, yy in self.ys.items()])
        self.add(self.axis, self.names)

    def X(self, t):
        return self.x0 + (self.x1 - self.x0) * t / self.t_max

    def bar(self, who, t0, t1, color=ICE, h=0.34, opacity=0.85):
        w = max(0.02, self.X(t1) - self.X(t0))
        return Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=opacity).move_to(
            [self.X(t0), self.ys[who], 0], aligned_edge=LEFT)

    def cross(self, who, t, color=BAD, s=0.14):
        p = np.array([self.X(t), self.ys[who], 0])
        return VGroup(Line(p + [-s, -s, 0], p + [s, s, 0], stroke_color=color, stroke_width=5),
                      Line(p + [-s, s, 0], p + [s, -s, 0], stroke_color=color, stroke_width=5))

    def cut(self, who, t, color=ICE):
        """A short vertical stroke where a task was cancelled."""
        p = np.array([self.X(t), self.ys[who], 0])
        return Line(p + [0, -0.26, 0], p + [0, 0.26, 0], stroke_color=color, stroke_width=5)

    def vline(self, t, text, color=INK, top=None):
        top = top if top is not None else max(self.ys.values()) + 0.55
        ln = DashedLine([self.X(t), self.axis_y, 0], [self.X(t), top, 0], stroke_color=color, stroke_width=2, dash_length=0.08)
        lab = mono(text, 14, color).next_to(ln, UP, 0.08)
        return VGroup(ln, lab)

    def grow(self, bar, run_time):
        return GrowFromEdge(bar, LEFT, run_time=run_time, rate_func=linear)


def counter_line(text, color=INK, size=18):
    return mono(text, size, color)
