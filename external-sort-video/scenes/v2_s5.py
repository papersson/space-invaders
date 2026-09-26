from v2kit import *
from s7_everywhere import box, mini_run, postgres_lines

MEM_GB, BLOCK_MB = 16, 1
FAN = MEM_GB * 1000 // BLOCK_MB          # about 16,000 blocks of 1 MB in 16 GB (decimal units)


def slot_row(n, width, y, h=0.5):
    w = (width - (n - 1) * 0.1) / n
    return VGroup(*[RoundedRectangle(corner_radius=0.05, width=w, height=h, stroke_color=FAINT, stroke_width=1.5,
                                     fill_color=TRAY_FILL, fill_opacity=1) for _ in range(n)]).arrange(RIGHT, buff=0.1)\
        .move_to([0, y, 0])


def many_runs_strip(n_runs, width, height=0.34, cols=600, seed=0):
    """Many sorted runs side by side, drawn as an image (each run a thin dark-to-light gradient)."""
    import seaborn as sns
    cmap = sns.color_palette("mako", as_cmap=True)
    per = max(cols // n_runs, 1)
    rng = np.random.default_rng(seed)
    vals = np.concatenate([np.sort(rng.random(per)) for _ in range(max(cols // per, 1))])[:cols]
    rgb = (np.array(cmap(0.22 + 0.74 * vals))[:, :3] * 255).astype(np.uint8)
    img = ImageMobject(np.repeat(rgb[None], 8, axis=0)).stretch_to_fit_width(width).stretch_to_fit_height(height)
    img.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    return img


class V2S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("How far it goes")
        # 01-02: GNU sort merges at most sixteen at once; twelve fit
        self.at("01")
        head = M('GNU sort: at most <span foreground="#8FD3FF">16</span> runs per merge, by default', 30, INK)
        head.move_to([0, 2.5, 0])
        slots = slot_row(16, 12.0, 1.0)
        fill = VGroup(*[mini_run(12, s.width - 0.12, 0.3, seed=40 + i).move_to(s) for i, s in enumerate(slots[:12])])
        b12 = Brace(slots[:12], DOWN, buff=0.1, color=ICE)
        l12 = mono("sort's 12 runs", 20, ICE).next_to(b12, DOWN, 0.08)
        b4 = Brace(slots[12:], DOWN, buff=0.1, color=FAINT)
        l4 = mono("4 to spare", 20, FAINT).next_to(b4, DOWN, 0.08)
        self.play(FadeIn(c), FadeIn(head), run_time=0.6)
        self.play(LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.05), run_time=0.8)
        self.at("01", 3.0)
        self.play(LaggedStart(*[FadeIn(f) for f in fill], lag_ratio=0.08), FadeIn(b12), FadeIn(l12), run_time=1.0)
        self.at("01", 5.2)
        caut = mono("a cautious default: less memory, at some cost in speed", 20, MUTED).move_to([0, -1.2, 0])
        self.play(FadeIn(caut), run_time=0.5)
        self.at("02")
        self.play(FadeIn(b4), FadeIn(l4), run_time=0.5)
        ok = T("12 ≤ 16: one merge", 26, INK).move_to([0, -2.3, 0])
        self.play(FadeIn(ok), run_time=0.4)

        # 03-04: the limit: one run per block of memory, less one for the output
        self.at("03")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        q = T("How many runs could one merge take?", 34, INK).move_to([0, 2.6, 0])
        self.play(FadeIn(q), run_time=0.5)
        tray = RoundedRectangle(corner_radius=0.14, width=12.2, height=1.0, stroke_color=TRAY_EDGE, stroke_width=2.5,
                                fill_color=TRAY_FILL, fill_opacity=1).move_to([0, 1.0, 0])
        tl = label("memory", 20, INK).next_to(tray, UP, 0.12, aligned_edge=LEFT)
        blocks10 = slot_row(10, 11.6, 1.0, h=0.62)
        self.play(FadeIn(tray), FadeIn(tl), FadeIn(blocks10), run_time=0.6)
        self.at("04")
        runs9 = VGroup(*[mini_run(10, b.width - 0.14, 0.3, seed=70 + i).move_to(b) for i, b in enumerate(blocks10[:9])])
        outb = blocks10[9].copy().set_stroke(AMBER, 3)
        lab_r = mono("one block per run", 20, ICE).next_to(blocks10[:9], DOWN, 0.2)
        lab_o = mono("output", 20, AMBER).next_to(blocks10[9], DOWN, 0.2)
        self.play(LaggedStart(*[FadeIn(r) for r in runs9], lag_ratio=0.1), FadeIn(lab_r), run_time=1.0)
        self.play(Create(outb), FadeIn(lab_o), run_time=0.5)
        rule = M('runs per merge = <span foreground="#8FD3FF">blocks of memory − 1</span>', 28, INK,
                 font=MONO).move_to([0, -0.9, 0])
        self.play(FadeIn(rule), run_time=0.5)

        # 05: real blocks are about a megabyte; a laptop's memory holds about sixteen thousand
        self.at("05")
        ours = mono(f"our simulation: blocks of {RACE['B']} items", 20, MUTED).move_to([0, -2.0, 0])
        real = mono("real sorting programs: often 1 MB per block, to cut down on fetches", 20, INK)
        real.next_to(ours, DOWN, 0.2)
        self.play(FadeIn(ours), run_time=0.4)
        self.play(FadeIn(real), run_time=0.5)
        self.at("05", 5.2)
        self.play(FadeOut(VGroup(runs9, outb, lab_r, lab_o, rule, ours, real, blocks10, q)), run_time=0.5)
        tl2 = label(f"memory · {MEM_GB} GB", 20, INK).move_to(tl, aligned_edge=LEFT)
        n = 200
        thin = VGroup(*[Line([tray.get_left()[0] + 0.1 + (12.0 * (k + 0.5) / n), 0.62, 0],
                             [tray.get_left()[0] + 0.1 + (12.0 * (k + 0.5) / n), 1.38, 0],
                             stroke_color=ICE, stroke_width=1.0, stroke_opacity=0.5) for k in range(n)])
        big = Counter(9, title="RUNS PER MERGE", size=52, anchor=[6.6, 3.35, 0], color=ICE)
        rng = np.random.default_rng(3)
        lines = VGroup()
        for k in range(260):
            x = -6.9 + 13.8 * k / 259
            end = np.array([tray.get_left()[0] + 0.1 + 12.0 * k / 259, 0.5, 0])
            lines.add(Line([x, -3.1, 0], end, stroke_width=1.1, stroke_color=vcolor(rng.random()), stroke_opacity=0.5))
        disk = label("runs on disk", 20, MUTED).move_to([0, -3.45, 0])
        calc = M(f'{MEM_GB} GB ÷ {BLOCK_MB} MB ≈ <span foreground="#8FD3FF">16,000 blocks</span>', 26, INK, font=MONO)
        calc.move_to([-2.6, 2.7, 0])
        self.play(ReplacementTransform(tl, tl2), FadeIn(thin, lag_ratio=0.01), FadeIn(big), FadeIn(calc), run_time=1.2)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.01), big.to(FAN - 1, rate_func=rush_into),
                  FadeIn(disk), run_time=3.0)
        about = mono("about 16,000 runs in one merge", 22, ICE).next_to(big, DOWN, 0.15).align_to(big, RIGHT)
        self.play(FadeIn(about), run_time=0.4)

        # 06-10: more runs than that: more merge passes
        self.at("06")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        more = T("more runs than one merge can take: more than one merge pass", 26, INK).move_to([0, 2.6, 0])
        self.play(FadeIn(more), run_time=0.5)
        self.at("07")
        xs = [-4.6, 0.0, 4.7]
        y = 0.5
        s0 = many_runs_strip(100_000, 3.4, seed=1).move_to([xs[0], y, 0])
        l0 = mono("100,000 runs", 24, INK).next_to(s0, DOWN, 0.25)
        self.play(FadeIn(s0), FadeIn(l0), run_time=0.6)
        self.at("08")
        s1 = VGroup(*[mini_run(30, 0.34, 0.34, seed=200 + i) for i in range(7)]).arrange(RIGHT, buff=0.06).move_to([xs[1], y, 0])
        l1 = mono("7 runs", 24, INK).next_to(s1, DOWN, 0.25)
        a1 = Arrow([xs[0] + 1.8, y, 0], [xs[1] - 1.45, y, 0], buff=0.05, color=ICE, stroke_width=3)
        t1 = mono("16,000 per merge", 18, ICE).next_to(a1, UP, 0.12)
        p1 = mono("merge pass", 16, FAINT).next_to(a1, DOWN, 0.12)
        self.play(GrowArrow(a1), FadeIn(t1), FadeIn(p1), run_time=0.6)
        self.play(FadeIn(s1), FadeIn(l1), run_time=0.5)
        ceil = mono("100,000 ÷ 16,000 = 6.25 → 7", 16, FAINT).next_to(l1, DOWN, 0.15)
        self.play(FadeIn(ceil), run_time=0.4)
        self.at("09")
        s2 = mini_run(120, 3.2, 0.34, seed=300).move_to([xs[2], y, 0])
        l2 = mono("1 file", 24, INK).next_to(s2, DOWN, 0.25)
        a2 = Arrow([xs[1] + 1.45, y, 0], [xs[2] - 1.65, y, 0], buff=0.05, color=ICE, stroke_width=3)
        p2 = mono("merge pass", 16, FAINT).next_to(a2, DOWN, 0.12)
        self.play(GrowArrow(a2), FadeIn(p2), run_time=0.5)
        self.play(FadeIn(s2), FadeIn(l2), run_time=0.5)
        self.at("10")
        grow = VGroup(mono("1 merge pass: up to 16,000 runs", 22, MUTED),
                      M('2 merge passes: up to 16,000 × 16,000 = <span foreground="#8FD3FF">256 million runs</span>',
                        22, MUTED, font=MONO)).arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([0, -2.0, 0])
        self.play(FadeIn(grow[0]), run_time=0.5)
        self.at("10", 2.2)
        self.play(FadeIn(grow[1]), run_time=0.5)

        # 11: two or three passes in practice
        self.at("11")
        prac = M('in practice: <span foreground="#E6EBF0">2 or 3 passes</span> in all, even for enormous files',
                 24, MUTED).move_to([0, -3.3, 0])
        self.play(FadeIn(prac, shift=0.1 * UP), run_time=0.6)

        # 12-13: PostgreSQL reports an external merge
        self.at("12")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        sql, plan = postgres_lines()
        term = box(12.8, 4.1, fill="#0B0F13").move_to([0, 0.2, 0])
        lines = [("postgres=# SET work_mem = '4MB';   -- the default", MUTED),
                 ("postgres=# SET max_parallel_workers_per_gather = 0;", MUTED),
                 (f"postgres=# {sql}", INK), ("", MUTED)] + [(l, MUTED) for l in plan]
        cw = Text("M" * 20, font=MONO, font_size=76).scale(0.25).width / 20
        txt = VGroup(*[Text(l.strip() if l.strip() else ".", font=MONO, font_size=76, color=col).scale(0.25)
                       for l, col in lines])
        txt.arrange(DOWN, buff=0.13, aligned_edge=LEFT).move_to(term).align_to(term, LEFT).shift(0.35 * RIGHT)
        for t, (l, _) in zip(txt, lines):
            t.shift(RIGHT * cw * (len(l) - len(l.lstrip())))
            if not l.strip():
                t.set_opacity(0)
        hl_i = next(k for k, (l, _) in enumerate(lines) if "Sort Method" in l)
        cap = mono("PostgreSQL 16 · a 1,000,000-row table (128 MB) · real output", 18, FAINT).next_to(term, DOWN, 0.2)
        self.play(FadeIn(term), FadeIn(cap), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in txt], lag_ratio=0.12), run_time=1.8)
        self.at("13", 4.5)
        hl = txt[hl_i]
        band = SurroundingRectangle(hl, buff=0.07, color=AMBER, stroke_width=2.5, corner_radius=0.06)
        others = VGroup(*[t for k, (t, (l, _)) in enumerate(zip(txt, lines)) if k != hl_i and l.strip()])
        self.play(hl.animate.set_color(AMBER), Create(band), others.animate.set_opacity(0.35), run_time=0.7)
        gloss = mono("= sorted runs on disk, then merges", 18, AMBER).next_to(band, RIGHT, 0.25)
        self.play(FadeIn(gloss), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
