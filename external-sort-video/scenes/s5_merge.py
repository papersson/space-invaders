import heapq

from common import *
from s3_model import TOY
from s4_runs import runs_stage, two_scans_stamp

RUNS = TOY["runs"]
FLAT = [v for run in RUNS for v in run]
HEAP_POS = [np.array([-1.4, 3.02, 0]), np.array([-2.75, 2.28, 0]), np.array([-0.05, 2.28, 0])]


def slot_label(i, text, color=MUTED):
    return T(text, 20, color, font=MONO).move_to(tray_center(i) + np.array([0, -0.98, 0]))


def front(cards):
    for c in cards:
        if c is not None:
            return c
    return None


def heap_view(fronts):
    """fronts: {run: Card}. A valid 3-node min-heap drawing: min at the root."""
    items = sorted(fronts.items(), key=lambda kv: kv[1].v)
    order = [items[0]] + sorted(items[1:], key=lambda kv: kv[0]) if items else []
    g = VGroup()
    edges = VGroup(*[Line(HEAP_POS[0], HEAP_POS[k], stroke_color=FAINT, stroke_width=2)
                     .scale(0.62) for k in (1, 2)])
    g.add(edges)
    for k in range(3):
        if k < len(order):
            r, card = order[k]
            circ = Circle(radius=0.3, fill_color=vcolor(card.x), fill_opacity=1,
                          stroke_color=ICE if k == 0 else BG, stroke_width=4 if k == 0 else 0)
            num = Text(str(card.v), font=MONO, weight=MEDIUM, color=ink_on(card.x), font_size=40)
            num.scale_to_fit_height(0.2)
            tag = T(f"run {r + 1}", 16, MUTED, font=MONO).next_to(circ, RIGHT if k != 1 else LEFT, 0.1)
            node = VGroup(circ, num.move_to(circ), tag).shift(HEAP_POS[k] - circ.get_center())
        else:
            node = Circle(radius=0.3, stroke_color=DIM, stroke_width=2).move_to(HEAP_POS[k])
        g.add(node)
    return g


