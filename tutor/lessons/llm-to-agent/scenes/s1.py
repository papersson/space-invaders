from skit import *


def mbox(x, y):
    b = rbox(1.9, 1.0, MODEL, fill=PANEL, sw=2.5).move_to([x, y, 0])
    return VGroup(b, T("model", 26, MODEL, weight=MEDIUM).move_to(b))


def tcard(s, color, x, y, w=2.3):
    b = rbox(w, 0.62, color, fill=PANEL, sw=1.8, r=0.1).move_to([x, y, 0])
    return VGroup(b, T(s, 18, INK).move_to(b))


def question_box(x, y):
    frame = DashedVMobject(rbox(2.2, 1.25, FAINT, fill=BG, fo=0, sw=2.2), num_dashes=36)
    frame.move_to([x, y, 0])
    q = T("?", 40, MUTED, weight=BOLD).move_to(frame)
    return frame, q


TOP_Y, BOT_Y, MX = 1.65, -1.55, -2.6


class S1(LScene):
    SEG = "s1"

    def construct(self):
        ch = chip("1 · the question")
        self.add(ch)
        self.fade_in_all(0.3)

        # 01-03: 2022, a chat: your message -> model -> its reply
        self.at("01")
        top = label("Nov 2022 · ChatGPT", 18, MUTED).move_to([-6.6, TOP_Y + 1.0, 0], aligned_edge=LEFT)
        self.play(FadeIn(top), run_time=0.5)
        self.at("02")
        msg = tcard("your message", INK, -5.35, TOP_Y)
        m1 = mbox(MX, TOP_Y)
        rep = tcard("its reply", MODEL, 0.25, TOP_Y)
        a1 = arrow(msg.get_right() + RIGHT * 0.08, m1.get_left() + LEFT * 0.08)
        a2 = arrow(m1.get_right() + RIGHT * 0.08, rep.get_left() + LEFT * 0.08)
        self.play(FadeIn(msg), run_time=0.35)
        self.play(GrowArrow(a1), FadeIn(m1), run_time=0.45)
        self.play(GrowArrow(a2), FadeIn(rep, shift=RIGHT * 0.2), run_time=0.45)
        self.at("03")
        self.play(Indicate(rep, color=MODEL, scale_factor=1.06), run_time=0.8)

        # 04-05: today, an agent: a bug -> model -> ? -> actions
        self.at("04")
        bot = label("today · an agent", 18, MUTED).move_to([-6.6, BOT_Y + 1.0, 0], aligned_edge=LEFT)
        m2 = mbox(MX, BOT_Y)
        self.play(FadeIn(bot), FadeIn(m2), run_time=0.5)
        self.at("05")
        bug = tcard("a bug in some code", INK, -5.35, BOT_Y, w=2.5)
        qf, qq = question_box(0.55, BOT_Y)
        acts = VGroup(*[tcard(s, INK, 4.6, BOT_Y + 0.75 - 0.75 * i, w=2.4) for i, s in
                        enumerate(["read files", "run tests", "fix the bug"])])
        b1 = arrow(bug.get_right() + RIGHT * 0.05, m2.get_left() + LEFT * 0.08)
        b2 = arrow(m2.get_right() + RIGHT * 0.08, qf.get_left() + LEFT * 0.06)
        b3 = VGroup(*[arrow(qf.get_right() + RIGHT * 0.06, a.get_left() + LEFT * 0.08) for a in acts])
        self.play(FadeIn(bug), GrowArrow(b1), run_time=0.45)
        self.play(Create(qf), FadeIn(qq), GrowArrow(b2), run_time=0.5)
        # the three actions, in step with "reads the files, runs the tests, fixes the bug"
        s, e = self.cues["05"]
        for i, a in enumerate(acts):
            self.until(s + (e - s) * (0.32 + 0.24 * i))
            self.play(GrowArrow(b3[i]), FadeIn(a, shift=RIGHT * 0.15), run_time=0.4)

        # 06: the same kind of model
        self.at("06", 0.8)
        self.play(Indicate(m1, color=MODEL, scale_factor=1.08), Indicate(m2, color=MODEL, scale_factor=1.08), run_time=1.0)

        # 07: and it only writes text: a text card leaves the model and stops at the ?
        self.at("07")
        tx = tcard("text", MODEL, MX, BOT_Y, w=1.0).scale(0.8)
        self.add(tx)
        self.bring_to_front(m2)
        self.play(tx.animate.move_to(b2.get_center() + UP * 0.45), run_time=0.8)

        # 08-09: so what sits in between?
        self.at("08")
        self.play(qf.animate.set_color(INK), qq.animate.set_color(INK).scale(1.5), run_time=0.6)
        self.at("09", 0.5)
        self.play(Circumscribe(qf, color=INK, buff=0.08), run_time=1.2)
        self.end()
