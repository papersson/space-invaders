"""Shared look and timing for every scene.

Style rules (see PLAN.md): memory on top and bright, disk at the bottom and dim;
only whole blocks travel between them; values are color *and* number; amber is
reserved for cost (block transfers, the trip counter); ice marks a selection.
"""
import json
from pathlib import Path

import numpy as np
from manim import *

ROOT = Path(__file__).resolve().parent.parent
DATA, AUDIO, CAPTURES = ROOT / "data", ROOT / "audio", ROOT / "captures"

BG = "#0F1318"
INK = "#E6EBF0"
MUTED = "#8C97A4"
FAINT = "#56606B"
DIM = "#2B333C"
PANEL = "#151B22"
TRAY_FILL = "#17202A"
TRAY_EDGE = "#C9D3DD"
AMBER = "#F2A93B"
ICE = "#8FD3FF"
IDLE = "#3E4750"

SANS = "IBM Plex Sans"
MONO = "IBM Plex Mono"

config.background_color = BG

# --- value colors: seaborn "mako", trimmed so the darkest cards still read on BG
_MAKO = None


def vcolor(x):
    global _MAKO
    if _MAKO is None:
        import seaborn as sns
        _MAKO = sns.color_palette("mako", as_cmap=True)
    r, g, b, _ = _MAKO(0.22 + 0.74 * float(np.clip(x, 0, 1)))
    return ManimColor.from_rgb((r, g, b))


def ink_on(x):
    c = vcolor(x).to_rgb()
    lum = 0.2126 * c[0] ** 2.2 + 0.7152 * c[1] ** 2.2 + 0.0722 * c[2] ** 2.2
    return BG if lum > 0.28 else INK


# Pango lays out small sizes with broken kerning, so text is set 4x large and scaled down.
# Manim renders text into a canvas as wide as the video (Text) or 600 px (MarkupText) and
# wraps at that width; at 4x that wraps ordinary lines, so give Pango a wide canvas instead.
_K = 4

import manimpango
from manimpango import MarkupUtils

_text2svg = manimpango.text2svg
_markup2svg = MarkupUtils.text2svg


def _wide_text2svg(settings, size, line_spacing, liga, file_name, sx, sy, w, h, orig, pango_width=None):
    return _text2svg(settings, size, line_spacing, liga, file_name, sx, sy, 16000, 4000, orig, None)


def _wide_markup2svg(text, font, slant, weight, size, ls, liga, file_name, sx, sy, w, h, **kw):
    kw["pango_width"] = None
    return _markup2svg(text, font, slant, weight, size, ls, liga, file_name, sx, sy, 16000, 4000, **kw)


manimpango.text2svg = _wide_text2svg
MarkupUtils.text2svg = staticmethod(_wide_markup2svg)


def T(s, size=30, color=INK, font=SANS, weight=NORMAL, **kw):
    return Text(s, font=font, font_size=size * _K, color=color, weight=weight, **kw).scale(1 / _K)


def M(s, size=30, color=INK, font=SANS, weight=NORMAL, **kw):
    return MarkupText(s, font=font, font_size=size * _K, color=color, weight=weight, **kw).scale(1 / _K)


def label(s, size=20, color=MUTED):
    """Small uppercase label."""
    return T(s.upper(), size, color, font=MONO, weight=MEDIUM)


# --- cards and blocks -------------------------------------------------------------
CARD_W, CARD_H, CARD_GAP = 0.54, 0.78, 0.06
BLOCK_B = 4
BLOCK_W = BLOCK_B * CARD_W + (BLOCK_B - 1) * CARD_GAP
SLOT_PAD = 0.09
DISK_SCALE = 0.37


class Card(VGroup):
    def __init__(self, v, vmax=48, num=True, **kw):
        super().__init__(**kw)
        self.v = v
        x = (v - 1) / (vmax - 1)
        self.x = x
        self.rect = RoundedRectangle(corner_radius=0.07, width=CARD_W, height=CARD_H,
                                     stroke_width=0, fill_color=vcolor(x), fill_opacity=1)
        self.add(self.rect)
        if num:
            t = Text(str(v), font=MONO, weight=MEDIUM, color=ink_on(x), font_size=40)
            t.scale_to_fit_height(CARD_H * 0.25).move_to(self.rect)
            self.add(t)


