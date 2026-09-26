from skit import *

# what sims/handler.py ran (return is not allowed inside except*, so the handler logs and falls through)
TGH = [(0, "async def handler():", INK), (1, "try:", INK), (2, "async with asyncio.TaskGroup() as tg:", ICE),
       (3, "user = tg.create_task(fetch_user())", INK), (3, "orders = tg.create_task(fetch_orders())", INK),
       (1, "except* Exception as eg:", INK), (2, 'log("returns error:", eg.exceptions)', INK)]


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("The same handler, in a task group")
        run = "taskgroup"
        t_fail, t_cut, t_ret = when(run, "fetch_orders", "raises"), when(run, "fetch_user", "cancelled"), when(run, "handler", "has returned")
        many = TL["many_taskgroup"]
        S1, S2, S3 = -2.8, -3.2, -3.65   # status lines, below the axis

        # 01: the code
        self.at("01")
        code = code_card(TGH, 15, title="the handler (asyncio.TaskGroup)").move_to([1.8, 1.7, 0])
        self.play(FadeIn(c), FadeIn(code), run_time=0.6)

        # 02-03: the real run: orders fails, user cancelled at once
        tl = Timeline(run, y=-1.05)
        self.at("02")
        self.play(FadeIn(tl), run_time=0.4)
        ub, ob = tl.bar("fetch_user", 0, t_cut), tl.bar("fetch_orders", 0, t_fail)
        self.play(tl.grow(ub, 0.8), tl.grow(ob, 0.8))
        self.play(FadeIn(tl.cross("fetch_orders", t_fail)), run_time=0.3)
        self.at("03")
        cu = tl.cut("fetch_user", t_cut)
        cl = mono(f"cancelled ({t_cut:.2f} s)", 15, ICE).next_to(cu, RIGHT, 0.15)
        self.play(Create(cu), FadeIn(cl), run_time=0.5)

        # 04-05: the error reaches the handler, inside an ExceptionGroup
        self.at("04")
        ret = tl.vline(t_ret, f"handler raised the error ({t_ret:.2f} s)")
        ret[1].align_to(ret[0], LEFT).shift(0.3 * LEFT)
        self.play(Create(ret[0]), FadeIn(ret[1]), run_time=0.5)
        self.at("05")
        lab2 = mono(f"handler raised ExceptionGroup: [ConnectionError] ({t_ret:.2f} s)", 14, INK).move_to(ret[1], aligned_edge=LEFT)
        self.play(ReplacementTransform(ret[1], lab2), run_time=0.5)

        # 06-07: which except matches it (data/except_check.txt)
        self.at("06")
        ex1 = mono("except ConnectionError:   no match (it's an ExceptionGroup)", 15, MUTED).move_to([0, S1, 0])
        self.play(FadeIn(ex1), run_time=0.4)
        self.at("07")
        ex2 = mono("except* ConnectionError:  matches (looks inside the group)", 15, ICE).move_to([0, S2, 0]).align_to(ex1, LEFT)
        self.play(FadeIn(ex2), Indicate(code[1][5], color=ICE, scale_factor=1.05), run_time=0.8)

        # 08-09: nothing left running
        self.at("08")
        n0 = mono("tasks still running: 0", 18, ICE).move_to([0, S1, 0])
        self.play(FadeOut(ex1), FadeOut(ex2), FadeIn(n0), run_time=0.4)
        self.at("09")
        later = mono("nothing left to fail later", 15, ICE).move_to([0, S2, 0])
        self.play(FadeIn(later), run_time=0.4)

        # 10: a thousand requests (the real run)
        self.at("10")
        cnt = mono(f"{many['n']:,} requests at once · all handlers returned · tasks still running: {many['alive']}", 17, ICE).move_to([0, S3, 0])
        self.play(FadeIn(cnt), run_time=0.4)

        # 11: the client gives up at 0.5 s (the real run, a different setup, so the old chart goes): both cancelled
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        run2 = "cancel_taskgroup"
        tl2 = Timeline(run2, y=-0.3)
        t_c = when(run2, "caller", "gave up")
        tg2 = tag("this run: both requests take 1.0 s, neither fails", tl2).shift(0.25 * UP)
        self.play(FadeIn(tl2), FadeIn(tg2), run_time=0.3)
        b1, b2 = tl2.bar("fetch_user", 0, t_c), tl2.bar("fetch_orders", 0, t_c)
        self.play(tl2.grow(b1, 1.0), tl2.grow(b2, 1.0))
        gv = tl2.vline(t_c, f"client gives up ({t_c:.2f} s)", color=MUTED)
        self.play(Create(gv[0]), FadeIn(gv[1]), Create(tl2.cut("fetch_user", t_c)), Create(tl2.cut("fetch_orders", t_c)), run_time=0.5)
        both = mono(f"both cancelled at {t_c:.2f} s", 17, ICE).move_to([0, tl2.axis_y - 0.8, 0])
        self.play(FadeIn(both), run_time=0.3)

        # 12-15: the spec from chapter 3, each box ticked as its guarantee is said, with the measured evidence
        self.at("12")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        head = mono("a task group guarantees", 22, INK).move_to([0, 2.1, 0])
        rows = [spec_row(i, x=-5.6, y=1.0 - 1.05 * i) for i in range(3)]
        self.play(FadeIn(head), *[FadeIn(r) for r in rows], run_time=0.5)
        ev = [f"handler returned at {t_ret:.2f} s · tasks left: 0",
              f"fetch_user cancelled at {t_cut:.2f} s · ExceptionGroup: [ConnectionError]",
              f"client gave up at {t_c:.2f} s · both cancelled"]
        for i, cue in enumerate(("13", "14", "15")):
            self.at(cue)
            e = mono(ev[i], 17, ICE).next_to(rows[i][1], DOWN, 0.12).align_to(rows[i][1], LEFT)
            self.play(Create(tick(rows[i][0])), rows[i][0].animate.set_stroke(ICE), FadeIn(e), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
