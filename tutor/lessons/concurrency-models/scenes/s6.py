from ckit import *
import re

YA, YB = 1.3, -0.3


def race_runs():
    m = re.search(r"two messages\): overdrawn to -\$100 in (\d+) of (\d+).*?one message\): overdrawn to -\$100 in (\d+) of (\d+)",
                  RUNS, re.S)
    return [int(g) for g in m.groups()]


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("A race without shared memory")
        actor = Actor(4.6, 0.5, "$100", r=0.9)
        self.at("01")
        self.play(FadeIn(c), FadeIn(actor), run_time=0.6)
        ok = mono("deposits: fixed", 18, GOOD).move_to([-2.0, 2.4, 0])
        self.play(FadeIn(ok), run_time=0.4)
        # 03-05: withdrawals take two messages
        self.at("03")
        la, lb = lane("A", YA, x1=2.2), lane("B", YB, x1=2.2)
        self.play(FadeOut(ok), FadeIn(la), FadeIn(lb), run_time=0.5)
        self.at("05")
        two = mono("\"balance?\" then \"withdraw 100\"", 18, MUTED).move_to([-2.0, 2.4, 0])
        self.play(FadeIn(two), run_time=0.4)
        # 06-10: the interleaving
        self.at("07")
        a1 = step("balance? → 100", -3.9, YA, ICE, w=2.4)
        self.play(FadeIn(a1), run_time=0.5)
        self.at("08")
        b1 = step("balance? → 100", -2.3, YB, ICE, w=2.4)
        self.play(FadeIn(b1), run_time=0.5)
        self.at("09")
        a2 = step("withdraw 100", -0.4, YA, AMBER, w=2.0)
        b2 = step("withdraw 100", 1.1, YB, AMBER, w=2.0)
        self.play(FadeIn(a2), run_time=0.4)
        self.play(FadeIn(b2), run_time=0.4)
        self.at("10")
        self.play(actor.set("$0"), run_time=0.5)
        self.play(actor.set("−$100", BAD), actor.circle.animate.set_stroke(color=BAD), run_time=0.6)
        # 11-13: no data race; still a race condition
        self.at("11")
        nd = mono("no data race", 20, GOOD).move_to([-3.4, -1.6, 0])
        self.play(FadeIn(nd), run_time=0.4)
        self.at("13")
        rc = mono("still a race condition: between messages", 20, BAD).move_to([1.4, -1.6, 0])
        self.play(FadeIn(rc), run_time=0.5)
        s2, n2, s1, n1 = race_runs()
        self.at("14")
        r1 = mono(f"two messages: overdrawn in {s2:,} of {n2:,} runs", 18, BAD).move_to([-1.0, -2.4, 0])
        self.play(FadeIn(r1), run_time=0.5)
        # 15-17: one message
        self.at("15")
        one = mono("one message: \"withdraw 100 if balance ≥ 100\"", 18, GOOD).move_to([-1.0, -3.0, 0])
        self.play(FadeIn(one), run_time=0.5)
        self.at("17")
        r0 = mono(f"{s1} of {n1:,}", 18, GOOD).next_to(one, RIGHT, 0.4)
        self.play(FadeIn(r0), run_time=0.4)
        # 18-19: which steps happen as one?
        self.at("18")
        q = mono("which steps must happen as one?", 22, AMBER).move_to([-1.0, 3.2, 0]).shift(0.2 * DOWN)
        self.play(FadeOut(two), FadeIn(q), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
