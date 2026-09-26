from v2kit import *

ARR_Y = -1.3            # the array on disk
MEM_Y = 1.3             # memory (four block frames)
NB = 12                 # blocks shown for the array
CPB = 6                 # cells per block in this diagram


def array_on_disk(y=ARR_Y, seed=4):
    rng = np.random.default_rng(seed)
    w = 0.12
    blocks = VGroup()
    for b in range(NB):
        cells = VGroup(*[Rectangle(width=w, height=0.34, stroke_width=0, fill_color=vcolor(rng.random()),
                                   fill_opacity=1) for _ in range(CPB)]).arrange(RIGHT, buff=0.02)
        frame = SurroundingRectangle(cells, buff=0.05, color=DIM, stroke_width=1.4, corner_radius=0.04)
        blocks.add(VGroup(frame, cells))
    blocks.arrange(RIGHT, buff=0.1).move_to([0, y, 0])
    return blocks


def memory_frames(n=4, y=MEM_Y, like=None):
    w = like.width if like is not None else 1.2
    h = like.height if like is not None else 0.44
    frames = VGroup(*[RoundedRectangle(corner_radius=0.06, width=w + 0.12, height=h + 0.12, stroke_color=TRAY_EDGE,
                                       stroke_width=2, fill_color=TRAY_FILL, fill_opacity=1) for _ in range(n)])
    frames.arrange(RIGHT, buff=0.25).move_to([0, y, 0])
    return frames


