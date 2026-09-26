from ikit import *

XC, XS = -5.2, -0.9             # client and server lanes
TOP = 2.3


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("Idempotency keys")
        self.at("01")
        ln = lanes(XC, XS, TOP, -2.9)
        table = VGroup(RoundedRectangle(corner_radius=0.1, width=4.2, height=2.1, stroke_color=DIM, stroke_width=1.5,
                                        fill_color=PANEL, fill_opacity=1),)
        table.move_to([4.85, 1.2, 0])
        tt = label("server's saved results", 16, MUTED).next_to(table, UP, 0.1)
        hdr = mono("key          result", 16, FAINT).move_to(table.get_top() + 0.3 * DOWN)
        card = Card([4.85, -1.9, 0])
        self.play(FadeIn(c), FadeIn(ln), FadeIn(table), FadeIn(tt), FadeIn(hdr), FadeIn(card), run_time=0.7)

        # 02-03: the client makes a key once, and sends it with every attempt
        self.at("02", 1.0)
        key = mono(f"key: {KEY}", 20, AMBER).next_to([XC, TOP, 0], DOWN, 0.2)
        made = mono("made once, for this payment", 14, MUTED).next_to(key, DOWN, 0.08)
        self.play(FadeIn(key), FadeIn(made), run_time=0.6)
        self.at("03")
        r1 = message([XC, 1.3, 0], [XS, 0.9, 0], f"charge $50 · key {KEY}", size=14)
        self.play(GrowArrow(r1[0]), FadeIn(r1[1]), run_time=0.8)

        # 04: first time: charge, and save the result under the key
        self.at("04")
        miss = mono("key not seen → charge", 14, INK).next_to([XS, 0.9, 0], RIGHT, 0.15)
        self.play(FadeIn(miss), card.set_total(50), run_time=0.6)
        row = mono(f"{KEY}  charged, receipt #1042", 16, INK).move_to(table.get_center() + 0.2 * DOWN)
        self.play(FadeIn(row, shift=0.1 * RIGHT), run_time=0.6)
        rep1 = message([XS, 0.5, 0], [XC, 0.1, 0], "receipt #1042", color=INK, lost_at=0.5, size=14)
        self.play(Create(rep1[0]), FadeIn(rep1[1]), FadeIn(rep1[2]), run_time=0.7)

        # 05-06: a retry with the same key: no second charge; the saved result comes back
        self.at("05")
        r2 = message([XC, -0.6, 0], [XS, -1.0, 0], f"retry · key {KEY}", size=14)
        self.play(GrowArrow(r2[0]), FadeIn(r2[1]), run_time=0.7)
        hit = mono("key seen → no charge", 14, ICE).next_to([XS, -1.0, 0], RIGHT, 0.15)
        self.play(FadeIn(hit), Indicate(row, color=ICE), run_time=0.7)
        self.at("06")
        rep2 = message([XS, -1.5, 0], [XC, -1.9, 0], "receipt #1042", color=INK, size=14)
        self.play(GrowArrow(rep2[0]), FadeIn(rep2[1]), run_time=0.7)

        # 07: the lost reply is recovered; the customer pays once
        self.at("07")
        once = mono("paid once", 20, ICE).next_to(card, UP, 0.15)
        self.play(FadeIn(once), Circumscribe(card.box, color=ICE), run_time=0.8)

        # 08-09: Stripe's header
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        req = VGroup(mono("POST /v1/charges", 24, INK), mono(f"Idempotency-Key: {KEY}", 24, AMBER),
                     mono("amount=5000&currency=usd", 24, MUTED)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        box = SurroundingRectangle(req, buff=0.3, color=DIM, stroke_width=1.5, corner_radius=0.1)
        cap = mono("Stripe's API: the key goes in a request header", 18, MUTED).next_to(box, UP, 0.25)
        self.play(FadeIn(box), FadeIn(req[0]), FadeIn(req[2]), FadeIn(cap), run_time=0.6)
        self.at("09")
        self.play(FadeIn(req[1]), Indicate(req[1], color=AMBER), run_time=0.8)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
