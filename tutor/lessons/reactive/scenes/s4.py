from rkit import *
import json

P = json.loads((DATA / "propagate.json").read_text())


def chain(k, x0=-5.6, dx=3.2, y=0.6, r=0.2):
    """k diamonds in a row: returns (group, list of the diamond ends)."""
    g, ends = VGroup(), []
    src = Dot([x0, y, 0], radius=r, color=INK)
    g.add(src)
    prev = src
    for i in range(k):
        cx = x0 + (i + 0.5) * dx
        a = Dot([cx, y + 0.8, 0], radius=r * 0.8, color=MUTED)
        b = Dot([cx, y - 0.8, 0], radius=r * 0.8, color=MUTED)
        d = Dot([x0 + (i + 1) * dx, y, 0], radius=r, color=INK)
        for p, q in ((prev, a), (prev, b), (a, d), (b, d)):
            g.add(Line(p.get_center(), q.get_center(), stroke_color=FAINT, stroke_width=2).set_z_index(-1))
        g.add(a, b, d)
        ends.append(d)
        prev = d
    return g, ends


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("Diamonds multiply")
        self.at("01")
        g, ends = chain(3)
        self.play(FadeIn(c), Create(g), run_time=1.2)

        # 02-04: each diamond doubles the runs after it
        self.at("02")
        runs = [2, 4, 8]
        labels = VGroup()
        for d, k in zip(ends, runs):
            labels.add(mono(f"runs {k}×", 20, AMBER if k < 8 else CORAL).next_to(d, DOWN, 0.95))
        self.play(FadeIn(labels[0]), Indicate(ends[0], color=AMBER), run_time=0.7)
        self.at("03")
        self.play(FadeIn(labels[1]), Indicate(ends[1], color=AMBER), run_time=0.7)
        self.at("04")
        self.play(FadeIn(labels[2]), Indicate(ends[2], color=CORAL), run_time=0.7)

        # 05-06: ten diamonds: 1,024
        self.at("05")
        rows = [(s["diamonds"], s["last_naive"]) for s in P["stacked"] if s["diamonds"] in (1, 2, 3, 10)]
        tbl = VGroup()
        for i, (k, v) in enumerate(rows):
            y = -1.75 - 0.42 * i
            tbl.add(VGroup(mono(f"{k} diamond{'s' if k > 1 else ''}", 20, MUTED).move_to([-5.6, y, 0], aligned_edge=LEFT),
                           mono(f"last value runs {v:,}×", 20, CORAL if k == 10 else INK).move_to([-2.6, y, 0], aligned_edge=LEFT)))
        self.play(FadeIn(tbl[:3]), run_time=0.5)
        self.play(FadeIn(tbl[3]), run_time=0.5)

        # 07: in the right order, once each
        self.at("07")
        once = mono("in the right order: 1× each", 22, GREEN).move_to([4.0, -2.4, 0])
        self.play(FadeIn(once), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
