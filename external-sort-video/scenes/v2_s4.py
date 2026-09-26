from v2kit import *
from s7_everywhere import mini_run

U, GAP = 0.78, 0.12                     # one run's width in the halving picture, and the gap
X0 = -4.2                               # left edge of the rows
ROW_YS = [2.35, 1.25, 0.15, -0.95, -2.05]
ROWS = [[1] * 12, [2] * 6, [4] * 3, [8, 4], [12]]   # run sizes, in original runs, two at a time


def bar(size, start, y, seed):
    w = size * U + (size - 1) * GAP
    b = mini_run(min(16 * size, 160), w, 0.28, seed=seed)
    return b.move_to([X0 + start * (U + GAP) + w / 2, y, 0])


def halving():
    rows, links, labs = [], VGroup(), VGroup()
    for k, (sizes, y) in enumerate(zip(ROWS, ROW_YS)):
        row, start = VGroup(), 0
        for i, s in enumerate(sizes):
            row.add(bar(s, start, y, seed=100 * k + i))
            start += s
        rows.append(row)
        n = len(sizes)
        labs.add(mono(f"{n} run{'s' if n > 1 else ''}" if k < 4 else "1 file", 20, MUTED)
                 .move_to([X0 - 0.35, y, 0], aligned_edge=RIGHT))
        if k:
            prev = rows[k - 1]
            starts = np.cumsum([0] + ROWS[k - 1])
            g = VGroup()
            for j, b in enumerate(prev):
                # the target bar is the one covering this source's start
                cum = np.cumsum([0] + sizes)
                t = max(i for i in range(len(sizes)) if cum[i] <= starts[j])
                g.add(Line(b.get_bottom(), [b.get_x(), row[t].get_top()[1], 0], stroke_color=FAINT, stroke_width=1.5))
            links.add(g)
    return rows, links, labs


def schedule(scene, events):
    """(start, duration) for the narrated events; None for the fast replay that follows."""
    s, t, pops = [], scene.start_of("10"), 0
    slow_done = False
    for ev in events:
        if slow_done:
            s.append(None)
            continue
        if ev["t"] == "pop":
            pops += 1
            d = 1.1 if pops == 1 else (0.55 if pops <= 4 else 0.45)
        elif ev["t"] == "flush":
            t, d = max(t, scene.start_of("11", 0.3)), 0.7
        else:                                   # run three's first refill
            t, d = max(t, scene.start_of("12", 1.6)), 0.8
            slow_done = True
        s.append((t, d))
        t += d
    return s


