from PIL import Image

from v2kit import *

W_PANEL = 11.4                       # the merge sort trace, as in the race
H_PANEL = W_PANEL * 300 / 1400
X_PANEL, Y_PANEL = 0.35, 1.5
NP = RACE["passes"]["mergesort"]     # 18
PW = W_PANEL / NP                    # one pass, in scene units
IMG_LEFT = X_PANEL - W_PANEL / 2
BASE, UNIT = -2.95, 0.14             # the piece-size ladder (log scale)
N_SMALL = RACE["pieces_below_memory"]  # 14


def col_x(k):
    """Center of pass k (0-based) on the trace."""
    return IMG_LEFT + PW * (k + 0.5)


def trace_parts():
    """The merge sort trace split at pass 14, so the last four passes can slide."""
    a = np.array(Image.open(DATA / "race_mergesort.png"))
    cut = round(N_SMALL * 1400 / NP)
    left = ImageMobject(a[:, :cut]).stretch_to_fit_width(W_PANEL * cut / 1400).stretch_to_fit_height(H_PANEL)
    right = ImageMobject(a[:, cut:]).stretch_to_fit_width(W_PANEL * (1400 - cut) / 1400).stretch_to_fit_height(H_PANEL)
    left.move_to([IMG_LEFT, Y_PANEL, 0], aligned_edge=LEFT)
    right.next_to(left, RIGHT, buff=0)
    return left, right


