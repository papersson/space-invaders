from qkit import *


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("The planner estimates")
        p1, p2, p3 = part("1"), part("2"), part("3")
        fast, slow = medians("1")
        full_rare, full_common = medians("2")[0], medians("3")[0]
        rare_part, common_part = p1.split("Execution Time")[0], p1.split("median_ms_of_7_runs")[1]
        est_rare = est_rows(rare_part, "Bitmap Heap Scan")
        est_common = est_rows(common_part, "Bitmap Heap Scan")
        cost_idx, cost_full = total_cost(rare_part), total_cost(p2)
        blocks = re.findall(r"Heap Blocks: exact=(\d+)", p1)

        # 01-03: the planner, its statistics, a cost for each plan
        self.at("01")
        pl = mono("query planner", 26, INK).move_to([0, 2.6, 0])
        self.play(FadeIn(c), FadeIn(pl), run_time=0.6)
        self.at("02")
        st = VGroup(mono("statistics: orders.customer_id", 15, MUTED),
                    mono("customer 1: ~30% of rows (most common value)", 16, INK),
                    mono(f"others: ~{est_rare} rows each (estimated)", 16, INK)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        sb = SurroundingRectangle(st, buff=0.25, color=DIM, stroke_width=1.5, corner_radius=0.1)
        sg = VGroup(sb, st).move_to([0, 1.2, 0])
        self.play(FadeIn(sg), run_time=0.6)
        self.at("03")
        steps = mono("each plan → estimated rows and pages → cost → pick the cheapest", 16, ICE).move_to([0, -0.1, 0])
        self.play(FadeIn(steps), run_time=0.6)

        # 04-06: customer 4242: rare; estimate 33 vs 10; costs
        self.at("04")
        self.play(FadeOut(sg), FadeOut(steps), FadeOut(pl), run_time=0.4)
        who = mono("customer 4242", 22, INK).move_to([-4.3, 2.6, 0])
        rare = mono("statistics: rare", 16, MUTED).next_to(who, DOWN, 0.15)
        self.play(FadeIn(who), FadeIn(rare), run_time=0.5)
        self.at("05")
        est = mono(f"estimated {est_rare} rows · actual 10", 16, INK).next_to(rare, DOWN, 0.15).align_to(rare, LEFT)
        self.play(FadeIn(est), run_time=0.4)
        self.at("06")
        costs = VGroup(mono(f"index (bitmap scan):  cost {cost_idx:,.0f}", 17, GOOD),
                       mono(f"full scan:            cost {cost_full:,.0f}", 17, BAD),
                       mono("(the planner's units, not ms)", 13, MUTED)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        costs.move_to([2.4, 2.2, 0])
        self.play(FadeIn(costs), run_time=0.6)

        # 07-09: the bitmap scan: two steps, ten pages
        self.at("07")
        tr = tree([node("Aggregate"), node("Bitmap Heap Scan on orders", f"reads the pages · Heap Blocks (pages): {blocks[0]}", GOOD),
                   node("Bitmap Index Scan on orders_customer", "reads the index", GOOD)], -6.3, 0.4)
        self.play(FadeIn(tr[0]), run_time=0.3)
        self.play(FadeIn(tr[2]), run_time=0.4)
        self.play(FadeIn(tr[1]), run_time=0.4)
        self.at("08")
        bn = mono("= a bitmap scan", 18, GOOD).next_to(VGroup(tr[1], tr[2]), RIGHT, 0.4)
        self.play(FadeIn(bn), run_time=0.4)
        self.at("09")
        res = mono(f"estimated {est_rare} · actual 10 · {blocks[0]} pages · {ms(fast)}", 16, GOOD).next_to(tr, DOWN, 0.25).align_to(tr, LEFT)
        self.play(FadeIn(res), run_time=0.4)

        # 10-11: forcing a full scan
        self.at("10")
        forced = mono(f"full scan forced (Seq Scan): {ms(full_rare)}", 17, BAD).next_to(res, DOWN, 0.3).align_to(res, LEFT)
        ratio = mono(f"≈ {round(full_rare / fast, -2):,.0f}× slower", 17, BAD).next_to(forced, RIGHT, 0.4)
        self.play(FadeIn(forced), run_time=0.4)
        self.play(FadeIn(ratio), run_time=0.4)
        self.at("11")
        self.play(Circumscribe(VGroup(forced, ratio), color=BAD, stroke_width=2), run_time=0.8)

        # 12-17: customer 1: same kind of plan, every page; a full scan is no faster
        self.at("12")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        who1 = mono("customer 1", 22, INK).move_to([-4.6, 2.6, 0])
        com = mono("statistics: about 3 in 10 orders", 16, MUTED).next_to(who1, DOWN, 0.15).align_to(who1, LEFT)
        self.play(FadeIn(who1), FadeIn(com), run_time=0.5)
        self.at("13")
        tr1 = tree([node("Aggregate"), node("Bitmap Heap Scan on orders", "reads the pages", BAD),
                    node("Bitmap Index Scan on orders_customer", "reads the index", INK)], -6.3, 1.3)
        e1 = mono(f"estimated {est_common:,} · actual 600,698", 16, INK).next_to(tr1, DOWN, 0.25).align_to(tr1, LEFT)
        self.play(FadeIn(tr1), FadeIn(e1), run_time=0.7)
        self.at("14")
        hb = mono(f"Heap Blocks (pages): {int(blocks[1]):,} of {RELPAGES:,}", 16, BAD).next_to(e1, DOWN, 0.15).align_to(e1, LEFT)
        self.play(FadeIn(hb), run_time=0.4)
        self.at("15")
        t1 = mono(ms(slow), 22, BAD).next_to(hb, DOWN, 0.3).align_to(hb, LEFT)
        self.play(FadeIn(t1), run_time=0.4)
        self.at("16")
        f1 = VGroup(mono(f"full scan forced: {ms(full_common)}", 18, MUTED), mono("no faster", 18, MUTED)).arrange(DOWN, buff=0.12)
        f1.move_to([3.8, -0.9, 0])
        why = mono("same pages · still ~600,000 rows to add up", 14, MUTED).next_to(f1, DOWN, 0.2)
        self.play(FadeIn(f1), run_time=0.5)
        self.play(FadeIn(why), run_time=0.4)
        self.at("17")
        end = mono("rows on every page: the index doesn't help, no plan is fast", 17, AMBER).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(end), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
