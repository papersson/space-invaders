from qkit import *

Q = "SELECT count(*), sum(amount) FROM orders WHERE customer_id = "


def bar(t_ms, y, color, x0=-3.2, per_decade=1.55, lo=0.01):
    """Horizontal bar on a log scale starting at lo ms."""
    w = max(0.08, per_decade * np.log10(t_ms / lo))
    return Rectangle(width=w, height=0.42, stroke_width=0, fill_color=color, fill_opacity=0.85).move_to([x0, y, 0], aligned_edge=LEFT)


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        fast, slow = medians("1")
        # 01: the table and the query
        self.at("01")
        cap = mono("PostgreSQL 16.9 · 2,000,000 orders · data in memory · parallel query off · "
                   "execution time (planning excluded), median of 7 runs", 12, FAINT).to_edge(DOWN, buff=0.4)
        q1 = code_card(Q + "4242", 17).move_to([0, 2.5, 0])
        self.play(FadeIn(q1), FadeIn(cap), run_time=0.7)

        # 02-04: two runs, two times (log scale)
        self.at("02")
        l1 = mono("customer 4242", 18, INK).move_to([-4.7, 0.9, 0])
        b1 = bar(fast, 0.9, GOOD)
        v1 = mono(ms(fast), 18, GOOD).next_to(b1, RIGHT, 0.2)
        self.play(FadeIn(l1), GrowFromEdge(b1, LEFT), FadeIn(v1), run_time=0.7)
        self.at("03")
        q2 = code_card(Q + "1", 17).move_to(q1)
        self.play(Transform(q1, q2), run_time=0.4)
        l2 = mono("customer 1", 18, INK).move_to([-4.7, -0.2, 0]).align_to(l1, RIGHT)
        b2 = bar(slow, -0.2, BAD)
        v2 = mono(ms(slow), 18, BAD).next_to(b2, RIGHT, 0.2)
        self.play(FadeIn(l2), GrowFromEdge(b2, LEFT), FadeIn(v2), run_time=1.0)
        axis = VGroup(*[VGroup(Line([-3.2 + 1.55 * k, -0.6, 0], [-3.2 + 1.55 * k, -0.7, 0], stroke_color=FAINT, stroke_width=1.5),
                               mono(t, 12, FAINT).move_to([-3.2 + 1.55 * k, -0.9, 0]))
                        for k, t in enumerate(["0.01", "0.1", "1", "10", "100", "1000 ms"])])
        logn = mono("log scale", 12, FAINT).next_to(axis, RIGHT, 0.3)
        self.play(FadeIn(axis), FadeIn(logn), run_time=0.4)
        self.at("04")
        x = mono(f"≈ {round(slow / fast, -3):,.0f}×", 26, AMBER).move_to([4.6, 0.35, 0])
        self.play(FadeIn(x, scale=0.8), run_time=0.5)

        # 05-06: same everything; nothing says how
        self.at("05")
        same = mono("same query · same table · same machine", 20, INK).move_to([0, -1.8, 0])
        self.play(FadeIn(same), run_time=0.5)
        self.at("06")
        how = mono("nothing in the query says how to run it", 18, MUTED).next_to(same, DOWN, 0.25)
        self.play(FadeIn(how), run_time=0.5)

        # 07-08: the question
        self.at("07")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        t1 = T("So who decides?", 38, INK).move_to([0, 0.6, 0])
        self.play(FadeIn(t1), run_time=0.5)
        self.at("08")
        t2 = T("And why is the same query sometimes fast, and sometimes slow?", 28, MUTED).next_to(t1, DOWN, 0.5)
        self.play(FadeIn(t2), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
