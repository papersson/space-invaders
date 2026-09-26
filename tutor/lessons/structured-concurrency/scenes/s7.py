import re
from skit import *

GO = re.search(r"bare goroutines: all (\d+) handlers returned after ([\d.]+)s; goroutines left over: (\d+); 1.2 s later: (\d+)\n"
               r"errgroup \+ context: all (\d+) handlers returned after ([\d.]+)s; goroutines left over: (\d+); 1.2 s later: (\d+)", RUNS)


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("Not just Python")
        n, _, bare_now, bare_later, _, _, grp_now, grp_later = GO.groups()
        # 01-03: the same handler in Go, with bare goroutines (the real run)
        self.at("01")
        self.play(FadeIn(c), run_time=0.3)
        self.at("02")
        bare = code_card([(0, "go func() { u, _ := fetchUser(context.Background()); users <- u }()", INK),
                          (0, "go func() { _, err := fetchOrders(context.Background()); errs <- err }()", INK),
                          (0, "select { case <-users: ...  case err := <-errs: return err }", INK)], 15,
                         title="Go, plain goroutines").move_to([0, 2.2, 0])
        self.play(FadeIn(bare), run_time=0.6)
        self.at("03")
        gr = Circle(radius=0.35, stroke_color=AMBER, stroke_width=2.5, fill_color=TRAY_FILL, fill_opacity=1).move_to([-3.0, 0.2, 0])
        grl = mono("goroutine", 13, AMBER).next_to(gr, DOWN, 0.1)
        ch = VGroup(Line([-2.3, 0.35, 0], [0.8, 0.35, 0], stroke_color=MUTED, stroke_width=2),
                    Line([-2.3, 0.05, 0], [0.8, 0.05, 0], stroke_color=MUTED, stroke_width=2))
        chl = mono("channel", 13, MUTED).next_to(ch, UP, 0.1)
        res = mono("user", 13, INK).move_to([-2.0, 0.2, 0])
        gone = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=2.3, height=0.9, stroke_color=FAINT, stroke_width=2).move_to([2.1, 0.2, 0]), num_dashes=36)
        gl = mono("handler:\nalready returned", 12, FAINT).move_to(gone)
        self.play(FadeIn(gr), FadeIn(grl), Create(ch), FadeIn(chl), FadeIn(res), Create(gone), FadeIn(gl), run_time=0.8)
        stuck = mono("waits forever", 14, AMBER).next_to(ch, DOWN, 0.15)
        self.play(FadeIn(stuck), run_time=0.3)
        cnt = mono(f"{int(n):,} requests · goroutines left over: {int(bare_now):,} · 1.2 s later: {int(bare_later):,}", 17, AMBER).move_to([0, -1.2, 0])
        self.play(FadeIn(cnt), run_time=0.4)

        self.at("04")
        nogrp = mono("Go: no task group in the language", 16, MUTED).move_to([0, -0.55, 0])
        self.play(FadeIn(nogrp), run_time=0.4)
        # 04-07: errgroup with a context (the real run)
        self.at("05")
        grp = code_card([(0, "g, ctx := errgroup.WithContext(context.Background())", INK),
                         (0, "g.Go(func() error { _, err := fetchUser(ctx); return err })", INK),
                         (0, "g.Go(func() error { _, err := fetchOrders(ctx); return err })", INK),
                         (0, "return g.Wait()", INK)], 15, title="Go, an error group with a context").move_to([0, -2.55, 0])
        self.play(FadeIn(grp), run_time=0.6)
        self.at("06")
        ctxl = mono("context: Go's standard way of passing cancellation (and deadlines) to goroutines", 13, MUTED).next_to(grp, UP, 0.35)
        self.play(FadeIn(ctxl), run_time=0.4)
        self.at("07")
        self.play(*[FadeOut(m) for m in (bare, gr, grl, ch, chl, res, gone, gl, stuck, nogrp, ctxl)], grp.animate.move_to([0, 2.1, 0]),
                  cnt.animate.move_to([0, -0.6, 0]), run_time=0.6)
        cnt2 = mono(f"{int(n):,} requests · goroutines left over: {int(grp_now)} · 1.2 s later: {int(grp_later)}", 17, ICE).move_to([0, -1.2, 0])
        self.play(FadeIn(cnt2), run_time=0.4)
        self.at("08")
        why = mono("first error cancels ctx · each goroutine checks ctx and returns", 15, MUTED).move_to([0, 0.3, 0])
        self.play(FadeIn(why), run_time=0.4)

        # 08-09: the same block elsewhere
        self.at("09")
        names = mono("Swift: task groups (built in) · Java: StructuredTaskScope (built in)", 16, INK).move_to([0, -2.5, 0])
        self.play(FadeIn(names), run_time=0.5)
        self.at("10")
        pv = mono("Java: still a preview · Kotlin: coroutineScope, in the kotlinx.coroutines library", 14, MUTED).next_to(names, DOWN, 0.15)
        self.play(FadeIn(pv), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