class S5Merge(CueScene):
    SEG = "s5"

    def construct(self):
        tray, disk1, blocks, labels, counter = runs_stage(24)
        c1 = chip("Phase 1 · sorted runs")
        stamp = two_scans_stamp()
        self.add(tray, disk1, *blocks, labels, counter, c1, stamp)
        r1 = row_centers(ROW1_Y)
        r2 = row_centers(ROW2_Y)

        # l1: phase two
        self.at("l1")
        c2 = chip("Phase 2 · merge")
        disk2 = build_disk(2)
        out_lab = T("output", 20, MUTED, font=MONO).next_to(disk2[3], DOWN, buff=0.12)
        self.play(FadeOut(stamp), ReplacementTransform(c1, c2),
                  ReplacementTransform(disk1, disk2), run_time=0.8)
        self.bring_to_front(*blocks, labels)
        self.play(FadeIn(out_lab), run_time=0.3)

        # l2: the merge you already know, on two runs
        self.at("l2")
        lab2 = VGroup(slot_label(0, "run 1"), slot_label(1, "run 2"), slot_label(3, "output"))
        self.play(FadeIn(lab2), run_time=0.4)
        ins = []
        for r in (0, 1):
            ins.append(blocks[4 * r].copy())
        frames = [amber_frame(b.get_center(), DISK_SCALE) for b in ins]
        self.add(*ins, *frames)
        self.play(*[VGroup(b, f).animate.scale(1 / DISK_SCALE).move_to(tray_center(i))
                    for i, (b, f) in enumerate(zip(ins, frames))],
                  blocks[0].animate.set_opacity(0.22), blocks[4].animate.set_opacity(0.22),
                  counter.to(26), run_time=0.8)
        self.remove(*frames)
        bufs = [list(ins[0]), list(ins[1])]
        outpos = block_positions(tray_center(3))
        demo_out = []
        for k in range(3):
            f0, f1 = front(bufs[0]), front(bufs[1])
            win = 0 if f0.v < f1.v else 1
            rings = VGroup(*[SurroundingRectangle(f, buff=0.04, color=ICE if f is (f0, f1)[win] else FAINT,
                                                  corner_radius=0.08, stroke_width=3) for f in (f0, f1)])
            self.play(FadeIn(rings), run_time=0.25)
            card = (f0, f1)[win]
            bufs[win][bufs[win].index(card)] = None
            self.play(card.animate.move_to(outpos[k]), FadeOut(rings), run_time=0.6)
            demo_out.append(card)
            self.wait(0.15)

        # l3: round after round, each reading and writing the whole file
        self.at("l3")
        self.play(FadeOut(VGroup(*ins)), run_time=0.3)
        head = T("round 1 · merge run 1 with run 2", 26, INK).move_to([-0.9, 2.75, 0])
        r12 = sorted(RUNS[0] + RUNS[1])
        out1 = [make_block(r12[4 * i: 4 * i + 4], r2[i], DISK_SCALE) for i in range(8)]
        wf = [amber_frame(r2[i], DISK_SCALE) for i in range(8)]
        reads = [amber_frame(r1[i], DISK_SCALE) for i in range(1, 8) if i != 4]
        self.play(FadeIn(head), run_time=0.3)
        t1 = 2.6
        self.play(LaggedStart(*[Succession(FadeIn(f, run_time=0.2), FadeOut(f, run_time=0.3)) for f in reads],
                              lag_ratio=0.9),
                  LaggedStart(*[Succession(FadeIn(VGroup(b, f), run_time=0.3), FadeOut(f, run_time=0.2))
                                for b, f in zip(out1, wf)], lag_ratio=0.7),
                  *[blocks[i].animate.set_opacity(0.22) for i in range(8)],
                  counter.to(40), run_time=t1, rate_func=linear)
        head2 = T("round 2 · merge (1 + 2) with run 3", 26, INK).move_to(head)
        final = sorted(FLAT)
        out2 = [make_block(final[4 * i: 4 * i + 4], r1[i], DISK_SCALE) for i in range(12)]
        wf2 = [amber_frame(r1[i], DISK_SCALE) for i in range(12)]
        self.play(ReplacementTransform(head, head2), run_time=0.3)
        self.play(*[b.animate.set_opacity(0.22) for b in out1 + blocks[8:]], run_time=0.8)
        self.play(*[FadeOut(b) for b in blocks],
                  LaggedStart(*[Succession(FadeIn(VGroup(b, f), run_time=0.25), FadeOut(f, run_time=0.15))
                                for b, f in zip(out2, wf2)], lag_ratio=0.6),
                  counter.to(64), run_time=2.4, rate_func=linear)
        self.play(*[FadeOut(b) for b in out1], FadeOut(labels), run_time=0.4)
        note2 = T("2-way: 64 trips", 20, MUTED, font=MONO).next_to(counter, DOWN, 0.18).align_to(counter, RIGHT)
        self.play(FadeIn(note2), run_time=0.3)

        # l4-l5: memory during a 2-way merge: two input blocks, one output block, the rest idle
        self.at("l4")
        snap = self.two_way_snapshot()
        scrim = Rectangle(width=14.4, height=2.9, fill_color=BG, fill_opacity=0.7, stroke_width=0)
        scrim.move_to(disk2[0])
        lab_snap = VGroup(slot_label(0, "runs 1+2"), slot_label(1, "run 3"))
        self.play(FadeOut(head2), FadeIn(scrim), FadeIn(snap), FadeOut(lab2[:2]), FadeIn(lab_snap), run_time=0.7)
        self.at("l5", 0.4)
        rings = VGroup(*[slot(tray_center(i), 1.0, color=ICE, width=4) for i in (0, 1)])
        self.play(Create(rings), run_time=0.5)
        self.play(rings.animate.set_stroke(opacity=0.3), run_time=0.8)
        self.at("l5", 3.2)
        ring_o = slot(tray_center(3), 1.0, color=ICE, width=4)
        self.play(Create(ring_o), run_time=0.5)
        self.play(ring_o.animate.set_stroke(opacity=0.3), run_time=0.8)
        self.at("l5", 5.1)
        idle = slot(tray_center(2), 1.0, color=IDLE, width=2, fill=IDLE, fill_opacity=0.55)
        idle_lab = slot_label(2, "idle", INK)
        self.play(FadeIn(idle), FadeIn(idle_lab), run_time=0.5)
        self.play(idle.animate.set_fill(opacity=0.25), rate_func=there_and_back, run_time=1.0)

        # l6: use the whole desk: every run gets a buffer; rewind the count
        self.at("l6")
        tray2, disk_b, blocks, labels, _ = runs_stage(24)
        lab3 = VGroup(slot_label(0, "run 1"), slot_label(1, "run 2"), slot_label(2, "run 3"),
                      slot_label(3, "output"))
        self.play(FadeOut(VGroup(snap, rings, ring_o, idle, idle_lab, lab2[2], lab_snap)), FadeOut(VGroup(*out2)),
                  FadeOut(scrim), counter.to(24), run_time=0.7)
        self.play(FadeIn(VGroup(*blocks)), FadeIn(labels), FadeIn(lab3), run_time=0.6)
        self.at("l6", 1.9)
        bufs = []
        ups = [blocks[4 * r].copy() for r in range(3)]
        frames = [amber_frame(b.get_center(), DISK_SCALE) for b in ups]
        self.add(*ups, *frames)
        self.play(LaggedStart(*[VGroup(b, f).animate.scale(1 / DISK_SCALE).move_to(tray_center(r))
                                for r, (b, f) in enumerate(zip(ups, frames))], lag_ratio=0.35),
                  *[blocks[4 * r].animate.set_opacity(0.22) for r in range(3)],
                  tick_at(counter, 24, lagged_arrivals(3, 1.8, 0.35), 1.8), run_time=1.8)
        self.remove(*frames)
        bufs = [list(u) for u in ups]
        self.remove(*ups)
        self.add(*[c for b in bufs for c in b])

        # l7: the heap over the three fronts
        self.at("l7")
        heap_lab = T("heap", 20, MUTED, font=MONO).next_to(HEAP_POS[0], LEFT, buff=0.55)
        heap = heap_view({r: front(bufs[r]) for r in range(3)})
        self.play(FadeIn(heap), FadeIn(heap_lab), run_time=0.8)

        # l8-l11: replay the event log
        events = TOY["events"][3:]
        sched = self.schedule(events)
        out_cards = []
        fps = config.frame_rate
        for i, (ev, (t_start, dur)) in enumerate(zip(events, sched)):
            if dur is None:
                rest = len(events) - i
                dur = max(3, round((self.end_fast - self.now()) / rest * fps)) / fps
            else:
                self.until(t_start)
            if ev["t"] == "pop":
                r = ev["run"]
                card = front(bufs[r])
                slow = dur > 0.3
                if slow:
                    ring = SurroundingRectangle(card, buff=0.04, color=ICE, corner_radius=0.08, stroke_width=3)
                    self.play(FadeIn(ring), run_time=0.15)
                bufs[r][bufs[r].index(card)] = None
                fronts = {k: front(bufs[k]) for k in range(3) if front(bufs[k]) is not None}
                new_heap = heap_view(fronts)
                anims = [card.animate.move_to(outpos[ev["out"]])]
                if slow:
                    anims += [FadeOut(ring)]
                self.play(*anims, run_time=dur - (0.15 if slow else 0))
                self.remove(heap)
                heap = new_heap
                self.add(heap)
                out_cards.append(card)
            elif ev["t"] == "flush":
                blk = VGroup(*out_cards[-4:])
                fr = amber_frame(tray_center(3), 1.0)
                self.add(fr)
                self.play(VGroup(blk, fr).animate.scale(DISK_SCALE).move_to(r2[ev["block"]]),
                          counter.to(counter.value() + 1), run_time=dur)
                self.remove(fr)
            elif ev["t"] == "refill":
                r, b = ev["run"], ev["block"]
                src = blocks[4 * r + b]
                up = src.copy()
                fr = amber_frame(src.get_center(), DISK_SCALE)
                self.add(up, fr)
                self.play(VGroup(up, fr).animate.scale(1 / DISK_SCALE).move_to(tray_center(r)),
                          src.animate.set_opacity(0.22), counter.to(counter.value() + 1), run_time=dur)
                self.remove(fr, up)
                bufs[r] = list(up)
                self.add(*bufs[r])
                fronts = {k: front(bufs[k]) for k in range(3) if front(bufs[k]) is not None}
                self.remove(heap)
                heap = heap_view(fronts)
                self.add(heap)
        note3 = T("wide: 48 trips", 20, ICE, font=MONO).next_to(note2, DOWN, 0.1).align_to(counter, RIGHT)
        self.play(FadeIn(note3), run_time=0.4)

        # l12: how many runs fit at once
        self.at("l12")
        fan = M('one block per run, one for output → <span foreground="#8FD3FF">fan-in ≈ M/B</span>',
                24, INK, font=MONO).move_to([-1.6, 2.85, 0])
        self.play(FadeOut(heap), FadeOut(heap_lab), run_time=0.4)
        self.play(FadeIn(fan, shift=0.1 * DOWN), run_time=0.6)
        braces = VGroup(*[slot(tray_center(i), 1.0, color=ICE, width=3) for i in range(3)])
        self.play(LaggedStart(*[Create(b) for b in braces], lag_ratio=0.3), run_time=1.0)

        # l13: at real scale
        self.at("l13")
        everything = Group(*self.mobjects)
        self.play(FadeOut(everything), run_time=0.6)
        self.fan_in_scene()
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()

    def two_way_snapshot(self):
        """A real mid-merge state of round 2 (run 1+2 with run 3), as the tray would hold it."""
        a, b = sorted(RUNS[0] + RUNS[1]), RUNS[2]
        runs = [a, b]
        pos = [0, 0]
        heap = [(a[0], 0), (b[0], 1)]
        out = []
        while len(out) < 11:
            v, r = heapq.heappop(heap)
            out.append(v)
            pos[r] += 1
            heapq.heappush(heap, (runs[r][pos[r]], r))
        g = VGroup()
        for r in (0, 1):
            blk = pos[r] // 4
            vals = runs[r][4 * blk: 4 * blk + 4]
            cards = make_block(vals, tray_center(r))
            for i in range(pos[r] % 4):
                cards[i].set_opacity(0)
            g.add(cards)
        kept = out[len(out) - len(out) % 4:]
        oc = VGroup(*[Card(v).move_to(p) for v, p in zip(kept, block_positions(tray_center(3)))])
        g.add(oc)
        return g

    def schedule(self, events):
        """Start time and duration of every event, pinned to the narration."""
        s = []
        t = self.start_of("l8")
        pops = 0
        first_refill_done = False
        for i, ev in enumerate(events):
            if ev["t"] == "pop":
                pops += 1
            if pops <= 4 and ev["t"] == "pop":
                d = 0.55
            elif ev["t"] == "flush" and ev["block"] == 0:
                t = max(t, self.start_of("l9", 0.3))
                d = 0.6
            elif not first_refill_done and ev["t"] != "refill":
                d = 0.42
            elif ev["t"] == "refill" and not first_refill_done:
                t = max(t, self.start_of("l10", 0.35))
                d = 0.6
                first_refill_done = True
            else:
                self.end_fast = self.end_of("l11", 2.2)
                s.append((None, None))
                continue
            s.append((t, d))
            t += d
        return s

    def fan_in_scene(self):
        tray = RoundedRectangle(corner_radius=0.14, width=4.2, height=0.9, stroke_color=TRAY_EDGE,
                                stroke_width=2.5, fill_color=TRAY_FILL, fill_opacity=1).move_to([0, 1.2, 0])
        tl = label("memory · 16 GB", 20, INK).next_to(tray, UP, 0.12, aligned_edge=LEFT)
        n = 260
        rng = np.random.default_rng(3)
        lines = VGroup()
        for k in range(n):
            x = -6.9 + 13.8 * k / (n - 1)
            end = np.array([-1.9 + 3.8 * k / (n - 1), 0.75, 0])
            ln = Line([x, -3.3, 0], end, stroke_width=1.1, stroke_color=vcolor(rng.random()),
                      stroke_opacity=0.55)
            lines.add(ln)
        disk = label("16,383 sorted runs on disk", 20, MUTED).move_to([0, -3.6, 0])
        big = Counter(3, title="RUNS MERGED AT ONCE", size=58, anchor=[6.6, 3.35, 0], color=ICE)
        sub = M('16 GB ÷ 1 MB = 16,384 blocks:\n<span foreground="#8FD3FF">16,383</span> in + 1 out',
                22, MUTED, font=MONO).move_to([-6.6, 3.05, 0], aligned_edge=LEFT)
        self.play(FadeIn(tray), FadeIn(tl), FadeIn(big), run_time=0.6)
        self.play(LaggedStart(*[Create(l) for l in lines], lag_ratio=0.01),
                  big.to(16383, rate_func=rush_into), run_time=3.2)
        self.play(FadeIn(disk), FadeIn(sub), run_time=0.6)
        one = T("one pass", 30, INK, weight=MEDIUM).next_to(tray, RIGHT, 0.5)
        self.play(FadeIn(one, shift=0.1 * LEFT), run_time=0.5)
