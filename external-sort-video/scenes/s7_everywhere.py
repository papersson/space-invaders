from common import *


def mini_run(n_cols, width, height=0.22, seed=0, sorted_=True):
    """A small horizontal gradient bar standing for a sorted run (or noise)."""
    rng = np.random.default_rng(seed)
    vals = np.sort(rng.random(n_cols)) if sorted_ else rng.random(n_cols)
    w = width / n_cols
    return VGroup(*[Rectangle(width=w * 1.02, height=height, fill_color=vcolor(v), fill_opacity=1,
                              stroke_width=0).move_to([i * w, 0, 0]) for i, v in enumerate(vals)])


def box(w, h, title=None, edge=DIM, fill=PANEL, size=20):
    r = RoundedRectangle(corner_radius=0.12, width=w, height=h, stroke_color=edge, stroke_width=2,
                         fill_color=fill, fill_opacity=1)
    if title:
        t = label(title, size, MUTED).next_to(r.get_top(), DOWN, 0.12)
        return VGroup(r, t)
    return VGroup(r)


def postgres_lines():
    """Run 3 from captures/postgres_explain.txt: the default work_mem, serial plan."""
    txt = (CAPTURES / "postgres_explain.txt").read_text().splitlines()
    i = next(k for k, l in enumerate(txt) if l.startswith("--- RUN 3"))
    block = txt[i + 1:]
    j = next(k for k, l in enumerate(block) if l.startswith("EXPLAIN"))
    plan = []
    for l in block[j + 3:]:
        if l.startswith("("):
            break
        plan.append(l.rstrip())
    return block[j].strip(), [l for l in plan if l.strip()]


