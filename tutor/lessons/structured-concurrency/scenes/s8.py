from skit import *


class S8(CueScene):
    SEG = "s8"

    def construct(self):
        c = chip("The answer")
        g, t = "gather", "taskgroup"
        # 01-02: why it ran on
        self.at("01")
        tg = Timeline(g, y=1.6, gap=0.55, x0=-3.6)
        lg = mono("gather", 17, AMBER).move_to([-3.6, tg.ys["fetch_user"] + 0.55, 0], aligned_edge=LEFT)
        tg_fail, tg_ret, tg_user = when(g, "fetch_orders", "raises"), when(g, "handler", "has returned"), when(g, "fetch_user", "finished")
        bars = VGroup(tg.bar("fetch_user", 0, tg_ret, h=0.28), tg.bar("fetch_user", tg_ret, tg_user, color=AMBER, h=0.28),
                      tg.bar("fetch_orders", 0, tg_fail, h=0.28), tg.cross("fetch_orders", tg_fail))
        self.play(FadeIn(c), FadeIn(tg), FadeIn(bars), FadeIn(lg), run_time=0.7)
        self.at("02")
        own = mono("started, but not owned", 15, AMBER).next_to(bars[1], UP, 0.1).align_to(bars[1], RIGHT)
        self.play(FadeIn(own), run_time=0.4)

        # 03-05: a block that owns its tasks (the real run)
        self.at("03")
        tt = Timeline(t, y=-1.3, gap=0.55, x0=-3.6)
        lt = mono("task group", 17, ICE).move_to([-3.6, tt.ys["fetch_user"] + 0.55, 0], aligned_edge=LEFT)
        tt_fail, tt_cut = when(t, "fetch_orders", "raises"), when(t, "fetch_user", "cancelled")
        bars2 = VGroup(tt.bar("fetch_user", 0, tt_cut, h=0.28), tt.cut("fetch_user", tt_cut),
                       tt.bar("fetch_orders", 0, tt_fail, h=0.28), tt.cross("fetch_orders", tt_fail))
        self.play(FadeIn(tt), FadeIn(lt), FadeIn(bars2), run_time=0.7)
        self.at("04")
        e = mono("the others cancelled · the error comes back", 15, ICE).move_to([tt.X(0.8), tt.ys["fetch_user"] + 0.45, 0])
        self.play(FadeIn(e), run_time=0.4)
        self.at("05")
        e2 = mono("caller cancelled → its tasks too", 15, ICE).next_to(e, DOWN, 0.1)
        self.play(FadeIn(e2), run_time=0.4)

        # 06: 0.1 s, nothing left (the real counts)
        self.at("06")
        n1 = mono(f"still running: {TL['many_gather']['alive']:,}", 16, AMBER).move_to([tg.X(1.15), tg.ys["fetch_orders"] - 0.1, 0])
        n2 = mono(f"still running: {TL['many_taskgroup']['alive']}", 16, ICE).move_to([tt.X(1.15), tt.ys["fetch_orders"] - 0.1, 0])
        self.play(FadeIn(n1), FadeIn(n2), run_time=0.5)

        # 07: the takeaway
        self.at("07")
        tk = T("Give every task an owner, and “returned” means “done”.", 28, INK).to_edge(DOWN, buff=0.35)
        self.play(FadeIn(tk), run_time=0.6)

        # end card
        self.until(self.end_of("07", 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("Where Did That Task Go?", 40, INK, weight=SEMIBOLD).move_to([0, 2.5, 0])
        s1 = T("Start concurrent work inside a block that waits for it, cancels it when something fails,", 22, INK).next_to(name, DOWN, 0.5)
        s1b = T("and hands you its errors. Then a function that has returned is really done.", 22, INK).next_to(s1, DOWN, 0.12)
        refs = VGroup(T("Further reading", 17, MUTED, weight=MEDIUM),
                      T("Smith, \"Notes on structured concurrency, or: Go statement considered harmful\" (2018) · Sústrik, \"Structured Concurrency\" (2016)", 15, MUTED),
                      T("Dijkstra, \"Go To Statement Considered Harmful\", CACM (1968)", 15, MUTED),
                      T("Python documentation, \"Coroutines and Tasks\": Task Groups · JEP 505/533, JEP 543: Structured Concurrency", 15, MUTED),
                      T("Kotlin documentation, \"Composing suspending functions\" · SE-0304, Structured concurrency (Swift)", 15, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s1b, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(s1), FadeIn(s1b), run_time=0.7)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
