from skit import *
from s6 import staircase, counts, keyerror_bar_index, SCALE, BOT

A7, B7 = 1.05, -0.5


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        # the end of chapter 6: the staircase, its counts, the total, the key error outlined
        rows = staircase()
        cnt = counts(rows)
        total = sum(S["loop_1"]["calls"])
        br = Brace(VGroup(*cnt), RIGHT, buff=0.15, color=AMBER)
        tt = VGroup(mono_b(f"{total:,}", 22, AMBER), mono("tokens read", 15, AMBER)).arrange(DOWN, buff=0.08).next_to(br, RIGHT, 0.15)
        keep_on_screen(tt)
        k = keyerror_bar_index()
        outs = VGroup(*[SurroundingRectangle(rows[n][k], color=CORAL, buff=0.03, stroke_width=3) for n in range(9) if len(rows[n]) > k])
        cli, ours = rows[0][0], VGroup(rows[0][1], rows[0][2])
        b1 = Brace(cli, UP, buff=0.06, color=MUTED)
        t1 = mono("notes added by claude -p ≈1,180", 13, MUTED).next_to(b1, UP, 0.06)
        b2 = Brace(ours, UP, buff=0.06, color=MUTED)
        t2 = mono("our instructions + task ≈240", 13, MUTED).next_to(b2, UP, 0.06).align_to(b2, LEFT)
        tok = mono("tokens", 15, MUTED).next_to(rows[8], DOWN, 0.12).align_to(rows[8], LEFT)
        self.add(*rows, *cnt, br, tt, outs, b1, t1, b2, t2, tok)

        A = Strip("loop_1", A7, labels={18: "Fixed."})
        B = Strip("no_tests_1", B7, labels={10: "Fixed."})
        la = label("run A", 15, INK).next_to(A.cards[0], UP, 0.18).align_to(A.cards[0], LEFT)
        lb = label("run B", 15, INK).next_to(B.cards[0], UP, 0.18).align_to(B.cards[0], LEFT)

        # 01: the staircase folds back into run A's cards
        self.at("01")
        self.play(FadeOut(VGroup(*rows[:8], *cnt, br, tt, outs, b1, t1, b2, t2, tok)), run_time=0.6)
        bars = rows[8]
        tr = [ReplacementTransform(VGroup(bars[0], bars[1]), A.cards[0]), ReplacementTransform(bars[2], A.cards[1])]
        tr += [ReplacementTransform(bars[kk + 1], A.cards[kk]) for kk in range(2, 18)]
        tr += [FadeIn(A.cards[18]), FadeIn(la)]
        self.play(*tr, run_time=1.2)

        # 02-03: same loop, same model; its tool list has no run_tests
        self.at("02")
        self.play(FadeIn(lb), FadeIn(B.cards[0]), FadeIn(B.cards[1]), run_time=0.6)
        self.at("03")
        tools = [("list_files", INK), ("read_file", INK), ("write_file", INK), ("run_tests", CORAL)]
        tp = quote(tools, 15, title="run B's tools")
        tp.move_to([4.3, B7, 0])
        strike = Line(tp[1][3].get_left() + LEFT * 0.05, tp[1][3].get_right() + RIGHT * 0.05, stroke_color=CORAL, stroke_width=3)
        self.play(FadeIn(tp), run_time=0.5)
        self.play(Create(strike), run_time=0.4)

        # 04: its first four steps match run A's
        self.at("04")
        self.play(LaggedStart(*[FadeIn(B.cards[i], shift=0.1 * DOWN) for i in range(2, 10)], lag_ratio=0.2), run_time=1.6)

        # 05: where A asked to run the test, B had nothing to ask for
        self.at("05")
        ra = SurroundingRectangle(VGroup(A.cards[10], A.cards[11]), color=AMBER, buff=0.06, corner_radius=0.08, stroke_width=3)
        self.play(Create(ra), run_time=0.5)

        # 06: so it replied
        self.at("06")
        self.play(FadeIn(B.cards[10], shift=0.15 * DOWN), run_time=0.5)

        # 07-08: its context when it did: its own fix, and nothing after it
        self.at("07")
        self.play(FadeOut(tp), FadeOut(strike), run_time=0.3)
        bb = Brace(VGroup(*B.cards[:10]), DOWN, buff=0.08, color=MUTED)
        bt = mono("its context", 14, MUTED).next_to(bb, DOWN, 0.06)
        gap = DashedVMobject(Rectangle(width=A.cards[17].get_right()[0] - A.cards[11].get_left()[0], height=0.78,
                                       stroke_color=MUTED, stroke_width=2).move_to(
            [(A.cards[11].get_left()[0] + A.cards[17].get_right()[0]) / 2, B7, 0]), num_dashes=40)
        gt = mono("no test result", 14, MUTED).move_to(gap)
        self.play(GrowFromCenter(bb), FadeIn(bt), run_time=0.5)
        self.play(Create(gap), FadeIn(gt), run_time=0.6)

        # 09-13: its reply, as it wrote it (captures/no_tests_1.json)
        self.at("09")
        tb = B.cards[10].data["text"]
        l1 = "Fixed. The bug was that revenue was being computed with `+` instead of `*`"
        l3 = "matching the expected values in `test_report.py`."
        assert l1 in tb and l3 in tb
        qb = quote([l1, ("…", MUTED), l3], 14, title="run B's reply").move_to([0, -2.3, 0]).align_to([X0, 0, 0], LEFT)
        self.play(FadeOut(bb), FadeOut(bt), FadeIn(qb), run_time=0.6)

        # 14-16: it could have read the data file (A's read sales.csv); it had the tool
        self.at("14")
        rc = SurroundingRectangle(A.cards[12], color=INK, buff=0.06, corner_radius=0.08, stroke_width=3)
        self.play(Create(rc), run_time=0.5)

        # 17-19: the first way agents break down
        self.at("17")
        self.play(FadeOut(qb), FadeOut(rc), run_time=0.4)
        w1 = mono("nothing checks the work", 18, INK).to_corner(UL, buff=0.45)
        self.at("19")
        self.play(FadeIn(w1), run_time=0.5)

        # 20-22: in a longer task, later steps would build on the guess: compounding errors
        self.at("20")
        fx = SurroundingRectangle(B.cards[10], color=CORAL, buff=0.06, corner_radius=0.08, stroke_width=3)
        self.play(Create(fx), run_time=0.5)
        self.at("22")
        w1b = mono("compounding errors", 15, MUTED).next_to(w1, DOWN, 0.12).align_to(w1, LEFT)
        self.play(FadeIn(w1b), run_time=0.4)

        # 23-24: a more capable model, run B's setup, three times (captures/no_tests_strong_*.json)
        self.at("23")
        top = VGroup(*A.cards, *B.cards, la, lb, ra, gap, gt, fx)
        self.play(top.animate.scale(0.72, about_point=[X0, 2.95, 0]), run_time=0.8)
        runs = ["no_tests_strong_1", "no_tests_strong_2", "no_tests_strong_3"]
        ys = [-0.7, -1.5, -2.3]
        St = []
        for r, y in zip(runs, ys):
            n = len(card_items(r))
            st = Strip(r, y, labels={n - 1: "reply"})
            VGroup(*st.cards).scale(0.72, about_point=[X0, y, 0])
            St.append(st)
        lc = label("more capable model", 15, INK).next_to(St[0].cards[0], UP, 0.2).align_to(St[0].cards[0], LEFT)
        self.at("24")
        self.play(FadeIn(lc), run_time=0.4)

        # 25-26: twice, it read the data file, found the mark, fixed both bugs; our test run passed
        self.at("25")
        for st in St[:2]:
            self.play(LaggedStart(*[FadeIn(c, shift=0.08 * DOWN) for c in st.cards], lag_ratio=0.1), run_time=1.2)
        csv_rings = VGroup()
        for st in St[:2]:
            ci = next(i for i, c in enumerate(st.cards) if c.kind == "model" and c.data.get("sub") == "sales.csv")
            csv_rings.add(SurroundingRectangle(VGroup(st.cards[ci], st.cards[ci + 1]), color=INK, buff=0.05, corner_radius=0.06, stroke_width=2.5))
        self.play(Create(csv_rings), run_time=0.5)
        self.at("26")
        oks = VGroup()
        for st, r in zip(St[:2], runs[:2]):
            assert S[r]["passed_after"]
            oks.add(VGroup(check(ORIGIN, 0.9, GREEN, 5), mono("OK", 15, GREEN)).arrange(RIGHT, buff=0.15).next_to(st.cards[-1], RIGHT, 0.4))
        self.play(FadeIn(oks), run_time=0.5)

        # 27: it said it couldn't run the test
        self.at("27")
        t1 = S[runs[0]]["cards"][-1]["text"]
        s1_ = "I fixed `report.py`, but I couldn't run the test because I have no tool to execute code."
        s2_ = "I checked the result by hand against `sales.csv` instead."
        assert s1_ in t1 and s2_ in t1
        qs = quote([s1_, s2_], 13, title="its reply").move_to([0, -3.35, 0]).align_to([X0, 0, 0], LEFT)
        self.play(FadeIn(qs), run_time=0.5)

        # 28: more ground truth in its own context: the sales.csv results
        self.at("28")
        self.play(Indicate(csv_rings, color=GREEN, scale_factor=1.05), run_time=0.9)

        # 29-30: the third time: a request our code did not recognise
        self.at("29")
        self.play(FadeOut(qs), run_time=0.3)
        st3 = St[2]
        self.play(LaggedStart(*[FadeIn(c, shift=0.08 * DOWN) for c in st3.cards], lag_ratio=0.1), run_time=1.0)
        last = st3.cards[-1]
        t3 = S[runs[2]]["cards"][-1]["text"].strip().split("\n")
        assert t3[0] == "<invoke_read_file>", t3
        p3 = quote([(t, CORAL) for t in t3], 14).next_to(last, RIGHT, 0.5)
        keep_on_screen(p3)
        ring3 = SurroundingRectangle(last, color=CORAL, buff=0.05, corner_radius=0.06, stroke_width=3)
        self.play(Create(ring3), FadeIn(p3), run_time=0.6)
        self.at("30")
        assert not S[runs[2]]["passed_after"]
        bad = VGroup(cross(ORIGIN, 0.1, CORAL, 5), mono("FAIL", 15, CORAL)).arrange(RIGHT, buff=0.15).next_to(p3, RIGHT, 0.3)
        keep_on_screen(bad)
        self.play(FadeIn(bad), run_time=0.4)

        # 31-33: not the model's failure: our code decides what counts as asking, and as done
        self.at("31")
        cb = code_box().scale(0.85).next_to(p3, DOWN, 0.35).align_to(p3, LEFT)
        note = mono("no tool call found → done", 14, INK).next_to(cb, RIGHT, 0.25)
        keep_on_screen(VGroup(cb, note))
        self.play(FadeIn(cb), run_time=0.4)
        self.at("32")
        self.play(FadeIn(note), run_time=0.5)
        self.at("33")
        self.play(Circumscribe(cb, color=INK, time_width=0.6), run_time=1.0)
        self.until(self.dur - 0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.finish()