def runs_pass_image():
    """One pass of run formation in the same style: read a memory-full, write it back, twelve times."""
    from scipy.ndimage import maximum_filter
    W, H = round(1400 / NP), 300
    nblocks, per = RACE["n"] // RACE["B"], RACE["M"] // RACE["B"]
    img = np.zeros((H, W), np.float32)
    steps = 2 * nblocks
    t = 0
    for r in range(nblocks // per):
        for phase in range(2):                       # read the run's blocks, then write them
            for b in range(r * per, (r + 1) * per):
                x = min(t * W // steps, W - 1)
                y = H - 1 - b * H // nblocks
                img[y, x] += 1
                t += 1
    img = maximum_filter(img, size=2)
    alpha = np.clip(img / 8.0, 0, 1) ** 0.5
    rgba = np.zeros((H, W, 4), np.uint8)
    rgba[..., :3] = [int(AMBER[i:i + 2], 16) for i in (1, 3, 5)]
    rgba[..., 3] = (alpha * 255).astype(np.uint8)
    m = ImageMobject(rgba).stretch_to_fit_width(PW).stretch_to_fit_height(H_PANEL)
    return m.move_to([IMG_LEFT, Y_PANEL, 0], aligned_edge=LEFT)


def pass_numbers(n, y):
    return VGroup(*[mono(str(k + 1), 15, FAINT).move_to([col_x(k), y, 0]) for k in range(n)])


def ladder():
    bars, labs = VGroup(), VGroup()
    for k in range(1, NP + 1):
        h = UNIT * k
        b = Rectangle(width=0.42, height=h, stroke_width=0, fill_color=MUTED, fill_opacity=0.85)
        b.move_to([col_x(k - 1), BASE + h / 2, 0])
        size = 2 ** k if k < NP else RACE["n"]
        if k <= 4:
            t = mono(f"{size:,}", 13, MUTED).next_to(b, UP, 0.06)
        else:
            t = mono(f"{size:,}", 13, BG).rotate(PI / 2).move_to(b).align_to(b, DOWN).shift(0.08 * UP)
        bars.add(b)
        labs.add(t)
    return bars, labs


class V2S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("Runs")
        # 01-02: merge sort's eighteen passes
        left, right = trace_parts()
        frame = Rectangle(width=W_PANEL + 0.1, height=H_PANEL + 0.1, stroke_color=DIM, stroke_width=1.5)
        frame.move_to([X_PANEL, Y_PANEL, 0])
        title = T("merge sort, from the race", 26, INK, weight=MEDIUM).next_to(frame, UP, 0.14, aligned_edge=LEFT)
        ylab = mono("position in file", 16, FAINT).rotate(PI / 2).next_to(frame, LEFT, 0.12)
        nums = pass_numbers(NP, frame.get_bottom()[1] - 0.2)
        pl = mono("pass", 15, FAINT).next_to(nums, LEFT, 0.25)
        self.at("01")
        self.play(FadeIn(c), FadeIn(Group(left, right, frame, title, ylab)), run_time=0.7)
        self.play(FadeIn(pl), LaggedStart(*[FadeIn(n, shift=0.05 * UP) for n in nums], lag_ratio=0.5), run_time=4.5)
        self.at("02")
        dbl = M('2<sup>18</sup> = 262,144 ≥ 261,120 items: <span foreground="#E6EBF0">18 passes</span>', 18, MUTED,
                font=MONO).next_to(frame, UP, 0.16).align_to(frame, RIGHT)
        self.play(FadeIn(dbl), run_time=0.6)

        # 03-04: the piece sizes against memory
        self.at("03")
        bars, labs = ladder()
        self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.25),
                  LaggedStart(*[FadeIn(t) for t in labs], lag_ratio=0.25), run_time=2.0)
        axis = mono("piece size after each pass (log scale)", 15, FAINT)
        mem_y = BASE + UNIT * math.log2(RACE["M"])
        mline = DashedLine([IMG_LEFT - 0.1, mem_y, 0], [IMG_LEFT + W_PANEL + 0.1, mem_y, 0], color=TRAY_EDGE,
                           stroke_width=2, dash_length=0.08)
        mlab = mono(f"memory holds {RACE['M']:,} items", 16, INK).next_to(mline, UP, 0.08).align_to(mline, LEFT)
        axis.next_to(mlab, UP, 0.1, aligned_edge=LEFT)
        self.play(FadeIn(axis), run_time=0.4)
        self.at("04")
        self.play(Create(mline), FadeIn(mlab), run_time=0.8)
        brace = Brace(bars[:N_SMALL], DOWN, buff=0.08, color=ICE)
        btxt = T("the first 14 passes: every piece smaller than memory", 18, ICE).next_to(brace, DOWN, 0.06)
        self.play(*[b.animate.set_fill(ICE) for b in bars[:N_SMALL]], FadeIn(brace), FadeIn(btxt), run_time=0.8)

        # 05-06: those pieces could have been sorted in memory, without the disk
        self.at("05")
        band = Rectangle(width=PW * N_SMALL, height=H_PANEL, stroke_width=0, fill_color=ICE, fill_opacity=0.14)
        band.move_to([IMG_LEFT, Y_PANEL, 0], aligned_edge=LEFT)
        self.play(FadeIn(band), run_time=0.6)
        self.at("06", 2.0)
        inmem = T("could have been sorted in memory: no I/O", 22, ICE).move_to(band).shift(0.55 * UP)
        bg = BackgroundRectangle(inmem, color=BG, fill_opacity=0.75, buff=0.1)
        self.play(FadeIn(bg), FadeIn(inmem), run_time=0.6)

        # 07-09: do exactly that, on the toy
        self.at("07")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.6)
        tray, disk = build_tray(), build_disk(1)
        blocks = disk_blocks(TOY["deck"])
        counter = Counter(0, title="I/Os")
        toy = mono("toy file: 12 blocks of 4 · memory holds 4 blocks", 18, MUTED).move_to([-0.6, 2.85, 0])
        self.play(FadeIn(tray), FadeIn(disk), FadeIn(VGroup(*blocks)), FadeIn(counter), FadeIn(toy), run_time=0.7)
        run_labels = VGroup()
        self.at("08", 0.1)
        tag = mono("sorting in memory: +0 I/Os", 20, ICE).next_to(tray[0], UP, 0.14).align_to(tray[0], RIGHT)
        form_run(self, blocks, counter, 0, 1.6, 1.4, 1.6, 0.3, run_labels, tag=tag)
        run_def = T("run: a sorted piece, written to disk", 22, INK)
        run_def.move_to([run_labels[0].get_x(), disk[0].get_bottom()[1] - 0.3, 0])
        self.play(FadeIn(run_def), run_time=0.4)
        self.at("09")
        self.play(FadeOut(run_def), run_time=0.2)
        form_run(self, blocks, counter, 1, 0.45, 0.4, 0.45, 0.15, run_labels)
        form_run(self, blocks, counter, 2, 0.45, 0.4, 0.45, 0.15, run_labels)

        # 10: the simulated file: twelve runs, in one pass
        self.at("10")
        onep = mono("12 blocks read + 12 written: one pass", 18, AMBER).next_to(counter, DOWN, 0.15).align_to(counter, RIGHT)
        self.play(FadeIn(onep), run_time=0.4)
        self.wait(0.8)
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        left, right = trace_parts()
        nums = pass_numbers(NP, frame.get_bottom()[1] - 0.2)
        title2 = T("the simulated file", 26, INK, weight=MEDIUM).move_to(title, aligned_edge=LEFT)
        self.play(FadeIn(Group(left, right, frame, title2, ylab, nums, pl)), run_time=0.6)
        band = Rectangle(width=PW * N_SMALL, height=H_PANEL, stroke_width=0, fill_color=ICE, fill_opacity=0.14)
        band.move_to([IMG_LEFT, Y_PANEL, 0], aligned_edge=LEFT)
        rp = runs_pass_image()
        rp_band = Rectangle(width=PW, height=H_PANEL, stroke_width=0, fill_color=ICE, fill_opacity=0.22)
        rp_band.move_to(rp)
        rp_lab = mono("pass 1: make 12 runs", 16, ICE)
        rp_lab.next_to(frame, DOWN, 0.5).align_to(frame, LEFT)
        self.play(FadeIn(band), run_time=0.5)

        # 11: the runs pass replaces the first fourteen; the last four remain
        self.at("11")
        self.play(FadeOut(left), FadeOut(nums[:N_SMALL]), band.animate.set_fill(opacity=0.06), run_time=0.8)
        self.play(FadeIn(rp_band), FadeIn(rp), run_time=0.6)
        self.play(FadeOut(band), right.animate.next_to(rp, RIGHT, buff=0),
                  *[n.animate.move_to([col_x(k + 1), n.get_y(), 0]) for k, n in enumerate(nums[N_SMALL:])],
                  frame.animate.stretch_to_fit_width(PW * 5 + 0.1).move_to([IMG_LEFT - 0.05, Y_PANEL, 0], aligned_edge=LEFT),
                  run_time=1.4)
        new_nums = pass_numbers(5, nums.get_y())
        self.play(FadeIn(new_nums[0]), *[ReplacementTransform(nums[N_SMALL + k], new_nums[k + 1]) for k in range(4)],
                  FadeIn(rp_lab), run_time=0.6)
        last4 = mono("passes 2-5: the last 4 merge passes", 16, MUTED).next_to(rp_lab, DOWN, 0.12, aligned_edge=LEFT)
        self.play(FadeIn(last4), run_time=0.4)

        # 12: eighteen passes become five
        self.at("12")
        tally = M('<span foreground="#56606B">18 passes →</span> 5 passes = 1 + 4', 34, INK, font=MONO)
        tally.next_to(frame, RIGHT, 0.7)
        self.play(FadeIn(tally, shift=0.1 * LEFT), run_time=0.6)

        # 13: sort's twelve files were runs
        self.at("13")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.5)
        tmp = TmpFolder([-1.75, -0.3, 0], width=7.4, height=3.5)
        tmp.tt.set_value(peak_time())
        n = len(tmp.names)
        for i, nm in enumerate(tmp.names):
            tmp.labels[nm] = f"run {i + 1}" + (" · partly full" if i == n - 1 else "")
        rows = tmp.draw()
        head = T("sort's temporary folder at its fullest", 26, INK, weight=MEDIUM).next_to(tmp.panel, UP, 0.25,
                                                                                           aligned_edge=LEFT)
        self.play(FadeIn(tmp.panel), FadeIn(tmp.title), FadeIn(head), FadeIn(rows), run_time=0.7)
        ratio = VGroup(mono("1,000 MB ÷ 86 MB ≈ 11.6", 22, MUTED),
                       M('so <span foreground="#8FD3FF">12 runs</span>', 26, INK, font=MONO))
        ratio.arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(tmp.panel, RIGHT, 0.45)
        self.play(FadeIn(ratio[0]), run_time=0.5)
        self.play(FadeIn(ratio[1]), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
