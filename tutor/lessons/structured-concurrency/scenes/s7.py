import re
from skit import *

GO = re.search(r"bare goroutines: all (\d+) handlers returned after ([\d.]+)s; goroutines left over: (\d+); 1.2 s later: (\d+)\n"
               r"errgroup \+ context: all (\d+) handlers returned after ([\d.]+)s; goroutines left over: (\d+); 1.2 s later: (\d+)", RUNS)


def count_row(label, now, later, color):
    """One labelled row of the Go leak counts: 'bare goroutines:   1,000 left over · 1.2 s later: 1,000'."""
    return VGroup(mono(label, 17, color), mono(f"{int(now):,} left over · 1.2 s later: {int(later):,}", 17, color))


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("Not just Python")
        n, _, bare_now, bare_later, _, _, grp_now, grp_later = GO.groups()
        # 01-02: the same handler in Go, with bare goroutines (the real run)
        self.at("01")
        self.play(FadeIn(c), run_time=0.3)
        self.at("02")
        bare = code_card([(0, "go func() { u, _ := fetchUser(context.Background()); users <- u }()", INK),
                          (0, "go func() { _, err := fetchOrders(context.Background()); errs <- err }()", INK),
                          (0, "select { case <-users: ...  case err := <-errs: return err }", INK)], 15,
                         title="Go, plain goroutines").move_to([0, 2.3, 0])
        gloss = mono("goroutine: Go's lightweight thread", 14, MUTED).next_to(bare, DOWN, 0.12).align_to(bare, RIGHT)
        self.play(FadeIn(bare), FadeIn(gloss), run_time=0.6)

        # 03: one leaked goroutine, then the counts
        self.at("03")
        gr = Circle(radius=0.35, stroke_color=AMBER, stroke_width=2.5, fill_color=TRAY_FILL, fill_opacity=1).move_to([-3.0, 0.1, 0])
        grl = mono("goroutine", 14, AMBER).next_to(gr, DOWN, 0.1)
        ch = VGroup(Line([-2.3, 0.25, 0], [0.8, 0.25, 0], stroke_color=MUTED, stroke_width=2),
                    Line([-2.3, -0.05, 0], [0.8, -0.05, 0], stroke_color=MUTED, stroke_width=2))
        chl = mono("channel", 14, MUTED).next_to(ch, UP, 0.1)
        res = mono("user", 14, INK).move_to([-2.0, 0.1, 0])
        gone = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=2.5, height=0.95, stroke_color=MUTED, stroke_width=2).move_to([2.2, 0.1, 0]), num_dashes=36)
        gl = VGroup(mono("handler:", 15, INK), mono("already returned", 15, INK)).arrange(DOWN, buff=0.08).move_to(gone)
        self.play(FadeIn(gr), FadeIn(grl), Create(ch), FadeIn(chl), FadeIn(res), Create(gone), FadeIn(gl), run_time=0.8)
        stuck = mono("waits forever", 15, AMBER).next_to(ch, DOWN, 0.15)
        self.play(FadeIn(stuck), run_time=0.3)
        head = mono(f"after {int(n):,} requests", 15, MUTED)
        r1 = count_row("bare goroutines:", bare_now, bare_later, AMBER)
        r2 = count_row("errgroup + context:", grp_now, grp_later, ICE)
        lab_w = max(r1[0].width, r2[0].width) + 0.3
        for r in (r1, r2):
            r[1].next_to(r[0], RIGHT, 0).align_to(r[0], LEFT).shift(lab_w * RIGHT)
        r1.move_to([0, -1.55, 0])
        r2.move_to([0, -1.55, 0]).align_to(r1, LEFT)
        head.next_to(r1, UP, 0.15).align_to(r1, LEFT)
        self.play(FadeIn(head), FadeIn(r1), run_time=0.4)

        # 04-05: no task group in the language; the error group replaces the picture
        self.at("04")
        nogrp = mono("Go has no task group in the language", 16, MUTED).move_to([0, -2.7, 0])
        self.play(FadeIn(nogrp), run_time=0.4)
        self.at("05")
        grp = code_card([(0, "g, ctx := errgroup.WithContext(context.Background())", INK),
                         (0, "g.Go(func() error { _, err := fetchUser(ctx); return err })", INK),
                         (0, "g.Go(func() error { _, err := fetchOrders(ctx); return err })", INK),
                         (0, "return g.Wait()", INK)], 15, title="Go, an error group (golang.org/x/sync) with a context").move_to([0, 2.2, 0])
        self.play(*[FadeOut(m) for m in (bare, gloss, gr, grl, ch, chl, res, gone, gl, stuck, nogrp)], run_time=0.4)
        self.play(FadeIn(grp), VGroup(head, r1).animate.shift(0.75 * UP), run_time=0.6)
        r2.shift(0.75 * UP + 0.5 * DOWN)

        # 06: what a context is (under the card, not under a picture)
        self.at("06")
        ctxl = mono("context: Go's standard way of passing cancellation (and deadlines) to goroutines", 14, MUTED).next_to(grp, DOWN, 0.15)
        self.play(FadeIn(ctxl), run_time=0.4)

        # 07-09: none left, and why (the real run)
        self.at("07")
        self.play(FadeIn(r2), run_time=0.4)
        self.at("08")
        why = mono("the first error cancels ctx · each goroutine checks ctx and returns", 16, INK).move_to([0, -2.0, 0])
        self.play(FadeIn(why), run_time=0.4)
        self.at("09")
        ask = mono("like a task group, it can only ask", 16, MUTED).next_to(why, DOWN, 0.15)
        self.play(FadeIn(ask), run_time=0.4)

        # 10-11: the same block elsewhere
        self.at("10")
        names = mono("built in: Swift task groups · Java StructuredTaskScope (preview)", 16, INK).move_to([0, -3.1, 0])
        self.play(FadeIn(names), run_time=0.5)
        self.at("11")
        pv = mono("Kotlin: coroutineScope, in the kotlinx.coroutines library", 16, MUTED).next_to(names, DOWN, 0.15)
        self.play(FadeIn(pv), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
