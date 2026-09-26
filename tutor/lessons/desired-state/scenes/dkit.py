"""Pieces shared by the desired-state scenes: machines holding pods, server boxes, a terminal,
the measure-compare-act loop, and the pod-count timelines from the controller simulation."""
import json
from common import *

RUN = (DATA / "terraform_run.txt").read_text()
CTRL = json.loads((DATA / "controller.json").read_text())
GOOD = ICE
BAD = CORAL


def run_line(prefix):
    """The first line of the real Terraform run that starts with prefix."""
    return next(l for l in RUN.splitlines() if l.startswith(prefix))


def terminal(lines, width=6.0, size=15):
    """A dark terminal box with monospace lines; each line is (text, color)."""
    rows = VGroup(*[mono(t, size, c) for t, c in lines]).arrange(DOWN, buff=0.13, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.1, width=max(width, rows.width + 0.5), height=rows.height + 0.5,
                           stroke_color=DIM, stroke_width=1.5, fill_color="#0B0E12", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(0.25 * RIGHT)
    return VGroup(box, rows)


class Machine(VGroup):
    """A machine: a box with its name, holding pods in a row."""
    def __init__(self, name, x, y, w=2.6, h=1.7):
        super().__init__()
        self.box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=MUTED, stroke_width=2,
                                    fill_color=PANEL, fill_opacity=1).move_to([x, y, 0])
        self.name = mono(name, 14, MUTED).move_to(self.box.get_bottom() + 0.25 * UP)
        self.add(self.box, self.name)

    def slot(self, i, n=2):
        """Centre of pod slot i (of n) inside the box."""
        c = self.box.get_center() + 0.2 * UP
        return c + (i - (n - 1) / 2) * 1.05 * RIGHT


def pod(p, text="web", color=ICE):
    r = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.5, stroke_color=color, stroke_width=2,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to(p)
    return VGroup(r, mono(text, 14, color).move_to(r))


def server(name, x, y, color=INK, w=1.35, h=0.8):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=TRAY_EDGE, stroke_width=2,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    return VGroup(r, mono(name, 15, color).move_to(r))


def cross(p, s=0.2, color=BAD):
    return VGroup(Line(p + np.array([-s, -s, 0]), p + np.array([s, s, 0]), stroke_color=color, stroke_width=5),
                  Line(p + np.array([-s, s, 0]), p + np.array([s, -s, 0]), stroke_color=color, stroke_width=5))


class Loop(VGroup):
    """Three steps on a circle, joined by curved arrows: measure -> compare -> act -> measure."""
    def __init__(self, steps=("measure", "compare", "act"), center=(0, 0), r=1.35, color=ICE, size=17):
        super().__init__()
        c = np.array([center[0], center[1], 0])
        angles = [PI / 2, PI / 2 - 2 * PI / 3, PI / 2 - 4 * PI / 3]
        self.pts = [c + r * np.array([np.cos(a), np.sin(a), 0]) for a in angles]
        self.labels = VGroup(*[self._lab(s, p, color, size) for s, p in zip(steps, self.pts)])
        self.arcs = VGroup()
        for i in range(3):
            a0, a1 = angles[i] - 0.42, angles[(i + 1) % 3] + 0.42 - (2 * PI if i == 2 else 0)
            arc = Arc(radius=r, start_angle=a0, angle=(a1 - a0), arc_center=c, stroke_color=FAINT, stroke_width=2.5)
            arc.add_tip(tip_length=0.16, tip_width=0.16)
            arc.get_tip().set_color(FAINT)
            self.arcs.add(arc)
        self.r = r
        self.hub = Dot(c, radius=0.001, fill_opacity=0, stroke_width=0)
        self.add(self.hub, self.arcs, self.labels)

    @property
    def center_pt(self):
        return self.hub.get_center()

    @staticmethod
    def _lab(s, p, color, size):
        t = mono(s, size, color)
        bg = RoundedRectangle(corner_radius=0.08, width=t.width + 0.35, height=t.height + 0.3, stroke_width=0,
                              fill_color=BG, fill_opacity=1).move_to(p)
        return VGroup(bg, t.move_to(p))

    def relabel(self, steps, color=ICE, size=17):
        new = VGroup(*[self._lab(s, o.get_center(), color, size) for s, o in zip(steps, self.labels)])
        return [Transform(o, n) for o, n in zip(self.labels, new)]

    def spin(self, turns=1, run_time=2.0):
        """A dot running round the loop."""
        r = self.r
        dot = Dot(self.center_pt + r * UP, radius=0.08, color=AMBER)
        path = Arc(radius=r, start_angle=PI / 2, angle=-2 * PI * turns, arc_center=self.center_pt)
        return Succession(FadeIn(dot, run_time=0.1), MoveAlongPath(dot, path, run_time=run_time, rate_func=linear),
                          FadeOut(dot, run_time=0.1))
