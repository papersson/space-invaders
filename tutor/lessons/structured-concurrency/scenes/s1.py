from skit import *

GATHER = [(0, "async def handler():", INK), (1, "try:", INK),
          (2, "user, orders = await asyncio.gather(", INK), (3, "fetch_user(), fetch_orders())", INK),
          (1, "except Exception as e:", INK), (2, 'return "error"', INK)]


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        run = "gather"
        t_fail = when(run, "fetch_orders", "raises")
        t_ret = when(run, "handler", "has returned")
        t_user = when(run, "fetch_user", "finished")
        many = TL["many_gather"]

        # 01-02: the handler
        self.at("01")
        code = code_card(GATHER, 16, title="the handler (asyncio.gather)").move_to([0, 2.35, 0])
        self.play(FadeIn(code), run_time=0.7)
        self.at("02")
        self.play(Indicate(code[1][2], color=AMBER, scale_factor=1.04), Indicate(code[1][3], color=AMBER, scale_factor=1.04), run_time=1.0)

        # 03-05: the two requests on a timeline (the real run); ghost bars for the premise first
        tl = Timeline(run, y=-0.55)
        self.at("03")
        gu = ghost(tl, "fetch_user", 0, 1.0)
        u1 = mono("takes 1.00 s", 14, MUTED).move_to(gu.get_right() + 0.95 * LEFT)
        self.play(FadeIn(tl), run_time=0.5)
        self.play(Create(gu), FadeIn(u1), run_time=0.5)
        self.at("04")
        go = ghost(tl, "fetch_orders", 0, 0.1)
        o1 = mono("fails at 0.10 s", 14, MUTED).next_to(go, RIGHT, 0.2)
        self.play(Create(go), FadeIn(o1), run_time=0.5)
        self.at("05")
        ub1 = tl.bar("fetch_user", 0, t_ret)
        ob = tl.bar("fetch_orders", 0, t_fail)
        self.play(FadeOut(u1), FadeOut(o1), FadeOut(go), tl.grow(ub1, 0.8), tl.grow(ob, 0.8))
        self.play(FadeIn(tl.cross("fetch_orders", t_fail)), run_time=0.3)
        ret = tl.vline(t_ret, f"handler returned an error ({t_ret:.2f} s)")
        self.play(Create(ret[0]), FadeIn(ret[1]), run_time=0.5)

        # 07-08: the user request runs on
        self.at("07")
        ub2 = tl.bar("fetch_user", t_ret, t_user, color=AMBER)
        self.play(FadeOut(gu), tl.grow(ub2, 2.2))
        self.at("08")
        still = mono(f"still running until {t_user:.2f} s", 15, AMBER).next_to(ub2, DOWN, 0.12).align_to(ub2, RIGHT)
        self.play(FadeIn(still), run_time=0.4)

        # 09-10: had it failed (a second real run, gather_late), its error goes nowhere
        self.at("09")
        t_late = when("gather_late", "fetch_user", "raises")
        second = mono(f"a second run, where fetch_user fails at {t_late:.2f} s:", 14, MUTED).move_to([tl.X(0.72), tl.ys["fetch_user"] + 0.95, 0])
        x = tl.cross("fetch_user", t_late)
        te = mono("TimeoutError", 15, BAD).next_to(x, UP, 0.12)
        self.play(FadeIn(second), FadeIn(x), FadeIn(te), run_time=0.5)
        self.at("10")
        void = Circle(radius=0.16, stroke_color=BAD, stroke_width=2.5).move_to([tl.X(1.33), tl.ys["fetch_user"] + 0.95, 0])
        vl = mono("not raised · not logged", 14, BAD).next_to(void, DOWN, 0.1)
        ar = Arrow(te.get_right(), void.get_left(), buff=0.08, color=BAD, stroke_width=2.5, tip_length=0.14)
        self.play(GrowArrow(ar), Create(void), FadeIn(vl), run_time=0.6)

        # 11-12: a thousand requests (the real run)
        self.at("11")
        self.play(FadeOut(VGroup(second, x, te, ar, void, vl)), run_time=0.3)
        c1 = mono(f"{many['n']:,} requests at once", 18, INK).move_to([0, -3.05, 0])
        self.play(FadeIn(c1), run_time=0.4)
        self.at("12")
        c2 = VGroup(mono(f"{many['n']:,} requests at once · all handlers returned ·", 17, INK),
                    mono(f"tasks still running: {many['alive']:,}", 20, AMBER)).arrange(RIGHT, buff=0.3).move_to([0, -3.05, 0])
        self.play(FadeOut(c1), FadeIn(c2[0]), run_time=0.4)
        self.play(FadeIn(c2[1]), run_time=0.4)

        # 13-15: the question
        self.at("13")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        q0 = T("The function returned.", 34, INK).move_to([0, 1.0, 0])
        self.play(FadeIn(q0), run_time=0.5)
        self.at("14")
        q1 = T("Why is its work still running?", 34, INK).next_to(q0, DOWN, 0.45)
        self.play(FadeIn(q1), run_time=0.5)
        self.at("15")
        q2 = T("What would make “returned” mean “done”?", 30, AMBER).next_to(q1, DOWN, 0.45)
        self.play(FadeIn(q2), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
