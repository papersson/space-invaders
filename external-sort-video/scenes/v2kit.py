"""Reusable pieces for the version 2 scenes: real-capture replays, the race, the toy's
run formation and multiway merge, and small diagram helpers."""
import heapq
import math

from common import *

SORTCAP = json.loads((CAPTURES / "gnu_sort_tmp.json").read_text())
PYCAP = json.loads((CAPTURES / "python_memoryerror.json").read_text())
RACE = json.loads((DATA / "race.json").read_text())
TOY = json.loads((DATA / "toy.json").read_text())
CORAL = "#E4715F"          # errors only
BUDGET_B = 86_000_000       # sort's -S and Python's address-space cap, in bytes


def mono(s, size=20, color=INK):
    return T(s, size, color, font=MONO)


def terminal(w, h, title):
    r = RoundedRectangle(corner_radius=0.14, width=w, height=h, stroke_color=DIM, stroke_width=2,
                         fill_color="#0B0F13", fill_opacity=1)
    t = label(title, 16, FAINT).next_to(r.get_corner(UL), DR, buff=0.14)
    return VGroup(r, t)


def file_and_memory_bars(width=11.0, y_file=2.95, y_mem=1.95, x_left=-5.6):
    """The opening picture: the 1 GB file as a noise strip, and the 86 MB budget to scale."""
    from s4_runs import STRIP, strip_images
    _, noise = strip_images(STRIP["states"][0], strip_h=10)
    fbar = ImageMobject(noise).stretch_to_fit_width(width).stretch_to_fit_height(0.42)
    fbar.move_to([x_left, y_file, 0], aligned_edge=LEFT)
    flab = mono("records.txt · 1,000 MB (10,000-byte records)", 20, INK).next_to(fbar, UP, 0.1, aligned_edge=LEFT)
    mbar = Rectangle(width=width * 86 / 1000, height=0.42, stroke_color=TRAY_EDGE, stroke_width=2.5,
                     fill_color=TRAY_FILL, fill_opacity=1).move_to([x_left, y_mem, 0], aligned_edge=LEFT)
    mlab = mono("memory we allow: 86 MB", 20, INK).next_to(mbar, RIGHT, 0.25)
    return Group(fbar, flab, mbar, mlab)


class TmpFolder:
    """Replays the /tmp listing from the real GNU sort capture."""

    def __init__(self, center, width=6.6, height=3.35):
        self.panel = RoundedRectangle(corner_radius=0.14, width=width, height=height, stroke_color=DIM,
                                      stroke_width=2, fill_color=PANEL, fill_opacity=1).move_to(center)
        self.title = mono("/tmp", 16, FAINT).next_to(self.panel.get_corner(UL), DR, buff=0.12)
        self.names = []
        for s in SORTCAP["samples"]:
            for f in s["tmp_files"]:
                if f["name"] not in self.names:
                    self.names.append(f["name"])
        self.full = max(f["bytes"] for s in SORTCAP["samples"] for f in s["tmp_files"])
        top = self.panel.get_top()[1]
        self.row_y = [top - 0.52 - 0.21 * i for i in range(len(self.names))]
        self.x0 = self.panel.get_left()[0] + 0.25
        self.tt = ValueTracker(0.0)
        self.cache = {}
        self.labels = {}

    def _text(self, key, s, color, size=14):
        if key not in self.cache:
            self.cache[key] = mono(s, size, color)
        return self.cache[key].copy()

    def sample_at(self, t):
        cur = SORTCAP["samples"][0]
        for s in SORTCAP["samples"]:
            if s["t"] <= t:
                cur = s
        return cur

    def draw(self, rows_only=False):
        s = self.sample_at(self.tt.get_value())
        g = VGroup()
        present = {f["name"]: f["bytes"] for f in s["tmp_files"]}
        for i, nm in enumerate(self.names):
            if nm not in present:
                continue
            y = self.row_y[i]
            g.add(self._text(("n", nm), nm, INK).move_to([self.x0, y, 0], aligned_edge=LEFT))
            w = 3.2 * present[nm] / self.full
            g.add(Rectangle(width=max(w, 0.01), height=0.1, stroke_width=0, fill_color=MUTED,
                            fill_opacity=0.8).move_to([self.x0 + 1.55, y, 0], aligned_edge=LEFT))
            if nm in self.labels:
                g.add(self._text(("l", nm), self.labels[nm], ICE).move_to([self.x0 + 5.0, y, 0], aligned_edge=LEFT))
        if rows_only:
            return g
        out = s["output_bytes"]
        yo = self.panel.get_bottom()[1] + 0.3
        g.add(self._text(("o",), "sorted.txt", ICE).move_to([self.x0, yo, 0], aligned_edge=LEFT))
        g.add(Rectangle(width=max(3.2 * out / SORTCAP["input_bytes"], 0.01), height=0.1, stroke_width=0,
                        fill_color=ICE, fill_opacity=0.9).move_to([self.x0 + 1.55, yo, 0], aligned_edge=LEFT))
        mb = out // 10 ** 6
        g.add(self._text(("om", mb), f"{mb:,} MB", MUTED).move_to([self.x0 + 5.0, yo, 0], aligned_edge=LEFT))
        n = len(present)
        g.add(self._text(("c", n), f"{n} temp files", MUTED).move_to(
            [self.panel.get_right()[0] - 0.25, self.panel.get_top()[1] - 0.2, 0], aligned_edge=RIGHT))
        return g

    def mobject(self):
        return always_redraw(self.draw)