def block_positions(center, scale=1.0):
    """Centers of the B card positions of a block centered at `center`."""
    step = (CARD_W + CARD_GAP) * scale
    x0 = -step * (BLOCK_B - 1) / 2
    return [np.array(center) + np.array([x0 + i * step, 0, 0]) for i in range(BLOCK_B)]


def make_block(values, center, scale=1.0, vmax=48):
    cards = VGroup(*[Card(v, vmax) for v in values])
    for c, p in zip(cards, block_positions(center, scale)):
        c.scale(scale).move_to(p)
    return cards


def slot(center, scale=1.0, color=DIM, width=2.2, fill=None, fill_opacity=0.0):
    w = (BLOCK_W + 2 * SLOT_PAD) * scale
    h = (CARD_H + 2 * SLOT_PAD) * scale
    r = RoundedRectangle(corner_radius=0.1 * scale + 0.02, width=w, height=h, stroke_color=color,
                         stroke_width=width, fill_color=fill or BG, fill_opacity=fill_opacity)
    return r.move_to(center)


SLOT_W = BLOCK_W + 2 * SLOT_PAD
DISK_SLOT_W = SLOT_W * DISK_SCALE
DISK_GAP = 0.1
RUN_GAP = 0.3


def disk_row_centers(y, n_blocks=12, run_len=4, gap=DISK_GAP, run_gap=RUN_GAP):
    xs, x = [], 0.0
    for i in range(n_blocks):
        if i:
            x += DISK_SLOT_W + gap + (run_gap if i % run_len == 0 else 0)
        xs.append(x)
    off = (xs[0] + xs[-1]) / 2
    return [np.array([xx - off, y, 0]) for xx in xs]


# --- the trip counter --------------------------------------------------------------
class Counter(VGroup):
    """Amber number with a small label. Animate with `counter.to(n)`."""

    def __init__(self, value=0, title="TRIPS", size=44, anchor=None, color=AMBER, **kw):
        super().__init__(**kw)
        self.color = color
        self.tracker = ValueTracker(value)
        self.size = size
        self._cache = {}
        self.title = T(title, size * 0.38, MUTED, font=MONO, weight=MEDIUM)
        self.anchor = np.array(anchor if anchor is not None else [6.55, 3.3, 0])
        self.num = self._text(value)
        self._place()
        def update(m):
            m.become(self._text(int(round(self.tracker.get_value()))))
            self._align(m)
        self.num.add_updater(update)
        self.add(self.title, self.num)

    def _text(self, v):
        if v not in self._cache:
            self._cache[v] = Text(f"{v:,}", font=MONO, font_size=self.size, color=self.color,
                                  weight=MEDIUM)
        return self._cache[v].copy()

    def _align(self, m):
        m.next_to(self.title, DOWN, buff=0.08, aligned_edge=RIGHT)

    def _place(self):
        self.title.move_to(self.anchor, aligned_edge=RIGHT)
        self._align(self.num)

    def to(self, n, **kw):
        return self.tracker.animate(**kw).set_value(n)

    def value(self):
        return int(round(self.tracker.get_value()))


# --- scene with narration cues -----------------------------------------------------
_TIMINGS = None


def timings():
    global _TIMINGS
    if _TIMINGS is None:
        _TIMINGS = json.loads((AUDIO / "timings.json").read_text())
    return _TIMINGS


class CueScene(Scene):
    SEG = None

    def setup(self):
        seg = next(s for s in timings()["segments"] if s["id"] == self.SEG)
        self.t0, self.dur = seg["start"], seg["end"] - seg["start"]
        self.cues = {l["id"].split("_")[1]: (l["start"] - self.t0, l["end"] - self.t0)
                     for l in seg["lines"]}

    def now(self):
        return self.renderer.time

    def until(self, t):
        dt = t - self.now()
        if dt > 1 / 60:
            self.wait(dt)

    def at(self, lid, dt=0.0):
        self.until(self.cues[lid][0] + dt)

    def end_of(self, lid, dt=0.0):
        return self.cues[lid][1] + dt

    def start_of(self, lid, dt=0.0):
        return self.cues[lid][0] + dt

    def finish(self):
        self.until(self.dur)


def chip(text, color=MUTED):
    """Top-left section marker."""
    return label(text, 20, color).to_corner(UL, buff=0.45)


