"""Pieces shared by the queueing lesson's scenes: a live queue driven by a simulated trace, a
response-time bar, a request Gantt chart and the response-time curve."""
import bisect

from common import *

Q = json.loads((DATA / "queue.json").read_text())
S_MS = Q["S_ms"]
WAIT = "#5E6874"          # waiting time (grey); work is amber


class QueueView:
    """Requests as dots: arriving from the left, queueing, one in service, leaving to the right.

    Driven by a FIFO trace (arrival and departure times in seconds). Request k sits at slot
    k - D(tau), where D(tau) counts departures, each easing in over `ease` seconds of trace time,
    so the line shuffles forward smoothly; slot 0 is the server, negative slots have left."""

    def __init__(self, trace, server_x=2.4, y=0.0, gap=0.36, speed=25.0, max_slots=16):
        self.arr, self.dep = trace["arrivals"], trace["departures"]
        self.sx, self.y, self.gap, self.speed, self.max_slots = server_x, y, gap, speed, max_slots
        self.tau = ValueTracker(0.0)            # trace time, seconds
        self.ease = 0.15 / speed                # 0.15 s of video
        self.fly = 0.35 / speed                 # arrivals drop in over 0.35 s of video
        self.box = RoundedRectangle(corner_radius=0.12, width=0.8, height=0.8, stroke_color=TRAY_EDGE,
                                    stroke_width=2.5, fill_color=TRAY_FILL, fill_opacity=1).move_to([server_x, y, 0])
        self.lab = label("server", 18, INK).next_to(self.box, DOWN, 0.15)
        self.qlab = label("queue", 18, MUTED).move_to([server_x - 0.36 * 5.5, y - 0.55, 0])

    def draw(self):
        tau = self.tau.get_value()
        g = VGroup()
        lo = bisect.bisect_left(self.dep, tau - 3 * self.ease - 2 * self.fly)
        hi = bisect.bisect_right(self.arr, tau + self.fly)
        ndep_done = bisect.bisect_right(self.dep, tau - self.ease)
        for k in range(max(lo, 0), hi):
            # smooth departure count around k's neighbourhood
            D = ndep_done
            for j in range(ndep_done, min(len(self.dep), ndep_done + 3)):
                D += min(1.0, max(0.0, (tau - self.dep[j]) / self.ease))
            slot = k - D
            if slot > self.max_slots:
                continue
            if slot >= 1:
                x = self.sx - 0.35 - self.gap * slot
            elif slot >= 0:
                x = self.sx - (0.35 + self.gap) * slot
            else:
                x = self.sx + 1.1 * (-slot)
            op, y = 1.0, self.y
            if tau < self.arr[k]:                       # still dropping in from above
                f = (self.arr[k] - tau) / self.fly
                y += 1.3 * f
                op = max(0.0, 1 - f)
            if slot < 0:
                op = max(0.0, 1 + slot)                 # fade as it leaves
            dot = Dot([x, y, 0], radius=0.12, color=ICE).set_opacity(op)
            g.add(dot)
            if 0 <= slot < 0.5 and tau >= self.arr[k]:
                g.add(Circle(radius=0.2, stroke_color=AMBER, stroke_width=3).move_to([x, self.y, 0]).set_stroke(opacity=op))
        return g

    def mobject(self):
        return always_redraw(self.draw)

    def run(self, scene, t0, t1, run_time):
        self.tau.set_value(t0)
        scene.play(self.tau.animate.set_value(t1), run_time=run_time, rate_func=linear)


def response_bar(wait_ms, y, unit=0.085, x0=-5.2, h=0.46, label_text=None):
    """A response time drawn to scale: grey waiting, then amber work."""
    w = Rectangle(width=max(wait_ms * unit, 0.001), height=h, stroke_width=0, fill_color=WAIT, fill_opacity=0.9)
    w.move_to([x0, y, 0], aligned_edge=LEFT)
    k = Rectangle(width=S_MS * unit, height=h, stroke_width=0, fill_color=AMBER, fill_opacity=0.95)
    k.next_to(w, RIGHT, buff=0)
    g = VGroup(w, k)
    return g


def curve_axes(x0=-5.4, y0=-2.7, w=10.2, h=5.2, tmax=250.0):
    """Utilization 0..100% across, average response time 0..tmax ms up."""
    def P(rho, t):
        return np.array([x0 + w * rho, y0 + h * min(t, tmax) / tmax, 0])
    ax = VGroup(Line(P(0, 0), P(1.0, 0), stroke_color=FAINT, stroke_width=2),
                Line(P(0, 0), P(0, tmax), stroke_color=FAINT, stroke_width=2))
    ticks = VGroup()
    for r in (0, 0.25, 0.5, 0.75, 1.0):
        ticks.add(mono(f"{int(r * 100)}%", 16, MUTED).next_to(P(r, 0), DOWN, 0.12))
    for t in (0, 50, 100, 150, 200, 250):
        ticks.add(mono(f"{t}", 16, MUTED).next_to(P(0, t), LEFT, 0.12))
    xl = mono("utilization (how busy)", 18, MUTED).next_to(P(0.5, 0), DOWN, 0.55)
    yl = mono("average response time (ms)", 18, MUTED).next_to(P(0, tmax), UP, 0.2).align_to(P(0, 0), LEFT)
    return P, VGroup(ax, ticks, xl, yl)


def mm1_curve(P, rmax=0.96, color=ICE, width=4, factor=1.0):
    """T = S + factor * rho * S / (1 - rho); factor 1 is M/M/1, larger is burstier (Kingman)."""
    pts = [P(r, S_MS + factor * r * S_MS / (1 - r)) for r in np.linspace(0, rmax, 200)
           if S_MS + factor * r * S_MS / (1 - r) <= 250]
    return VMobject(stroke_color=color, stroke_width=width).set_points_smoothly(pts)
