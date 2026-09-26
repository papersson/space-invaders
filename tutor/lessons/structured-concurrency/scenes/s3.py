from skit import *

CT = [(0, "u = asyncio.create_task(fetch_user())", INK), (0, "o = asyncio.create_task(fetch_orders())", INK),
      (0, "user = await u", AMBER), (0, "orders = await o", INK)]


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("Starting a task")
        # 01-03: starting a task splits control
        self.at("01")
        self.play(FadeIn(c), run_time=0.3)
        fs = flow("sequential", c=(-3.2, 0.6))
        fsl = mono("call a function", 16, MUTED).next_to(fs, DOWN, 0.2)
        self.play(FadeIn(fs), FadeIn(fsl), run_time=0.6)
        self.at("02")
        fp = flow("spawn", c=(1.6, 0.6))
        fpl = mono("start a task", 16, MUTED).next_to(fp, DOWN, 0.2).align_to(fp[0], LEFT)
        self.play(FadeIn(fp[0]), FadeIn(fpl), Create(fp[1]), run_time=0.5)
        self.play(GrowArrow(fp[2]), FadeIn(fp[4]), run_time=0.5)
        self.at("03")
        self.play(Create(fp[3]), run_time=0.8)
        away = mono("no way back", 15, AMBER).next_to(fp[3], RIGHT, 0.1).shift(0.3 * DOWN)
        self.play(FadeIn(away), run_time=0.3)

        # 04-09: gather waits for results, not tasks (the real run, and the docstring)
        self.at("04")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        exp = mono("expected: gather behaves like the calls", 18, INK).move_to([0, 2.5, 0])
        self.play(FadeIn(exp), run_time=0.4)
        self.at("05")
        ok = mono("both succeed → it waits for both results", 16, ICE).next_to(exp, DOWN, 0.2)
        self.play(FadeIn(ok), run_time=0.4)
        self.at("06")
        run = "gather"
        tl = Timeline(run, y=0.2)
        t_fail, t_ret, t_user = when(run, "fetch_orders", "raises"), when(run, "handler", "has returned"), when(run, "fetch_user", "finished")
        self.play(FadeIn(tl), FadeIn(tl.bar("fetch_user", 0, t_ret)), FadeIn(tl.bar("fetch_orders", 0, t_fail)),
                  FadeIn(tl.cross("fetch_orders", t_fail)), run_time=0.5)
        ret = tl.vline(t_ret, "gather passes the error on")
        self.play(Create(ret[0]), FadeIn(ret[1]), run_time=0.4)
        ub2 = tl.bar("fetch_user", t_ret, t_user, color=AMBER)
        nc = mono("not cancelled", 15, AMBER).next_to(ub2, DOWN, 0.12).align_to(ub2, RIGHT)
        self.play(tl.grow(ub2, 1.2), FadeIn(nc))
        self.at("07")
        doc = VGroup(mono("asyncio.gather docstring (Python 3.11):", 13, MUTED),
                     mono("“the first raised exception will be immediately propagated”", 14, INK)).arrange(DOWN, buff=0.08)
        doc.move_to([0, -2.5, 0])
        self.play(FadeIn(doc), run_time=0.5)
        self.at("08")
        own = VGroup(mono("gather waited for results", 18, INK), mono("it never owned the tasks", 18, AMBER)).arrange(DOWN, buff=0.12)
        own.move_to([0, -2.4, 0])
        self.play(FadeOut(doc), FadeIn(own[0]), run_time=0.4)
        self.at("09")
        self.play(FadeIn(own[1]), run_time=0.4)

        # 10-13: awaiting one at a time; the client gives up at 0.5 s (the real run)
        self.at("10")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        code = code_card(CT, 16, title="start both, await them in turn").move_to([0, 2.2, 0])
        self.play(FadeIn(code), run_time=0.5)
        self.at("11")
        run = "cancel_create_task"
        tl2 = Timeline(run, y=-0.9)
        t_c, t_end = when(run, "caller", "gave up"), when(run, "fetch_orders", "finished")
        self.play(FadeIn(tl2), run_time=0.4)
        ub = tl2.bar("fetch_user", 0, t_c)
        ob1 = tl2.bar("fetch_orders", 0, t_c)
        self.play(tl2.grow(ub, 1.2), tl2.grow(ob1, 1.2))
        self.at("12")
        gv = tl2.vline(t_c, f"client gives up ({t_c:.2f} s)", color=AMBER)
        self.play(Create(gv[0]), FadeIn(gv[1]), run_time=0.4)
        cu = tl2.cut("fetch_user", t_c)
        cl = mono("cancelled", 14, ICE).next_to(ub, UP, 0.08).align_to(ub, RIGHT)
        self.play(Create(cu), FadeIn(cl), run_time=0.4)
        self.at("13")
        ob2 = tl2.bar("fetch_orders", t_c, t_end, color=AMBER)
        rn = mono("runs on", 14, AMBER).next_to(ob2, DOWN, 0.1).align_to(ob2, RIGHT)
        self.play(tl2.grow(ob2, 1.2), FadeIn(rn))
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
