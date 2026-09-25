from common import *

TOY = json.loads((DATA / "toy.json").read_text())


def base_stage(counter_value=0):
    """The S3/S4 starting picture: the shuffled deck on disk, an empty tray, the counter."""
    tray = build_tray()
    disk = build_disk(1)
    blocks = disk_blocks(TOY["deck"])
    counter = Counter(counter_value)
    return tray, disk, blocks, counter


class S3Model(CueScene):
    SEG = "s3"

    def construct(self):
        tray, disk, blocks, counter = base_stage()
        c = chip("The I/O model")

        # l1: the model's picture
        self.at("l1")
        self.play(FadeIn(c), FadeIn(disk), FadeIn(tray), run_time=0.9)
        self.play(LaggedStart(*[FadeIn(b, shift=0.1 * UP) for b in blocks], lag_ratio=0.08),
                  FadeIn(counter), run_time=1.4)

        row = VGroup(*blocks)
        # l2: N
        self.at("l2")
        bn = Brace(row, DOWN, buff=0.28, color=MUTED)
        tn = M('<span foreground="#E6EBF0">N</span> = 48 items', 26, MUTED, font=MONO).next_to(bn, DOWN, 0.08)
        self.play(GrowFromCenter(bn), FadeIn(tn), run_time=0.7)

        # l3: M
        self.at("l3")
        slots = tray[1]
        bm = Brace(slots, UP, buff=0.12, color=MUTED)
        tm = M('<span foreground="#E6EBF0">M</span> = 16 items fit in memory', 26, MUTED, font=MONO)
        tm.next_to(bm, UP, 0.08)
        self.play(GrowFromCenter(bm), FadeIn(tm), run_time=0.7)

        # l4: B
        self.at("l4")
        hl = slot(blocks[0].get_center(), DISK_SCALE, color=ICE, width=3)
        tb = M('<span foreground="#E6EBF0">B</span> = 4 items per block', 24, MUTED, font=MONO)
        tb.next_to(disk[0], UP, 0.12).set_x(-5.0 + tb.width / 2)
        self.play(Create(hl), FadeIn(tb, shift=0.1 * UP), run_time=0.7)

        # l5: computation is free; the only cost is blocks moved
        self.at("l5", 0.2)
        self.play(FadeOut(VGroup(bn, tn, bm, tm, tb, hl)), run_time=0.5)
        free = M('computation: <span foreground="#8FD3FF">free</span>', 30, MUTED, font=MONO)
        cost = M('cost: <span foreground="#F2A93B">blocks moved</span>', 30, MUTED, font=MONO)
        rules = VGroup(free, cost).arrange(RIGHT, buff=1.2).move_to([-0.9, 2.75, 0])
        self.play(FadeIn(free, shift=0.1 * UP), run_time=0.6)
        self.at("l5", 3.6)
        self.play(FadeIn(cost, shift=0.1 * UP), run_time=0.6)
        # one block up (+1), shuffled for free, back down (+1)
        up = transfer(self, blocks[0], tray_center(0), 1.0, DISK_SCALE, counter, 0.7, copy_from=True)
        tag = T("+0", 26, ICE, font=MONO).next_to(counter, LEFT, buff=0.35)
        order = sorted(range(4), key=lambda i: up[i].v)
        pos = block_positions(tray_center(0), 1.0)
        self.play(*[up[i].animate.move_to(pos[order.index(i)]) for i in range(4)], FadeIn(tag),
                  run_time=0.9, path_arc=0.8)
        self.play(FadeOut(tag), run_time=0.2)
        cards0 = VGroup(*[up[i] for i in order])
        down = transfer(self, cards0, blocks[0].get_center(), DISK_SCALE, 1.0, counter, 0.7)
        self.play(FadeOut(blocks[0]), run_time=0.2)
        blocks[0] = down

        # l6: a scan costs N/B
        self.at("l6")
        self.play(counter.to(0), run_time=0.4)
        cite = T("Aggarwal and Vitter, 1988", 20, FAINT, slant=ITALIC).next_to(rules, DOWN, 0.15)
        self.play(FadeIn(cite), run_time=0.3)
        ghosts = []
        for i, b in enumerate(blocks):
            g = b.copy()
            fr = amber_frame(g.get_center(), DISK_SCALE).set_stroke(opacity=0)
            self.add(g, fr)
            ghosts.append((g, fr))
        self.play(LaggedStart(*[
            Succession(fr.animate(run_time=0.1).set_stroke(opacity=1),
                       VGroup(g, fr).animate.scale(1 / DISK_SCALE).move_to(tray_center(i % 4)).set_opacity(0))
            for i, (g, fr) in enumerate(ghosts)], lag_ratio=0.28),
            tick_at(counter, 0, lagged_arrivals(12, 3.0, 0.28, 0.5), 3.0), run_time=3.0)
        for g, fr in ghosts:
            self.remove(g, fr)
        stamp = M('1 scan = <span foreground="#F2A93B">N/B</span> = 12 trips', 28, INK, font=MONO)
        stamp.move_to([0, -2.85, 0])
        self.play(FadeIn(stamp, shift=0.1 * DOWN), run_time=0.5)
        self.until(self.dur - 0.6)
        self.play(FadeOut(VGroup(stamp, rules, cite, c)), run_time=0.5)
        self.finish()
