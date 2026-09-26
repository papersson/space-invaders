from rkit import *

HEIGHTS = {"price": 0, "qty": 0, "subtotal": 1, "tax": 2, "total": 3, "free": 4, "banner": 5}
AFTER = {"subtotal": "$60", "tax": "$6", "total": "$66", "free": "yes", "banner": "Free shipping!"}


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("Mark, then compute in order")
        g = Graph()
        n = g.n
        self.at("01")
        self.play(FadeIn(c), FadeIn(g), run_time=0.7)

        # 02-04: mark
        self.at("02")
        ph1 = mono("1. mark", 24, MARK).move_to([-4.6, -2.3, 0])
        self.play(FadeIn(ph1), n["qty"].set("3", AMBER), run_time=0.5)
        self.at("03")
        for a, b in [("qty", "subtotal"), ("subtotal", "tax"), ("tax", "total"), ("total", "free"), ("free", "banner")]:
            self.play(g.pulse(a, b), run_time=0.3)
            self.play(n[b].edge(MARK), run_time=0.15)
        self.at("04")
        nc = mono("nothing computed yet", 16, MUTED).next_to(ph1, DOWN, 0.15).align_to(ph1, LEFT)
        self.play(FadeIn(nc), run_time=0.4)

        # 05-12: heights
        self.at("05")
        ph2 = mono("2. compute, in order", 24, GREEN).move_to([0.6, -2.3, 0])
        self.play(FadeIn(ph2), run_time=0.5)
        hl = {}
        for k in LAYOUT:
            hl[k] = mono(f"h{HEIGHTS[k]}", 18, ICE).next_to(n[k], UP, 0.12)
        for cue, keys in (("07", ["price", "qty"]), ("08", ["subtotal"]), ("09", ["tax"]), ("10", ["total"]),
                          ("11", ["free", "banner"])):
            self.at(cue)
            self.play(*[FadeIn(hl[k], shift=0.1 * DOWN) for k in keys], run_time=0.5)
        self.at("12")
        rule = mono("height = 1 + highest height it reads", 18, ICE).to_edge(UP, buff=0.35).shift(1.2 * RIGHT)
        self.play(FadeIn(rule), run_time=0.5)

        # 13-16: recompute marked values from the lowest height up, once each
        self.at("13")
        tally = Tally()
        self.play(FadeIn(tally), FadeOut(nc), run_time=0.3)
        for k in ["subtotal", "tax", "total", "free", "banner"]:
            self.play(n[k].set(AFTER[k], GREEN), n[k].edge(TRAY_EDGE), Indicate(hl[k], color=GREEN), tally.inc(),
                      run_time=0.55)
        self.at("16")
        cmp = mono("no $64 · 5 recomputations instead of 8", 20, GREEN).move_to([0.6, -3.0, 0])
        self.play(FadeIn(cmp), run_time=0.5)

        # 17: ten diamonds: once
        self.at("17")
        ten = mono("10 diamonds: last value runs 1× (was 1,024×)", 20, GREEN).next_to(cmp, DOWN, 0.15)
        self.play(FadeIn(ten), run_time=0.5)
        # 19: free shipping once, on 66: yes
        self.at("19")
        self.play(Indicate(n["free"], color=GREEN, scale_factor=1.08), run_time=0.8)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
