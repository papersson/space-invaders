from rkit import *


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("Just tell the readers")
        g = Graph()
        n = g.n
        tally = Tally()
        self.at("01")
        self.play(FadeIn(c), FadeIn(g), run_time=0.7)

        # 01-03: each value tells its readers
        self.play(g.pulse("qty", "subtotal", ICE), run_time=0.5)
        self.at("03")
        self.play(g.pulse("subtotal", "tax", ICE), g.pulse("subtotal", "total", ICE), run_time=0.6)
        self.play(g.pulse("total", "free", ICE), run_time=0.4)
        self.play(g.pulse("free", "banner", ICE), run_time=0.4)

        # 04: the observer pattern
        self.at("04")
        op = T("the observer pattern", 30, INK).move_to([0, -2.3, 0])
        self.play(FadeIn(op), run_time=0.6)

        # 05-07: qty -> 3, subtotal -> 60; two readers
        self.at("06")
        self.play(FadeOut(op), FadeIn(tally), n["qty"].set("3", AMBER), run_time=0.6)
        self.play(g.pulse("qty", "subtotal", ICE), run_time=0.4)
        self.play(n["subtotal"].set("$60", GREEN), tally.inc(), run_time=0.5)
        self.at("07")
        self.play(Indicate(n["tax"].box, color=AMBER, scale_factor=1.05),
                  Indicate(n["total"].box, color=AMBER, scale_factor=1.05), run_time=0.8)

        # 08-10: which first? whichever subscribed first; say the total
        self.at("10")
        self.play(g.pulse("subtotal", "total", BAD, run_time=0.6))

        # 11-12: 60 + old 4 = 64
        self.at("11")
        calc = mono("60 + 4 (old tax)", 18, BAD).next_to(n["total"], DOWN, 0.3)
        self.play(FadeIn(calc), Indicate(n["tax"].val, color=BAD), run_time=0.8)
        self.at("12")
        self.play(n["total"].set("$64", BAD), n["total"].edge(BAD), tally.inc(), run_time=0.6)

        # 13-15: never a correct total; free shipping says no
        self.at("14")
        right = mono("right: $44 before, $66 after", 16, GREEN).next_to(calc, DOWN, 0.15)
        self.play(FadeIn(right), run_time=0.5)
        self.at("15")
        self.play(g.pulse("total", "free", BAD), run_time=0.4)
        self.play(n["free"].set("no", BAD), n["free"].edge(BAD), tally.inc(), run_time=0.5)
        self.play(g.pulse("free", "banner", BAD), run_time=0.4)
        self.play(n["banner"].set("Spend $65…", BAD), tally.inc(), run_time=0.5)

        # 16: a glitch
        self.at("16")
        gl = T("glitch", 34, BAD).move_to([1.2, 2.3, 0])
        self.play(FadeIn(gl, scale=1.2), run_time=0.5)

        # 17-19: then the tax, and everything after it again
        self.at("17")
        self.play(FadeOut(calc), FadeOut(right), g.pulse("subtotal", "tax", ICE), run_time=0.5)
        self.play(n["tax"].set("$6", GREEN), tally.inc(), run_time=0.5)
        self.at("18")
        self.play(g.pulse("tax", "total", ICE), run_time=0.4)
        self.play(n["total"].set("$66", GREEN), n["total"].edge(TRAY_EDGE), tally.inc(), run_time=0.5)
        self.at("19")
        self.play(g.pulse("total", "free", ICE), run_time=0.3)
        self.play(n["free"].set("yes", GREEN), n["free"].edge(TRAY_EDGE), tally.inc(), run_time=0.4)
        self.play(g.pulse("free", "banner", ICE), run_time=0.3)
        self.play(n["banner"].set("Free shipping!", GREEN), tally.inc(), run_time=0.4)
        twice = mono("total, free shipping and banner: computed twice", 17, AMBER).to_edge(DOWN, buff=0.7)
        self.play(FadeIn(twice), run_time=0.4)

        # 20-22: the shape: a diamond
        self.at("21")
        self.play(FadeOut(gl), FadeOut(twice), run_time=0.3)
        p1 = g.e[("subtotal", "total")].copy().set_color(AMBER).set_stroke(width=6)
        p2 = VGroup(g.e[("subtotal", "tax")].copy(), g.e[("tax", "total")].copy()).set_color(AMBER).set_stroke(width=6)
        self.play(Create(p1), run_time=0.6)
        self.play(Create(p2), run_time=0.8)
        self.at("22")
        dl = T("diamond", 32, AMBER).move_to([-1.0, -1.6, 0])
        self.play(FadeIn(dl), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