class V2S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("The multiway merge")
        # 01-03: two at a time, 12 -> 6 -> 3 -> 2 -> 1
        rows, links, labs = halving()
        self.at("01")
        cap = T("each run is sorted, but not against the others", 22, MUTED).next_to(rows[0], UP, 0.3)
        self.play(FadeIn(c), FadeIn(rows[0], lag_ratio=0.1), FadeIn(labs[0]), run_time=1.0)
        self.play(FadeIn(cap), run_time=0.5)
        self.at("02")
        for k in range(1, 5):
            self.play(Create(links[k - 1]), FadeIn(rows[k]), FadeIn(labs[k]), run_time=0.7)
        self.at("03")
        four = M('two at a time: <span foreground="#F2A93B">4 merge passes</span> '
                 '<span foreground="#56606B">(5 passes = 1 + 4)</span>', 24, INK, font=MONO).move_to([0.8, -3.2, 0])
        self.play(FadeIn(four), run_time=0.5)

        # 04-06: memory during a two-way merge
        self.at("04")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        tray = build_tray()
        snap = two_way_snapshot()
        head = T("memory during a two-way merge", 24, INK).move_to([0, 2.75, 0])
        labs2 = VGroup(slot_label(0, "runs 1+2"), slot_label(1, "run 3"), slot_label(3, "output"))
        self.play(FadeIn(tray), FadeIn(head), run_time=0.5)
        self.play(FadeIn(snap), FadeIn(labs2), run_time=0.6)
        self.at("05", 0.3)
        rings = VGroup(*[slot(tray_center(i), 1.0, color=ICE, width=4) for i in (0, 1)])
        self.play(Create(rings), run_time=0.5)
        self.at("05", 2.5)
        ring_o = slot(tray_center(3), 1.0, color=ICE, width=4)
        self.play(Create(ring_o), run_time=0.5)
        self.at("06")
        idle = slot(tray_center(2), 1.0, color=IDLE, width=2, fill=IDLE, fill_opacity=0.55)
        idle_lab = slot_label(2, "idle", INK)
        self.play(FadeIn(idle), FadeIn(idle_lab), run_time=0.5)
        real = mono(f"in the simulation: 3 of {RACE['M'] // RACE['B']} blocks of memory in use, "
                    f"{RACE['M'] // RACE['B'] - 3} idle", 18, MUTED).move_to([0, -1.2, 0])
        self.play(FadeIn(real), run_time=0.5)

        # 07: one block per run, all at once
        self.at("07")
        self.play(FadeOut(VGroup(snap, labs2, rings, ring_o, idle, idle_lab, real, head)), run_time=0.5)
        disk = build_disk(2)
        flat = [v for run in TOY["runs"] for v in run]
        blocks = disk_blocks(flat)
        rlabs = VGroup(*[T(f"run {r + 1}", 20, MUTED, font=MONO).next_to(VGroup(*blocks[4 * r: 4 * r + 4]), DOWN, 0.1)
                         for r in range(3)])
        out_lab = T("output", 20, MUTED, font=MONO).next_to(disk[3], DOWN, buff=0.1)
        counter = Counter(24, title="I/Os")
        before = mono("24 so far: the runs pass", 16, FAINT).next_to(counter, DOWN, 0.12).align_to(counter, RIGHT)
        labs3 = VGroup(slot_label(0, "run 1"), slot_label(1, "run 2"), slot_label(2, "run 3"), slot_label(3, "output"))
        head = T("multiway merge: every run gets a block", 24, INK).move_to([0, 2.75, 0])
        self.play(FadeIn(disk), FadeIn(VGroup(*blocks)), FadeIn(rlabs), FadeIn(out_lab), FadeIn(counter),
                  FadeIn(before), FadeIn(labs3), FadeIn(head), run_time=0.8)
        self.wait(0.4)
        ups = [blocks[4 * r].copy() for r in range(3)]
        frames = [amber_frame(b.get_center(), DISK_SCALE) for b in ups]
        self.add(*ups, *frames)
        self.play(LaggedStart(*[VGroup(b, f).animate.scale(1 / DISK_SCALE).move_to(tray_center(r))
                                for r, (b, f) in enumerate(zip(ups, frames))], lag_ratio=0.35),
                  *[blocks[4 * r].animate.set_opacity(0.22) for r in range(3)],
                  tick_at(counter, 24, lagged_arrivals(3, 1.8, 0.35), 1.8), run_time=1.8)
        self.remove(*frames, *ups)
        bufs = [list(u) for u in ups]
        self.add(*[cd for b in bufs for cd in b])

        # 08-09: a small heap over the fronts, in memory
        self.at("08", 3.0)
        heap_lab = T("heap", 20, MUTED, font=MONO).move_to([-2.3, 3.05, 0], aligned_edge=RIGHT)
        heap = heap_view({r: front(bufs[r]) for r in range(3)})
        self.play(FadeOut(head), FadeIn(heap), FadeIn(heap_lab), run_time=0.8)
        per_run = mono("one entry per run", 20, INK).move_to([1.3, 3.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(per_run), FadeOut(before), run_time=0.4)
        self.at("09", 1.0)
        in_mem = mono("in memory the whole time", 20, ICE).next_to(per_run, DOWN, 0.15, aligned_edge=LEFT)
        not_hs = mono("(heapsort's heap was the whole file)", 16, FAINT).next_to(in_mem, DOWN, 0.12, aligned_edge=LEFT)
        self.play(FadeIn(in_mem), run_time=0.4)
        self.play(FadeIn(not_hs), run_time=0.4)

        # 10-13: the merge, from the event log: run three first, a flush, run three's refill, then the rest
        events = TOY["events"][3:]
        sched = schedule(self, events)
        outpos = block_positions(tray_center(3))
        r2 = row_centers(ROW2_Y)
        out_cards = []
        state = dict(heap=heap)

        def reheap():
            fronts = {k: front(bufs[k]) for k in range(3) if front(bufs[k]) is not None}
            self.remove(state["heap"])
            state["heap"] = heap_view(fronts) if fronts else VGroup()
            self.add(state["heap"])

        def flush_anim(ev):
            blk = VGroup(*out_cards[-4:])
            fr = amber_frame(tray_center(3), 1.0)
            self.add(fr)
            return [VGroup(blk, fr).animate.scale(DISK_SCALE).move_to(r2[ev["block"]]),
                    counter.to(counter.value() + 1)], [fr]

        def refill_anim(ev):
            r, b = ev["run"], ev["block"]
            src = blocks[4 * r + b]
            up = src.copy()
            fr = amber_frame(src.get_center(), DISK_SCALE)
            self.add(up, fr)
            bufs[r] = list(up)
            return [VGroup(up, fr).animate.scale(1 / DISK_SCALE).move_to(tray_center(r)),
                    src.animate.set_opacity(0.22), counter.to(counter.value() + 1)], [fr]

        slow_note = None
        fast = []
        for ev, sc in zip(events, sched):
            if sc is None:
                fast.append(ev)
                continue
            t0, d = sc
            self.until(t0)
            if ev["t"] == "pop":
                r = ev["run"]
                card = front(bufs[r])
                if d > 1:
                    ring = SurroundingRectangle(card, buff=0.04, color=ICE, corner_radius=0.08, stroke_width=3)
                    slow_note = mono("smallest front: run 3", 18, ICE).move_to([1.5, 2.45, 0], aligned_edge=LEFT)
                    self.play(Create(ring), FadeIn(slow_note), FadeOut(VGroup(per_run, in_mem, not_hs)), run_time=0.35)
                    bufs[r][bufs[r].index(card)] = None
                    self.play(card.animate.move_to(outpos[ev["out"]]), FadeOut(ring), run_time=d - 0.35)
                else:
                    bufs[r][bufs[r].index(card)] = None
                    self.play(card.animate.move_to(outpos[ev["out"]]), run_time=d)
                out_cards.append(card)
                reheap()
            elif ev["t"] == "flush":
                anims, tmp = flush_anim(ev)
                self.play(*anims, *([FadeOut(slow_note)] if slow_note else []), run_time=d)
                self.remove(*tmp)
                slow_note = None
            else:
                anims, tmp = refill_anim(ev)
                self.play(*anims, run_time=d)
                self.remove(*tmp)
                self.add(*bufs[ev["run"]])
                reheap()

        # the rest, fast, grouped: consecutive pops move together
        groups, cur = [], []
        for ev in fast:
            if ev["t"] == "pop":
                cur.append(ev)
            else:
                if cur:
                    groups.append(("pops", cur))
                    cur = []
                groups.append((ev["t"], ev))
        if cur:
            groups.append(("pops", cur))
        end_fast = self.end_of("13", 1.3)
        weight = {"pops": 1.0, "flush": 0.8, "refill": 0.8}
        unit = (end_fast - self.now()) / sum(weight[g[0]] * (len(g[1]) ** 0.5 if g[0] == "pops" else 1)
                                             for g in groups)
        fps = config.frame_rate
        note13 = None
        for kind, x in groups:
            w = weight[kind] * (len(x) ** 0.5 if kind == "pops" else 1)
            d = max(2, round(unit * w * fps)) / fps
            if note13 is None and self.now() >= self.start_of("13"):
                note13 = mono("every block read once, written once", 18, AMBER)
                note13.next_to(counter, DOWN, 0.15).align_to(counter, RIGHT)
                self.add(note13)
            if kind == "pops":
                anims = []
                for ev in x:
                    card = front(bufs[ev["run"]])
                    bufs[ev["run"]][bufs[ev["run"]].index(card)] = None
                    anims.append(card.animate.move_to(outpos[ev["out"]]))
                    out_cards.append(card)
                self.play(*anims, run_time=d)
                reheap()
            elif kind == "flush":
                anims, tmp = flush_anim(x)
                self.play(*anims, run_time=d)
                self.remove(*tmp)
            else:
                anims, tmp = refill_anim(x)
                self.play(*anims, run_time=d)
                self.remove(*tmp)
                self.add(*bufs[x["run"]])
                reheap()
        if note13 is None:
            note13 = mono("every block read once, written once", 18, AMBER)
            note13.next_to(counter, DOWN, 0.15).align_to(counter, RIGHT)
            self.play(FadeIn(note13), run_time=0.3)

        # 14: a block for every run, plus one for the output: one pass
        self.at("14")
        rings = VGroup(*[slot(tray_center(i), 1.0, color=ICE, width=4) for i in range(4)])
        cond = M('memory: 4 blocks = <span foreground="#8FD3FF">3 runs + 1 output</span> → one merge pass', 22, INK,
                 font=MONO).move_to([-0.6, 2.62, 0])
        self.play(FadeOut(VGroup(state["heap"], heap_lab, note13)), run_time=0.4)
        self.play(Create(rings), FadeIn(cond), run_time=0.8)

        # 15-16: four merge passes fold into one; eighteen passes become two
        self.at("15")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        rows, links, labs = halving()
        top = rows[0]
        ghost = VGroup(*rows[1:4], *links, labs[1:4]).set_opacity(0.25)
        self.play(FadeIn(top), FadeIn(labs[0]), FadeIn(ghost), FadeIn(rows[4]), FadeIn(labs[4]), run_time=0.5)
        fan = VGroup(*[Line(b.get_bottom(), rows[4].get_top() + RIGHT * (b.get_x() - rows[4].get_x()) * 0.05,
                            stroke_color=ICE, stroke_width=2) for b in top])
        self.play(FadeOut(ghost), run_time=0.4)
        self.play(Create(fan), run_time=0.8)
        one = mono("one 12-way merge: 1 pass", 24, ICE).move_to([X0 + 5.3, ROW_YS[2], 0])
        self.play(FadeIn(BackgroundRectangle(one, color=BG, fill_opacity=0.9, buff=0.15)), FadeIn(one), run_time=0.4)
        self.at("16")
        tally = M('<span foreground="#56606B">18 → 5 →</span> 2 passes = 1 + 1', 34, INK, font=MONO)
        tally.move_to([0.8, -3.1, 0])
        self.play(FadeIn(tally, shift=0.1 * UP), run_time=0.6)

        # 17-18: external merge sort
        self.at("17")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        name = T("external merge sort", 54, INK, weight=SEMIBOLD).move_to([0, 1.6, 0])
        s1 = M('<span foreground="#8FD3FF">1.</span> sort memory-sized runs', 30, INK).move_to([0, 0.35, 0])
        s2 = M('<span foreground="#8FD3FF">2.</span> merge them from disk', 30, INK)
        s1.align_to(name, LEFT).shift(0.3 * RIGHT)
        s2.next_to(s1, DOWN, 0.3, aligned_edge=LEFT)
        self.play(FadeIn(name, shift=0.1 * UP), run_time=0.6)
        self.play(FadeIn(s1), run_time=0.4)
        self.play(FadeIn(s2), run_time=0.4)
        self.at("18")
        s3 = mono("as many runs at once as memory allows: the fewest passes", 20, MUTED).next_to(s2, DOWN, 0.3,
                                                                                            aligned_edge=LEFT)
        self.play(FadeIn(s3), run_time=0.5)

        # 19-20: what sort did at the end, replayed from the capture at real speed
        self.at("19")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        tmp = TmpFolder([-0.8, -0.3, 0], width=7.4, height=3.5)
        for i, nm in enumerate(tmp.names):
            tmp.labels[nm] = f"run {i + 1}"
        tmp.tt.set_value(merge_start_time() - 0.05)
        fold = tmp.mobject()
        head = T("sort's temporary folder: the merge", 26, INK, weight=MEDIUM).next_to(tmp.panel, UP, 0.25,
                                                                                      aligned_edge=LEFT)
        real = mono("replayed from the capture, real speed", 16, FAINT).next_to(tmp.panel, DOWN, 0.2, aligned_edge=LEFT)
        self.play(FadeIn(tmp.panel), FadeIn(tmp.title), FadeIn(fold), FadeIn(head), FadeIn(real), run_time=0.6)
        self.at("20")
        span = SORTCAP["duration_s"] - merge_start_time() + 0.05
        self.play(tmp.tt.animate.set_value(SORTCAP["duration_s"]), run_time=span, rate_func=linear)
        fold.clear_updaters()
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
