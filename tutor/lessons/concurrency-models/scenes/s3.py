from ckit import *
import re

YA, YB = 1.3, -0.3


def lock_runs():
    m = re.search(r"locks its own account first: stuck in (\d+) of (\d+).*?lower account number first: stuck in (\d+) of (\d+)",
                  RUNS, re.S)
    return [int(g) for g in m.groups()]


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("Locks")
        la, lb = lane("A", YA), lane("B", YB)
        acct = Account(5.3, 0.5, "$100")
        lk = padlock(acct.box.get_top() + 0.35 * UP, AMBER, 1.3)
        self.at("01")
        self.play(FadeIn(c), FadeIn(la), FadeIn(lb), FadeIn(acct), FadeIn(lk), run_time=0.7)
        # 02-04: A holds the lock through read-add-write; B waits
        self.at("02")
        own = padlock([-5.3, YA + 0.55, 0], AMBER)
        a = VGroup(step("read 100", -4.2, YA, ICE), step("add → 150", -2.2, YA), step("write 150", -0.2, YA, AMBER))
        self.play(lk.animate.move_to([-5.3, YA + 0.55, 0]), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(s) for s in a], lag_ratio=0.5), acct.set("$150", AMBER), run_time=1.4)
        self.at("03")
        wait = waiting_bar([-4.9, YB, 0], 4.2)
        self.play(FadeIn(wait), run_time=0.5)
        self.at("04")
        self.play(lk.animate.move_to([1.0, YB + 0.55, 0]), run_time=0.5)
        b = VGroup(step("read 150", 2.0, YB, ICE), step("write 200", 3.9, YB, AMBER, w=1.6))
        self.play(FadeIn(b[0]), run_time=0.4)
        self.play(FadeIn(b[1]), acct.set("$200", GOOD), run_time=0.5)
        # 05: counter with a lock
        self.at("05")
        wl = mono("counter with a lock: 20,000,000 · 20,000,000 · 20,000,000 (3 runs)", 17, GOOD).move_to([-0.8, -1.4, 0])
        self.play(FadeIn(wl), run_time=0.5)
        # 06-07: a forgotten code path
        self.at("07")
        corner = np.array([acct.box.get_bottom()[0], -2.5, 0])
        side = VGroup(DashedLine([-5.5, -2.5, 0], corner, color=BAD, stroke_width=3),
                      DashedLine(corner, acct.box.get_bottom() + 0.05 * DOWN, color=BAD, stroke_width=3))
        sl = mono("forgot the lock", 18, BAD).next_to([-5.5, -2.5, 0], UP, 0.15, aligned_edge=LEFT)
        self.play(Create(side), FadeIn(sl), run_time=0.8)

        # 08-16: two accounts, two locks, a cycle
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        A, B = Account(-2.6, 0.2, "A", "account"), Account(2.6, 0.2, "B", "account")
        la_, lb_ = padlock(A.box.get_top() + 0.3 * UP), padlock(B.box.get_top() + 0.3 * UP)
        self.play(FadeIn(A), FadeIn(B), FadeIn(la_), FadeIn(lb_), run_time=0.6)
        self.at("10")
        rule = mono("each transfer: lock the paying account, then the receiving one", 17, MUTED).move_to([0, 2.6, 0])
        self.play(FadeIn(rule), run_time=0.5)
        t1 = mono("thread 1: A → B", 18, ICE).move_to([-2.6, -1.9, 0])
        t2 = mono("thread 2: B → A", 18, AMBER).move_to([2.6, -1.9, 0])
        self.at("11")
        self.play(FadeIn(t1), run_time=0.4)
        self.at("12")
        self.play(la_.animate.set_color(ICE), run_time=0.3)
        w1 = CurvedArrow(A.box.get_top() + 0.6 * UP + 0.3 * RIGHT, B.box.get_top() + 0.6 * UP + 0.3 * LEFT, angle=-0.6,
                         color=ICE, stroke_width=3)
        w1l = mono("waits for B", 16, ICE).next_to(w1, UP, 0.05)
        self.play(Create(w1), FadeIn(w1l), run_time=0.6)
        self.at("13")
        self.play(FadeIn(t2), run_time=0.4)
        self.at("14")
        self.play(lb_.animate.set_color(AMBER), run_time=0.3)
        w2 = CurvedArrow(B.box.get_bottom() + 0.2 * DOWN + 0.3 * LEFT, A.box.get_bottom() + 0.2 * DOWN + 0.3 * RIGHT,
                         angle=-0.6, color=AMBER, stroke_width=3)
        w2l = mono("waits for A", 16, AMBER).next_to(w2, DOWN, 0.05)
        self.play(Create(w2), FadeIn(w2l), FadeOut(t1), FadeOut(t2), run_time=0.6)
        self.at("15")
        self.play(w1.animate.set_color(BAD), w2.animate.set_color(BAD), run_time=0.5)
        self.at("16")
        dl = T("deadlock", 36, BAD).move_to([0, 0.2, 0])
        self.play(FadeIn(dl, scale=1.2), run_time=0.5)

        # 17-19: fixed order breaks the cycle
        self.at("17")
        fix = mono("fix: every transfer locks the lower account number first", 17, GOOD).move_to(rule)
        self.play(FadeOut(rule), FadeIn(fix), FadeOut(dl), FadeOut(w2), FadeOut(w2l), run_time=0.6)
        self.at("18")
        w2b = mono("thread 2 also takes A first → waits, holding nothing", 16, AMBER).move_to([0, -2.2, 0])
        self.play(FadeIn(w2b), lb_.animate.set_color(TRAY_EDGE), w1.animate.set_color(ICE), run_time=0.6)
        self.at("19")
        s0, n0, s1, n1 = lock_runs()
        res = mono(f"both at once, {n0:,} runs (a little work between the two locks): stuck in {s0:,} → {s1} with a fixed order",
                   15, INK).move_to([0, -2.9, 0])
        self.play(FadeIn(res), run_time=0.5)
        self.at("20")
        every = mono("…and every piece of code must follow the order", 17, MUTED).move_to([0, 3.2, 0])
        self.play(FadeIn(every), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
