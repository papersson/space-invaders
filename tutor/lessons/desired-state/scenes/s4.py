from dkit import *

X0, X1, T_END = -4.0, 5.8, 40
TOP, BOT = 1.1, -1.9          # baselines of the two timelines
H = 0.55                      # height of one pod on the count axis


def X(t):
    return X0 + (X1 - X0) * t / T_END


def Y(base, n):
    return base + (n - 2) * H


def count_path(base, timeline, t0, t1, color):
    """Step line of the pod count from t0 to t1."""
    pts = [[X(t0), Y(base, timeline[t0 - 1]), 0]] if t0 > 0 else []
    for t in range(t0, t1):
        n = timeline[t]
        pts += [[X(t), Y(base, n), 0], [X(t + 1), Y(base, n), 0]]
    return VMobject(stroke_color=color, stroke_width=3.5).set_points_as_corners(pts)


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("Compare states, not events")
        edge, level = CTRL["edge"]["timeline"], CTRL["level"]["timeline"]
        down0, down1 = CTRL["down"]

        # 01-02: react to events instead?
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        q = mono("why count the pods every time?", 22, INK).move_to([0, 2.0, 0])
        self.play(FadeIn(q), run_time=0.5)
        self.at("02")
        ev = VGroup(mono("event: pod died", 20, AMBER), mono("→", 20, MUTED), mono("start one pod", 20, INK)).arrange(RIGHT, buff=0.3)
        ev.move_to([0, 0.8, 0])
        self.play(FadeIn(ev, shift=0.2 * RIGHT), run_time=0.7)

        # 03-04: two controllers on one timeline
        self.at("03")
        self.play(FadeOut(q), FadeOut(ev), run_time=0.4)
        self.at("04")
        rows = VGroup()
        for base, name in ((TOP, "event-driven"), (BOT, "counts pods")):
            ax = Line([X(0), base - 0.9, 0], [X(T_END), base - 0.9, 0], stroke_color=FAINT, stroke_width=1.5)
            guide = VGroup(*[DashedLine([X(0), Y(base, n), 0], [X(T_END), Y(base, n), 0], stroke_color=DIM,
                                        stroke_width=1, dash_length=0.06) for n in (2, 3)])
            nums = VGroup(mono("3", 14, MUTED).move_to([X(0) - 0.3, Y(base, 3), 0]),
                          mono("2", 14, MUTED).move_to([X(0) - 0.3, Y(base, 2), 0]))
            rows.add(VGroup(ax, guide, nums))
        tlab = VGroup(*[mono(f"{t}s", 13, MUTED).move_to([X(t), BOT - 1.15, 0]) for t in (0, 10, 20, 30, 40)])
        names = [mono("event-driven", 18, INK).move_to([-5.6, TOP + 0.25, 0]),
                 mono("counts pods", 18, INK).move_to([-5.6, BOT + 0.25, 0])]
        pods_l = mono("pods", 13, MUTED).move_to([X(0) - 0.3, TOP + 1.05, 0])
        self.play(FadeIn(rows), FadeIn(tlab), FadeIn(names[0]), FadeIn(names[1]), FadeIn(pods_l), run_time=0.8)
        top = count_path(TOP, edge, 0, 10, ICE)
        bot = count_path(BOT, level, 0, 10, ICE)
        self.play(Create(top), Create(bot), run_time=1.0)

        # 05-06: crash at 10, both recover
        self.at("05")
        crashes = VGroup(*[cross(np.array([X(10), Y(b, 2) - 0.35, 0]), 0.1) for b in (TOP, BOT)])
        self.play(FadeIn(crashes), run_time=0.3)
        self.play(Create(count_path(TOP, edge, 10, 12, ICE)), Create(count_path(BOT, level, 10, 12, ICE)), run_time=0.6)
        self.at("06")
        env = mono("event → start one", 13, AMBER).move_to([X(11), TOP + 1.0, 0])
        env2 = mono("counted 2 → start one", 13, ICE).move_to([X(11), BOT + 1.0, 0])
        self.play(FadeIn(env), FadeIn(env2), run_time=0.4)
        self.play(Create(count_path(TOP, edge, 12, 20, ICE)), Create(count_path(BOT, level, 12, 20, ICE)), run_time=1.0)

        # 07-08: both controllers down 20-26; a crash at 22
        self.at("07")
        bands = VGroup()
        for b in (TOP, BOT):
            r = Rectangle(width=X(down1) - X(down0), height=1.5, stroke_width=0, fill_color=FAINT, fill_opacity=0.35)
            r.move_to([(X(down0) + X(down1)) / 2, b - 0.1, 0])
            bands.add(r)
        dl = mono("controller down", 13, MUTED).next_to(bands[0], UP, 0.08)
        self.play(FadeIn(bands), FadeIn(dl), FadeOut(env), FadeOut(env2), run_time=0.5)
        self.at("08")
        self.play(Create(count_path(TOP, edge, 20, 22, ICE)), Create(count_path(BOT, level, 20, 22, ICE)), run_time=0.5)
        c2 = VGroup(*[cross(np.array([X(22), Y(b, 2) - 0.35, 0]), 0.1) for b in (TOP, BOT)])
        self.play(FadeIn(c2), run_time=0.3)
        self.play(Create(count_path(TOP, edge, 22, 26, BAD)), Create(count_path(BOT, level, 22, 26, BAD)), run_time=0.6)

        # 09-11: the event is lost; the first controller stays at 2
        self.at("09")
        e = mono("pod died", 13, AMBER).move_to([X(22), TOP + 1.4, 0])
        self.play(FadeIn(e), run_time=0.3)
        self.at("10")
        self.play(e.animate.move_to([X(23), TOP - 0.4, 0]).set_opacity(0), run_time=0.9)
        lost = mono("lost", 14, BAD).move_to([X(23), TOP + 1.4, 0])
        self.play(FadeIn(lost), run_time=0.3)
        self.at("11")
        self.play(Create(count_path(TOP, edge, 26, T_END, BAD)), run_time=1.2)
        good = mono("2 for good", 16, BAD).move_to([X(36), Y(TOP, 2) - 0.35, 0])
        self.play(FadeIn(good), run_time=0.4)

        # 12-13: the second one counts, and starts one
        self.at("12")
        self.play(Create(count_path(BOT, level, 26, 27, BAD)), run_time=0.4)
        self.at("13")
        note = mono("t=27: counted 2, want 3 → start one", 14, ICE).move_to([X(31.5), BOT + 1.0, 0])
        self.play(FadeIn(note), run_time=0.4)
        self.play(Create(count_path(BOT, level, 27, 29, BAD)), run_time=0.4)
        self.play(Create(count_path(BOT, level, 29, T_END, ICE)), run_time=0.9)
        back = mono("back to 3", 16, ICE).move_to([X(36), Y(BOT, 2) - 0.35, 0])
        self.play(FadeIn(back), run_time=0.3)

        # 14-15: the names
        self.at("14")
        n1 = mono("edge-triggered", 18, AMBER).move_to(names[0])
        self.play(Transform(names[0], n1), run_time=0.6)
        self.at("15")
        n2 = mono("level-triggered", 18, ICE).move_to(names[1])
        self.play(Transform(names[1], n2), run_time=0.6)

        # 16-17: what Kubernetes requires
        self.at("16")
        req = mono("Kubernetes design principles: level-based", 15, INK).move_to([3.3, 3.4, 0])
        self.play(FadeIn(req), run_time=0.5)
        self.at("17")
        hint = mono("events: only a hint to look again soon", 14, MUTED).next_to(req, DOWN, 0.12).align_to(req, LEFT)
        self.play(FadeIn(hint), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
