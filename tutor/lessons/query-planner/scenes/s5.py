from qkit import *


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("Joins")
        trom, oslo = medians("4")
        forced = medians("4b")[0]
        p4 = part("4")
        loops = re.search(r"Bitmap Heap Scan on orders o .*?rows=(\d+) loops=(\d+)", p4)
        per_cust, n_loops = loops.group(1), loops.group(2)

        # 01-04: two tables have to meet
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        self.at("02")
        q = code_card("… FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Tromsø'", 15).move_to([0, 2.7, 0])
        self.play(FadeIn(q), run_time=0.6)
        self.at("03")
        cu = box_t("customers", "100,000 rows", -4.6, 1.2)
        orr = box_t("orders", "2,000,000 rows", 4.6, 1.2)
        meet = mono("which method matches their rows?", 16, AMBER).move_to([0, 1.2, 0])
        self.play(FadeIn(cu), FadeIn(orr), FadeIn(meet), run_time=0.6)
        self.at("04")
        tromso = mono("Tromsø: 100 customers", 17, ICE).next_to(cu, DOWN, 0.25)
        self.play(FadeIn(tromso), run_time=0.4)

        # 05-07: a nested loop: 100 index lookups (real plan)
        self.at("05")
        self.play(FadeOut(meet), run_time=0.2)
        lookups = VGroup(*[Line(cu.get_right() + (0.35 - 0.07 * i) * UP, orr.get_left() + (0.45 - 0.09 * i) * UP,
                                stroke_color=ICE, stroke_width=1.2, stroke_opacity=0.7) for i in range(10)])
        self.play(LaggedStart(*[Create(l) for l in lookups], lag_ratio=0.15), run_time=1.6)
        self.at("06")
        nl = tree([node("Nested Loop", "for each Tromsø customer, look up its orders", ICE, w=5.6),
                   node("Seq Scan on customers", "100 rows"),
                   node("Bitmap Heap Scan on orders", f"{n_loops} loops · {per_cust} rows each")], -6.3, -0.4)
        self.play(FadeIn(nl), run_time=0.7)
        self.at("07")
        t1 = mono(ms(trom), 22, ICE).next_to(nl, RIGHT, 0.5).align_to(nl, UP)
        self.play(FadeIn(t1), run_time=0.4)

        # 08-11: Oslo: build a hash table, stream the orders through it once (real plan)
        self.at("08")
        self.play(FadeOut(lookups), FadeOut(nl), FadeOut(t1), FadeOut(tromso), run_time=0.4)
        q2 = code_card("… FROM orders o JOIN customers c ON c.id = o.customer_id WHERE c.city = 'Oslo'", 15).move_to(q)
        self.play(Transform(q, q2), run_time=0.4)
        osl = mono("Oslo: almost all of them (99,900)", 17, AMBER).next_to(cu, DOWN, 0.25)
        self.play(FadeIn(osl), run_time=0.4)
        self.at("09")
        ht = RoundedRectangle(corner_radius=0.1, width=2.4, height=1.3, stroke_color=AMBER, stroke_width=2,
                              fill_color=TRAY_FILL, fill_opacity=1).move_to([0, 1.2, 0])
        htl = VGroup(mono("hash table", 16, AMBER), mono("Oslo customers", 13, MUTED)).arrange(DOWN, buff=0.1).move_to(ht)
        ba = Arrow(cu.get_right(), ht.get_left(), buff=0.1, color=AMBER, stroke_width=2.5, tip_length=0.15)
        self.play(GrowArrow(ba), FadeIn(ht), FadeIn(htl), run_time=0.6)
        stream = VGroup(*[Dot(orr.get_left() + 0.1 * LEFT, radius=0.05, color=INK) for _ in range(12)])
        self.play(LaggedStart(*[MoveAlongPath(d, Line(orr.get_left(), ht.get_right())) for d in stream],
                              lag_ratio=0.12), run_time=1.6)
        self.remove(stream)
        once = mono("all 2,000,000 orders, streamed through once", 15, MUTED).next_to(ht, DOWN, 0.2)
        self.play(FadeIn(once), run_time=0.4)
        self.at("10")
        hj = tree([node("Hash Join", "", AMBER, w=5.0), node("Seq Scan on orders", "2,000,000 rows · Seq Scan = full scan"),
                   node("Hash", "built from: Seq Scan on customers, 99,900 rows")], -6.3, -0.6)
        self.play(FadeIn(hj), run_time=0.7)
        self.at("11")
        t2 = mono(f"{ms(oslo)} · 1,998,654 rows", 20, AMBER).next_to(hj, RIGHT, 0.5).align_to(hj, UP)
        self.play(FadeIn(t2), run_time=0.4)

        # 12: a nested loop forced for Oslo
        self.at("12")
        f = mono(f"nested loop forced: {forced / 1000:.1f} s  (≈ {forced / oslo:.1f}× as long)", 18, BAD).next_to(t2, DOWN, 0.3).align_to(t2, LEFT)
        self.play(FadeIn(f), run_time=0.5)
        mj = mono("PostgreSQL has a third join method, merge join, not covered here", 12, FAINT).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(mj), run_time=0.3)

        # 13-14: same shape, different plan
        self.at("13")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        s1 = mono("same query shape", 24, INK).move_to([0, 0.6, 0])
        self.play(FadeIn(s1), run_time=0.4)
        self.at("14")
        s2 = mono("a different plan, because a different number of rows match", 20, AMBER).next_to(s1, DOWN, 0.4)
        self.play(FadeIn(s2), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()


def box_t(name, detail, x, y):
    r = RoundedRectangle(corner_radius=0.1, width=3.2, height=1.1, stroke_color=TRAY_EDGE, stroke_width=2,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    return VGroup(r, VGroup(mono(name, 18, INK), mono(detail, 13, MUTED)).arrange(DOWN, buff=0.1).move_to(r))
