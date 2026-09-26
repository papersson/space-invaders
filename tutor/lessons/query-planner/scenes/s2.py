from qkit import *


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("Say what, not how")
        # 01-02: the loop says how
        self.at("01")
        loop = VGroup(mono("total, n = 0, 0", 17, INK), mono("for order in orders:", 17, INK),
                      mono("    if order.customer_id == 4242:", 17, INK), mono("        n += 1", 17, INK),
                      mono("        total += order.amount", 17, INK)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        lb = SurroundingRectangle(loop, buff=0.3, color=DIM, stroke_width=1.5, corner_radius=0.1)
        ll = label("ordinary code", 15).next_to(lb, UP, 0.15).align_to(lb, LEFT)
        lg = VGroup(lb, loop, ll).move_to([-3.4, 0.6, 0])
        self.play(FadeIn(c), FadeIn(lg), run_time=0.7)
        self.at("02")
        self.play(LaggedStart(*[Indicate(r, color=AMBER, scale_factor=1.03) for r in loop[1:]], lag_ratio=0.5), run_time=1.6)
        how = mono("says exactly how", 18, AMBER).next_to(lb, DOWN, 0.3)
        self.play(FadeIn(how), run_time=0.4)

        # 03-04: SQL says what
        self.at("03")
        sql = VGroup(mono("SELECT count(*), sum(amount)", 17, INK), mono("FROM orders", 17, INK),
                     mono("WHERE customer_id = 4242", 17, INK)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        sb = SurroundingRectangle(sql, buff=0.3, color=DIM, stroke_width=1.5, corner_radius=0.1)
        sl = label("SQL: declarative", 15).next_to(sb, UP, 0.15).align_to(sb, LEFT)
        sg = VGroup(sb, sql, sl).move_to([3.5, 0.9, 0])
        self.play(FadeIn(sg), run_time=0.6)
        self.at("04")
        self.play(Indicate(sql[2], color=ICE, scale_factor=1.05), run_time=0.8)
        what = mono("says only what", 18, ICE).next_to(sb, DOWN, 0.3)
        self.play(FadeIn(what), run_time=0.4)

        # 05-06: the database chooses, every time
        self.at("05")
        q = mono("how?", 28, AMBER).move_to([3.5, -1.9, 0])
        qa = Arrow(what.get_bottom(), q.get_top(), buff=0.1, color=AMBER, stroke_width=2.5, tip_length=0.15)
        self.play(GrowArrow(qa), FadeIn(q), run_time=0.5)
        chooses = mono("the database chooses", 18, INK).next_to(q, DOWN, 0.2)
        self.play(FadeIn(chooses), run_time=0.4)
        self.at("06")
        every = mono("every time the query runs", 16, MUTED).next_to(chooses, DOWN, 0.15)
        self.play(FadeIn(every), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
