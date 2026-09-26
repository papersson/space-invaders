from qkit import *

UNIT = 0.1          # scene units per millisecond
X0 = -4.4


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("Waiting, not working")
        ys = {80: 1.0, 90: -0.7}
        waits = {80: 40, 90: 90}
        names = {r: mono(f"{r}% busy", 24, INK).move_to([X0 - 0.3, y, 0], aligned_edge=RIGHT) for r, y in ys.items()}
        totals = {r: Rectangle(width=(waits[r] + S_MS) * UNIT, height=0.5, stroke_width=0, fill_color=ICE,
                               fill_opacity=0.35).move_to([X0, y, 0], aligned_edge=LEFT) for r, y in ys.items()}
        tot_lab = {r: mono(f"{waits[r] + 10:.0f} ms", 22, INK).next_to(totals[r], RIGHT, 0.2) for r in ys}

        # 01: response time = working + waiting
        self.at("01")
        self.play(FadeIn(c), *[FadeIn(names[r]) for r in ys], *[GrowFromEdge(totals[r], LEFT) for r in ys],
                  *[FadeIn(tot_lab[r]) for r in ys], run_time=0.9)
        bars = {r: response_bar(waits[r], ys[r], unit=UNIT, x0=X0, h=0.5) for r in ys}
        legend = VGroup(
            VGroup(Square(0.22, stroke_width=0, fill_color=WAIT, fill_opacity=0.9), mono("waiting for the server", 18, MUTED)).arrange(RIGHT, buff=0.15),
            VGroup(Square(0.22, stroke_width=0, fill_color=AMBER, fill_opacity=0.95), mono("work", 18, MUTED)).arrange(RIGHT, buff=0.15),
        ).arrange(RIGHT, buff=0.6).move_to([X0, 2.4, 0], aligned_edge=LEFT)
        self.at("01", 2.5)
        self.play(*[ReplacementTransform(totals[r], bars[r]) for r in ys], FadeIn(legend), run_time=1.0)

        # 02: the work is 10 ms either way
        self.at("02")
        works = VGroup(*[bars[r][1] for r in ys])
        wl = VGroup(*[mono("10", 16, BG).move_to(bars[r][1]) for r in ys])
        self.play(Indicate(works, color=AMBER, scale_factor=1.08), FadeIn(wl), run_time=0.9)

        # 03-04: the rest is waiting: 40 ms at 80%, 90 ms at 90%
        self.at("03", 1.0)
        w80 = mono("waiting 40 ms: 4× the work", 20, INK).move_to(bars[80][0])
        self.play(FadeIn(w80), run_time=0.5)
        self.at("04")
        w90 = mono("waiting 90 ms", 20, INK).move_to(bars[90][0])
        self.play(FadeIn(w90), run_time=0.5)

        # 05-06: it's about queues
        self.at("05")
        q = T("Why do queues get so long, when the server still has time to spare?", 26, ICE).move_to([0, -2.4, 0])
        self.play(*[Indicate(bars[r][0], color=MUTED, scale_factor=1.04) for r in ys], run_time=0.8)
        self.at("06")
        self.play(FadeIn(q, shift=0.1 * UP), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
