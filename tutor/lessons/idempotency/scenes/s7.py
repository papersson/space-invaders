from ikit import *


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("The answer")
        client = node("checkout page", -4.2, 1.6)
        server = node("payment server", 4.2, 1.6)
        card = Card([4.2, -1.0, 0])
        # 01: retry with the same key
        self.at("01")
        self.play(FadeIn(c), FadeIn(client), FadeIn(server), FadeIn(card), run_time=0.5)
        r1 = message(client.get_right() + 0.15 * UP, server.get_left() + 0.15 * UP, f"charge $50 · key {KEY}", size=14)
        self.play(GrowArrow(r1[0]), FadeIn(r1[1]), card.set_total(50), run_time=0.8)
        back = message(server.get_left() + 0.25 * DOWN, client.get_right() + 0.25 * DOWN, "receipt", color=INK,
                       lost_at=0.5, size=14)
        self.play(Create(back[0]), FadeIn(back[1]), FadeIn(back[2]), run_time=0.6)
        to = VGroup(mono("timeout →", 16, AMBER), mono("retry, same key", 16, AMBER)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        to.next_to(client, DOWN, 0.3).align_to(client, LEFT)
        self.play(FadeIn(to), run_time=0.4)
        r2 = message(client.get_right() + 0.9 * DOWN, server.get_left() + 0.9 * DOWN, f"retry · key {KEY}", size=14)
        self.play(GrowArrow(r2[0]), FadeIn(r2[1]), run_time=0.6)
        ok = message(server.get_left() + 1.3 * DOWN, client.get_right() + 1.3 * DOWN, "receipt #1042", color=INK,
                     size=14)
        self.play(GrowArrow(ok[0]), FadeIn(ok[1]), run_time=0.6)
        once = mono("charged once", 20, ICE).next_to(card, DOWN, 0.2)
        self.play(FadeIn(once), run_time=0.4)

        # 02-03: at-least-once delivery + idempotent handling = exactly-once effect
        self.at("02")
        eq = M('at-least-once delivery + idempotent handling = <span foreground="#8FD3FF">charged exactly once</span>',
               26, INK).to_edge(DOWN, buff=0.8)
        no = mono("the network can't deliver exactly once", 18, MUTED).next_to(eq, UP, 0.25)
        self.play(FadeIn(no), run_time=0.5)
        self.at("03")
        self.play(FadeIn(eq), run_time=0.7)

        # 04: effectively-once processing
        self.at("04")
        eff = mono("\"effectively once\": exactly-once effect, not exactly-once delivery", 18, ICE).next_to(eq, DOWN, 0.25)
        self.play(FadeIn(eff), run_time=0.6)

        # end card
        self.until(self.end_of("04", 0.7))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("Charged Twice", 40, INK, weight=SEMIBOLD).move_to([0, 2.4, 0])
        s1 = T("Retry after a timeout, with the same idempotency key.", 26, INK).next_to(name, DOWN, 0.5)
        s2 = T("The server charges once per key, and returns the saved result to repeats.", 22, MUTED).next_to(s1, DOWN, 0.2)
        refs = VGroup(T("Further reading", 18, MUTED, weight=MEDIUM),
                      T("Kleppmann, Designing Data-Intensive Applications (2017), ch. 8 and 11", 18, MUTED),
                      T("Stripe API reference: Idempotent requests · RFC 9110 §9.2.2 (idempotent methods)", 18, MUTED),
                      T("Helland, \"Idempotence Is Not a Medical Condition\", ACM Queue (2012)", 18, MUTED),
                      T("The Two Generals Problem (Akkoyunlu, Ekanadham & Huber, 1975; Gray, 1978)", 18, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s2, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(s1), run_time=0.6)
        self.play(FadeIn(s2), run_time=0.4)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
