from skit import *

RETRY = [(0, "async def fetch_user():", INK), (1, "for attempt in (1, 2):", INK), (2, "try:", INK),
         (3, "await asyncio.sleep(1.0)  # stands in for the user service", INK), (3, 'return "ada"', INK),
         (2, "except:  # a bare except: it catches CancelledError too", AMBER), (3, 'log("retrying")', INK)]


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("What it doesn't promise")
        # 01-03: cancellation is a request, delivered at an await
        self.at("01")
        ask = mono("cancel = a request to stop", 22, INK).move_to([0, 1.6, 0])
        self.play(FadeIn(c), FadeIn(ask), run_time=0.5)
        self.at("02")
        at = mono("delivered at the task's next await", 17, MUTED).next_to(ask, DOWN, 0.25)
        self.play(FadeIn(at), run_time=0.4)
        self.at("03")
        at2 = mono("as an exception: CancelledError", 17, MUTED).next_to(at, DOWN, 0.15)
        self.play(FadeIn(at2), run_time=0.4)
        self.at("04")
        keep = mono("never awaits, or catches it and carries on → keeps running", 17, AMBER).next_to(at2, DOWN, 0.25)
        self.play(FadeIn(keep), run_time=0.4)

        # 05-08: a retry loop with a bare except (the real run)
        self.at("05")
        self.play(FadeOut(ask), FadeOut(at), FadeOut(at2), FadeOut(keep), run_time=0.3)
        code = code_card(RETRY, 15, title="fetch_user, with a retry loop").move_to([0.8, 1.75, 0])
        self.play(FadeIn(code), run_time=0.5)
        run = "retrying"
        t_fail = when(run, "fetch_orders", "raises")
        t_caught = when(run, "fetch_user", "caught")
        t_done = when(run, "fetch_user", "finished")
        t_ret = when(run, "handler", "has returned")
        tl = Timeline(run, y=-1.35)
        self.at("06")
        self.play(FadeIn(tl), run_time=0.3)
        b1, ob = tl.bar("fetch_user", 0, t_caught), tl.bar("fetch_orders", 0, t_fail)
        self.play(tl.grow(b1, 0.6), tl.grow(ob, 0.6))
        self.play(FadeIn(tl.cross("fetch_orders", t_fail)), run_time=0.2)
        ca = mono("caught CancelledError, retrying", 14, INK).move_to([tl.X(t_caught) + 1.9, tl.ys["fetch_user"] + 0.4, 0])
        self.play(FadeIn(ca), run_time=0.4)
        tk = Arrow([tl.X(t_fail), tl.ys["fetch_orders"] + 0.2, 0], [tl.X(t_caught), tl.ys["fetch_user"] - 0.2, 0], buff=0,
                   color=ICE, stroke_width=3, tip_length=0.12)
        self.play(GrowArrow(tk), run_time=0.3)
        b2 = Rectangle(width=tl.X(t_done) - tl.X(t_caught), height=0.34, stroke_color=ICE, stroke_width=2.5, fill_opacity=0).move_to(
            [tl.X(t_caught), tl.ys["fetch_user"], 0], aligned_edge=LEFT)
        own = mono("still owned: the task group waits", 14, ICE).next_to(b2, DOWN, 0.1).align_to(b2, RIGHT)
        self.play(Create(b2), FadeIn(own), run_time=1.6)
        self.at("07")
        ret = tl.vline(t_ret, f"handler returns ({t_ret:.2f} s)")
        self.play(Create(ret[0]), FadeIn(ret[1]), run_time=0.5)
        self.at("08")
        cmp_ = mono(f"{t_ret:.2f} s instead of {when('taskgroup', 'handler', 'has returned'):.2f} s", 17, INK).move_to([0, -3.35, 0])
        self.play(FadeIn(cmp_), run_time=0.4)

        # 08-09: before it ran on; now the handler waits
        self.at("09")
        bf = VGroup(mono("before (gather, chapter 1): the work ran on after the handler returned", 16, MUTED),
                    mono("task group: the handler waits for it", 16, ICE)).arrange(DOWN, buff=0.1).move_to([0, -3.3, 0])
        self.play(FadeOut(cmp_), FadeIn(bf[0]), run_time=0.4)
        self.at("10")
        self.play(FadeIn(bf[1]), run_time=0.4)

        # 10-12: only tasks started through the group; lifetimes, not shared data
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        l1 = mono("covered: tasks started through the task group", 18, ICE).move_to([0, 1.0, 0])
        l1b = mono("not covered: a plain asyncio.create_task", 18, AMBER).next_to(l1, DOWN, 0.2)
        self.play(FadeIn(l1), run_time=0.4)
        self.at("12")
        self.play(FadeIn(l1b), run_time=0.4)
        self.at("13")
        l2 = mono("about lifetimes, not shared data", 18, INK).next_to(l1b, DOWN, 0.6)
        self.play(FadeIn(l2), run_time=0.4)
        self.at("14")
        l3 = mono("races and deadlocks are still possible", 16, MUTED).next_to(l2, DOWN, 0.15)
        self.play(FadeIn(l3), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
