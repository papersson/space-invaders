from common import *

RACE = json.loads((DATA / "race.json").read_text())
FURN = "#2A3440"


def desk():
    top = RoundedRectangle(corner_radius=0.05, width=3.4, height=0.14, fill_color=FURN, fill_opacity=1,
                           stroke_width=0)
    legs = VGroup(*[Rectangle(width=0.1, height=0.9, fill_color=FURN, fill_opacity=1, stroke_width=0)
                    .next_to(top, DOWN, buff=0).shift(dx * RIGHT) for dx in (-1.45, 1.45)])
    items = VGroup(*[Card(v, num=False).scale(0.42) for v in (9, 30, 17, 41)]).arrange(RIGHT, buff=0.08)
    items.next_to(top, UP, buff=0.02)
    return VGroup(legs, top, items)


def warehouse(seed=2):
    body = Rectangle(width=6.4, height=2.0, fill_color=PANEL, fill_opacity=1, stroke_color=DIM, stroke_width=2)
    teeth = []
    x0, w = -3.2, 6.4 / 5
    for i in range(5):
        a = x0 + i * w
        teeth += [[a, 1.0, 0], [a + w * 0.75, 1.45, 0], [a + w, 1.0, 0]]
    roof = Polygon(*teeth, [3.2, 1.0, 0], fill_color=DIM, fill_opacity=1, stroke_width=0)
    rng = np.random.default_rng(seed)
    shelves = VGroup()
    for row in range(3):
        shelf = VGroup(*[Card(int(v), num=False).scale(0.3) for v in rng.integers(1, 49, 18)])
        shelf.arrange(RIGHT, buff=0.05).move_to([0, 0.55 - row * 0.5, 0])
        shelves.add(shelf)
    door = Rectangle(width=0.9, height=0.55, fill_color=BG, fill_opacity=1, stroke_color=DIM,
                     stroke_width=2).move_to([0, -0.72, 0])
    return VGroup(body, roof, shelves, door)


def truck(cargo=None):
    box = RoundedRectangle(corner_radius=0.05, width=0.75, height=0.4, fill_color="#3A4654", fill_opacity=1,
                           stroke_width=0)
    cab = RoundedRectangle(corner_radius=0.05, width=0.3, height=0.3, fill_color="#4A5766", fill_opacity=1,
                           stroke_width=0).next_to(box, RIGHT, buff=0.03).align_to(box, DOWN)
    wheels = VGroup(*[Circle(radius=0.08, fill_color=INK, fill_opacity=1, stroke_width=0)
                      .move_to(box.get_bottom() + np.array([dx, -0.02, 0])) for dx in (-0.22, 0.45)])
    g = VGroup(box, cab, wheels)
    if cargo is not None:
        cargo.scale_to_fit_height(0.26).next_to(box, UP, buff=0.03)
        g.add(cargo)
    return g


