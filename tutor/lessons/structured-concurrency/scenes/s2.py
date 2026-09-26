from skit import *

SEQ = [(0, "async def handler():", INK), (1, "try:", INK), (2, "user = await fetch_user()", INK),
       (2, "orders = await fetch_orders()", INK), (1, "except Exception as e:", INK), (2, 'return "error"', INK)]


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("What a call promises")
        run = "sequential"
        # 01: plain code
        self.at("01")
        code = code_card(SEQ, 16, title="one after the other").move_to([-3.2, 1.6, 0])
        self.play(FadeIn(c), FadeIn(code), run_time=0.7)

        # 02-05: one way in, one way out; the error comes back; cancelling reaches the call
        self.at("02")
        fd = flow("sequential", c=(3.4, 1.4), w=2.4, h=2.2)
        inner = VGroup(RoundedRectangle(corner_radius=0.08, width=1.6, height=0.5, stroke_color=MUTED, stroke_width=1.5,
                                        fill_color=PANEL, fill_opacity=1).move_to([3.4, 1.85, 0]),
                       RoundedRectangle(corner_radius=0.08, width=1.6, height=0.5, stroke_color=MUTED, stroke_width=1.5,
                                        fill_color=PANEL, fill_opacity=1).move_to([3.4, 0.95, 0]))
        inner.add(mono("fetch_user", 14, INK).move_to(inner[0]), mono("fetch_orders", 14, INK).move_to(inner[1]))
        hl = mono("handler", 14, MUTED).next_to(fd[0], LEFT, 0.15).align_to(fd[0], UP)
        self.play(FadeIn(fd[0]), FadeIn(hl), run_time=0.4)
        self.play(GrowArrow(fd[1]), FadeIn(inner), run_time=0.8)
        tag = mono("one way in, one way out", 15, ICE).next_to(fd, DOWN, 0.15)
        self.play(FadeIn(tag), run_time=0.4)
        self.at("03")
        d1 = mono("returned = finished", 15, MUTED).move_to([3.4, -0.6, 0])
        self.play(FadeIn(d1), run_time=0.4)
        self.at("04")
        d2 = mono("error → back to the caller", 15, MUTED).next_to(d1, DOWN, 0.12)
        self.play(FadeIn(d2), run_time=0.4)
        self.at("05")
        d3 = mono("caller cancelled → the call stops too", 15, MUTED).next_to(d2, DOWN, 0.12)
        self.play(FadeIn(d3), run_time=0.4)
        self.at("07")
        bb = mono("a black box", 18, ICE).next_to(code, DOWN, 0.35)
        self.play(FadeIn(bb), run_time=0.4)

        # 08-09: but slow (the real run)
        self.at("08")
        self.play(FadeOut(d1), FadeOut(d2), FadeOut(d3), FadeOut(bb), run_time=0.3)
        tl = Timeline(run, y=-1.8, gap=0.6)
        t_user, t_fail = when(run, "fetch_user", "finished"), when(run, "fetch_orders", "raises")
        self.play(FadeIn(tl), run_time=0.4)
        ub = tl.bar("fetch_user", 0, t_user)
        self.play(tl.grow(ub, 1.2))
        self.at("09")
        ob = tl.bar("fetch_orders", t_user, t_fail)
        self.play(tl.grow(ob, 0.3))
        self.play(FadeIn(tl.cross("fetch_orders", t_fail)), run_time=0.2)
        ret = tl.vline(t_fail, f"error at {t_fail:.2f} s", color=AMBER)
        self.play(Create(ret[0]), FadeIn(ret[1]), run_time=0.5)

        # 10: so start them at the same time
        self.at("10")
        same = mono("start both at the same time?", 18, AMBER).move_to([3.4, -0.55, 0])
        self.play(FadeIn(same), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
