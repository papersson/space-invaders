from rkit import *

AFTER3 = {"price": "$20", "qty": "3", "subtotal": "$60", "tax": "$6", "total": "$66", "free": "yes",
          "banner": "Free shipping!"}


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("Doing less")
        g = Graph(AFTER3)
        n = g.n
        self.at("01")
        self.play(FadeIn(c), FadeIn(g), run_time=0.7)
        waste = mono("still recomputes: values that come out the same, values nobody reads", 17, MUTED).to_edge(DOWN, buff=0.6)
        self.play(FadeIn(waste), run_time=0.5)

        # 03-08: early cutoff
        self.at("03")
        ec = T("early cutoff", 30, AMBER).move_to([0, 2.9, 0])
        self.play(FadeOut(waste), FadeIn(ec), run_time=0.5)
        self.at("04")
        self.play(n["qty"].set("4", AMBER), run_time=0.5)
        self.at("05")
        for k, v in (("subtotal", "$80"), ("tax", "$8"), ("total", "$88")):
            self.play(n[k].set(v, GREEN), run_time=0.45)
        self.at("06")
        self.play(n["free"].set("yes", GREEN), run_time=0.4)
        same = mono("unchanged", 16, GREEN).next_to(n["free"], DOWN, 0.2)
        self.play(FadeIn(same), run_time=0.3)
        self.at("07")
        arr = g.e[("free", "banner")]
        bar = Line(arr.get_center() + 0.35 * UP, arr.get_center() + 0.35 * DOWN, stroke_color=AMBER, stroke_width=6)
        self.play(Create(bar), run_time=0.4)
        skip = mono("not recomputed", 16, MUTED).next_to(n["banner"], DOWN, 0.2)
        self.play(FadeIn(skip), n["banner"].animate.set_opacity(0.55), run_time=0.5)

        # 09-11: laziness
        self.at("09")
        lz = T("laziness", 30, ICE).move_to(ec)
        self.play(FadeOut(ec), FadeIn(lz), run_time=0.5)
        self.at("10")
        box = RoundedRectangle(corner_radius=0.1, width=1.9, height=1.05, stroke_color=FAINT, stroke_width=2,
                               fill_color=TRAY_FILL, fill_opacity=1).move_to([1.2, -2.0, 0])
        name = mono("invoice total", 14, MUTED).move_to(box.get_top() + 0.22 * DOWN)
        val = mono("…", 22, FAINT).move_to(box.get_center() + 0.12 * DOWN)
        tag = mono("not on screen", 14, FAINT).next_to(box, RIGHT, 0.2)
        link = Arrow(n["total"].box.get_bottom(), box.get_top(), buff=0.06, color=FAINT, stroke_width=2.5, tip_length=0.16)
        self.play(FadeIn(box), FadeIn(name), FadeIn(val), FadeIn(tag), GrowArrow(link), run_time=0.7)
        self.at("11")
        self.play(box.animate.set_stroke(color=MARK), run_time=0.4)
        marked = mono("marked now", 16, MARK).next_to(box, LEFT, 0.25)
        self.play(FadeIn(marked), run_time=0.3)
        reader = Arrow(box.get_bottom() + 0.9 * DOWN + 1.2 * RIGHT, box.get_bottom() + 0.05 * DOWN, buff=0,
                       color=ICE, stroke_width=3, tip_length=0.16)
        self.play(GrowArrow(reader), run_time=0.5)
        v2 = mono("$88", 22, GREEN).move_to(val)
        self.play(Transform(val, v2), box.animate.set_stroke(color=TRAY_EDGE), FadeOut(tag),
                  FadeIn(mono("computed when read", 16, ICE).next_to(box, RIGHT, 0.2)), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
