from ckit import *
import re


def dl_runs():
    m = re.search(r"waits in its own send: stuck in (\d+) of (\d+).*?keeps listening: stuck in (\d+) of (\d+)", RUNS, re.S)
    return [int(g) for g in m.groups()]


STUDY = {"wrong": (86, 69, 17), "hang": (85, 36, 49)}      # Tu et al. 2019, Tables 6 and 9


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("Waiting in a circle")
        A, B = Account(-3.0, 0.3, "A", "account process", w=2.8), Account(3.0, 0.3, "B", "account process", w=2.8)
        self.at("01")
        self.play(FadeIn(c), run_time=0.3)
        md = T("messages can deadlock too", 30, INK).move_to([0, 2.6, 0])
        self.play(FadeIn(md), run_time=0.5)
        self.at("02")
        self.play(FadeIn(A), FadeIn(B), FadeOut(md), run_time=0.6)
        # 03-07: both send, both wait
        self.at("03")
        top = channel(A.box.get_right() + 0.35 * UP, B.box.get_left() + 0.35 * UP)
        bot = channel(B.box.get_left() + 0.35 * DOWN, A.box.get_right() + 0.35 * DOWN)
        self.play(Create(top), Create(bot), run_time=0.6)
        e1 = envelope("", AMBER, w=0.5, h=0.32).move_to(A.box.get_right() + 0.35 * UP + 0.6 * RIGHT)
        c1 = mono("credit 30 →", 15, AMBER).next_to(top, UP, 0.25)
        self.play(FadeIn(e1), FadeIn(c1), run_time=0.3)
        self.at("04")
        e2 = envelope("", AMBER, w=0.5, h=0.32).move_to(B.box.get_left() + 0.35 * DOWN + 0.6 * LEFT)
        c2 = mono("← credit 20", 15, AMBER).next_to(bot, DOWN, 0.25)
        self.play(FadeIn(e2), FadeIn(c2), e1.animate.shift(1.2 * RIGHT), run_time=0.6)
        self.play(e2.animate.shift(1.2 * LEFT), run_time=0.5)
        self.at("05")
        w1 = waiting_bar(A.box.get_top() + 0.35 * UP + 0.8 * LEFT, 1.6, AMBER, "A: waiting to send")
        self.play(FadeIn(w1), run_time=0.4)
        self.at("06")
        w2 = waiting_bar(B.box.get_top() + 0.35 * UP + 0.8 * LEFT, 1.6, AMBER, "B: waiting to send")
        self.play(FadeIn(w2), run_time=0.4)
        self.at("07")
        nl = mono("neither is listening", 18, BAD).move_to([0, -1.4, 0])
        self.play(FadeIn(nl), run_time=0.4)
        self.at("08")
        dl = T("deadlock, no locks", 30, BAD).move_to([0, 2.6, 0])
        self.play(FadeIn(dl), top.animate.set_color(BAD), bot.animate.set_color(BAD), run_time=0.6)
        s0, n0, s1, n1 = dl_runs()
        self.at("09")
        r0 = mono(f"both at once, {n0:,} runs: stuck in {s0}", 18, INK).move_to([0, -2.1, 0])
        self.play(FadeIn(r0), run_time=0.4)
        # 10-14: hand the send to a helper
        self.at("11")
        h = RoundedRectangle(corner_radius=0.08, width=1.6, height=0.6, stroke_color=ICE, stroke_width=2).set_stroke(opacity=1)
        h = DashedVMobject(h, num_dashes=24).move_to(A.box.get_right() + 1.5 * RIGHT + 1.2 * UP)
        hl = mono("helper", 14, ICE).move_to(h)
        self.play(Create(h), FadeIn(hl), run_time=0.5)
        self.at("12")
        lis = mono("keeps listening", 16, GOOD).next_to(A, DOWN, 0.3)
        self.play(FadeOut(w1), FadeOut(w2), FadeIn(lis), top.animate.set_color(MUTED), bot.animate.set_color(MUTED),
                  FadeOut(dl), FadeOut(nl), run_time=0.6)
        self.at("14")
        r1 = mono(f"with the helper: stuck in {s1} of {n1:,}", 18, GOOD).next_to(r0, DOWN, 0.15)
        self.play(FadeIn(r1), run_time=0.4)

        # 15-18: actors waiting for replies
        self.at("15")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        a1, a2 = Actor(-2.4, 0.3, "X", r=0.8), Actor(3.2, 0.3, "Y", r=0.8)
        self.play(FadeIn(a1), FadeIn(a2), run_time=0.5)
        self.at("17")
        r_1 = envelope("", AMBER).move_to(a2.slot(0))
        r_2 = envelope("", AMBER).move_to(a1.slot(0))
        self.play(FadeIn(r_1), FadeIn(r_2), run_time=0.5)
        wr1 = mono("waiting for reply", 15, AMBER).next_to(a1.circle, UP, 0.2)
        wr2 = mono("waiting for reply", 15, AMBER).next_to(a2.circle, UP, 0.2)
        self.play(FadeIn(wr1), FadeIn(wr2), run_time=0.4)
        self.at("18")
        fe = mono("each waits on the other forever", 18, BAD).move_to([0.4, -2.0, 0])
        self.play(FadeIn(fe), run_time=0.4)

        # 19-22: the study
        self.at("20")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        head = mono("171 concurrency bugs in six Go projects (Tu et al., ASPLOS 2019)", 17, MUTED).move_to([0, 2.7, 0])
        proj = mono("Docker · Kubernetes · etcd · CockroachDB · gRPC · BoltDB", 14, FAINT).next_to(head, DOWN, 0.1)
        self.play(FadeIn(head), FadeIn(proj), run_time=0.5)
        unit = 0.075
        def stacked(key, y, label_):
            tot, sm, mp = STUDY[key]
            b1 = Rectangle(width=sm * unit, height=0.6, stroke_width=0, fill_color=MUTED, fill_opacity=0.8)
            b2 = Rectangle(width=mp * unit, height=0.6, stroke_width=0, fill_color=ICE, fill_opacity=0.9)
            bars = VGroup(b1, b2).arrange(RIGHT, buff=0).move_to([-5.0, y, 0], aligned_edge=LEFT)
            t = mono(label_, 18, INK).next_to(bars, UP, 0.12).align_to(bars, LEFT)
            n1_ = mono(f"shared memory {sm}", 14, INK).move_to(b1)
            n2_ = mono(f"message passing {mp}", 14, "#0F1318" if mp > 20 else ICE)
            n2_.move_to(b2) if mp > 20 else n2_.next_to(b2, RIGHT, 0.15)
            return VGroup(bars, t, n1_, n2_)
        g1 = stacked("wrong", 0.9, "wrong results (86)")
        self.at("21")
        self.play(FadeIn(g1), run_time=0.6)
        f1 = mono("≈ 1 in 5", 20, ICE).next_to(g1[0], RIGHT, 2.3)
        self.play(FadeIn(f1), run_time=0.3)
        g2 = stacked("hang", -1.1, "code hung (85)")
        self.at("22")
        self.play(FadeIn(g2), run_time=0.6)
        f2 = mono("more than half", 20, AMBER).next_to(g2[0], RIGHT, 0.5)
        self.play(FadeIn(f2), run_time=0.3)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
