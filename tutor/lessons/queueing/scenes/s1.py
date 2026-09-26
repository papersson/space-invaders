from qkit import *


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        # 01: a server that does 10 ms of work per request, requests queueing for it
        self.at("01")
        qv = QueueView(Q["trace"]["0.80"], server_x=3.2, y=-1.9, speed=40)
        work = mono("work: 10 ms per request, on average", 20, AMBER).next_to(qv.lab, DOWN, 0.3).align_to(qv.box, RIGHT)
        sim = mono("simulated server", 16, FAINT).to_corner(DL, buff=0.45)
        live = qv.mobject()
        self.play(FadeIn(qv.box), FadeIn(qv.lab), FadeIn(qv.qlab), FadeIn(work), FadeIn(sim), run_time=0.8)
        self.add(live)
        t_sim = 0.0
        rate = 1 / 40              # trace seconds per video second

        # 02: 80% busy -> 50 ms (the queue keeps running under the panel)
        def advance(until_t):
            nonlocal t_sim
            d = until_t - self.now()
            if d > 1 / 30:
                self.play(qv.tau.animate.set_value(t_sim + d * rate), run_time=d, rate_func=linear)
                t_sim += d * rate

        row_a = VGroup(mono("80 requests/s × 10 ms = 80% busy", 26, INK),
                       Arrow(ORIGIN, 1.0 * RIGHT, buff=0, color=MUTED, stroke_width=3),
                       mono("50 ms", 30, INK)).arrange(RIGHT, buff=0.3).move_to([-6.0, 2.3, 0], aligned_edge=LEFT)
        row_b = VGroup(mono("90 requests/s → 90% busy", 26, INK),
                       Arrow(ORIGIN, 1.0 * RIGHT, buff=0, color=MUTED, stroke_width=3),
                       mono("100 ms", 30, AMBER)).arrange(RIGHT, buff=0.3).move_to([-6.0, 1.0, 0], aligned_edge=LEFT)
        row_b[1].align_to(row_a[1], LEFT)
        row_b[2].next_to(row_b[1], RIGHT, 0.3)
        cap = mono("average response time, arrival to reply", 16, FAINT).next_to(row_a, UP, 0.3, aligned_edge=LEFT)
        advance(self.start_of("02"))
        self.play(FadeIn(cap), FadeIn(row_a[0]), qv.tau.animate.set_value(t_sim + 0.6 * rate), run_time=0.6, rate_func=linear)
        t_sim += 0.6 * rate
        advance(self.start_of("03"))
        self.play(GrowArrow(row_a[1]), FadeIn(row_a[2]), qv.tau.animate.set_value(t_sim + 0.8 * rate), run_time=0.8,
                  rate_func=linear)
        t_sim += 0.8 * rate

        # 04-05: an eighth more traffic: 90% busy -> 100 ms
        advance(self.start_of("04"))
        # switch the live queue to the 90% trace at the same point in simulated time
        self.remove(live)
        qv9 = QueueView(Q["trace"]["0.90"], server_x=3.2, y=-1.9, speed=40)
        qv9.tau.set_value(t_sim)
        live = qv9.mobject()
        self.add(live)
        qv = qv9
        more = mono("+12.5% traffic", 18, MUTED).next_to(row_b[0], DOWN, 0.12, aligned_edge=LEFT)
        self.play(FadeIn(row_b[0]), FadeIn(more), qv.tau.animate.set_value(t_sim + 0.7 * rate), run_time=0.7,
                  rate_func=linear)
        t_sim += 0.7 * rate
        advance(self.start_of("05"))
        self.play(GrowArrow(row_b[1]), FadeIn(row_b[2]), qv.tau.animate.set_value(t_sim + 0.8 * rate), run_time=0.8,
                  rate_func=linear)
        t_sim += 0.8 * rate

        # 07: the response time doubled
        advance(self.start_of("07"))
        dbl = mono("2× response time", 20, AMBER).next_to(row_b[2], DOWN, 0.12)
        self.play(FadeIn(dbl, shift=0.1 * LEFT), qv.tau.animate.set_value(t_sim + 0.6 * rate), run_time=0.6,
                  rate_func=linear)
        t_sim += 0.6 * rate

        # 09: 40 of the 50 ms at 80% are not work
        advance(self.start_of("09"))
        forty = mono("50 ms − 10 ms of work = 40 ms of what?", 22, ICE).next_to(more, DOWN, 0.35, aligned_edge=LEFT)
        self.play(Indicate(row_a[2], color=ICE), FadeIn(forty), qv.tau.animate.set_value(t_sim + 0.8 * rate),
                  run_time=0.8, rate_func=linear)
        t_sim += 0.8 * rate
        advance(self.end_of("09", 0.3))

        # title
        self.remove(live)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title = T("Why Busy Servers Get Slow", 64, INK, weight=SEMIBOLD)
        sub = T("queues, and the last ten percent", 28, MUTED)
        g = VGroup(title, sub).arrange(DOWN, buff=0.3)
        self.play(FadeIn(title, shift=0.15 * UP), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        self.until(self.dur - 0.45)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()
