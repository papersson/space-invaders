from skit import *

TGH = [(0, "async def handler():", INK), (1, "try:", INK), (2, "async with asyncio.TaskGroup() as tg:", ICE),
       (3, "user = tg.create_task(fetch_user())", INK), (3, "orders = tg.create_task(fetch_orders())", INK),
       (1, "except* Exception as eg:", INK), (2, 'return "error"', INK)]


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("The same handler, in a task group")
        run = "taskgroup"
        t_fail, t_cut, t_ret = when(run, "fetch_orders", "raises"), when(run, "fetch_user", "cancelled"), when(run, "handler", "has returned")
        # 01: the code
        self.at("01")
        code = code_card(TGH, 15).move_to([1.2, 1.8, 0])
        self.play(FadeIn(c), FadeIn(code), run_time=0.6)

        # 02-06: the real run: orders fails, user cancelled, error raised, nothing left
        tl = Timeline(run, y=-1.2)
        self.at("02")
        self.play(FadeIn(tl), run_time=0.4)
        ub, ob = tl.bar("fetch_user", 0, t_cut), tl.bar("fetch_orders", 0, t_fail)
        self.play(tl.grow(ub, 0.8), tl.grow(ob, 0.8))
        self.play(FadeIn(tl.cross("fetch_orders", t_fail)), run_time=0.3)
        self.at("03")
        cu = tl.cut("fetch_user", t_cut)
        cl = mono(f"cancelled ({t_cut:.2f} s)", 15, ICE).next_to(cu, RIGHT, 0.15)
        self.play(Create(cu), FadeIn(cl), run_time=0.5)
        self.at("04")
        ret = tl.vline(t_ret, "error raised in the handler")
        self.play(Create(ret[0]), FadeIn(ret[1]), run_time=0.5)
        self.at("05")
        eg = mono("ExceptionGroup: [ConnectionError]", 16, INK).move_to([tl.X(0.85), tl.ys["fetch_orders"] - 0.05, 0])
        self.play(FadeIn(eg), run_time=0.4)
        self.at("06")
        st = mono("caught with except*, not a plain except", 15, INK).next_to(eg, DOWN, 0.12)
        self.play(FadeIn(st), Indicate(code[1][5], color=ICE, scale_factor=1.05), run_time=0.8)
        self.at("07")
        n0 = mono("tasks still running: 0", 18, ICE).move_to([tl.X(0.85), tl.ys["fetch_user"] + 0.05, 0])
        self.play(FadeIn(n0), run_time=0.4)

        self.at("08")
        later = mono("nothing left to fail later", 15, ICE).next_to(n0, DOWN, 0.12)
        self.play(FadeIn(later), run_time=0.4)

        # 08: a thousand requests (the real run)
        self.at("09")
        many = TL["many_taskgroup"]
        cnt = mono(f"{many['n']:,} requests · tasks still running: {many['alive']}", 18, ICE).move_to([0, -3.35, 0])
        self.play(FadeIn(cnt), run_time=0.4)

        # 09: the client gives up at 0.5 s (the real run): both cancelled
        self.at("10")
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (c, code)], run_time=0.4)
        run2 = "cancel_taskgroup"
        tl2 = Timeline(run2, y=-1.2)
        t_c = when(run2, "caller", "gave up")
        self.play(FadeIn(tl2), run_time=0.3)
        b1, b2 = tl2.bar("fetch_user", 0, t_c), tl2.bar("fetch_orders", 0, t_c)
        self.play(tl2.grow(b1, 1.0), tl2.grow(b2, 1.0))
        gv = tl2.vline(t_c, f"client gives up ({t_c:.2f} s)", color=AMBER)
        self.play(Create(gv[0]), FadeIn(gv[1]), Create(tl2.cut("fetch_user", t_c)), Create(tl2.cut("fetch_orders", t_c)), run_time=0.5)
        both = mono("both cancelled", 15, ICE).move_to([tl2.X(0.95), tl2.ys["fetch_user"], 0])
        self.play(FadeIn(both), run_time=0.3)

        # 10-13: the spec from chapter 3, ticked off, with the measured evidence
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        head = mono("a task group guarantees", 22, INK).move_to([0, 1.9, 0])
        rows = [spec_row(i, x=-5.6, y=0.9 - 0.95 * i) for i in range(3)]
        self.play(FadeIn(head), *[FadeIn(r) for r in rows], run_time=0.5)
        ev = [f"handler returned at {t_ret:.2f} s · tasks left: 0",
              f"fetch_user cancelled at {t_cut:.2f} s · ExceptionGroup: [ConnectionError]",
              f"both cancelled at {when('cancel_taskgroup', 'caller', 'gave up'):.2f} s"]
        for i, cue in enumerate(("12", "12", "13")):
            self.at(cue)
            e = mono(ev[i], 14, ICE).next_to(rows[i][1], DOWN, 0.1).align_to(rows[i][1], LEFT)
            self.play(Create(tick(rows[i][0])), rows[i][0].animate.set_stroke(ICE), FadeIn(e), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
