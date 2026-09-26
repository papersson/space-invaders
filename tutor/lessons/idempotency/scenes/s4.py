from ikit import *


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("Safe to repeat")
        self.at("01")
        d = T("idempotent: doing it any number of times has the same effect as doing it once", 24, INK)
        d.move_to([0, 2.9, 0])
        self.play(FadeIn(c), FadeIn(d), run_time=0.7)

        ys = [1.5, 0.0, -1.5]
        heads = [mono("set shipping address", 22, INK), mono("delete order 7", 22, INK), mono("charge $50", 22, INK)]
        for h, y in zip(heads, ys):
            h.move_to([-4.3, y, 0])
        once = [mono("address: 12 Elm St", 20, MUTED), mono("order 7: gone", 20, MUTED), mono("card: $50", 20, MUTED)]
        twice = [mono("address: 12 Elm St", 20, ICE), mono("order 7: gone (not found)", 20, ICE),
                 mono("card: $100", 20, CORAL)]
        for o, t, y in zip(once, twice, ys):
            o.move_to([0.3, y, 0])
            t.move_to([4.4, y, 0])
        col1 = label("after once", 16, FAINT).move_to([0.3, 2.3, 0])
        col2 = label("after twice", 16, FAINT).move_to([4.4, 2.3, 0])

        # 02-03: set address
        self.at("02")
        self.play(FadeIn(heads[0]), FadeIn(col1), FadeIn(col2), FadeIn(once[0]), run_time=0.6)
        self.at("03")
        self.play(FadeIn(twice[0]), run_time=0.5)
        ok1 = mono("same", 16, ICE).next_to(twice[0], DOWN, 0.1)
        self.play(FadeIn(ok1), run_time=0.3)

        # 04-05: delete order 7
        self.at("04")
        self.play(FadeIn(heads[1]), FadeIn(once[1]), run_time=0.5)
        self.at("05")
        ok2 = mono("same", 16, ICE).next_to(twice[1], DOWN, 0.1)
        self.play(FadeIn(twice[1]), FadeIn(ok2), run_time=0.5)

        # 06-07: charge $50 is not
        self.at("06")
        self.play(FadeIn(heads[2]), FadeIn(once[2]), run_time=0.5)
        self.at("07")
        bad = mono("charged again", 16, CORAL).next_to(twice[2], DOWN, 0.1)
        self.play(FadeIn(twice[2]), FadeIn(bad), run_time=0.5)

        # 08: make the charge safe to repeat
        self.at("08")
        http = mono("in HTTP: PUT and DELETE are meant to be idempotent; POST is not", 16, FAINT).to_edge(DOWN, buff=0.4)
        self.play(FadeIn(http), Indicate(heads[2], color=CORAL), run_time=0.8)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
