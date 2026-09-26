"""Pieces shared by the concurrency scenes: the account, cash machines, step boxes on two
timelines, a padlock, an actor with a mailbox, envelopes, a channel, and small bar charts."""
import json
from common import *

RUNS = (DATA / "runs.txt").read_text()
GOOD = ICE
BAD = CORAL


def box(text, x, y, w=2.2, h=0.8, edge=TRAY_EDGE, size=20, color=INK):
    r = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=edge, stroke_width=2.2,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    return VGroup(r, mono(text, size, color).move_to(r))


class Account(VGroup):
    """A labelled box with a balance that can change."""
    def __init__(self, x=0, y=0, value="$100", title="balance", w=2.4):
        super().__init__()
        self.box = RoundedRectangle(corner_radius=0.12, width=w, height=1.2, stroke_color=TRAY_EDGE, stroke_width=2.5,
                                    fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
        self.title = mono(title, 15, MUTED).move_to(self.box.get_top() + 0.25 * DOWN)
        self.val = mono(value, 30, INK).move_to(self.box.get_center() + 0.12 * DOWN)
        self.add(self.box, self.title, self.val)

    def set(self, value, color=INK):
        new = mono(value, 30, color).move_to(self.val)
        old = self.val
        self.remove(old)
        self.val = new
        self.add(new)
        return AnimationGroup(FadeOut(old, shift=0.15 * UP), FadeIn(new, shift=0.15 * UP), lag_ratio=0.3)


def machine(name, x, y):
    """A cash machine: a small box with a screen line and its name."""
    r = RoundedRectangle(corner_radius=0.08, width=1.3, height=1.5, stroke_color=MUTED, stroke_width=2,
                         fill_color=PANEL, fill_opacity=1).move_to([x, y, 0])
    scr = Rectangle(width=0.9, height=0.45, stroke_color=FAINT, stroke_width=1.5, fill_color=DIM,
                    fill_opacity=1).move_to(r.get_top() + 0.4 * DOWN)
    lab = mono(name, 22, INK).move_to(r.get_center() + 0.3 * DOWN)
    return VGroup(r, scr, lab)


def step(text, x, y, color=INK, w=1.9, size=16, edge=None):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=0.55, stroke_color=edge or color, stroke_width=1.8,
                         fill_color=PANEL, fill_opacity=1).move_to([x, y, 0])
    return VGroup(r, mono(text, size, color).move_to(r))


def lane(name, y, x0=-6.3, x1=3.4, color=MUTED):
    ln = Line([x0 + 0.9, y, 0], [x1, y, 0], stroke_color=DIM, stroke_width=1.5)
    return VGroup(mono(name, 20, color).move_to([x0 + 0.3, y, 0]), ln)


def padlock(p, color=AMBER, s=1.0):
    body = RoundedRectangle(corner_radius=0.05, width=0.36 * s, height=0.28 * s, stroke_color=color, stroke_width=2.5,
                            fill_color=color, fill_opacity=0.25).move_to(p)
    shackle = Arc(radius=0.12 * s, start_angle=0, angle=PI, stroke_color=color, stroke_width=2.5)
    shackle.move_to(body.get_top() + 0.1 * s * UP)
    return VGroup(body, shackle)


def envelope(text="", color=INK, w=0.7, h=0.45):
    r = Rectangle(width=w, height=h, stroke_color=color, stroke_width=1.8, fill_color=PANEL, fill_opacity=1)
    v = VMobject(stroke_color=color, stroke_width=1.5).set_points_as_corners(
        [r.get_corner(UL), r.get_center() + 0.05 * DOWN, r.get_corner(UR)])
    g = VGroup(r, v)
    if text:
        g.add(mono(text, 13, color).next_to(r, UP, 0.06))
    return g


class Actor(VGroup):
    """A circle holding private state, with a mailbox slot on its left."""
    def __init__(self, x=1.5, y=0.3, value="$100", r=1.05):
        super().__init__()
        self.circle = Circle(radius=r, stroke_color=ICE, stroke_width=3, fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
        self.title = mono("actor", 15, ICE).move_to(self.circle.get_top() + 0.3 * DOWN)
        self.val = mono(value, 28, INK).move_to(self.circle.get_center())
        self.priv = mono("private", 13, MUTED).move_to(self.circle.get_bottom() + 0.3 * UP)
        self.mail = Rectangle(width=0.9, height=1.5, stroke_color=MUTED, stroke_width=2, fill_color=PANEL,
                              fill_opacity=1).next_to(self.circle, LEFT, 0.15)
        self.mail_l = mono("mailbox", 14, MUTED).next_to(self.mail, DOWN, 0.12)
        self.add(self.mail, self.mail_l, self.circle, self.title, self.val, self.priv)

    def set(self, value, color=INK):
        new = mono(value, 28, color).move_to(self.val)
        old = self.val
        self.remove(old)
        self.val = new
        self.add(new)
        return AnimationGroup(FadeOut(old, shift=0.15 * UP), FadeIn(new, shift=0.15 * UP), lag_ratio=0.3)

    def slot(self, i):
        """Position of the i-th queued message in the mailbox (0 = next)."""
        return self.mail.get_bottom() + (0.35 + 0.5 * i) * UP


def channel(a, b, color=MUTED):
    """A pipe from point a to point b."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    d = (b - a) / np.linalg.norm(b - a)
    n = np.array([-d[1], d[0], 0]) * 0.16
    pipe = VGroup(Line(a + n, b + n, stroke_color=color, stroke_width=2.5), Line(a - n, b - n, stroke_color=color,
                                                                                  stroke_width=2.5))
    return pipe


def waiting_bar(p, w=1.6, color=FAINT, text="waiting"):
    r = Rectangle(width=w, height=0.22, stroke_width=0, fill_color=color, fill_opacity=0.8).move_to(p, aligned_edge=LEFT)
    return VGroup(r, mono(text, 13, MUTED).next_to(r, UP, 0.05))


def cross(p, s=0.16, color=BAD):
    return VGroup(Line(p + np.array([-s, -s, 0]), p + np.array([s, s, 0]), stroke_color=color, stroke_width=5),
                  Line(p + np.array([-s, s, 0]), p + np.array([s, -s, 0]), stroke_color=color, stroke_width=5))
