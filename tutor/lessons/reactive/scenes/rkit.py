"""Pieces shared by the reactive scenes: the cart's dependency graph (nodes with a name and a
value, arrows from each value to its readers), a recomputation counter, and a terminal box."""
from common import *

GREEN = ICE          # right values
BAD = CORAL          # glitches and stale values
MARK = AMBER         # "out of date"

# the cart graph: name -> (label, x, y, width)
LAYOUT = {
    "price": ("price", -5.8, 1.1, 1.8),
    "qty": ("qty", -5.8, -0.7, 1.8),
    "subtotal": ("subtotal", -3.25, 0.2, 1.9),
    "tax": ("tax 10%", -1.0, 1.7, 1.8),
    "total": ("total", 1.2, 0.2, 1.8),
    "free": ("free shipping", 3.45, 0.2, 2.1),
    "banner": ("banner", 5.85, 0.2, 2.2),
}
EDGES = [("price", "subtotal"), ("qty", "subtotal"), ("subtotal", "tax"), ("subtotal", "total"),
         ("tax", "total"), ("total", "free"), ("free", "banner")]
BEFORE = {"price": "$20", "qty": "2", "subtotal": "$40", "tax": "$4", "total": "$44", "free": "no",
          "banner": "Spend $65…"}


class Node(VGroup):
    def __init__(self, key, value, h=1.05):
        name, x, y, w = LAYOUT[key]
        super().__init__()
        self.key = key
        self.box = RoundedRectangle(corner_radius=0.1, width=w, height=h, stroke_color=TRAY_EDGE, stroke_width=2,
                                    fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
        self.name = mono(name, 14, MUTED).move_to(self.box.get_top() + 0.22 * DOWN)
        self.val = self._v(value, INK)
        self.add(self.box, self.name, self.val)

    def _v(self, value, color):
        size = 22 if len(str(value)) <= 6 else 15
        return mono(str(value), size, color).move_to(self.box.get_center() + 0.12 * DOWN)

    def set(self, value, color=INK):
        """Animation: the value changes."""
        new = self._v(value, color)
        old = self.val
        self.remove(old)
        self.val = new
        self.add(new)
        return AnimationGroup(FadeOut(old, shift=0.15 * UP), FadeIn(new, shift=0.15 * UP), lag_ratio=0.3)

    def edge(self, color):
        return self.box.animate.set_stroke(color=color)


def arrow_between(a, b, color=FAINT):
    """Arrow from node a's box to node b's box, edge to edge."""
    pa, pb = a.box.get_center(), b.box.get_center()
    d = pb - pa
    d /= np.linalg.norm(d)
    start = a.box.get_boundary_point(d)
    end = b.box.get_boundary_point(-d)
    return Arrow(start, end, buff=0.06, color=color, stroke_width=2.5, max_tip_length_to_length_ratio=0.18,
                 tip_length=0.16)


class Graph(VGroup):
    def __init__(self, values=None):
        super().__init__()
        values = values or BEFORE
        self.n = {k: Node(k, values[k]) for k in LAYOUT}
        self.e = {(a, b): arrow_between(self.n[a], self.n[b]) for a, b in EDGES}
        self.add(*self.e.values(), *self.n.values())

    def pulse(self, a, b, color=MARK, run_time=0.5):
        """A dot travelling along the arrow a -> b."""
        arr = self.e[(a, b)]
        dot = Dot(arr.get_start(), radius=0.07, color=color)
        return Succession(FadeIn(dot, run_time=0.05), MoveAlongPath(dot, Line(arr.get_start(), arr.get_end()),
                                                                    run_time=run_time), FadeOut(dot, run_time=0.1))


class Tally(VGroup):
    """'recomputations: n' in the top right."""
    def __init__(self, title="recomputations", color=AMBER, pos=(6.7, 3.25)):
        super().__init__()
        self.title, self.color, self.pos = title, color, np.array([pos[0], pos[1], 0])
        self.n = 0
        self.t = self._t(0)
        self.add(self.t)

    def _t(self, n):
        return mono(f"{self.title}: {n}", 20, self.color).move_to(self.pos, aligned_edge=RIGHT)

    def inc(self, k=1):
        self.n += k
        new = self._t(self.n)
        old = self.t
        self.remove(old)
        self.t = new
        self.add(new)
        return FadeTransform(old, new, run_time=0.2)


def terminal(lines, width=9.5, size=17):
    """A dark terminal box with monospace lines; each line is (text, color)."""
    rows = VGroup(*[mono(t, size, c) for t, c in lines]).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.1, width=max(width, rows.width + 0.6), height=rows.height + 0.6,
                           stroke_color=DIM, stroke_width=1.5, fill_color="#0B0E12", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(0.3 * RIGHT)
    return VGroup(box, rows)
