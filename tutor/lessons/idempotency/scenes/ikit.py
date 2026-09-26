"""Pieces shared by the idempotency scenes: client and server boxes, messages that can be lost,
sequence diagrams, and the customer's card."""
from common import *

KEY = "7f3a…c91"


def node(text, x, y, w=2.6, h=0.9, edge=TRAY_EDGE):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=edge, stroke_width=2.5,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    t = mono(text, 20, INK).move_to(r)
    return VGroup(r, t)


def lost_mark(p):
    s = 0.16
    return VGroup(Line(p + np.array([-s, -s, 0]), p + np.array([s, s, 0]), stroke_color=CORAL, stroke_width=5),
                  Line(p + np.array([-s, s, 0]), p + np.array([s, -s, 0]), stroke_color=CORAL, stroke_width=5))


def message(a, b, text="", color=ICE, lost_at=None, size=16):
    """An arrow from a to b; if lost_at (0..1) is given, it stops there with a coral cross."""
    a, b = np.array(a, dtype=float), np.array(b, dtype=float)
    end = a + (b - a) * (lost_at if lost_at is not None else 1.0)
    arr = Arrow(a, end, buff=0, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.12,
                tip_length=0.18) if lost_at is None else Line(a, end, color=color, stroke_width=3)
    g = VGroup(arr)
    if lost_at is not None:
        g.add(lost_mark(end))
    if text:
        lab = mono(text, size, color)
        ang = math.atan2(b[1] - a[1], b[0] - a[0])
        lab.rotate(ang if abs(ang) < PI / 2 else ang - PI).move_to((a + (end if lost_at else b)) / 2)
        lab.shift(0.2 * np.array([-math.sin(ang), math.cos(ang), 0]))
        g.add(lab)
    return g


class Card(VGroup):
    """The customer's card: total charged."""

    def __init__(self, pos, **kw):
        super().__init__(**kw)
        self.box = RoundedRectangle(corner_radius=0.1, width=2.7, height=0.95, stroke_color=MUTED, stroke_width=2,
                                    fill_color=PANEL, fill_opacity=1).move_to(pos)
        self.title = label("customer's card", 14, MUTED).next_to(self.box.get_top(), DOWN, 0.1)
        self.amount = mono("charged $0", 22, INK).next_to(self.title, DOWN, 0.1)
        self.add(self.box, self.title, self.amount)

    def set_total(self, dollars, color=None):
        new = mono(f"charged ${dollars}", 22, color or (CORAL if dollars > 50 else INK)).move_to(self.amount)
        return Transform(self.amount, new)


def lanes(x_client, x_server, top, bottom, names=("client", "server"), size=16):
    g = VGroup()
    for x, n in zip((x_client, x_server), names):
        g.add(mono(n, size, INK).move_to([x, top + 0.3, 0]),
              DashedLine([x, top, 0], [x, bottom, 0], color=DIM, stroke_width=1.5, dash_length=0.08))
    return g
