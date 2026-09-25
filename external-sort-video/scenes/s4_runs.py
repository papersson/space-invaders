from common import *
from s3_model import TOY

STRIP = json.loads((DATA / "strip.json").read_text())


def strip_images(values, W=1600, plot_h=360, strip_h=40):
    """Dot plot (key value vs position) and a color strip for one state of the file."""
    import seaborn as sns
    cmap = sns.color_palette("mako", as_cmap=True)
    v = np.asarray(values)
    rgb = (np.array(cmap(0.22 + 0.74 * v))[:, :3] * 255).astype(np.uint8)
    plot = np.zeros((plot_h, W, 4), np.uint8)
    ys = ((1 - v) * (plot_h - 5) + 2).astype(int)
    for dy in (-1, 0, 1):
        for dx in (-1, 0, 1):
            xs = np.clip(np.arange(W) + dx, 0, W - 1)
            plot[np.clip(ys + dy, 0, plot_h - 1), xs, :3] = rgb
            plot[np.clip(ys + dy, 0, plot_h - 1), xs, 3] = 255
    strip = np.repeat(rgb[None, :, :], strip_h, axis=0)
    return plot, strip


def strip_group(values, plot_w=12.6, plot_h=2.9, strip_h=0.5, y=0.6):
    plot, strip = strip_images(values)
    p = ImageMobject(plot).stretch_to_fit_width(plot_w).stretch_to_fit_height(plot_h)
    s = ImageMobject(strip).stretch_to_fit_width(plot_w).stretch_to_fit_height(strip_h)
    s.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    p.move_to([0, y, 0])
    s.next_to(p, DOWN, buff=0.25)
    return Group(p, s)


def runs_stage(counter_value=24):
    """The toy after phase 1: three sorted runs on disk, an empty tray."""
    flat = [v for run in TOY["runs"] for v in run]
    blocks = disk_blocks(flat)
    labels = VGroup(*[T(f"run {r + 1}", 22, MUTED, font=MONO)
                      .next_to(VGroup(*blocks[4 * r: 4 * r + 4]), DOWN, buff=0.14) for r in range(3)])
    return build_tray(), build_disk(1), blocks, labels, Counter(counter_value)


def two_scans_stamp():
    s = M('2 scans = 2 × <span foreground="#F2A93B">N/B</span> = 24 trips', 28, INK, font=MONO)
    return s.move_to([0, -3.05, 0])


def run_starts_x(plot_w=12.6):
    cols = STRIP["run_start_columns"]
    return [-plot_w / 2 + plot_w * c / 1600 for c in cols]