def peak_time():
    """Capture time when all twelve runs exist at full size, before the merge starts."""
    best = None
    for s in SORTCAP["samples"]:
        if len(s["tmp_files"]) == SORTCAP["n_temp_files_max"] and s["output_bytes"] == 0:
            best = s["t"]
    return best


def merge_start_time():
    return next(s["t"] for s in SORTCAP["samples"] if s["output_bytes"] > 0)


# --- the race (heapsort vs merge sort under virtual memory) ----------------------------------
def race_panels(width=11.4, ys=(1.55, -1.75), x=0.35):
    H = width * 300 / 1400
    panels = []
    for name, key, y in (("heapsort", "heapsort", ys[0]), ("merge sort", "mergesort", ys[1])):
        img = ImageMobject(str(DATA / f"race_{key}.png"))
        img.stretch_to_fit_width(width).stretch_to_fit_height(H).move_to([x, y, 0])
        frame = Rectangle(width=width + 0.1, height=H + 0.1, stroke_color=DIM, stroke_width=1.5).move_to(img)
        title = T(name, 28, INK, weight=MEDIUM).next_to(frame, UP, 0.12, aligned_edge=LEFT)
        cnt = Counter(0, title="I/Os", size=34, anchor=frame.get_corner(UR) + np.array([0, 0.62, 0]))
        ylab = T("position in file", 16, FAINT, font=MONO).rotate(PI / 2).next_to(frame, LEFT, 0.12)
        p = dict(img=img, frame=frame, title=title, cnt=cnt, key=key, ylab=ylab, curtain_p=ValueTracker(0.0))

        def make_curtain(fr=frame, tr=p["curtain_p"]):
            x0 = fr.get_left()[0] + fr.width * tr.get_value()
            w = max(fr.get_right()[0] - x0, 0.001)
            r = Rectangle(width=w, height=fr.height - 0.06, fill_color=BG, fill_opacity=1, stroke_width=0)
            return r.move_to([x0 + w / 2, fr.get_center()[1], 0])
        p["curtain"] = always_redraw(make_curtain)
        panels.append(p)
    return panels


def reveal(scene, p, run_time):
    cum = RACE[p["key"]]["cum_by_column"]
    head = Line(UP, DOWN, stroke_color=ICE, stroke_width=2).set_height(p["frame"].height)
    head.add_updater(lambda m: m.move_to([p["frame"].get_left()[0] + p["frame"].width * p["curtain_p"].get_value(),
                                          p["frame"].get_y(), 0]))
    scene.add(head)

    def upd(m, a):
        p["curtain_p"].set_value(a)
        p["cnt"].tracker.set_value(cum[min(int(a * (len(cum) - 1)), len(cum) - 1)] if a < 1 else cum[-1])
    scene.play(UpdateFromAlphaFunc(p["cnt"].tracker, upd, rate_func=linear), run_time=run_time)
    scene.remove(head)


