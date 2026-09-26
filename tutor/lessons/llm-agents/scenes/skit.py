"""Pieces shared by the LLM-agents scenes.

The central picture is the context: a strip of cards along the bottom of the frame, one card per
message, replayed from the real runs (data/strips.json, made by sims/make_data.py from captures/).
Colours are bound to parts of the picture in every chapter: grey instructions, white task, blue what
the model wrote, green tool results, red a failing test, amber tokens read.
Fixed geography from chapter 2 on: the model box above, "our code" to the right, the project's
files at the top right, the strip along the bottom.
"""
import inspect
import json
import sys

from common import *

S = json.loads((DATA / "strips.json").read_text())
sys.path.insert(0, str(ROOT / "sims"))
import agent as AGENT  # noqa: E402  (the real loop, shown on screen from its source)

GREEN = "#7FD6A4"      # tool results: the world's answers
BLUE = ICE             # the model's writing
CLI_GREY = "#39414A"   # notes the command-line tool adds
OUR_GREY = "#66717C"   # our instructions
CARD_W, CARD_H, GAP = 0.6, 0.78, 0.06
INSTR_W = 1.3
X0 = -6.6

MODEL_POS = np.array([-0.8, 2.45, 0])
CODE_POS = np.array([3.05, 0.55, 0])
FILES_X = 5.55


def mono_b(s, size, color=INK):
    return T(s, size, color, font=MONO, weight=MEDIUM)


# --- cards --------------------------------------------------------------------------------------
def card_items(run):
    """Cards for the card view: the tool's notes and our instructions are one grey card."""
    cs = S[run]["cards"]
    return [{"kind": "instr", "label": "instructions"}] + cs[2:]


def make_card(c, final_label=None):
    kind = c["kind"]
    w = INSTR_W if kind == "instr" else CARD_W
    g = VGroup()
    if kind == "instr":
        box = RoundedRectangle(corner_radius=0.07, width=w, height=CARD_H, stroke_width=0,
                               fill_color=OUR_GREY, fill_opacity=1)
        g.add(box, mono("instructions", 11, INK).move_to(box))
    elif kind == "task":
        box = RoundedRectangle(corner_radius=0.07, width=w, height=CARD_H, stroke_color=INK, stroke_width=2,
                               fill_color=PANEL, fill_opacity=1)
        g.add(box, mono("task", 13, INK).move_to(box))
    elif kind == "model":
        box = RoundedRectangle(corner_radius=0.07, width=w, height=CARD_H, stroke_width=0,
                               fill_color=BLUE, fill_opacity=0.92)
        lab = final_label or c["label"]
        top = mono_b(lab, 13 if len(lab) <= 5 else 11, BG)
        sub = c.get("sub", "")
        short = {"test_report.py": "test", "report.py": "report", "sales.csv": "csv"}.get(sub, sub)
        if short:
            txt = VGroup(top, mono(short, 11, BG)).arrange(DOWN, buff=0.06)
        else:
            txt = VGroup(top)
        g.add(box, txt.move_to(box))
    else:  # result
        box = RoundedRectangle(corner_radius=0.07, width=w, height=CARD_H, stroke_width=0,
                               fill_color=GREEN, fill_opacity=0.88)
        g.add(box)
        marks = c.get("marks", [])
        if "fail" in marks:
            g.add(cross(box.get_center(), 0.16, CORAL, 6))
        if "pass" in marks:
            g.add(check(box.get_center(), 0.9, BG, 6))
        if "bom" in marks:
            g.add(Dot(box.get_corner(UL) + [0.12, -0.12, 0], radius=0.06, color=INK))
    g.kind = kind
    g.data = c
    return g


def cross(c, s=0.14, color=CORAL, width=5):
    c = np.array(c)
    return VGroup(Line(c + [-s, -s, 0], c + [s, s, 0], stroke_color=color, stroke_width=width),
                  Line(c + [-s, s, 0], c + [s, -s, 0], stroke_color=color, stroke_width=width))


def check(c, k=1.0, color=GREEN, width=5):
    c = np.array(c)
    return VMobject(stroke_color=color, stroke_width=width).set_points_as_corners(
        [c + k * np.array([-0.13, 0.0, 0]), c + k * np.array([-0.04, -0.1, 0]), c + k * np.array([0.14, 0.13, 0])])


class Strip(VGroup):
    """A run's context as cards in a row. Cards are built at their slots; scenes reveal them."""

    def __init__(self, run, y, x0=X0, labels=None, upto=None):
        super().__init__()
        self.run, self.y, self.x0 = run, y, x0
        items = card_items(run)
        if upto is not None:
            items = items[:upto]
        self.items = items
        self.cards = []
        x = x0
        for i, c in enumerate(items):
            lab = None
            if labels and i in labels:
                lab = labels[i]
            m = make_card(c, lab)
            w = m[0].width
            m.move_to([x + w / 2, y, 0])
            x += w + GAP
            self.cards.append(m)
        self.right = x - GAP

    def slot(self, i):
        return self.cards[i].get_center()

    def first(self, n):
        return VGroup(*self.cards[:n])