class S2Wall(CueScene):
    SEG = "s2"

    def construct(self):
        c = self.c = chip("The memory wall")
        # l1: desk and warehouse
        self.at("l1")
        d = desk().move_to([0, 2.35, 0])
        w = warehouse().scale(0.8).move_to([0, -2.2, 0])
        dl = VGroup(label("memory", 20, INK), T("your desk", 24, MUTED, slant=ITALIC)).arrange(DOWN, buff=0.08)
        dl.next_to(d, RIGHT, buff=0.6)
        wl = VGroup(label("disk", 20, INK), T("a warehouse across town", 24, MUTED, slant=ITALIC))
        wl.arrange(DOWN, buff=0.08, aligned_edge=LEFT).next_to(w, RIGHT, buff=0.5)
        road = CubicBezier([0, -0.95, 0], [4.8, -0.4, 0], [-4.8, 0.9, 0], [0, 1.45, 0])
        road_d = DashedVMobject(road, num_dashes=40).set_stroke(FAINT, 3)
        self.play(FadeIn(c), FadeIn(d, shift=0.1 * DOWN), FadeIn(dl), run_time=0.9)
        self.play(FadeIn(w, shift=0.1 * UP), FadeIn(wl), Create(road_d), run_time=1.2)

        # l2: instant desk, slow trips
        self.at("l2", 0.4)
        inst = T("instant", 24, ICE).next_to(d, LEFT, buff=0.6)
        self.play(FadeIn(inst), LaggedStart(*[Indicate(it, color=ICE, scale_factor=1.25) for it in d[2]],
                                            lag_ratio=0.2), run_time=1.2)
        self.at("l2", 3.6)
        tr = truck(Card(23, num=False))
        tr.move_to(road.point_from_proportion(0))
        slow = T("every trip: slow", 24, AMBER).next_to(w, LEFT, buff=0.35).shift(0.9 * UP)
        self.play(FadeIn(tr), FadeIn(slow), run_time=0.4)
        self.play(MoveAlongPath(tr, road), run_time=self.start_of("l3") - self.now() - 0.1, rate_func=linear)

        # l3-l4: the latency ladder, scaled so memory = 1 second
        self.at("l3")
        scene1 = VGroup(d, w, dl, wl, road_d, tr, inst, slow)
        self.play(FadeOut(scene1), run_time=0.5)
        self.ladder()

        # l5: one item or a crate: one trip either way
        self.at("l5")
        self.crate()

        # l6: count trips
        self.at("l6")
        big = M('what matters: <span foreground="#F2A93B">trips</span>, not operations', 40, INK,
                weight=MEDIUM).move_to([0, 0.3, 0])
        counter = Counter(0)
        self.play(FadeIn(big, shift=0.1 * UP), run_time=0.7)
        self.at("l6", 2.4)
        self.play(FadeIn(counter), Indicate(counter, color=AMBER, scale_factor=1.15), run_time=0.9)

        # l7-l10: the race
        self.at("l7")
        self.play(FadeOut(big), FadeOut(counter), FadeOut(self.c), run_time=0.5)
        self.race()
        self.finish()

    def ladder(self):
        # log10(seconds) axis, 0 .. 5.25 mapped to x in [-3.2, 6.3]
        def X(sec):
            return -3.2 + 9.5 * np.log10(max(sec, 1)) / 5.25
        rows = [("memory", "~100 ns", 1, "1 second"),
                ("SSD", "~90 µs", 900, "15 minutes"),
                ("hard disk", "~10 ms", 100_000, "28 hours")]
        head = M('if one memory access took <span foreground="#E6EBF0">one second</span>…', 30, MUTED)
        head.move_to([0, 2.6, 0])
        ticks = VGroup()
        for sec, name in ((1, "1 s"), (60, "1 min"), (3600, "1 hour"), (86400, "1 day")):
            x = X(sec)
            ticks.add(VGroup(DashedLine([x, 1.75, 0], [x, -2.35, 0], dash_length=0.05, stroke_width=1.2,
                                        color=DIM),
                             T(name, 18, FAINT, font=MONO).move_to([x, -2.6, 0])))
        axis_lab = T("log scale", 16, FAINT, font=MONO, slant=ITALIC).move_to([5.6, -2.95, 0])
        self.play(FadeIn(head), FadeIn(ticks), FadeIn(axis_lab), run_time=0.7)
        ys = [1.2, -0.1, -1.4]
        bars = []
        for (name, real, sec, human), y in zip(rows, ys):
            nl = T(name, 26, INK, weight=MEDIUM).move_to([-5.4, y + 0.14, 0], aligned_edge=LEFT)
            rl = T(real, 18, FAINT, font=MONO).move_to([-5.4, y - 0.2, 0], aligned_edge=LEFT)
            bar = Rectangle(width=max(X(sec) + 3.2, 0.12), height=0.36, fill_color=AMBER, fill_opacity=0.85,
                            stroke_width=0).move_to([-3.2, y, 0], aligned_edge=LEFT)
            hl = T(human, 24, INK, font=MONO)
            bars.append((nl, rl, bar, hl, y))
        # memory, then SSD during l3; the hard disk lands on l4
        for i, (nl, rl, bar, hl, y) in enumerate(bars):
            if i == 1:
                self.at("l3", 4.4)
            if i == 2:
                self.at("l4")
            if i < 2:
                hl.next_to(bar, RIGHT, buff=0.2)
            else:
                hl.set_color(BG).move_to(bar.get_right() + LEFT * (hl.width / 2 + 0.25))
            self.play(FadeIn(nl), FadeIn(rl), GrowFromEdge(bar, LEFT), run_time=0.9 if i else 0.6)
            self.play(FadeIn(hl), run_time=0.3)
        more = T("more than a day", 24, AMBER).next_to(bars[2][2], DOWN, buff=0.18).align_to(bars[2][2], RIGHT)
        self.play(FadeIn(more), run_time=0.4)
        self.until(self.start_of("l5") - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not self.c], run_time=0.45)

    def crate(self):
        lanes = []
        for y, cargo, text in ((1.2, Card(23), "one item"), (-1.0, make_block([5, 17, 23, 38], ORIGIN),
                                                            "a whole crate (a block)")):
            start, end = np.array([-4.4, y, 0]), np.array([3.5, y, 0])
            road = DashedLine(start + 0.6 * LEFT, end + 0.6 * RIGHT, dash_length=0.12, stroke_width=2,
                              color=FAINT).shift(0.32 * DOWN)
            src = label("disk", 18, MUTED).next_to(road, LEFT, 0.25)
            dst = label("memory", 18, INK).next_to(road, RIGHT, 0.25)
            tr = truck(cargo).scale(1.6).move_to(start)
            name = T(text, 24, MUTED).next_to(start, UP, buff=0.65).align_to(road, LEFT)
            lanes.append((road, src, dst, tr, name, end))
        self.play(*[FadeIn(VGroup(r, s, d, t, n)) for r, s, d, t, n, _ in lanes], run_time=0.7)
        self.play(*[tr.animate.move_to(end) for _, _, _, tr, _, end in lanes], run_time=2.6,
                  rate_func=smooth)
        stamps = VGroup(*[T("1 trip", 26, AMBER, font=MONO, weight=MEDIUM).next_to(tr, UP, 0.2)
                          for _, _, _, tr, _, _ in lanes])
        self.play(FadeIn(stamps, shift=0.1 * UP), run_time=0.4)
        self.until(self.start_of("l6") - 0.45)
        self.play(*[FadeOut(VGroup(*lane[:5])) for lane in lanes], FadeOut(stamps), run_time=0.4)

    def race(self):
        W, H = 11.4, 11.4 * 300 / 1400
        panels = []
        for name, key, y in (("heapsort", "heapsort", 1.55), ("merge sort", "mergesort", -1.75)):
            img = ImageMobject(str(DATA / f"race_{key}.png"))
            img.stretch_to_fit_width(W).stretch_to_fit_height(H).move_to([0.35, y, 0])
            frame = Rectangle(width=W + 0.1, height=H + 0.1, stroke_color=DIM, stroke_width=1.5).move_to(img)
            title = VGroup(T(name, 28, INK, weight=MEDIUM), T("N log N", 20, FAINT, font=MONO))
            title.arrange(RIGHT, buff=0.3, aligned_edge=DOWN).next_to(frame, UP, 0.12, aligned_edge=LEFT)
            cnt = Counter(0, title="TRIPS", size=34, anchor=frame.get_corner(UR) + np.array([0, 0.62, 0]))
            ylab = T("position in file", 16, FAINT, font=MONO).rotate(PI / 2).next_to(frame, LEFT, 0.12)
            panels.append(dict(img=img, frame=frame, title=title, cnt=cnt, key=key, ylab=ylab))
        xlab = T("time →", 16, FAINT, font=MONO).next_to(panels[1]["frame"], DOWN, 0.1, aligned_edge=RIGHT)
        foot = T("simulated: 262,144 keys · memory holds 1/16 · blocks of 256 · each dot is one trip",
                 18, FAINT, font=MONO).move_to([0, -3.62, 0])
        for p in panels:
            p["curtain_p"] = ValueTracker(0.0)
        for p in panels:
            fr, tr = p["frame"], p["curtain_p"]

            def make_curtain(fr=fr, tr=tr):
                x0 = fr.get_left()[0] + (fr.width) * tr.get_value()
                width = max(fr.get_right()[0] - x0, 0.001)
                r = Rectangle(width=width, height=fr.height - 0.06, fill_color=BG, fill_opacity=1,
                              stroke_width=0)
                return r.move_to([x0 + width / 2, fr.get_center()[1], 0])
            p["curtain"] = always_redraw(make_curtain)
        self.play(*[FadeIn(Group(p["img"], p["frame"], p["title"], p["cnt"], p["ylab"])) for p in panels],
                  *[FadeIn(p["curtain"]) for p in panels], FadeIn(xlab), FadeIn(foot), run_time=0.9)
        for p in panels:
            self.bring_to_front(p["curtain"], p["frame"])

        def reveal(p, run_time):
            cum = RACE[p["key"]]["cum_by_column"]
            head = Line(UP, DOWN, stroke_color=ICE, stroke_width=2).set_height(p["frame"].height)
            head.add_updater(lambda m, p=p: m.move_to([p["frame"].get_left()[0] + p["frame"].width *
                                                       p["curtain_p"].get_value(), p["frame"].get_y(), 0]))
            self.add(head)

            def upd(m, a):
                p["curtain_p"].set_value(a)
                p["cnt"].tracker.set_value(cum[min(int(a * (len(cum) - 1)), len(cum) - 1)] if a < 1 else cum[-1])
            self.play(UpdateFromAlphaFunc(p["cnt"].tracker, upd, rate_func=linear), run_time=run_time)
            self.remove(head)

        self.at("l8")
        reveal(panels[0], 4.3)
        per = T(f"≈ {RACE['heapsort']['trips'] / RACE['n']:.1f} trips per item", 22, AMBER, font=MONO)
        per.next_to(panels[0]["cnt"], LEFT, buff=0.5).align_to(panels[0]["title"], DOWN)
        self.play(FadeIn(per), run_time=0.35)
        self.at("l9")
        reveal(panels[1], 3.8)
        ratio = RACE["heapsort"]["trips"] / RACE["mergesort"]["trips"]
        fewer = T(f"{ratio:.1f}× fewer", 22, ICE, font=MONO)
        fewer.next_to(panels[1]["cnt"], LEFT, buff=0.5).align_to(panels[1]["title"], DOWN)
        self.play(FadeIn(fewer), run_time=0.35)
        # l10: bigger crates widen the gap (same simulation, B = 64 vs 256)
        self.at("l10")
        r64 = RACE["b64"]["heapsort"] / RACE["b64"]["mergesort"]
        gap = M(f'merge sort vs heapsort, blocks of 64: <span foreground="#8FD3FF">{r64:.1f}×</span> fewer · '
                f'blocks of 256: <span foreground="#8FD3FF">{ratio:.1f}×</span> fewer', 20, MUTED,
                font=MONO).move_to([0, -3.62, 0])
        self.play(FadeOut(foot), FadeIn(gap), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