class V2S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("Why the obvious fix fails")
        # 01: virtual memory: the OS keeps recently used blocks in memory, fetches the rest
        self.at("01")
        arr = array_on_disk()
        mem = memory_frames(like=arr[0])
        dl = label("disk: the array", 18, MUTED).next_to(arr, DOWN, 0.2, aligned_edge=LEFT)
        ml = label("memory", 18, INK).next_to(mem, UP, 0.15, aligned_edge=LEFT)
        os_l = T("the operating system moves blocks in and out as the program touches them", 20, MUTED).move_to([0, 0.1, 0])
        self.play(FadeIn(c), FadeIn(arr), FadeIn(dl), run_time=0.8)
        self.play(FadeIn(mem), FadeIn(ml), run_time=0.6)
        self.play(FadeIn(os_l), run_time=0.5)
        in_mem = []
        for k, b in enumerate((1, 7, 3, 10, 5)):
            slot_i = k % 4
            cp = arr[b].copy()
            if len(in_mem) == 4:
                old = in_mem.pop(0)
                self.play(FadeOut(old), run_time=0.25)
            self.play(cp.animate.move_to(mem[slot_i]), arr[b].animate.set_opacity(0.35), run_time=0.7)
            in_mem.append(cp)
            self.wait(0.35)

        # 02-03: a disk never fetches one number: a whole block, and every fetch is slow
        self.at("02")
        self.play(FadeOut(VGroup(*in_mem)), FadeOut(os_l), arr.animate.set_opacity(1), run_time=0.4)
        want = arr[8][1][2]
        ask = VGroup(Arrow(want.get_top() + 1.1 * UP, want.get_top(), buff=0.05, color=ICE, stroke_width=3),
                     T("the program wants one number", 20, ICE)).arrange(UP, buff=0.1).next_to(want, UP, 0.02)
        self.play(FadeIn(ask), Indicate(want, color=ICE, scale_factor=1.6), run_time=0.9)
        self.at("03")
        mover = arr[8].copy()
        fr = SurroundingRectangle(mover, buff=0.04, color=AMBER, stroke_width=3, corner_radius=0.05)
        self.play(FadeOut(ask), run_time=0.2)
        self.play(VGroup(mover, fr).animate.move_to(mem[0]), run_time=1.1)
        whole = T("the disk sends the whole block: thousands of bytes at least", 22, INK).move_to([0, 0.15, 0])
        slow = T("every fetch: hundreds to thousands of times a memory read", 22, AMBER).next_to(whole, DOWN, 0.2)
        self.play(FadeIn(whole), run_time=0.5)
        self.at("03", 4.2)
        self.play(FadeIn(slow), run_time=0.5)

        # 04-05: that's an I/O; the count of them is the cost
        self.at("04")
        counter = Counter(0, title="I/Os")
        self.play(FadeIn(counter), FadeOut(whole), run_time=0.4)
        self.play(counter.to(1), Indicate(fr, color=AMBER), run_time=0.8)
        self.at("05")
        rule = T("once data doesn't fit in memory, the I/O count typically dominates the running time", 24, INK)
        rule.move_to([0, 0.15, 0])
        self.play(FadeOut(slow), FadeIn(rule), run_time=0.5)

        # 06-07: two N log N sorts
        self.at("06")
        self.play(FadeOut(VGroup(arr, mem, dl, ml, mover, fr, rule)), FadeOut(counter), run_time=0.5)
        hs = VGroup(T("heapsort", 40, INK, weight=MEDIUM), T("N log N comparisons", 24, MUTED, font=MONO)).arrange(DOWN, buff=0.15)
        ms = VGroup(T("merge sort", 40, INK, weight=MEDIUM), T("N log N comparisons", 24, MUTED, font=MONO)).arrange(DOWN, buff=0.15)
        names = VGroup(hs, ms).arrange(RIGHT, buff=3.0).move_to([0, 1.6, 0])
        self.play(FadeIn(names, shift=0.1 * UP), run_time=0.7)
        self.at("07")
        cmp_note = T("by comparisons alone: heapsort at most about 2× slower", 22, MUTED).next_to(names, DOWN, 0.45)
        self.play(FadeIn(cmp_note), run_time=0.5)

        # 08-09: heapsort touches far-apart positions: blocks that aren't in memory
        self.at("08")
        arr2 = array_on_disk(y=-1.6, seed=9)
        mem2 = memory_frames(like=arr2[0], y=-0.25).scale(0.8)
        ml2 = label("memory", 16, INK).next_to(mem2, LEFT, 0.25)
        self.play(FadeOut(cmp_note), FadeIn(arr2), FadeIn(mem2), FadeIn(ml2), hs.animate.set_color(INK),
                  ms.animate.set_opacity(0.3), run_time=0.6)
        cells = [cell for blk in arr2 for cell in blk[1]]
        path = [0, 1, 4, 9, 20, 41]          # heap positions i, 2i+1, ... on a heap of 72 cells
        counter2 = Counter(0, title="I/Os")
        self.play(FadeIn(counter2), run_time=0.3)
        prev = None
        loaded = []
        self.at("09")
        for k, idx in enumerate(path):
            cell = cells[idx]
            ring = SurroundingRectangle(cell, buff=0.03, color=ICE, stroke_width=3)
            anims = [Create(ring)]
            if prev is not None:
                anims.append(Create(CurvedArrow(prev.get_top(), cell.get_top(), angle=-TAU / 5, color=ICE,
                                                stroke_width=2, tip_length=0.12)))
            blk = idx // CPB
            if blk not in loaded:
                cp = arr2[blk].copy()
                f2 = SurroundingRectangle(cp, buff=0.04, color=AMBER, stroke_width=3, corner_radius=0.05)
                self.add(cp, f2)
                anims += [VGroup(cp, f2).animate.move_to(mem2[len(loaded) % 4]).scale(0.8),
                          counter2.to(counter2.value() + 1)]
                loaded.append(blk)
            self.play(*anims, run_time=0.9)
            prev = cell
        far = T("each step down the heap jumps twice as far: soon every step needs a block that isn't in memory",
                20, AMBER).move_to([0, 0.55, 0])
        self.play(FadeIn(far), run_time=0.4)

        # 10: merge sort streams: every block it fetches is used completely
        self.at("10")
        self.play(*[FadeOut(m) for m in self.mobjects if m not in (c, names)], ms.animate.set_opacity(1),
                  hs.animate.set_opacity(0.3), run_time=0.5)
        arr3 = array_on_disk(y=-1.6, seed=11)
        cur = Triangle(color=ICE, fill_opacity=1).scale(0.1).rotate(PI).next_to(arr3[0], UP, 0.05)
        counter3 = Counter(0, title="I/Os")
        self.play(FadeIn(arr3), FadeIn(cur), FadeIn(counter3), run_time=0.4)
        stream = T("front to back: every block it fetches is used completely", 22, INK).move_to([0, 0.55, 0])
        self.play(FadeIn(stream), run_time=0.4)
        for b in range(NB):
            self.play(cur.animate.next_to(arr3[b], UP, 0.05), arr3[b][0].animate.set_stroke(AMBER, 3),
                      counter3.to(b + 1), run_time=0.42, rate_func=linear)
            arr3[b][0].set_stroke(DIM, 1.4)

        # 11-12: the simulation
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        panels = race_panels()
        cap = mono(f"LRU virtual memory · {RACE['n']:,} items · memory {RACE['M']:,} items (1/12) · "
                   f"blocks of {RACE['B']} items · a dot per I/O", 14, FAINT).move_to([0.35, -3.62, 0])
        self.play(FadeOut(c), *[FadeIn(Group(p["img"], p["frame"], p["title"], p["cnt"], p["ylab"])) for p in panels],
                  *[FadeIn(p["curtain"]) for p in panels], FadeIn(cap), run_time=0.8)
        for p in panels:
            self.bring_to_front(p["curtain"], p["frame"])
        xlab = T("time →", 16, FAINT, font=MONO).next_to(panels[1]["frame"], DOWN, 0.08, aligned_edge=RIGHT)
        self.play(FadeIn(xlab), run_time=0.3)

        self.at("11", 2.2)
        reveal(self, panels[0], 3.4)
        reveal(self, panels[1], 2.8)

        # 13: the measured counts: comparisons about 2x, I/Os more than 20x
        self.at("13")
        cmp = RACE["comparisons"]
        stats = []
        for p, key in zip(panels, ("heapsort", "mergesort")):
            txt = mono(f"{cmp[key] / 1e6:.1f} M comparisons", 20, MUTED)
            txt.next_to(p["title"], RIGHT, 0.5).align_to(p["title"], DOWN)
            stats.append(txt)
        per = mono(f"≈ {RACE['heapsort']['trips'] / RACE['n']:.1f} I/Os per item", 20, AMBER)
        per.next_to(panels[0]["frame"].get_corner(UR), DL, buff=0.2)
        self.play(FadeIn(stats[0]), FadeIn(stats[1]), run_time=0.6)
        self.at("13", 3.2)
        self.play(*[Circumscribe(p["cnt"], color=AMBER, buff=0.08) for p in panels], run_time=1.0)
        self.at("13", 6.6)
        self.play(FadeIn(per), run_time=0.4)

        # 14-16: time at typical speeds
        self.at("14")
        race_all = Group(*[Group(p["img"], p["frame"], p["title"], p["cnt"], p["ylab"]) for p in panels],
                         *stats, per, cap, xlab)
        self.remove(*[p["curtain"] for p in panels])
        self.play(FadeOut(race_all), run_time=0.5)
        t_cmp = cmp["heapsort"] * 100e-9
        t_io = RACE["heapsort"]["trips"] * 100e-6
        scale = 10.5 / t_io
        head = T("heapsort, at typical speeds", 26, INK, weight=MEDIUM).move_to([-5.9, 2.3, 0], aligned_edge=LEFT)
        b1 = Rectangle(width=max(t_cmp * scale, 0.06), height=0.5, fill_color=MUTED, fill_opacity=0.9, stroke_width=0)
        b1.move_to([-5.9, 1.2, 0], aligned_edge=LEFT)
        l1 = M(f'comparisons: {cmp["heapsort"] / 1e6:.1f} M × 100 ns = <span foreground="#E6EBF0">{t_cmp:.2f} s</span>',
               22, MUTED, font=MONO).next_to(b1, RIGHT, 0.3)
        b2 = Rectangle(width=t_io * scale, height=0.5, fill_color=AMBER, fill_opacity=0.9, stroke_width=0)
        b2.move_to([-5.9, -0.2, 0], aligned_edge=LEFT)
        l2 = M(f'I/Os: {RACE["heapsort"]["trips"]:,} × 100 µs = <span foreground="#F2A93B">{t_io:.0f} s</span>',
               22, MUTED, font=MONO).next_to(b2, DOWN, 0.2, aligned_edge=LEFT)
        typ = mono("typical: a memory access ~100 ns (a generous cost per comparison); an SSD I/O ~100 µs", 16, FAINT)
        typ.move_to([0, -2.2, 0])
        self.play(FadeIn(head), GrowFromEdge(b1, LEFT), FadeIn(l1), FadeIn(typ), run_time=0.8)
        self.at("15")
        self.play(GrowFromEdge(b2, LEFT), FadeIn(l2), run_time=1.0)
        self.at("16")
        decide = T("The I/Os decide.", 40, AMBER, weight=SEMIBOLD).move_to([0, -3.1, 0])
        self.play(FadeIn(decide, shift=0.1 * UP), run_time=0.5)

        # 17-18: merge sort is the starting point; a pass reads and writes every block once
        self.at("17")
        self.play(FadeOut(VGroup(head, b1, l1, b2, l2, typ, decide)), run_time=0.4)
        mp = race_panels()[1]
        mp["curtain_p"].set_value(1.0)
        keep = Group(mp["img"], mp["frame"], mp["title"], mp["ylab"]).move_to([0.35, 0.6, 0])
        self.play(FadeIn(keep), run_time=0.8)
        start = T("our starting point", 24, ICE).next_to(mp["title"], RIGHT, 0.4)
        self.play(FadeIn(start), run_time=0.4)
        self.at("18", 2.0)
        fw = mp["frame"].width / RACE["passes"]["mergesort"]
        band = Rectangle(width=fw, height=mp["frame"].height, stroke_width=0, fill_color=ICE, fill_opacity=0.2)
        band.move_to(mp["frame"].get_left() + RIGHT * fw / 2)
        onep = mono("one pass: read and write every block of the file once", 20, INK).next_to(mp["frame"], DOWN, 0.3)
        self.play(FadeIn(band), FadeIn(onep), run_time=0.6)
        self.play(band.animate.shift(RIGHT * fw * 3), run_time=2.0, rate_func=linear)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
