from skit import *

K = 0.5                      # the diagram's scale in this chapter
UPS = np.array([1.2, 2.0, 0])  # and its shift


def sp(p):
    """Where a point of the full-size diagram lands once it is shrunk to the top half."""
    return K * np.array(p, dtype=float) + UPS


DX0, DSTEP = -4.55, 0.58      # the twenty dots: x of the first, spacing
R1, R2 = -1.35, -2.7         # rows: y of the dots


def start_s6(sc):
    d, col = sc.d, sc.col
    sc.add(*d.base(4), d.tag_claude)
    col.place([instr_item(col, short=True), task_item(col, short=True)])


class S6(LScene):
    SEG = "s6"

    def row(self, y, values, head, color=NUM):
        dots = VGroup(*[Dot([DX0 + DSTEP * k, y, 0], radius=0.07, color=FAINT) for k in range(20)])
        nums = [T(str(v), 15, color, font=MONO).move_to([DX0 + DSTEP * k, y - 0.36, 0]) for k, v in enumerate(values)]
        hd = T(head, 16, INK, font=MONO).move_to([-6.85, y, 0], aligned_edge=LEFT)
        return dots, nums, hd

    def fill(self, dots, nums, t_end, first=0):
        """Light the dots and write the numbers from `first` on, evenly until t_end."""
        n = len(nums) - first
        dt = max((t_end - self.now()) / n, 1 / 15 + 0.01)
        for k in range(first, len(nums)):
            self.play(dots[k].animate.set_color(NUM), FadeIn(nums[k]), run_time=dt)

    def construct(self):
        d, col = self.d, self.col
        ch = chip("6 · why it took until now")
        start_s6(self)
        diagram = Group(*self.mobjects)
        self.add(ch)
        self.fade_in_all(0.3)

        # 01: shrink the diagram to the top half
        self.at("01", 0.3)
        self.play(diagram.animate.scale(K, about_point=ORIGIN).shift(UPS), run_time=1.0)

        # 02-03: 2023: models in loops that got stuck going round in circles
        self.at("02")
        yr = label("2023 · early agents", 18, INK).move_to([-6.85, -0.45, 0], aligned_edge=LEFT)
        circ = Circle(radius=0.55, color=FAINT, stroke_width=2.5).move_to([-5.9, -1.75, 0])
        tip = Triangle(fill_opacity=1, stroke_width=0, color=FAINT).scale(0.08).rotate(-PI / 2).move_to(circ.point_at_angle(PI / 2))
        self.play(FadeIn(yr), Create(circ), FadeIn(tip), run_time=0.6)
        self.at("03")
        dot = Dot(radius=0.08, color=INK).move_to(circ.point_at_angle(0))
        self.add(dot)
        s, e = self.cues["03"]
        self.play(Rotate(dot, angle=-3 * TAU, about_point=circ.get_center()), run_time=e - s + 0.6, rate_func=linear)

        # 04-05: small mistakes add up: twenty steps, 95% each
        self.at("04")
        self.play(FadeOut(VGroup(circ, tip, dot)), yr.animate.set_opacity(0.5), run_time=0.4)
        dots1, nums1, hd1 = self.row(R1, TR["runs95"], "95% each")
        st1 = tag("step 1", FAINT, 13).next_to(dots1[0], UP, buff=0.14)
        st20 = tag("step 20", FAINT, 13).next_to(dots1[-1], UP, buff=0.14)
        self.play(LaggedStart(*[FadeIn(x) for x in dots1], lag_ratio=0.05), FadeIn(st1), FadeIn(st20), run_time=1.0)
        self.at("05", 0.5)
        cav = tag("assuming each step's chance is the same whatever came before, and no mistake is caught",
                  MUTED, 14).move_to([0, -3.75, 0])
        self.play(FadeIn(hd1), FadeIn(cav), run_time=0.5)

        # 06-11: a hundred runs; 95 after one step, 90 after two, ... 36 after twenty
        self.at("06")
        start = T("100 runs", 15, MUTED, font=MONO).move_to([-6.85, R1 - 0.36, 0], aligned_edge=LEFT)
        self.play(FadeIn(start), run_time=0.4)
        self.at("07", 0.4)
        self.play(dots1[0].animate.set_color(NUM), FadeIn(nums1[0]), run_time=0.4)
        self.at("08", 0.8)
        self.play(dots1[1].animate.set_color(NUM), FadeIn(nums1[1]), run_time=0.4)
        ring = Circle(radius=0.22, color=NUM, stroke_width=2).move_to(nums1[1])
        self.play(Create(ring), run_time=0.4)
        self.at("09")
        self.play(FadeOut(ring), run_time=0.2)
        self.fill(dots1, nums1, self.cues["10"][0] + 1.0, first=2)
        self.at("10", 1.2)
        big = SurroundingRectangle(nums1[-1], color=NUM, buff=0.06, corner_radius=0.05)
        self.play(Create(big), run_time=0.4)
        self.at("11")
        third = T("about 1 in 3", 18, NUM, font=MONO, weight=MEDIUM).move_to([6.95, R1 - 0.78, 0], aligned_edge=RIGHT)
        self.play(FadeIn(third), run_time=0.4)

        # 12-13: three things changed; first, models trained for the loop
        self.at("13")
        m_tr = d.model
        mk1 = T("1 · trained for the loop", 18, INK, weight=MEDIUM).move_to(sp([2.4, 2.55, 0]), aligned_edge=LEFT)
        a1 = arrow(mk1.get_left() + LEFT * 0.08, m_tr.get_right() + RIGHT * 0.05 + UP * 0.1, color=INK, sw=2)
        self.play(FadeIn(mk1), GrowArrow(a1), Indicate(VGroup(d.model, d.model_name), color=MODEL, scale_factor=1.08), run_time=0.8)

        # 14-15: suppose 99% a step: 82 of the hundred, about 4 in 5
        self.at("14")
        dots2, nums2, hd2 = self.row(R2, TR["runs99"], "99% each")
        sup = tag("(suppose)", MUTED, 13).next_to(hd2, DOWN, buff=0.08, aligned_edge=LEFT)
        start2 = T("100", 15, MUTED, font=MONO).move_to([-6.85, R2 - 0.36, 0], aligned_edge=LEFT)
        self.play(FadeIn(hd2), FadeIn(sup), FadeIn(dots2), run_time=0.5)
        self.at("15")
        self.fill(dots2, nums2, self.cues["15"][1] - 1.0)
        box2 = SurroundingRectangle(nums2[-1], color=NUM, buff=0.06, corner_radius=0.05)
        five = T("about 4 in 5", 18, NUM, font=MONO, weight=MEDIUM).move_to([6.95, R2 - 0.78, 0], aligned_edge=RIGHT)
        self.play(Create(box2), FadeIn(five), run_time=0.5)

        # 16-17: second, feedback: a failing test catches a mistake (the discount, chapter 5)
        self.at("16")
        rows = VGroup(dots1, *nums1, hd1, st1, st20, start, big, third, dots2, *nums2, hd2, sup, box2, five, cav, yr)
        self.play(FadeOut(rows), run_time=0.6)
        rt = d.tools["run tests"]
        mk2 = T("2 · feedback", 18, INK, weight=MEDIUM).move_to([2.9, -0.3, 0], aligned_edge=LEFT)
        a2 = arrow(mk2.get_left() + LEFT * 0.05 + UP * 0.1, rt.get_bottom() + DOWN * 0.04, color=INK, sw=2)
        self.play(FadeIn(mk2), GrowArrow(a2), Indicate(rt, color=HARN, scale_factor=1.15), run_time=0.8)
        self.at("17", 0.3)
        fc = card(["AssertionError: 39.5 != 37.0"], FAIL, w=3.75, size=14).move_to([2.9, -1.1, 0], aligned_edge=LEFT)
        fix = card(["edited invoice.py", "> BULK  →  >= BULK"], HARN, w=3.75, size=14).move_to([2.9, -2.2, 0], aligned_edge=LEFT)
        af = arrow(fc.get_bottom() + DOWN * 0.03, fix.get_top() + UP * 0.03, color=FAINT, sw=2)
        self.play(FadeIn(fc, shift=DOWN * 0.1), run_time=0.5)
        s, e = self.cues["17"]
        self.until(s + (e - s) * 0.65)
        self.play(GrowArrow(af), FadeIn(fix, shift=DOWN * 0.1), run_time=0.6)

        # 18-22: third, searching step by step (e.g. Claude Code), instead of an index built in advance
        self.at("18")
        se = d.tools["search"]
        mk3 = T("3 · search step by step", 18, INK, weight=MEDIUM).move_to([1.3, -0.3, 0], aligned_edge=RIGHT)
        a3 = arrow(mk3.get_right() + RIGHT * 0.05 + UP * 0.1, se.get_bottom() + DOWN * 0.04, color=INK, sw=2)
        self.play(FadeIn(mk3), GrowArrow(a3), Indicate(se, color=HARN, scale_factor=1.15), run_time=0.8)
        # the run's own searches, from chapter 5
        srch = VGroup(*[card([s_["request"]], MODEL, w=3.4, size=15) for s_ in TR["steps"] if s_["kind"] == "search"])
        srch.arrange(DOWN, buff=0.08).move_to([mk3.get_left()[0], -0.7, 0], aligned_edge=UL)
        self.play(LaggedStart(*[FadeIn(x, shift=DOWN * 0.08) for x in srch], lag_ratio=0.3), run_time=1.2)
        self.at("19")
        cc = tag("e.g. Claude Code", MUTED, 16).next_to(mk3, DOWN, buff=0.12, aligned_edge=LEFT)
        srch.generate_target()
        srch.target.next_to(cc, DOWN, buff=0.2, aligned_edge=LEFT)
        self.play(FadeIn(cc), MoveToTarget(srch), run_time=0.5)
        self.at("20")
        idx = VGroup(rbox(3.0, 0.62, MUTED, fill=PANEL, sw=1.6, r=0.08), T("index built in advance", 16, INK, font=MONO))
        idx[1].move_to(idx[0])
        idx.move_to([-5.2, -1.6, 0])
        self.play(FadeIn(idx, shift=RIGHT * 0.1), run_time=0.5)
        self.at("21", 0.8)
        old = tag("out of date", FAIL, 15).next_to(idx, DOWN, buff=0.1)
        self.play(idx.animate.set_opacity(0.35), FadeIn(old), run_time=0.6)
        self.at("22")
        self.play(Indicate(srch, color=MODEL, scale_factor=1.04), run_time=0.8)
        self.end()
