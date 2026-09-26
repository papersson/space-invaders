from tkit import *

X0, X1, Y = -6.2, 6.2, -0.9


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("Why not fix the slow calls?")
        self.at("01")
        q = T("Why not find the slow 1% and fix it?", 30, INK).move_to([0, 2.7, 0])
        self.play(FadeIn(c), FadeIn(q), run_time=0.6)

        # 02-05: many brief causes along one server's timeline
        self.at("02")
        axis = Line([X0, Y, 0], [X1, Y, 0], stroke_color=FAINT, stroke_width=2)
        al = mono("one server, over a few seconds", 16, FAINT).next_to(axis, DOWN, 0.15).align_to(axis, LEFT)
        rng = np.random.default_rng(5)
        calls = VGroup()
        stalls = [(-3.9, 0.55, "queue after a burst", "03"), (-0.9, 0.7, "garbage collection pause", "04"),
                  (2.1, 0.5, "background job", "05"), (4.4, 0.45, "neighbour on the same machine", "05")]
        for k in range(46):
            x = X0 + 0.15 + k * 0.27
            hit = next((s for s in stalls if s[0] <= x <= s[0] + s[1]), None)
            h = 1.6 if hit else 0.18 + 0.05 * rng.random()
            calls.add(Line([x, Y, 0], [x, Y + h, 0], stroke_width=3, stroke_color=CORAL if hit else ICE))
        self.play(FadeIn(axis), FadeIn(al), LaggedStart(*[Create(l) for l in calls], lag_ratio=0.03), run_time=1.6)
        bands = {}
        for x, w, text, cue in stalls:
            band = Rectangle(width=w, height=2.2, stroke_width=0, fill_color=CORAL, fill_opacity=0.12)
            band.move_to([x + w / 2, Y + 1.1, 0])
            lab = mono(text, 16, CORAL).next_to(band, UP, 0.1 + 0.42 * (len(bands) % 2))
            bands[text] = (band, lab, cue)
        for i, (text, (band, lab, cue)) in enumerate(bands.items()):
            self.at(cue, 0.0 if i < 3 else 1.4)
            self.play(FadeIn(band), FadeIn(lab), run_time=0.5)

        # 06-07: short, random, never gone
        self.at("06")
        short = mono("each is brief, and hits whichever calls are running", 20, INK).move_to([0, -2.2, 0])
        self.play(FadeIn(short), run_time=0.5)
        self.at("07")
        rarer = mono("some causes can be removed; all of them, never", 20, MUTED).next_to(short, DOWN, 0.2)
        self.play(FadeIn(rarer), run_time=0.5)

        # 08: tolerate them
        self.at("08")
        tol = T("so: tolerate the tail, like failed machines", 28, ICE).move_to([0, -3.3, 0])
        self.play(FadeIn(tol), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