class S4Runs(CueScene):
    SEG = "s4"

    def construct(self):
        deck = sorted(TOY["deck"][:4]) + TOY["deck"][4:]      # S3 left block 0 sorted
        tray = build_tray()
        disk = build_disk(1)
        blocks = disk_blocks(deck)
        counter = Counter(12)
        self.add(tray, disk, *blocks, counter)

        # l1: the algorithm and its two phases
        self.at("l1")
        c = chip("Phase 1 · sorted runs")
        p1 = T("Phase 1: sorted runs", 30, INK, weight=MEDIUM)
        p2 = T("Phase 2: merge", 30, FAINT, weight=MEDIUM)
        phases = VGroup(p1, p2).arrange(RIGHT, buff=1.0).move_to([-0.9, 2.75, 0])
        self.play(FadeIn(c), FadeIn(phases, shift=0.1 * DOWN), counter.to(0), run_time=0.9)

        runs_mobs = []
        run_labels = VGroup()
        centers = row_centers(ROW1_Y)
        tag = T("+0", 26, ICE, font=MONO).next_to(counter, LEFT, buff=0.35)

        def form_run(r, t_up, t_sort, t_down, lag):
            src = blocks[4 * r: 4 * r + 4]
            ups = [b.copy() for b in src]
            frames = [amber_frame(b.get_center(), DISK_SCALE) for b in src]
            self.add(*ups, *frames)
            start = counter.value()
            self.play(LaggedStart(*[VGroup(u, f).animate.scale(1 / DISK_SCALE).move_to(tray_center(i))
                                    for i, (u, f) in enumerate(zip(ups, frames))], lag_ratio=lag),
                      *[b.animate.set_opacity(0.22) for b in src],
                      tick_at(counter, start, lagged_arrivals(4, t_up, lag), t_up), run_time=t_up)
            self.play(*[FadeOut(f) for f in frames], run_time=0.12)
            # sort inside memory: free
            cards = [card for u in ups for card in u]
            order = sorted(cards, key=lambda cd: cd.v)
            targets = [p for i in range(4) for p in block_positions(tray_center(i))]
            self.play(*[cd.animate.move_to(targets[order.index(cd)]) for cd in cards], FadeIn(tag),
                      run_time=t_sort, path_arc=0.6)
            self.play(FadeOut(tag), run_time=0.12)
            new_blocks = [VGroup(*order[4 * i: 4 * i + 4]) for i in range(4)]
            self.remove(*ups)
            self.add(*new_blocks)
            frames = [amber_frame(tray_center(i), 1.0) for i in range(4)]
            self.add(*frames)
            start = counter.value()
            self.play(LaggedStart(*[VGroup(nb, f).animate.scale(DISK_SCALE).move_to(centers[4 * r + i])
                                    for i, (nb, f) in enumerate(zip(new_blocks, frames))], lag_ratio=lag),
                      tick_at(counter, start, lagged_arrivals(4, t_down, lag), t_down), run_time=t_down)
            lab = T(f"run {r + 1}", 22, MUTED, font=MONO).next_to(VGroup(*new_blocks), DOWN, buff=0.14)
            self.play(*[FadeOut(f) for f in frames], *[FadeOut(b) for b in src], FadeIn(lab),
                      run_time=0.15)
            for i in range(4):
                blocks[4 * r + i] = new_blocks[i]
            run_labels.add(lab)

        # l2: fill memory, sort it (free), write a run
        self.at("l2", 0.1)
        form_run(0, 1.6, 1.4, 1.6, 0.3)
        # l3: repeat for the rest of the file
        self.at("l3")
        form_run(1, 0.5, 0.45, 0.5, 0.15)
        form_run(2, 0.5, 0.45, 0.5, 0.15)

        toy = Group(tray, disk, *blocks, run_labels, counter)
        # l4: the same thing at scale
        self.at("l4", 0.1)
        states = STRIP["states"]
        head = T("1,000,000 keys · memory holds 16% of them (the ratio of 16 GB to 100 GB)", 24, MUTED)
        head.move_to([0, 2.75, 0])
        g0 = strip_group(states[0])
        bounds = VGroup(*[DashedLine([x, -1.05, 0], [x, 2.1, 0], color=FAINT, stroke_width=1.5,
                                     dash_length=0.06) for x in run_starts_x()[1:-1]])
        self.play(FadeOut(toy), FadeOut(phases), run_time=0.45)
        self.play(FadeIn(g0), FadeIn(head), FadeIn(bounds), run_time=0.5)
        xs = run_starts_x()
        cur = g0
        rl = VGroup()
        for k in range(1, STRIP["runs"] + 1):
            nxt = strip_group(states[k])
            lab = T(f"run {k}", 20, MUTED, font=MONO).move_to([(xs[k - 1] + xs[k]) / 2, -1.9, 0])
            self.play(FadeIn(nxt), FadeIn(lab), run_time=0.27)
            self.remove(cur)
            cur = nxt
            rl.add(lab)

        # l5: two scans
        self.at("l5")
        cost = M('every block read once + written once = <span foreground="#F2A93B">2 scans</span>',
                 28, INK, font=MONO).move_to([0, -2.75, 0])
        self.play(FadeIn(cost, shift=0.1 * UP), run_time=0.6)

        # back to the toy for phase 2, with its count: 24 = 2 x 12
        self.until(self.end_of("l5", 0.6))
        self.play(FadeOut(Group(cur, rl, bounds, head, cost)), run_time=0.45)
        tray2, disk2, blocks2, labels2, counter2 = runs_stage(24)
        stamp = two_scans_stamp()
        self.play(FadeIn(Group(tray2, disk2, *blocks2, labels2, counter2)), FadeIn(stamp), run_time=0.5)
        self.finish()