class S7Everywhere(CueScene):
    SEG = "s7"

    def construct(self):
        # l1
        self.at("l1")
        title = T("You've seen this before", 48, INK, weight=SEMIBOLD)
        self.play(FadeIn(title, shift=0.1 * UP), run_time=0.7)
        c = chip("You've seen this before")
        self.at("l1", 1.7)
        self.play(ReplacementTransform(title, c), run_time=0.5)

        # l2: Postgres, real output
        self.at("l2")
        sql, plan = postgres_lines()
        term = box(12.8, 4.3, fill="#0B0F13")
        term.move_to([0, 0.1, 0])
        lines = [("postgres=# SET work_mem = '4MB';   -- the default", MUTED),
                 ("postgres=# SET max_parallel_workers_per_gather = 0;", MUTED),
                 (f"postgres=# {sql}", INK), ("", MUTED)] + [(l, MUTED) for l in plan]
        cw = Text("M" * 20, font=MONO, font_size=19).width / 20
        txt = VGroup(*[Text(l.strip() if l.strip() else ".", font=MONO, font_size=19, color=col)
                       for l, col in lines])
        txt.arrange(DOWN, buff=0.13, aligned_edge=LEFT).move_to(term).align_to(term, LEFT).shift(0.35 * RIGHT)
        for t, (l, _) in zip(txt, lines):
            t.shift(RIGHT * cw * (len(l) - len(l.lstrip())))
            if not l.strip():
                t.set_opacity(0)
        hl_i = next(k for k, (l, _) in enumerate(lines) if "Sort Method" in l)
        cap = T("PostgreSQL 16 · 1,000,000 rows · real output", 20, FAINT, font=MONO).next_to(term, DOWN, 0.2)
        self.play(FadeIn(term), FadeIn(cap), run_time=0.5)
        self.play(LaggedStart(*[FadeIn(t) for t in txt], lag_ratio=0.12), run_time=1.8)
        self.at("l2", 3.6)
        hl = txt[hl_i]
        band = SurroundingRectangle(hl, buff=0.07, color=AMBER, stroke_width=2.5, corner_radius=0.06)
        self.play(hl.animate.set_color(AMBER), Create(band), run_time=0.6)
        pg = Group(term, txt, cap, band)

        # l3: shuffles
        self.at("l3")
        self.play(FadeOut(pg), run_time=0.4)
        maps = VGroup(*[box(3.2, 1.3, "map") for _ in range(3)]).arrange(RIGHT, buff=0.9).move_to([0, 1.55, 0])
        spills = VGroup()
        for i, m in enumerate(maps):
            runs = VGroup(*[mini_run(24, 2.4, seed=10 * i + k) for k in range(2)]).arrange(DOWN, buff=0.1)
            spills.add(runs.move_to(m[0]).shift(0.18 * DOWN))
        reds = VGroup(*[box(4.2, 1.2, "reduce: merge") for _ in range(2)]).arrange(RIGHT, buff=1.4)
        reds.move_to([0, -1.55, 0])
        outs = VGroup(*[mini_run(40, 3.4, seed=99 + k).move_to(r[0]).shift(0.18 * DOWN) for k, r in enumerate(reds)])
        arrows = VGroup(*[Arrow(m.get_bottom(), r.get_top(), buff=0.1, stroke_width=2, color=FAINT,
                                max_tip_length_to_length_ratio=0.08) for m in maps for r in reds])
        cap3 = T("MapReduce, Spark: spill sorted runs, then merge them", 22, MUTED).move_to([0, -3.0, 0])
        self.play(FadeIn(maps), run_time=0.4)
        self.play(LaggedStart(*[FadeIn(s, shift=0.1 * DOWN) for s in spills], lag_ratio=0.3), run_time=0.9)
        self.play(FadeIn(reds), GrowFromCenter(arrows), FadeIn(cap3), run_time=0.7)
        self.play(LaggedStart(*[FadeIn(o) for o in outs], lag_ratio=0.3), run_time=0.7)
        shuffle = VGroup(maps, spills, reds, outs, arrows, cap3)

        # l4: LSM trees
        self.at("l4")
        self.play(FadeOut(shuffle), run_time=0.4)
        mem = box(4.0, 1.0, "memtable (memory)", edge=TRAY_EDGE, fill=TRAY_FILL).move_to([-3.6, 2.0, 0])
        memrun = mini_run(20, 3.0, seed=5).move_to(mem[0]).shift(0.15 * DOWN)
        l0 = VGroup(*[mini_run(18, 1.9, seed=20 + k) for k in range(4)]).arrange(RIGHT, buff=0.35)
        l0.move_to([0.6, 0.0, 0])
        l0lab = T("L0", 20, MUTED, font=MONO).next_to(l0, LEFT, 0.3)
        l0cap = T("sorted files, flushed from memory", 20, MUTED, font=MONO).next_to(l0, UP, 0.15)
        l0cap.align_to(l0, RIGHT)
        l1 = mini_run(80, 10.0, seed=77).move_to([0, -2.0, 0])
        l1lab = T("L1", 20, MUTED, font=MONO).next_to(l1, LEFT, 0.3)
        flush = Arrow(mem.get_bottom(), l0[0].get_top(), buff=0.1, color=AMBER, stroke_width=3)
        flab = T("flush", 20, AMBER, font=MONO).next_to(flush, LEFT, 0.1)
        comp = VGroup(*[Arrow(r.get_bottom(), l1.get_top() + (r.get_x() * 0.4) * RIGHT, buff=0.1, color=ICE,
                              stroke_width=2.5, max_tip_length_to_length_ratio=0.1) for r in l0])
        clab = T("compaction:\na k-way merge", 22, ICE, font=MONO).move_to([-4.9, -1.0, 0])
        cap4 = T("LSM-tree storage engines: RocksDB, LevelDB, Cassandra", 22, MUTED).move_to([0, -3.0, 0])
        self.play(FadeIn(mem), FadeIn(memrun), FadeIn(cap4), run_time=0.5)
        self.play(GrowArrow(flush), FadeIn(flab), LaggedStart(*[FadeIn(r) for r in l0], lag_ratio=0.3),
                  FadeIn(l0lab), FadeIn(l0cap), run_time=1.2)
        self.play(*[GrowArrow(a) for a in comp], FadeIn(clab), FadeIn(l1), FadeIn(l1lab), run_time=1.1)
        lsm = VGroup(mem, memrun, l0, l0lab, l0cap, l1, l1lab, flush, flab, comp, clab, cap4)

        # l5: B-trees
        self.at("l5")
        self.play(FadeOut(lsm), run_time=0.4)
        counter = Counter(0)

        def node(w=1.8, hot=False):
            r = RoundedRectangle(corner_radius=0.08, width=w, height=0.42, stroke_color=ICE if hot else DIM,
                                 stroke_width=3 if hot else 1.6, fill_color=PANEL, fill_opacity=1)
            keys = VGroup(*[Line(UP * 0.13, DOWN * 0.13, stroke_color=FAINT, stroke_width=1.5)
                            .move_to(r.get_left() + RIGHT * (0.2 + k * (w - 0.4) / 6)) for k in range(7)])
            return VGroup(r, keys)
        root = node(2.4).move_to([0, 2.1, 0])
        lvl2 = VGroup(*[node(1.5) for _ in range(5)]).arrange(RIGHT, buff=0.5).move_to([0, 0.5, 0])
        lvl3 = VGroup(*[node(0.9) for _ in range(11)]).arrange(RIGHT, buff=0.22).move_to([0, -1.1, 0])
        dots2 = T("…", 30, FAINT).next_to(lvl2, RIGHT, 0.2)
        dots3 = T("…", 30, FAINT).next_to(lvl3, RIGHT, 0.2)
        edges = VGroup(*[Line(root.get_bottom(), n.get_top(), stroke_color=DIM, stroke_width=1.2) for n in lvl2])
        edges.add(*[Line(lvl2[2].get_bottom(), n.get_top(), stroke_color=DIM, stroke_width=1.2) for n in lvl3[3:8]])
        cap5 = M('~500 children per node: 500³ ≈ 125 million, 500⁴ ≈ 62 billion keys', 22, MUTED,
                 font=MONO).move_to([0, -2.9, 0])
        self.play(FadeIn(root), FadeIn(counter), run_time=0.4)
        self.play(FadeIn(lvl2), FadeIn(dots2), Create(edges[:5]), run_time=0.6)
        self.play(FadeIn(lvl3), FadeIn(dots3), Create(edges[5:]), FadeIn(cap5), run_time=0.6)
        path = [root, lvl2[2], lvl3[5]]
        self.at("l5", 3.3)
        for n in path:
            ring = SurroundingRectangle(n[0], buff=0.05, color=ICE, stroke_width=3, corner_radius=0.1)
            self.play(Create(ring), counter.to(counter.value() + 1), run_time=0.5)
            self.add(ring)
        three = M('a billion keys: <span foreground="#F2A93B">3–4 trips</span>', 28, INK, font=MONO)
        three.next_to(lvl3, DOWN, 0.35)
        self.play(FadeIn(three), run_time=0.5)
        btree = [m for m in self.mobjects if m is not c]

        # l6: the hierarchy
        self.at("l6")
        self.play(*[FadeOut(m) for m in btree], run_time=0.4)
        levels = ["registers", "CPU cache", "RAM", "SSD", "hard disk"]
        rows = VGroup()
        for i, name in enumerate(levels):
            w = 3.0 + 1.6 * i
            r = Rectangle(width=w, height=0.62, stroke_color=DIM, stroke_width=1.6, fill_color=PANEL,
                          fill_opacity=1).move_to([-0.6, 2.2 - i * 0.78, 0])
            rows.add(VGroup(r, T(name, 24, INK).move_to(r)))
        faster = T("smaller, faster", 18, FAINT, font=MONO).next_to(rows[0], LEFT, 0.4)
        bigger = T("bigger, slower", 18, FAINT, font=MONO).next_to(rows[4], DOWN, 0.15)

        def tag(text, row, color):
            t = VGroup(Arrow(RIGHT, LEFT, buff=0, color=color, stroke_width=3, max_tip_length_to_length_ratio=0.3)
                       .scale(0.45), T(text, 24, color, slant=ITALIC)).arrange(RIGHT, buff=0.15)
            return t.next_to(rows[row], RIGHT, 0.25)
        desk_t = tag("the desk", 2, INK)
        ware_t = tag("the warehouse", 3, MUTED)
        self.play(FadeIn(rows), FadeIn(faster), FadeIn(bigger), run_time=0.7)
        self.play(FadeIn(desk_t), FadeIn(ware_t), run_time=0.5)
        self.at("l6", 3.0)
        self.play(desk_t.animate.next_to(rows[1], RIGHT, 0.25), ware_t.animate.next_to(rows[2], RIGHT, 0.25),
                  run_time=0.8)
        self.at("l6", 5.4)
        gpu = M('and on a GPU: <span foreground="#E6EBF0">GPU memory</span> is the desk, host RAM the warehouse',
                22, MUTED).move_to([0, -2.95, 0])
        self.play(FadeIn(gpu, shift=0.1 * UP), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
