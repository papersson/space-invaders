from rkit import *

ROWS = [("price", "$20", "$20"), ("qty", "2", "3"), ("subtotal", "$40", "$60"), ("tax (10%)", "$4", "$6"),
        ("total", "$44", "$66"), ("free shipping (from $65)", "no", "yes")]


def sheet(values, x=2.6, y=1.4):
    rows = VGroup()
    for i, (name, v) in enumerate(values):
        cell_n = Rectangle(width=3.6, height=0.55, stroke_color=DIM, stroke_width=1.2, fill_color=PANEL, fill_opacity=1)
        cell_v = Rectangle(width=1.6, height=0.55, stroke_color=DIM, stroke_width=1.2, fill_color=PANEL, fill_opacity=1)
        cell_v.next_to(cell_n, RIGHT, buff=0)
        rows.add(VGroup(cell_n, cell_v, mono(name, 17, MUTED).move_to(cell_n).align_to(cell_n, LEFT).shift(0.15 * RIGHT),
                        mono(v, 19, INK).move_to(cell_v)))
    rows.arrange(DOWN, buff=0).move_to([x, y - 1.0, 0])
    return rows


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        # 01-02: the cart
        self.at("01")
        sh = sheet([(n, a) for n, a, _ in ROWS])
        cap = label("spreadsheet", 16).next_to(sh, UP, 0.2).align_to(sh, LEFT)
        self.play(LaggedStart(*[FadeIn(r) for r in sh[:2]], lag_ratio=0.3), FadeIn(cap), run_time=0.8)
        self.at("02")
        self.play(LaggedStart(*[FadeIn(r) for r in sh[2:5]], lag_ratio=0.4), run_time=1.2)

        # 03-04: in code, the total is computed once, then goes stale
        self.at("03")
        code = VGroup(mono("subtotal = price * qty", 19, INK), mono("tax = subtotal * 0.10", 19, INK),
                      mono("total = subtotal + tax", 19, INK)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        box = SurroundingRectangle(code, buff=0.3, color=DIM, stroke_width=1.5, corner_radius=0.1)
        cl = label("code", 16).next_to(box, UP, 0.2).align_to(box, LEFT)
        cg = VGroup(box, code, cl).move_to([-3.9, 1.1, 0])
        outv = VGroup(mono("qty = 2", 19, MUTED), mono("total → 44", 22, INK)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        outv.next_to(box, DOWN, 0.4).align_to(box, LEFT)
        self.play(FadeIn(cg), FadeIn(outv), run_time=0.8)
        self.at("04")
        q3 = mono("qty = 3", 19, AMBER).move_to(outv[0], aligned_edge=LEFT)
        stale = mono("total → 44   (stale)", 22, BAD).move_to(outv[1], aligned_edge=LEFT)
        self.play(Transform(outv[0], q3), run_time=0.5)
        self.play(Transform(outv[1], stale), run_time=0.6)

        # 05-06: the spreadsheet updates by itself
        self.at("06")
        sh.add(sheet([(n, a) for n, a, _ in ROWS])[5].move_to(sh[4].get_center() + 0.55 * DOWN))
        self.play(FadeIn(sh[5]), run_time=0.3)
        for i, (_, _, b) in enumerate(ROWS[1:], start=1):
            v = mono(b, 19, AMBER if i == 1 else GREEN).move_to(sh[i][3])
            self.play(Transform(sh[i][3], v), run_time=0.3)

        # 07-08: build tools and UI frameworks do the same
        self.at("07")
        tags = VGroup(*[mono(t, 20, ICE) for t in ("spreadsheets", "build tools", "UI frameworks")]).arrange(RIGHT, buff=0.9)
        tags.to_edge(DOWN, buff=0.9)
        self.play(FadeIn(tags[0]), FadeIn(tags[1]), run_time=0.6)
        self.at("08")
        self.play(FadeIn(tags[2]), run_time=0.4)

        # 09-10: the question
        self.at("09")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        q1 = T("What should it recompute, and in what order?", 36, INK).move_to([0, 0.4, 0])
        self.play(FadeIn(q1), run_time=0.7)
        self.at("10")
        q2 = T("And what goes wrong when it gets that wrong?", 28, MUTED).next_to(q1, DOWN, 0.5)
        self.play(FadeIn(q2), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
