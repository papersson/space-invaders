from qkit import *

PW, PH = 11.6, 1.75           # panel width and height
PX = -5.5                     # panel left edge
T_MAX = 5.1                   # seconds of simulated time shown
Q_MAX = 20                    # requests in the system, top of the panel


def time_split(y, busy, w=10.0, x0=-5.0):
    b = Rectangle(width=w * busy, height=0.55, stroke_width=0, fill_color=AMBER, fill_opacity=0.9)
    b.move_to([x0, y, 0], aligned_edge=LEFT)
    sp = Rectangle(width=w * (1 - busy), height=0.55, stroke_width=0, fill_color=ICE, fill_opacity=0.85)
    sp.next_to(b, RIGHT, buff=0)
    lb = mono(f"new work arriving {int(busy * 100)}%", 18, BG).move_to(b)
    ls = mono(f"spare {int(round((1 - busy) * 100))}%", 18, BG).move_to(sp)
    if sp.width < 1.6:
        ls = mono(f"spare {int(round((1 - busy) * 100))}%", 18, ICE).next_to(sp, RIGHT, 0.15)
    return VGroup(b, sp, lb, ls)


def queue_panel(y_mid, label_text):
    frame = Rectangle(width=PW, height=PH, stroke_color=DIM, stroke_width=1.5).move_to([PX + PW / 2, y_mid, 0])
    lab = mono(label_text, 20, INK).next_to(frame, UP, 0.08, aligned_edge=LEFT)
    yl = mono("requests waiting or in service", 14, FAINT).next_to(frame, UP, 0.08, aligned_edge=RIGHT)
    return VGroup(frame, lab, yl)


def queue_line(trace, y_mid, upto):
    """Requests in the system over simulated time, as a step line, drawn up to `upto` seconds."""
    y0 = y_mid - PH / 2
    pts = []
    prev = 0
    for t, q in trace["queue"]:
        if t > upto or t > T_MAX:
            break
        x = PX + PW * t / T_MAX
        pts.append([x, y0 + PH * prev / Q_MAX, 0])
        pts.append([x, y0 + PH * q / Q_MAX, 0])
        prev = q
    x_end = PX + PW * min(upto, T_MAX) / T_MAX
    pts.append([x_end, y0 + PH * prev / Q_MAX, 0])
    if len(pts) < 2:
        pts = [[PX, y0, 0], [PX + 0.001, y0, 0]]
    line = VMobject(stroke_color=ICE, stroke_width=2.5).set_points_as_corners(pts)
    area = VMobject(stroke_width=0, fill_color=ICE, fill_opacity=0.18).set_points_as_corners(
        pts + [[pts[-1][0], y0, 0], [pts[0][0], y0, 0]])
    return VGroup(area, line)


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("Spare capacity")
        # 01-04: new work fills 80% of the server's time; the other 20% clears the queue
        self.at("01")
        head = T("what the server can do", 22, MUTED).move_to([-5.0, 2.4, 0], aligned_edge=LEFT)
        rule = T("a queue shrinks only when work finishes faster than it arrives", 22, INK).move_to([0, -2.6, 0])
        self.play(FadeIn(c), FadeIn(head), FadeIn(rule), run_time=0.6)
        split80 = time_split(1.5, 0.8)
        self.at("02")
        self.play(GrowFromEdge(split80[0], LEFT), FadeIn(split80[2]), run_time=0.8)
        self.at("03")
        self.play(GrowFromEdge(split80[1], LEFT), FadeIn(split80[3]), run_time=0.7)
        self.at("04")
        clears = mono("spare capacity: the only part that shrinks a queue", 20, ICE).next_to(split80, DOWN, 0.3, aligned_edge=RIGHT)
        self.play(FadeIn(clears), run_time=0.5)

        # 05-06: at 90% busy, half the spare capacity: the same queue takes about twice as long
        self.at("05")
        split90 = time_split(0.0, 0.9)
        self.play(GrowFromEdge(split90[0], LEFT), FadeIn(split90[2]), run_time=0.8)
        self.play(GrowFromEdge(split90[1], LEFT), FadeIn(split90[3]), run_time=0.5)
        self.at("06")
        twice = mono("half the spare capacity → about twice as long to clear, on average", 20, INK)
        twice.next_to(split90, DOWN, 0.35, aligned_edge=LEFT)
        self.play(FadeOut(rule), FadeIn(twice), run_time=0.6)

        # 08-09: the same random requests at both loads (simulated): the 90% queue is higher and longer
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        p80 = queue_panel(1.35, "80% busy")
        p90 = queue_panel(-1.75, "90% busy")
        note = mono("the same 400 random requests at both loads (simulated)", 16, FAINT).to_edge(DOWN, buff=0.3)
        tt = ValueTracker(0.0)
        l80 = always_redraw(lambda: queue_line(Q["trace"]["0.80"], 1.35, tt.get_value()))
        l90 = always_redraw(lambda: queue_line(Q["trace"]["0.90"], -1.75, tt.get_value()))
        self.play(FadeIn(p80), FadeIn(p90), FadeIn(note), run_time=0.5)
        self.add(l80, l90)
        span = max(self.end_of("09", -0.3) - self.now(), 4.0)
        self.play(tt.animate.set_value(T_MAX), run_time=span, rate_func=linear)
        l80.clear_updaters()
        l90.clear_updaters()
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
