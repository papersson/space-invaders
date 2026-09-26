from ikit import *


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        client = node("checkout page", -4.2, 1.0)
        server = node("payment server", 4.2, 1.0)
        card = Card([4.2, -1.6, 0])
        # 01: the request
        self.at("01")
        self.play(FadeIn(client), FadeIn(server), FadeIn(card), run_time=0.6)
        req = message(client.get_right(), server.get_left(), "charge $50")
        self.play(GrowArrow(req[0]), FadeIn(req[1]), run_time=0.9)

        # 02-03: silence, then a timeout
        self.at("02")
        clock = ValueTracker(0.0)
        cl = always_redraw(lambda: mono(f"waiting {clock.get_value():.1f} s", 20, MUTED).next_to(client, DOWN, 0.35))
        self.add(cl)
        span = max(self.start_of("03", 1.5) - self.now(), 1.5)
        self.play(clock.animate.set_value(5.0), run_time=span, rate_func=linear)
        cl.clear_updaters()
        to = mono("timeout", 24, CORAL).next_to(cl, DOWN, 0.2)
        self.play(FadeIn(to), run_time=0.4)

        # 04-06: did it happen? retry: maybe twice; give up: maybe lost
        self.at("04")
        q = mono("charged? 0 times? 1? 2?", 22, ICE).next_to(card, UP, 0.25)
        self.play(FadeIn(q), run_time=0.5)
        self.at("05")
        twice = mono("retry, if it did → pays twice", 20, CORAL).move_to([-2.0, -1.6, 0])
        self.play(FadeIn(twice), run_time=0.5)
        self.at("06")
        lost = mono("give up, if it didn't → sale lost", 20, CORAL).next_to(twice, DOWN, 0.25)
        self.play(FadeIn(lost), run_time=0.5)

        # 07: what should the client do?
        self.at("07")
        ask = T("What should the client do?", 34, ICE).to_edge(DOWN, buff=0.5)
        self.play(FadeIn(ask, shift=0.1 * UP), run_time=0.6)
        self.until(self.end_of("07", 0.6))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        title = T("Charged Twice", 64, INK, weight=SEMIBOLD)
        sub = T("retries, and why they need idempotency", 28, MUTED)
        g = VGroup(title, sub).arrange(DOWN, buff=0.3)
        self.play(FadeIn(title, shift=0.15 * UP), run_time=0.8)
        self.play(FadeIn(sub), run_time=0.5)
        self.until(self.dur - 0.45)
        self.play(FadeOut(g), run_time=0.4)
        self.finish()
