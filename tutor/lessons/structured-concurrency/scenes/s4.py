from skit import *

TG = [(0, "async with asyncio.TaskGroup() as tg:", INK), (1, "tg.create_task(fetch_user())", INK),
      (1, "tg.create_task(fetch_orders())", INK), (0, "# here, both tasks have finished", MUTED)]


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("Go to, again")
        xs = [-5.2, -1.75, 1.75, 5.2]
        # 01-04: goto and structured programming
        self.at("01")
        self.play(FadeIn(c), run_time=0.3)
        self.at("02")
        g1 = flow("goto", c=(xs[1], 0.8), w=1.9, h=2.2)
        l1 = mono("go to", 16, MUTED).next_to(g1[0], DOWN, 0.75)
        d = mono("Dijkstra, 1968", 15, MUTED).next_to(l1, DOWN, 0.08)
        self.play(FadeIn(g1[0]), FadeIn(l1), FadeIn(d), run_time=0.5)
        self.play(Create(g1[1]), Create(g1[2]), run_time=0.7)
        self.at("03")
        self.play(FadeIn(g1[3]), run_time=0.4)
        self.at("04")
        g0 = flow("sequential", c=(xs[0], 0.8), w=1.9, h=2.2)
        l0 = mono("structured", 16, MUTED).next_to(g0[0], DOWN, 0.75)
        self.play(FadeIn(g0[0]), FadeIn(l0), run_time=0.4)
        self.play(GrowArrow(g0[1]), run_time=0.6)

        # 05-07: starting a task is the same kind of jump
        self.at("05")
        g2 = flow("spawn", c=(xs[2], 0.8), w=1.9, h=2.2)
        l2 = mono("start a task", 16, MUTED).next_to(g2[0], DOWN, 0.75)
        s = mono("Smith, 2018", 15, MUTED).next_to(l2, DOWN, 0.08)
        self.play(FadeIn(g2[0]), FadeIn(l2), FadeIn(s), Create(g2[1]), GrowArrow(g2[2]), FadeIn(g2[4]), run_time=0.7)
        self.at("06")
        self.play(Create(g2[3]), run_time=0.7)
        self.at("07")
        title = VGroup(mono("“Notes on structured concurrency,", 15, INK), mono("or: Go statement considered harmful”", 15, INK))
        title.arrange(DOWN, buff=0.06).move_to([0, -2.7, 0])
        self.play(FadeIn(title), run_time=0.5)

        # 08-10: the fix is a block: box, inner block; split inside; rejoin before the bottom
        # flow("block") parts: 0 box, 1 inner block, 2 line in, 3 and 4 the two paths, 5 arrow out, 6 split dot, 7 join dot
        self.at("08")
        g3 = flow("block", c=(xs[3], 0.8), w=1.9, h=2.2)
        l3 = mono("block (task group)", 16, ICE).next_to(g3[0], DOWN, 0.75)
        self.play(FadeOut(title), FadeIn(g3[0]), FadeIn(l3), run_time=0.4)
        self.play(Create(g3[1]), run_time=0.5)
        self.at("09")
        self.play(Create(g3[2]), FadeIn(g3[6]), run_time=0.4)
        self.play(Create(g3[3]), Create(g3[4]), run_time=0.8)
        self.at("10")
        self.play(FadeIn(g3[7]), run_time=0.3)
        self.play(GrowArrow(g3[5]), run_time=0.5)

        # 11-12: the name, and asyncio's task group
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        nm = T("structured concurrency", 34, INK).move_to([0, 2.4, 0])
        rule = mono("a task can't outlive the block that started it", 17, ICE).next_to(nm, DOWN, 0.2)
        self.play(FadeIn(nm), FadeIn(rule), run_time=0.6)
        self.at("12")
        code = code_card(TG, 17).move_to([0, 0.1, 0])
        br = Brace(VGroup(code[1][0], code[1][2]), LEFT, buff=0.15, color=ICE)
        bl = mono("tasks can't\noutlive this block", 16, ICE).next_to(br, LEFT, 0.12)
        self.play(FadeIn(code), run_time=0.5)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.5)
        names = mono("Dijkstra 1968 · Sústrik 2016 · Smith 2018 · asyncio.TaskGroup: Python 3.11",
                     15, INK).move_to([0, -2.3, 0])
        self.play(FadeIn(names), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
