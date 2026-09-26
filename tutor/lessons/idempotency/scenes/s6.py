from ikit import *


def step(text, x, y, color=INK, w=2.5):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=0.6, stroke_color=color, stroke_width=2,
                         fill_color=PANEL, fill_opacity=1).move_to([x, y, 0])
    return VGroup(r, mono(text, 16, color).move_to(r))


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("Where it can still go wrong")
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)

        # 02: a crash between the charge and the saved result
        self.at("02")
        h1 = mono("1. a crash between charging and saving", 22, INK).move_to([-2.2, 2.8, 0])
        a = step("charge card", -4.4, 1.8)
        crash = lost_mark(np.array([-2.5, 1.8, 0]))
        b = step("save key → result", -0.6, 1.8, FAINT)
        retry = step("retry: no record", 3.0, 1.8, CORAL)
        again = mono("charged again", 18, CORAL).next_to(retry, DOWN, 0.15)
        self.play(FadeIn(h1), FadeIn(a), run_time=0.5)
        self.play(FadeIn(crash), FadeIn(b), run_time=0.5)
        self.play(FadeIn(retry), FadeIn(again), run_time=0.6)

        # 03: one database transaction: both saved or neither
        self.at("03")
        both = VGroup(step("charge", -3.3, 0.5, INK, 1.8), step("save result", -1.3, 0.5, INK, 1.8))
        tx = SurroundingRectangle(both, buff=0.15, color=ICE, stroke_width=3, corner_radius=0.12)
        txl = mono("one transaction: both saved, or neither", 16, ICE).next_to(tx, RIGHT, 0.3)
        self.play(FadeIn(both), Create(tx), FadeIn(txl), run_time=0.8)

        # 04-05: calling the card network: the server sends its own key
        self.at("04")
        srv = step("payment server", -3.3, -0.8, INK, 2.6)
        net = step("card network", 2.6, -0.8, INK, 2.4)
        call = message(srv.get_right(), net.get_left(), "charge $50", size=14)
        self.play(FadeIn(srv), FadeIn(net), GrowArrow(call[0]), FadeIn(call[1]), run_time=0.8)
        self.at("05")
        own = mono("+ its own idempotency key", 16, AMBER).next_to(call, DOWN, 0.12)
        self.play(FadeIn(own), run_time=0.5)

        # 06-08: two attempts at once: check and mark in one step
        self.at("06")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        h2 = mono("2. a retry arrives while the first attempt is running", 22, INK).move_to([-0.6, 2.8, 0])
        t = Line([-5.5, 0.9, 0], [5.5, 0.9, 0], stroke_color=FAINT, stroke_width=1.5)
        tl = mono("time →", 14, FAINT).next_to(t, DOWN, 0.05).align_to(t, RIGHT)
        first = step("attempt 1: running", -2.6, 1.7, ICE, 4.6)
        self.play(FadeIn(h2), FadeIn(t), FadeIn(tl), FadeIn(first), run_time=0.6)
        self.at("07")
        mark = mono(f"key {KEY}: in progress (checked and marked in one step)", 16, AMBER).move_to([-1.0, 0.4, 0])
        self.play(FadeIn(mark), run_time=0.6)
        self.at("08")
        second = step("attempt 2 (same key)", 2.4, 1.7, INK, 2.8)
        away = mono("→ \"still in progress, try again\"", 16, CORAL).next_to(second, DOWN, 0.55)
        self.play(FadeIn(second), run_time=0.4)
        self.play(FadeIn(away), run_time=0.4)

        # 09-10: a key belongs to one payment
        self.at("09")
        h3 = mono("3. a key belongs to one payment", 22, INK).move_to([-2.4, -0.7, 0])
        p1 = mono(f"key {KEY} · $50 → receipt #1042", 18, INK).move_to([-1.2, -1.5, 0])
        self.play(FadeIn(h3), FadeIn(p1), run_time=0.6)
        self.at("10")
        p2 = mono(f"key {KEY} · $80 → rejected: key reused with a different request", 18, CORAL)
        p2.next_to(p1, DOWN, 0.2, aligned_edge=LEFT)
        self.play(FadeIn(p2), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
