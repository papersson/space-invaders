from rkit import *


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("The dependency graph")
        g = Graph()
        n, e = g.n, g.e
        # 01: the threshold
        self.at("01")
        self.play(FadeIn(c), run_time=0.3)
        thr = mono("free shipping from $65", 20, MUTED).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(thr), run_time=0.4)

        # 02-06: each formula reads some values; arrows appear as they're named
        self.at("02")
        self.play(*[FadeIn(n[k]) for k in LAYOUT], run_time=0.8)
        self.at("03")
        self.play(GrowArrow(e[("price", "subtotal")]), GrowArrow(e[("qty", "subtotal")]), run_time=0.6)
        self.at("04")
        self.play(GrowArrow(e[("subtotal", "tax")]), run_time=0.5)
        self.at("05")
        self.play(GrowArrow(e[("subtotal", "total")]), GrowArrow(e[("tax", "total")]), run_time=0.6)
        self.at("06")
        self.play(GrowArrow(e[("total", "free")]), run_time=0.4)
        self.play(GrowArrow(e[("free", "banner")]), run_time=0.4)

        # 07: that's a dependency graph
        self.at("07")
        name = T("dependency graph", 30, ICE).move_to([0, -2.2, 0])
        self.play(FadeIn(name), run_time=0.6)

        # 08-09: change qty; everything reachable is out of date
        self.at("08")
        self.play(n["qty"].edge(AMBER), Flash(n["qty"].box, color=AMBER, flash_radius=1.2), run_time=0.6)
        self.at("09")
        order = [("qty", "subtotal"), ("subtotal", "tax"), ("subtotal", "total"), ("tax", "total"),
                 ("total", "free"), ("free", "banner")]
        marked = set()
        for a, b in order:
            anims = [g.pulse(a, b)]
            self.play(*anims, run_time=0.35)
            if b not in marked:
                marked.add(b)
                self.play(n[b].edge(MARK), run_time=0.2)
        ood = mono("out of date", 20, MARK).next_to(n["tax"], UP, 0.25)
        self.play(FadeIn(ood), run_time=0.4)

        # 10-11: the price is not reachable: still correct
        self.at("10")
        ok = mono("not reachable: still correct", 16, MUTED).next_to(n["price"], UP, 0.2).align_to(n["price"], LEFT)
        self.play(Indicate(n["price"], color=INK, scale_factor=1.06), FadeIn(ok), run_time=0.8)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