# --- toy run formation --------------------------------------------------------------------
def form_run(scene, blocks, counter, r, t_up, t_sort, t_down, lag, run_labels, tag=None):
    """Phase 1 on the toy: four blocks up, sort in memory (no I/O), four blocks down as a run."""
    centers = row_centers(ROW1_Y)
    src = blocks[4 * r: 4 * r + 4]
    ups = [b.copy() for b in src]
    frames = [amber_frame(b.get_center(), DISK_SCALE) for b in src]
    scene.add(*ups, *frames)
    start = counter.value()
    scene.play(LaggedStart(*[VGroup(u, f).animate.scale(1 / DISK_SCALE).move_to(tray_center(i))
                             for i, (u, f) in enumerate(zip(ups, frames))], lag_ratio=lag),
               *[b.animate.set_opacity(0.22) for b in src],
               tick_at(counter, start, lagged_arrivals(4, t_up, lag), t_up), run_time=t_up)
    scene.play(*[FadeOut(f) for f in frames], run_time=0.12)
    cards = [card for u in ups for card in u]
    order = sorted(cards, key=lambda cd: cd.v)
    targets = [p for i in range(4) for p in block_positions(tray_center(i))]
    extra = [FadeIn(tag)] if tag is not None else []
    scene.play(*[cd.animate.move_to(targets[order.index(cd)]) for cd in cards], *extra,
               run_time=t_sort, path_arc=0.6)
    if tag is not None:
        scene.play(FadeOut(tag), run_time=0.12)
    new_blocks = [VGroup(*order[4 * i: 4 * i + 4]) for i in range(4)]
    scene.remove(*ups)
    scene.add(*new_blocks)
    frames = [amber_frame(tray_center(i), 1.0) for i in range(4)]
    scene.add(*frames)
    start = counter.value()
    scene.play(LaggedStart(*[VGroup(nb, f).animate.scale(DISK_SCALE).move_to(centers[4 * r + i])
                             for i, (nb, f) in enumerate(zip(new_blocks, frames))], lag_ratio=lag),
               tick_at(counter, start, lagged_arrivals(4, t_down, lag), t_down), run_time=t_down)
    lab = T(f"run {r + 1}", 22, MUTED, font=MONO).next_to(VGroup(*new_blocks), DOWN, buff=0.14)
    scene.play(*[FadeOut(f) for f in frames], *[FadeOut(b) for b in src], FadeIn(lab), run_time=0.15)
    for i in range(4):
        blocks[4 * r + i] = new_blocks[i]
    run_labels.add(lab)


# --- toy multiway merge -------------------------------------------------------------------
HEAP_POS = [np.array([-1.4, 3.02, 0]), np.array([-2.75, 2.28, 0]), np.array([-0.05, 2.28, 0])]


def slot_label(i, text, color=MUTED):
    return T(text, 20, color, font=MONO).move_to(tray_center(i) + np.array([0, -0.98, 0]))


def front(cards):
    for c in cards:
        if c is not None:
            return c
    return None


def heap_view(fronts):
    items = sorted(fronts.items(), key=lambda kv: kv[1].v)
    order = [items[0]] + sorted(items[1:], key=lambda kv: kv[0]) if items else []
    g = VGroup()
    g.add(VGroup(*[Line(HEAP_POS[0], HEAP_POS[k], stroke_color=FAINT, stroke_width=2).scale(0.62) for k in (1, 2)]))
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


def two_way_snapshot():
    """A real mid-merge state of a two-way merge of (run 1 + run 2) with run 3."""
    runs = TOY["runs"]
    a, b = sorted(runs[0] + runs[1]), runs[2]
    rr = [a, b]
    pos = [0, 0]
    hp = [(a[0], 0), (b[0], 1)]
    out = []
    while len(out) < 11:
        v, r = heapq.heappop(hp)
        out.append(v)
        pos[r] += 1
        heapq.heappush(hp, (rr[r][pos[r]], r))
    g = VGroup()
    for r in (0, 1):
        blk = pos[r] // 4
        cards = make_block(rr[r][4 * blk: 4 * blk + 4], tray_center(r))
        for i in range(pos[r] % 4):
            cards[i].set_opacity(0)
        g.add(cards)
    kept = out[len(out) - len(out) % 4:]
    g.add(VGroup(*[Card(v).move_to(p) for v, p in zip(kept, block_positions(tray_center(3)))]))
    return g


def pass_tally(text, size=30):
    """Pass counter written as a sum, e.g. "5 passes = 1 + 4"."""
    return M(text, size, INK, font=MONO)