def grow_in(card, source, run_time=0.45):
    """A card leaves `source` (a point or mobject) and lands in its slot."""
    target = card.copy()
    card.scale(0.55).move_to(source.get_center() if hasattr(source, "get_center") else source)
    card.set_opacity(0.0)
    return Transform(card, target, run_time=run_time, rate_func=smooth)


def band_sweep(strip_or_group, run_time=0.6, color=ICE):
    """A light band sweeping the strip from left to right: the model reading all of it."""
    g = strip_or_group
    h = g.height + 0.22
    band = Rectangle(width=0.35, height=h, stroke_width=0, fill_color=color, fill_opacity=0.28)
    band.move_to([g.get_left()[0] + 0.17, g.get_center()[1], 0])
    return band, band.animate(run_time=run_time, rate_func=linear).move_to(
        [g.get_right()[0] - 0.17, g.get_center()[1], 0])


# --- the fixed picture --------------------------------------------------------------------------
def model_box(tag=True):
    box = RoundedRectangle(corner_radius=0.14, width=2.3, height=0.95, stroke_color=BLUE, stroke_width=2.5,
                           fill_color=PANEL, fill_opacity=1).move_to(MODEL_POS)
    g = VGroup(box, T("model", 28, INK).move_to(box))
    if tag:
        g.add(mono("claude -p, tools off", 13, MUTED).next_to(box, DOWN, 0.1))
    return g


def code_box():
    box = RoundedRectangle(corner_radius=0.12, width=2.1, height=0.8, stroke_color=TRAY_EDGE, stroke_width=2,
                           fill_color=PANEL, fill_opacity=1).move_to(CODE_POS)
    return VGroup(box, mono("our code", 19, INK).move_to(box))


class Project(VGroup):
    """The three files at the top right, with the test's state beside test_report.py."""

    def __init__(self, top=3.05, x=FILES_X, failing=True):
        super().__init__()
        self.files = {}
        y = top
        for name in ["report.py", "test_report.py", "sales.csv"]:
            box = RoundedRectangle(corner_radius=0.07, width=2.05, height=0.42, stroke_color=FAINT, stroke_width=1.5,
                                   fill_color=PANEL, fill_opacity=1).move_to([x, y, 0])
            f = VGroup(box, mono(name, 15, INK).move_to(box))
            self.files[name] = f
            self.add(f)
            y -= 0.52
        self.badge_pos = self.files["test_report.py"][0].get_left() + LEFT * 0.28
        self.badge = cross(self.badge_pos, 0.1, CORAL, 5) if failing else check(self.badge_pos, 0.8, GREEN, 5)
        self.add(self.badge)

    def passing(self):
        new = check(self.badge_pos, 0.8, GREEN, 5)
        return new


