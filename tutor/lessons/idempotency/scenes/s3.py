from ikit import *


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("At most once, or at least once")
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)

        def lane(y, name, rule, outcome, color):
            box = RoundedRectangle(corner_radius=0.12, width=12.4, height=1.7, stroke_color=DIM, stroke_width=1.5,
                                   fill_color=PANEL, fill_opacity=1).move_to([0, y, 0])
            n = mono(name, 26, INK).move_to([-5.8, y + 0.3, 0], aligned_edge=LEFT)
            r = mono(rule, 18, MUTED).move_to([-5.8, y - 0.3, 0], aligned_edge=LEFT)
            o = mono(outcome, 24, color).move_to([5.8, y + 0.15, 0], aligned_edge=RIGHT)
            return VGroup(box, n, r, o)

        top = lane(1.3, "at most once", "send once, never retry", "charged 0 or 1 times", MUTED)
        bot = lane(-1.0, "at least once", "retry until a reply arrives", "charged 1 or more times", MUTED)

        # 02-04: at most once
        self.at("02")
        self.play(FadeIn(top[0]), FadeIn(top[2]), run_time=0.5)
        self.at("03")
        risk1 = mono("never twice · a lost request stays lost", 16, CORAL).next_to(top[3], DOWN, 0.15, aligned_edge=RIGHT)
        self.play(FadeIn(top[3]), FadeIn(risk1), run_time=0.6)
        self.at("04")
        self.play(FadeIn(top[1]), run_time=0.4)

        # 05-07: at least once
        self.at("05")
        self.play(FadeIn(bot[0]), FadeIn(bot[2]), run_time=0.5)
        self.at("06")
        risk2 = mono("never lost · repeats whenever a reply was lost", 16, CORAL).next_to(bot[3], DOWN, 0.15, aligned_edge=RIGHT)
        self.play(FadeIn(bot[3]), FadeIn(risk2), run_time=0.6)
        self.at("07")
        self.play(FadeIn(bot[1]), run_time=0.4)

        # 08-09: a payment can't be lost: retry, and make repeats harmless
        self.at("08")
        pick = SurroundingRectangle(bot[0], buff=0.06, color=ICE, stroke_width=3, corner_radius=0.14)
        self.play(Create(pick), top.animate.set_opacity(0.35), risk1.animate.set_opacity(0.35), run_time=0.7)
        self.at("09")
        need = T("so the server must make a repeated request harmless", 26, ICE).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(need), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