# --- the fixed stage: memory tray on top, disk panel below ---------------------------
TRAY_Y = 1.0
TRAY_XS = [-4.2, -1.4, 1.4, 4.2]
ROW1_Y, ROW2_Y = -1.72, -2.82


def tray_center(i):
    return np.array([TRAY_XS[i], TRAY_Y, 0.0])


def build_tray():
    frame = RoundedRectangle(corner_radius=0.18, width=11.7, height=1.5, stroke_color=TRAY_EDGE,
                             stroke_width=2.5, fill_color=TRAY_FILL, fill_opacity=1)
    frame.move_to([0, TRAY_Y, 0])
    slots = VGroup(*[slot(tray_center(i), 1.0, color=FAINT, width=1.6) for i in range(4)])
    lab = label("memory", 20, INK).next_to(frame, UP, buff=0.14, aligned_edge=LEFT)
    return VGroup(frame, slots, lab)


def row_centers(y):
    return disk_row_centers(y)


def disk_panel(rows=1):
    top = ROW1_Y + 0.55
    bottom = (ROW1_Y if rows == 1 else ROW2_Y) - 0.66
    r = RoundedRectangle(corner_radius=0.16, width=13.5, height=top - bottom, stroke_color=DIM,
                         stroke_width=2, fill_color=PANEL, fill_opacity=1)
    return r.move_to([0, (top + bottom) / 2, 0])


def build_disk(rows=1):
    panel = disk_panel(rows)
    lab = label("disk", 20, MUTED).next_to(panel, UP, buff=0.14, aligned_edge=LEFT)
    slots1 = VGroup(*[slot(c, DISK_SCALE, color=DIM, width=1.4) for c in row_centers(ROW1_Y)])
    g = VGroup(panel, lab, slots1)
    if rows == 2:
        g.add(VGroup(*[slot(c, DISK_SCALE, color=DIM, width=1.4) for c in row_centers(ROW2_Y)]))
    return g


def disk_blocks(values, y=ROW1_Y, vmax=48):
    """One VGroup of cards per block, laid out on a disk row."""
    return [make_block(values[i * BLOCK_B:(i + 1) * BLOCK_B], c, DISK_SCALE, vmax)
            for i, c in enumerate(row_centers(y)[: len(values) // BLOCK_B])]


def move_block(cards, dst_center, dst_scale, src_scale, **kw):
    """Animate a block of cards to a new slot, rescaling (disk <-> memory)."""
    k = dst_scale / src_scale
    return cards.animate(**kw).scale(k).move_to(dst_center)


def amber_frame(center, scale):
    return slot(center, scale, color=AMBER, width=3)


def transfer(scene, cards, dst_center, dst_scale, src_scale, counter=None, run_time=0.6,
             copy_from=None):
    """Move a block between disk and memory with an amber outline; tick the counter.

    With copy_from set, `cards` is left in place (dimmed) and a copy travels, like a read.
    Returns the mobject that ends at the destination."""
    mover = cards.copy() if copy_from else cards
    if copy_from:
        scene.add(mover)
    fr = amber_frame(mover.get_center(), src_scale)
    grp = VGroup(mover, fr)
    anims = [grp.animate.scale(dst_scale / src_scale).move_to(dst_center)]
    if copy_from:
        anims.append(cards.animate.set_opacity(0.22))
    if counter is not None:
        anims.append(counter.to(counter.value() + 1))
    scene.play(*anims, run_time=run_time, rate_func=smooth)
    scene.play(FadeOut(fr), run_time=0.15)
    return mover


def tick_at(counter, start, arrivals, run_time):
    """Counter animation that steps +1 at each arrival time (seconds into the play call)."""
    arrivals = sorted(arrivals)

    def upd(m, a):
        t = a * run_time + 1e-6
        counter.tracker.set_value(start + sum(1 for x in arrivals if x <= t))
    return UpdateFromAlphaFunc(counter.tracker, upd, rate_func=linear)


def lagged_arrivals(n, run_time, lag_ratio, frac=1.0):
    """Arrival times for LaggedStart(n anims, lag_ratio) played over run_time."""
    d = run_time / (1 + lag_ratio * (n - 1))
    return [k * lag_ratio * d + frac * d for k in range(n)]
