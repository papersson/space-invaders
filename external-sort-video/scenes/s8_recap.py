from common import *
from s4_runs import STRIP, strip_images


def mini_strip(values, w=4.2, h=0.36):
    _, strip = strip_images(values, strip_h=8)
    im = ImageMobject(strip).stretch_to_fit_width(w).stretch_to_fit_height(h)
    im.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return im


class S8Recap(CueScene):
    SEG = "s8"

    def construct(self):
        c = chip("Recap")
        ys = [2.1, 0.55, -1.0]
        rules = [M('Count <span foreground="#F2A93B">trips</span>, not operations.', 34, INK, weight=MEDIUM),
                 M('Stream through data; don\'t hop around it.', 34, INK, weight=MEDIUM),
                 M('Runs as big as memory, then merge as many as memory allows.', 30, INK, weight=MEDIUM)]
        for r, y in zip(rules, ys):
            r.move_to([-6.4, y, 0], aligned_edge=LEFT)

        # l1
        self.at("l1")
        trips = Counter(4096, anchor=[6.4, ys[0] + 0.3, 0])
        self.play(FadeIn(c), FadeIn(rules[0], shift=0.1 * RIGHT), FadeIn(trips), run_time=0.7)

        # l2: the two access patterns, small
        self.at("l2")
        pats = Group()
        for key in ("heapsort", "mergesort"):
            im = ImageMobject(str(DATA / f"race_{key}.png")).stretch_to_fit_width(1.7).stretch_to_fit_height(0.55)
            fr = Rectangle(width=1.75, height=0.6, stroke_color=DIM, stroke_width=1.2).move_to(im)
            pats.add(Group(im, fr))
        pats.arrange(RIGHT, buff=0.25).move_to([4.95, ys[1] - 0.05, 0])
        cross = Line(pats[0].get_corner(DL), pats[0].get_corner(UR), stroke_color=INK, stroke_width=3)
        self.play(FadeIn(rules[1], shift=0.1 * RIGHT), FadeIn(pats), run_time=0.6)
        self.play(Create(cross), run_time=0.4)

        # l3: noise -> sawtooth -> sorted
        self.at("l3")
        st = STRIP["states"]
        strips = Group(*[mini_strip(v, w=4.0) for v in (st[0], st[STRIP["runs"]], st[-1])])
        strips.arrange(DOWN, buff=0.12).next_to(rules[2], DOWN, buff=0.35).align_to(rules[2], LEFT)
        names = VGroup(*[T(n, 18, MUTED, font=MONO).next_to(s, RIGHT, 0.25)
                         for n, s in zip(("the file", "phase 1: runs", "phase 2: merged"), strips)])
        self.play(FadeIn(rules[2], shift=0.1 * RIGHT), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(Group(s, n)) for s, n in zip(strips, names)], lag_ratio=0.5),
                  run_time=1.8)

        # l4: the formula, then the end card
        self.at("l4")
        f = M('passes = 1 + ⌈log<sub><span foreground="#8FD3FF">M/B</span></sub>(N/M)⌉ = '
              '<span foreground="#8FD3FF">2</span>, up to ~¼ PB on 16 GB of memory', 22, INK, font=MONO)
        f.move_to([0, -3.1, 0])
        self.play(FadeIn(f, shift=0.1 * UP), run_time=0.7)
        self.at("l4", 5.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        title = T("Bigger Than Memory", 64, INK, weight=SEMIBOLD)
        sub = T("external merge sort, and the I/O model behind it", 28, MUTED)
        refs = VGroup(
            T("A. Aggarwal and J. S. Vitter, The input/output complexity of sorting and related problems, CACM 31(9), 1988",
              17, FAINT),
            T("D. E. Knuth, The Art of Computer Programming, Vol. 3, §5.4: External sorting", 17, FAINT),
            T("Real runs: GNU sort 9.4, PostgreSQL 16 · simulation: iosim.py (LRU cache, block transfers)", 17, FAINT),
        ).arrange(DOWN, buff=0.12)
        card = VGroup(title, sub).arrange(DOWN, buff=0.3).move_to([0, 0.6, 0])
        refs.move_to([0, -2.4, 0])
        self.play(FadeIn(card, shift=0.1 * UP), run_time=0.9)
        self.play(FadeIn(refs), run_time=0.6)
        self.until(self.dur - 0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.55)
        self.finish()