def quote(lines, size=15, width=None, color=INK, title=None, border=DIM):
    """A panel of real text, one entry per line: (text, color) or text."""
    rows = VGroup()
    for ln in lines:
        txt, col = (ln, color) if isinstance(ln, str) else ln
        if txt:
            rows.add(mono(txt, size, col))
        else:
            rows.add(Rectangle(width=0.1, height=mono("Ag", size).height * 0.6, stroke_width=0, fill_opacity=0))
    rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    w = max(width or 0, rows.width + 0.5)
    box = RoundedRectangle(corner_radius=0.1, width=w, height=rows.height + 0.4, stroke_color=border,
                           stroke_width=1.5, fill_color="#0B0E12", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(0.25 * RIGHT)
    g = VGroup(box, rows)
    if title:
        g.add(label(title, 13).next_to(box, UP, 0.1).align_to(box, LEFT))
    return g


def code_lines(src, size=16):
    """Source code as a card; Text drops leading spaces, so indent by measured width."""
    lines = src.rstrip("\n").split("\n")
    rows = VGroup()
    step = mono("x", size).width
    for ln in lines:
        stripped = ln.lstrip(" ")
        ind = len(ln) - len(stripped)
        rows.add(mono(stripped, size, INK) if stripped else
                 Rectangle(width=0.1, height=mono("Ag", size).height, stroke_width=0, fill_opacity=0))
    rows.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
    for ln, t in zip(lines, rows):
        ind = len(ln) - len(ln.lstrip(" "))
        t.shift(ind * step * RIGHT)
    box = RoundedRectangle(corner_radius=0.1, width=rows.width + 0.6, height=rows.height + 0.45, stroke_color=DIM,
                           stroke_width=1.5, fill_color="#0B0E12", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(0.3 * RIGHT)
    return VGroup(box, rows)


AGENT_SRC = inspect.getsource(AGENT.agent)


# --- the token view -----------------------------------------------------------------------------
TOK_H = 0.36
KCOL = {"cli": CLI_GREY, "instr": OUR_GREY, "task": INK, "model": BLUE, "result": GREEN}


def token_bars(run, scale, y, x0=X0, n_cards=None):
    """The context as bars sized by tokens. n_cards: how many cards (in data order) to include."""
    cs = S[run]["cards"]
    if n_cards is not None:
        cs = cs[:n_cards]
    g = VGroup()
    x = x0
    for c in cs:
        w = c["tokens"] * scale
        if w <= 0:
            continue
        r = Rectangle(width=w, height=TOK_H, stroke_width=0.6 if w > 0.03 else 0, stroke_color=BG,
                      fill_color=KCOL[c["kind"]], fill_opacity=0.95 if c["kind"] != "task" else 0.85)
        r.move_to([x + w / 2, y, 0])
        r.data = c
        g.add(r)
        x += w
    return g


def row_cards(n_call):
    """Cards (in data order) that call n (1-based) read: notes, instructions, task, and n-1 pairs."""
    return 3 + 2 * (n_call - 1)


def amber_num(n, size=18):
    return mono_b(f"{n:,}", size, AMBER)


# --- a scene with the fixed picture, and one-call replay steps -----------------------------------
STRIP_Y = -2.75


class AgentScene(CueScene):
    def picture(self, run, shown, tag=True, code=True, failing=True, labels=None, add=True):
        self.model = model_box(tag)
        self.code = code_box()
        self.proj = Project(failing=failing)
        self.strip = Strip(run, STRIP_Y, labels=labels)
        self.shown = shown
        if add:
            self.add(self.model, self.proj, *self.strip.cards[:shown])
            if code:
                self.add(self.code)
        return self

    def visible(self):
        return VGroup(*self.strip.cards[:self.shown])

    def read(self, run_time=0.45):
        """The model reads the whole context: a band sweeps it, and a faint line joins it to the model."""
        band, anim = band_sweep(self.visible(), run_time)
        self.add(band)
        self.play(anim)
        self.remove(band)

    def model_writes(self, run_time=0.45):
        c = self.strip.cards[self.shown]
        self.play(grow_in(c, self.model[0], run_time))
        self.shown += 1
        return c

    def tool_runs(self, file=None, run_time=0.45, keep=False):
        """The last card (a tool call) goes to our code, which acts on the project; a result comes back.
        keep: leave the arrows (tool call -> our code -> result) on screen and return them."""
        req = self.strip.cards[self.shown - 1]
        ar = Arrow(req.get_top(), self.code[0].get_bottom(), buff=0.08, color=BLUE, stroke_width=3,
                   max_tip_length_to_length_ratio=0.12)
        anims = [GrowArrow(ar), Indicate(self.code[0], color=INK, scale_factor=1.04)]
        if file:
            anims.append(Indicate(self.proj.files[file][0], color=INK, scale_factor=1.05))
        self.play(*anims, run_time=run_time)
        c = self.strip.cards[self.shown]
        if keep:
            act = Arrow(self.code[0].get_right(), self.proj.get_left() + DOWN * 0.3, buff=0.1, color=MUTED,
                        stroke_width=2.5, max_tip_length_to_length_ratio=0.15)
            self.play(GrowArrow(act), run_time=run_time)
            back = CurvedArrow(self.code[0].get_bottom() + RIGHT * 0.2, c.get_right() + RIGHT * 0.05, angle=-TAU / 7,
                               color=GREEN, stroke_width=3, tip_length=0.16)
            self.play(grow_in(c, self.code[0], run_time), Create(back, run_time=run_time))
            self.shown += 1
            return c, VGroup(ar, act, back)
        self.play(grow_in(c, self.code[0], run_time), FadeOut(ar, run_time=run_time * 0.8))
        self.shown += 1
        return c

    def step(self, file=None, with_result=True, t=1.6):
        """One call of a run: read, write a card, and (if it is a tool call) run it."""
        k = t / 3.3
        self.read(max(0.25, k))
        self.model_writes(max(0.25, k))
        if with_result:
            self.tool_runs(file, max(0.25, k))


def callout(card, panel, side=UP, buff=0.25):
    """A panel of text opened from a card, with a thin line joining them."""
    panel.next_to(card, side, buff=buff)
    ln = Line(card.get_edge_center(side), panel.get_edge_center(-side), stroke_color=FAINT, stroke_width=1.5)
    return VGroup(ln, panel)


def keep_on_screen(m, margin=0.2):
    fw, fh = config.frame_width / 2 - margin, config.frame_height / 2 - margin
    if m.get_right()[0] > fw:
        m.shift((fw - m.get_right()[0]) * RIGHT)
    if m.get_left()[0] < -fw:
        m.shift((-fw - m.get_left()[0]) * RIGHT)
    if m.get_top()[1] > fh:
        m.shift((fh - m.get_top()[1]) * UP)
    return m


FILE_OF = {"test_report.py": "test_report.py", "report.py": "report.py", "sales.csv": "sales.csv"}


def tool_file(card):
    t = card.data.get("tool") or {}
    if t.get("tool") == "run_tests":
        return "test_report.py"
    return FILE_OF.get(t.get("path", ""), None)
