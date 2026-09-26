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

        # 04-11: two common ways to wait; the first, gather, waits for results, not tasks
        self.at("04")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        two = mono("two common ways to wait for tasks", 18, MUTED).move_to([0, 2.9, 0])
        self.play(FadeIn(two), run_time=0.4)
        self.at("05")
        exp = mono("1. gather", 20, INK).move_to([0, 2.4, 0])
        self.play(FadeIn(exp), run_time=0.3)
        self.at("07")
        ok = mono("both succeed → it waits for both results", 16, ICE).next_to(exp, DOWN, 0.15)
        self.play(FadeIn(ok), run_time=0.4)
        self.at("08")
        run = "gather"
        tl = Timeline(run, y=0.1)
        t_fail, t_ret, t_user = when(run, "fetch_orders", "raises"), when(run, "handler", "has returned"), when(run, "fetch_user", "finished")
        self.play(FadeIn(tl), FadeIn(tl.bar("fetch_user", 0, t_ret)), FadeIn(tl.bar("fetch_orders", 0, t_fail)),
                  FadeIn(tl.cross("fetch_orders", t_fail)), run_time=0.5)
        ret = tl.vline(t_ret, "gather passes the error on")
        self.play(Create(ret[0]), FadeIn(ret[1]), run_time=0.4)
        q1 = VGroup(mono("Python docs, asyncio.gather:", 12, MUTED),
                    mono("\u201cIf return_exceptions is False (default), the first raised exception is", 13, INK),
                    mono("immediately propagated to the task that awaits on gather().", 13, INK)).arrange(DOWN, buff=0.05, aligned_edge=LEFT)
        q1.move_to([0, -2.1, 0])
        self.play(FadeIn(q1), run_time=0.4)
        ub2 = tl.bar("fetch_user", t_ret, t_user, color=AMBER)
        nc = mono("not cancelled", 15, AMBER).next_to(ub2, DOWN, 0.12).align_to(ub2, RIGHT)
        self.play(tl.grow(ub2, 1.2), FadeIn(nc))
        self.at("09")
        q2 = VGroup(mono("Other awaitables in the aws sequence won't be cancelled and will continue to run.\u201d", 13, INK),
                    mono("(awaitables in the aws sequence: here, the two requests)", 12, MUTED)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        q2.next_to(q1, DOWN, 0.06).align_to(q1, LEFT)
        self.play(FadeIn(q2), run_time=0.5)
        self.at("10")
        own = VGroup(mono("gather waited for results", 18, INK), mono("it never owned the tasks", 18, AMBER)).arrange(DOWN, buff=0.12)
        own.move_to([0, -2.45, 0])
        self.play(FadeOut(q1), FadeOut(q2), FadeIn(own[0]), run_time=0.4)
        self.at("11")
        self.play(FadeIn(own[1]), run_time=0.4)

        # 12-14: the second way, awaiting one at a time; the client gives up at 0.5 s (the real run)
        self.at("12")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        code = code_card(CT, 16, title="2. start both, await them in turn").move_to([0, 2.2, 0])
        self.play(FadeIn(code), run_time=0.5)
        run = "cancel_create_task"
        tl2 = Timeline(run, y=-0.9)
        t_c, t_end = when(run, "caller", "gave up"), when(run, "fetch_orders", "finished")
        self.play(FadeIn(tl2), run_time=0.4)
        ub = tl2.bar("fetch_user", 0, t_c)
        ob1 = tl2.bar("fetch_orders", 0, t_c)
        self.play(tl2.grow(ub, 1.2), tl2.grow(ob1, 1.2))
        self.at("13")
        gv = tl2.vline(t_c, f"client gives up ({t_c:.2f} s)", color=AMBER)
        self.play(Create(gv[0]), FadeIn(gv[1]), run_time=0.4)
        cu = tl2.cut("fetch_user", t_c)
        cl = mono("cancelled", 14, ICE).next_to(ub, UP, 0.08).align_to(ub, RIGHT)
        self.play(Create(cu), FadeIn(cl), run_time=0.4)
        self.at("14")
        ob2 = tl2.bar("fetch_orders", t_c, t_end, color=AMBER)
        rn = mono("runs on", 14, AMBER).next_to(ob2, DOWN, 0.1).align_to(ob2, RIGHT)
        self.play(tl2.grow(ob2, 1.2), FadeIn(rn))

        # 15-18: so a fix has to do three things (the spec, boxes left empty)
        self.at("15")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        head = mono("a real fix has to", 22, INK).move_to([0, 1.6, 0])
        self.play(FadeIn(head), run_time=0.4)
        for i, cue in enumerate(("16", "17", "18")):
            self.at(cue)
            self.play(FadeIn(spec_row(i, y=0.6 - 0.75 * i)), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
