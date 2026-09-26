from ckit import *


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        acct = Account(0, 0.4)
        ma, mb = machine("A", -4.6, 0.4), machine("B", 4.6, 0.4)
        # 01: two deposits at once
        self.at("01")
        self.play(FadeIn(acct), FadeIn(ma), FadeIn(mb), run_time=0.7)
        ea, eb = envelope("+$50", AMBER), envelope("+$50", AMBER)
        ea.move_to(ma.get_right() + 0.6 * RIGHT)
        eb.move_to(mb.get_left() + 0.6 * LEFT)
        self.play(FadeIn(ea), FadeIn(eb), run_time=0.4)
        self.play(ea.animate.move_to(acct.get_left() + 0.5 * LEFT), eb.animate.move_to(acct.get_right() + 0.5 * RIGHT),
                  run_time=1.2)
        # 02-04: should be 200; ends at 150
        self.at("02")
        exp = mono("expected $200", 20, MUTED).next_to(acct, DOWN, 0.4)
        self.play(FadeIn(exp), FadeOut(ea), FadeOut(eb), run_time=0.5)
        self.at("03")
        self.play(acct.set("$150", BAD), acct.box.animate.set_stroke(color=BAD), run_time=0.6)
        self.at("04")
        gone = mono("one deposit vanished", 20, BAD).next_to(exp, DOWN, 0.2)
        self.play(FadeIn(gone), run_time=0.4)

        # 05-08: two families
        self.at("05")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        colA = VGroup(label("share memory", 18, INK), mono("threads + locks", 22, AMBER)).arrange(DOWN, buff=0.25)
        colB = VGroup(label("pass messages", 18, INK), mono("actors · channels", 22, ICE)).arrange(DOWN, buff=0.25)
        colA.move_to([-3.2, 1.2, 0]); colB.move_to([3.2, 1.2, 0])
        head = T("coordinating work done at the same time", 30, INK).move_to([0, 2.7, 0])
        self.play(FadeIn(head), run_time=0.6)
        self.at("06")
        fam = mono("two broad families (there are others)", 18, MUTED).next_to(head, DOWN, 0.2)
        self.play(FadeIn(fam), run_time=0.5)
        self.at("07")
        self.play(FadeIn(colA), run_time=0.6)
        self.at("08")
        self.play(FadeIn(colB), run_time=0.6)
        # 09: the slogan
        self.at("09")
        slogan = VGroup(T("“Do not communicate by sharing memory;", 26, INK),
                        T("instead, share memory by communicating.”", 26, INK),
                        mono("Effective Go", 16, MUTED)).arrange(DOWN, buff=0.15)
        slogan.move_to([0, -1.2, 0])
        self.play(FadeIn(slogan), run_time=0.8)
        # 10-11: the question
        self.at("10")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        q = T("Does passing messages make bugs like this go away?", 34, INK).move_to([0, 0.3, 0])
        self.play(FadeIn(q), run_time=0.7)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
