from skit import *


class S8(CueScene):
    SEG = "s8"

    def construct(self):
        c = chip("The answer")
        g, t = "gather", "taskgroup"
        mg, mt = TL["many_gather"], TL["many_taskgroup"]
        # 01-02: why it ran on (chapter 1's run)
        self.at("01")
        tg = Timeline(g, y=2.15, gap=0.55, x0=-3.6)
        lg = mono("gather (ch. 1)", 17, INK).move_to([-3.6, tg.ys["fetch_user"] + 0.5, 0], aligned_edge=LEFT)
        tg_fail, tg_ret, tg_user = when(g, "fetch_orders", "raises"), when(g, "handler", "has returned"), when(g, "fetch_user", "finished")
        bars = VGroup(tg.bar("fetch_user", 0, tg_ret, h=0.28), tg.bar("fetch_user", tg_ret, tg_user, color=AMBER, h=0.28),
                      tg.bar("fetch_orders", 0, tg_fail, h=0.28), tg.cross("fetch_orders", tg_fail))
        self.play(FadeIn(c), FadeIn(tg), FadeIn(bars), FadeIn(lg), run_time=0.7)
        self.at("02")
        own = mono("started, but not owned", 15, AMBER).next_to(bars[1], UP, 0.1).align_to(bars[1], RIGHT)
        self.play(FadeIn(own), run_time=0.4)

        # 03-05: a block that owns its tasks (chapter 5's run)
        self.at("03")
        tt = Timeline(t, y=-0.8, gap=0.55, x0=-3.6)
        lt = mono("task group (ch. 5)", 17, INK).move_to([-5.9, tt.ys["fetch_user"] + 0.5, 0], aligned_edge=LEFT)
        tt_fail, tt_cut, tt_ret = when(t, "fetch_orders", "raises"), when(t, "fetch_user", "cancelled"), when(t, "handler", "has returned")
        bars2 = VGroup(tt.bar("fetch_user", 0, tt_cut, h=0.28), tt.cut("fetch_user", tt_cut),
                       tt.bar("fetch_orders", 0, tt_fail, h=0.28), tt.cross("fetch_orders", tt_fail))
        self.play(FadeIn(tt), FadeIn(lt), FadeIn(bars2), run_time=0.7)
        top, bot = tt.ys["fetch_user"] + 0.3, tt.ys["fetch_orders"] - 0.3
        blk = RoundedRectangle(corner_radius=0.06, width=tt.X(tt_ret) - tt.X(0) + 0.3, height=top - bot, stroke_color=ICE, stroke_width=2.5)
        blk.move_to([(tt.X(0) + tt.X(tt_ret)) / 2, (top + bot) / 2, 0])
        bl = mono(f"the block: ends at {tt_ret:.2f} s, with its tasks", 15, ICE).next_to(blk, RIGHT, 0.35).shift(0.12 * UP)
        self.play(Create(blk), FadeIn(bl), run_time=0.6)
        self.at("04")
        e = mono("one fails → the others cancelled · the error comes back", 15, ICE).move_to([0, -2.45, 0])
        self.play(FadeIn(e), run_time=0.4)
        self.at("05")
        e2 = mono(f"caller cancelled → its tasks too (ch. 5: both cancelled at {when('cancel_taskgroup', 'caller', 'gave up'):.2f} s)", 15, ICE)
        e2.next_to(e, DOWN, 0.14)
        self.play(FadeIn(e2), run_time=0.4)

        # 06: when every handler had returned, what was still running (the real counts), below each chart
        self.at("06")
        n1 = mono(f"{mg['n']:,} requests: when all handlers had returned ({mg['returned_after']:.2f} s), still running: {mg['alive']:,}", 15, AMBER)
        n1.move_to([0, tg.axis_y - 0.72, 0])
        n2 = mono(f"{mt['n']:,} requests: when all handlers had returned ({mt['returned_after']:.2f} s), still running: {mt['alive']}", 15, ICE)
        n2.next_to(e2, DOWN, 0.14)
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.5)

        # 07: the takeaway
        self.at("07")
        tk = T("Give every task an owner, and “returned” means “done”.", 26, INK).to_edge(DOWN, buff=0.3)
        self.play(FadeIn(tk), run_time=0.6)

        # end card
        self.until(self.end_of("07", 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("Where Did That Task Go?", 40, INK, weight=SEMIBOLD).move_to([0, 2.5, 0])
        s1 = T("Start concurrent work inside a block that waits for it, cancels it when something fails,", 22, INK).next_to(name, DOWN, 0.5)
        s1b = T("and hands you its errors. Then a function that has returned is really done.", 22, INK).next_to(s1, DOWN, 0.12)
        refs = VGroup(T("Further reading", 17, MUTED, weight=MEDIUM),
                      T("Smith, \"Notes on structured concurrency, or: Go statement considered harmful\" (2018) · Sústrik, \"Structured Concurrency\" (2016)", 15, MUTED),
                      T("Dijkstra, \"Go To Statement Considered Harmful\" (title by the editor, Niklaus Wirth), CACM (1968)", 15, MUTED),
                      T("Python documentation, \"Coroutines and Tasks\": Task Groups · JEP 533 (seventh preview, JDK 27), JEP 543 (candidate): Structured Concurrency", 15, MUTED),
                      T("Kotlin documentation, \"Composing suspending functions\" · SE-0304, Structured concurrency (Swift)", 15, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s1b, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(s1), FadeIn(s1b), run_time=0.7)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
