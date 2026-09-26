from ckit import *
import re

YA, YB = 1.3, -0.3
X = {"read": -3.6, "add": -1.6, "write": 0.4}


def runs():
    block = RUNS.split("no lock:")[1].split("with lock:")[0]
    return [int(v) for v in re.findall(r"\d{6,}", block)]


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("The lost update")
        la, lb = lane("A", YA), lane("B", YB)
        acct = Account(5.3, 0.5, "$100")
        t_ax = mono("time →", 14, FAINT).move_to([2.6, -1.1, 0])
        self.at("01")
        self.play(FadeIn(c), FadeIn(la), FadeIn(lb), FadeIn(acct), FadeIn(t_ax), run_time=0.7)
        # 02: three steps
        self.at("02")
        steps = VGroup(mono("read", 18, MUTED), mono("add 50", 18, MUTED), mono("write", 18, MUTED)).arrange(RIGHT, buff=0.6)
        steps.move_to([-1.6, 2.6, 0])
        self.play(FadeIn(steps), run_time=0.6)
        # 03-06: the losing interleaving
        self.at("03")
        a1 = step("read 100", -4.2, YA, ICE)
        self.play(FadeIn(a1), Indicate(acct.val, color=ICE), run_time=0.6)
        a2 = step("add → 150", -2.2, YA, INK)
        self.play(FadeIn(a2), run_time=0.4)
        self.at("04")
        b1 = step("read 100", -1.4, YB, ICE)
        self.play(FadeIn(b1), Indicate(acct.val, color=ICE), run_time=0.6)
        b2 = step("add → 150", 0.6, YB, INK)
        self.play(FadeIn(b2), run_time=0.4)
        self.at("05")
        a3 = step("write 150", 0.3, YA, AMBER)
        self.play(FadeIn(a3), acct.set("$150", AMBER), run_time=0.6)
        self.at("06")
        b3 = step("write 150", 2.6, YB, AMBER)
        self.play(FadeIn(b3), acct.set("$150", BAD), run_time=0.6)
        self.at("07")
        x = cross(a3.get_center(), 0.3)
        self.play(Create(x), a3.animate.set_opacity(0.4), run_time=0.5)
        self.at("08")
        lu = T("lost update", 32, BAD).move_to([2.6, 2.6, 0])
        self.play(FadeIn(lu), run_time=0.5)

        # 09-11: only two safe orders out of twenty
        self.at("09")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        def order(seq, y, ok):
            cells = VGroup(*[step(s, 0, 0, ICE if s == "A" else AMBER, w=0.55, size=18) for s in seq]).arrange(RIGHT, buff=0.08)
            mark = mono("✓ safe" if ok else "✗ loses one", 18, GOOD if ok else BAD)
            return VGroup(cells, mark).arrange(RIGHT, buff=0.5).move_to([0, y, 0])
        o1, o2 = order("AAABBB", 1.6, True), order("BBBAAA", 0.8, True)
        self.play(FadeIn(o1), FadeIn(o2), run_time=0.7)
        self.at("10")
        o3, o4 = order("AABABB", -0.2, False), order("ABABAB", -1.0, False)
        rest = mono("… and 16 more orders: all lose a deposit (2 safe of 20)", 17, BAD).move_to([0, -1.8, 0])
        self.play(FadeIn(o3), FadeIn(o4), FadeIn(rest), run_time=0.8)
        self.at("11")
        rare = mono("usually the deposits don't overlap at all → the bug is intermittent", 17, MUTED).move_to([0, -2.6, 0])
        self.play(FadeIn(rare), run_time=0.5)

        # 12-20: race condition vs data race
        self.at("12")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        rc = VGroup(T("race condition", 30, AMBER), mono("the result depends on timing", 18, MUTED)).arrange(DOWN, buff=0.15)
        rc.move_to([-3.3, 1.6, 0])
        self.play(FadeIn(rc), run_time=0.6)
        self.at("13")
        dr = VGroup(T("data race", 30, BAD)).move_to([3.3, 1.9, 0])
        self.play(FadeIn(dr), run_time=0.5)
        checks = VGroup()
        for i, (cue, t) in enumerate((("14", "same memory"), ("15", "at least one writes"), ("16", "no order between them"))):
            self.at(cue)
            ck = VGroup(mono("✓", 20, GOOD), mono(t, 18, INK)).arrange(RIGHT, buff=0.2)
            ck.move_to([3.3, 1.2 - 0.5 * i, 0])
            checks.add(ck)
            self.play(FadeIn(ck), run_time=0.4)
        self.at("18")
        about1 = mono("about the result", 18, AMBER).next_to(rc, DOWN, 0.3)
        self.play(FadeIn(about1), run_time=0.4)
        self.at("19")
        about2 = mono("about how memory is used", 18, BAD).next_to(checks, DOWN, 0.3)
        self.play(FadeIn(about2), run_time=0.4)
        self.at("20")
        both = mono("the lost update: both", 20, INK).move_to([0, -1.6, 0])
        self.play(FadeIn(both), run_time=0.4)
        self.at("22")
        ub = mono("C, C++: a program with a data race has undefined behaviour", 16, MUTED).move_to([0, -2.4, 0])
        self.play(FadeIn(ub), run_time=0.5)

        # 23-25: the counter, measured
        self.at("23")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        head = mono("2 threads × 10,000,000 increments, no lock (a small C program)", 18, INK).move_to([0, 2.7, 0])
        base, top = -2.4, 1.9
        full = Line([-4.5, top, 0], [4.5, top, 0], stroke_color=GOOD, stroke_width=2)
        fl = mono("expected 20,000,000", 16, GOOD).next_to(full, UP, 0.08).align_to(full, RIGHT)
        self.play(FadeIn(head), Create(full), FadeIn(fl), run_time=0.7)
        self.at("25")
        bars = VGroup()
        for i, v in enumerate(runs()):
            h = (top - base) * v / 20_000_000
            b = Rectangle(width=1.1, height=h, stroke_width=0, fill_color=BAD, fill_opacity=0.85)
            b.move_to([-3.6 + 1.8 * i, base, 0], aligned_edge=DOWN)
            lab = mono(f"{v / 1e6:.1f} M", 16, INK).next_to(b, UP, 0.08)
            bars.add(VGroup(b, lab))
        self.play(LaggedStart(*[GrowFromEdge(b[0], DOWN) for b in bars], lag_ratio=0.2),
                  LaggedStart(*[FadeIn(b[1]) for b in bars], lag_ratio=0.2), run_time=1.6)
        runs_l = mono("five runs", 14, MUTED).move_to([0, base - 0.35, 0])
        self.play(FadeIn(runs_l), run_time=0.3)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
