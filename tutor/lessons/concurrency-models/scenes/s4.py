from ckit import *


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("One owner")
        acct = Account(1.5, 0.3, "$100")
        self.at("01")
        side = DashedLine([-5.5, -2.4, 0], acct.box.get_bottom() + 0.05 * DOWN, color=BAD, stroke_width=3)
        sl = mono("forgot the lock", 18, BAD).next_to(side.get_start(), UP, 0.15).align_to(side, LEFT)
        self.play(FadeIn(c), FadeIn(acct), Create(side), FadeIn(sl), run_time=0.8)
        # 02-05: nothing else can reach it
        self.at("02")
        actor = Actor(1.5, 0.3)
        wall = actor.circle.copy().set_stroke(color=ICE, width=6)
        self.play(FadeOut(acct), FadeIn(actor), run_time=0.8)
        self.at("03")
        stop = cross(side.get_end() + 0.35 * DOWN + 0.2 * LEFT, 0.2)
        self.play(Create(wall), Create(stop), run_time=0.6)
        self.play(FadeOut(wall), run_time=0.3)
        self.at("05")
        one = mono("one owner; nothing else touches the balance", 18, ICE).move_to([1.2, 2.5, 0])
        self.play(FadeIn(one), FadeOut(side), FadeOut(sl), FadeOut(stop), run_time=0.6)
        # 06: actor
        self.at("06")
        self.play(Indicate(actor.mail, color=ICE), Indicate(actor.circle, color=ICE, scale_factor=1.04), run_time=0.9)
        # 07-08: machines send deposit messages
        self.at("07")
        ma, mb = machine("A", -5.3, 1.4), machine("B", -5.3, -1.1)
        self.play(FadeIn(ma), FadeIn(mb), run_time=0.5)
        self.at("08")
        ea, eb = envelope("deposit 50", AMBER), envelope("deposit 50", AMBER)
        ea.move_to(ma.get_right() + 0.7 * RIGHT); eb.move_to(mb.get_right() + 0.7 * RIGHT)
        self.play(FadeIn(ea), FadeIn(eb), run_time=0.4)
        self.play(FadeOut(ea[2]), FadeOut(eb[2]), run_time=0.2)
        ea, eb = ea[:2], eb[:2]
        self.play(ea.animate.move_to(actor.slot(0)), eb.animate.move_to(actor.slot(1)), run_time=1.0)
        # 09-11: one at a time
        self.at("09")
        self.play(ea.animate.move_to(actor.circle.get_center() + 0.55 * UP).scale(0.6), run_time=0.6)
        self.play(FadeOut(ea), actor.set("$150"), run_time=0.5)
        self.at("11")
        self.play(eb.animate.move_to(actor.slot(0)), run_time=0.3)
        self.play(eb.animate.move_to(actor.circle.get_center() + 0.55 * UP).scale(0.6), run_time=0.5)
        self.play(FadeOut(eb), actor.set("$200", GOOD), run_time=0.5)
        # 12: no lock, no data race
        self.at("12")
        nl = mono("no lock · no data race on the balance", 18, GOOD).move_to([1.2, -2.3, 0])
        self.play(FadeIn(nl), run_time=0.5)
        # 13: sending doesn't wait
        self.at("13")
        e3 = envelope("", AMBER).move_to(ma.get_right() + 0.7 * RIGHT)
        self.play(FadeIn(e3), run_time=0.3)
        self.play(e3.animate.move_to(actor.slot(0)), ma.animate.shift(0.5 * UP), run_time=0.8)
        on = mono("carries on", 15, MUTED).next_to(ma, UP, 0.1)
        self.play(FadeIn(on), run_time=0.3)
        # 14-18: how firmly
        self.at("15")
        self.play(FadeOut(nl), run_time=0.3)
        er = mono("Erlang: default", 18, GOOD).move_to([0.2, -2.4, 0])
        self.play(FadeIn(er), run_time=0.4)
        self.at("16")
        cp = mono("(messages are copied)", 15, MUTED).next_to(er, DOWN, 0.1)
        self.play(FadeIn(cp), run_time=0.3)
        self.at("17")
        opt = mono("(shared tables: opt-in)", 15, MUTED).next_to(cp, DOWN, 0.05)
        self.play(FadeIn(opt), run_time=0.3)
        self.at("18")
        ak = mono("Akka: convention", 18, AMBER).move_to([4.4, -2.4, 0])
        self.play(FadeIn(ak), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
