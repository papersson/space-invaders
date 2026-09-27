"""The lesson's one diagram, built up chapter by chapter, and the helpers every scene shares.

Geography (fixed from chapter 2 on): the context panel on the left; the LLM box at the top middle,
with what it writes to its right; the program (with its tools) below that; the project on the
right. Colour roles: ice blue is the model and what it writes; mint is the harness (the program,
its tools, the results it pastes back, the instructions it writes); coral a failing test; lime a
passing one; amber a number (a probability, a count).
"""
import json

from common import *

MODEL = ICE
HARN = "#6CCFB6"
PASS = "#A6E36B"
FAIL = CORAL
NUM = AMBER

TR = json.loads((DATA / "trace.json").read_text())

# --- geometry -------------------------------------------------------------------------------------
CTX_L, CTX_R, CTX_T, CTX_B = -6.85, -2.3, 2.95, -3.35
CTX_X = (CTX_L + CTX_R) / 2
MOD_C = np.array([-0.35, 1.9, 0.0])
MOD_W, MOD_H = 2.2, 1.2
SLOT_L, SLOT_Y = 1.1, 1.9
PROG_C = np.array([1.75, -1.35, 0.0])
PROG_W, PROG_H = 3.7, 2.1
PROJ_L, PROJ_R = 4.35, 6.85
PROJ_X = (PROJ_L + PROJ_R) / 2
RES_Y = -1.95          # the result arrow, program -> context
PJ_Y = -0.55           # the program -> project arrow
SP_X = 1.75             # the slot -> program arrow
FILES = ["invoice.py", "prices.py", "orders.csv", "test_invoice.py"]


def rbox(w, h, color, fill=PANEL, fo=1.0, sw=2.0, r=0.14):
    return RoundedRectangle(width=w, height=h, corner_radius=r, stroke_color=color, stroke_width=sw,
                            fill_color=fill, fill_opacity=fo)


def fit(s, size, width, font=MONO, color=INK, weight=NORMAL):
    """Text that fits in `width`, cut with an ellipsis if it must be."""
    t = T(s, size, color, font=font, weight=weight)
    while t.width > width and len(s) > 4:
        s = s[:-2].rstrip() + "…"
        t = T(s, size, color, font=font, weight=weight)
    t.src = s
    return t


def glyphs(t, sub, nth=1):
    """The glyphs of `sub` inside a Text made by T() or fit() (Text drops spaces from its glyphs)."""
    s = t.src
    i = -1
    for _ in range(nth):
        i = s.index(sub, i + 1)
    a = len(s[:i].replace(" ", ""))
    return VGroup(*t[a:a + len(sub.replace(" ", ""))])


def arrow(a, b, color=FAINT, sw=3.0, tip=0.16):
    return Arrow(np.array(a, dtype=float), np.array(b, dtype=float), buff=0, stroke_width=sw, color=color,
                 tip_length=tip, max_tip_length_to_length_ratio=0.5, max_stroke_width_to_length_ratio=20)


def card(lines, color, w=4.3, size=15, font=MONO, tcolor=INK, fill=PANEL):
    """A context card: a thin coloured stripe on the left, one or more lines of text."""
    if isinstance(lines, str):
        lines = [lines]
    texts = VGroup(*[fit(l, size, w - 0.42, font=font, color=tcolor) for l in lines])
    texts.arrange(DOWN, aligned_edge=LEFT, buff=0.1)
    h = max(texts.height + 0.24, 0.36)
    rect = rbox(w, h, color, fill=fill, sw=1.4, r=0.07)
    stripe = Rectangle(width=0.07, height=h - 0.1, stroke_width=0, fill_color=color, fill_opacity=1)
    stripe.move_to(rect.get_left() + RIGHT * 0.1)
    texts.move_to(rect).align_to(rect, LEFT).shift(RIGHT * 0.24)
    g = VGroup(rect, stripe, texts)
    g.color_role = color
    return g


def sliver(color, w=4.3, h=0.06):
    return RoundedRectangle(width=w, height=h, corner_radius=0.02, stroke_width=0, fill_color=color,
                            fill_opacity=0.75)


def tag(s, color=MUTED, size=14):
    return T(s, size, color, font=MONO)


# --- the diagram ----------------------------------------------------------------------------------
class Diagram:
    def __init__(self):
        # context panel
        self.ctx = rbox(CTX_R - CTX_L, CTX_T - CTX_B, FAINT, fill=TRAY_FILL, sw=2).move_to(
            [CTX_X, (CTX_T + CTX_B) / 2, 0])
        self.ctx_label = label("context", 17, MUTED).move_to([CTX_L + 0.2, CTX_T - 0.24, 0], aligned_edge=LEFT)
        # model
        self.model = rbox(MOD_W, MOD_H, MODEL, fill=PANEL, sw=2.5).move_to(MOD_C)
        self.model_name = T("LLM", 36, MODEL, weight=BOLD).move_to(MOD_C)
        self.model_word = T("model", 30, MODEL, weight=MEDIUM).move_to(MOD_C)
        self.model_sub = T("large language model", 14, MUTED).next_to(self.model, DOWN, buff=0.1)
        self.tag_gpt2 = tag("GPT-2 (small, freely available)", MUTED, 13).next_to(self.model_sub, DOWN, 0.06)
        self.tag_claude = tag("a large model (Claude)", MUTED, 13).next_to(self.model_sub, DOWN, 0.06)
        # program and tools
        self.prog = rbox(PROG_W, PROG_H, HARN, fill=PANEL, sw=2.5).move_to(PROG_C)
        self.prog_name = T("program", 20, HARN, weight=MEDIUM).move_to(
            self.prog.get_corner(UL) + np.array([0.2, -0.28, 0]), aligned_edge=LEFT)
        names = ["search", "open file", "edit file", "run tests"]
        self.tools = {}
        for i, n in enumerate(names):
            c = VGroup(rbox(1.62, 0.5, HARN, fill=TRAY_FILL, sw=1.5, r=0.1), T(n, 16, HARN, font=MONO))
            c[1].move_to(c[0])
            c.move_to(PROG_C + np.array([-0.86 + 1.72 * (i % 2), 0.02 - 0.64 * (i // 2), 0]))
            self.tools[n] = c
        self.tool_group = VGroup(*self.tools.values())
        # project
        self.proj_label = label("project", 17, MUTED).move_to([PROJ_L, 0.95, 0], aligned_edge=LEFT)
        self.files = {}
        for i, f in enumerate(FILES):
            c = VGroup(rbox(PROJ_R - PROJ_L, 0.44, FAINT, fill=PANEL, sw=1.4, r=0.07), T(f, 16, INK, font=MONO))
            c[1].move_to(c[0]).align_to(c[0], LEFT).shift(RIGHT * 0.2)
            c.move_to([PROJ_X, 0.45 - 0.56 * i, 0])
            self.files[f] = c
        self.file_group = VGroup(*self.files.values())
        self.badge_fail = self._badge("tests: fail", FAIL)
        self.badge_pass = self._badge("tests: pass", PASS)
        # arrows
        self.a_cm = arrow([CTX_R, MOD_C[1], 0], [MOD_C[0] - MOD_W / 2, MOD_C[1], 0])
        self.a_ms = arrow([MOD_C[0] + MOD_W / 2, SLOT_Y, 0], [SLOT_L - 0.05, SLOT_Y, 0])
        self.a_sp = arrow([SP_X, SLOT_Y - 0.36, 0], [SP_X, PROG_C[1] + PROG_H / 2, 0])
        self.a_pj = arrow([PROG_C[0] + PROG_W / 2, PJ_Y, 0], [PROJ_L - 0.02, PJ_Y, 0])
        self.a_pc = arrow([PROG_C[0] - PROG_W / 2, RES_Y, 0], [CTX_R, RES_Y, 0])
        self.res_label = T("result", 16, HARN, font=MONO).next_to(self.a_pc, UP, buff=0.08)
        self.loop_label = T("the loop", 20, HARN, weight=MEDIUM).move_to([-1.2, 0.3, 0])

    def _badge(self, s, color):
        b = VGroup(rbox(PROJ_R - PROJ_L, 0.5, color, fill=PANEL, sw=2.2, r=0.1), T(s, 17, color, font=MONO, weight=MEDIUM))
        b[1].move_to(b[0])
        b.move_to([PROJ_X, -2.05, 0])
        return b

    def loop_path(self):
        """The loop, for a dot to run round: context -> model -> its output -> program -> context."""
        pts = [[CTX_R, MOD_C[1]], [SLOT_L - 0.05, SLOT_Y], [SP_X, SLOT_Y], [SP_X, PROG_C[1] + PROG_H / 2],
               [SP_X, RES_Y], [CTX_R, RES_Y], [CTX_R, MOD_C[1]]]
        p = VMobject().set_points_as_corners([np.array([x, y, 0]) for x, y in pts])
        return p

    def harness_outline(self):
        """Dashed, around everything except the LLM box (a notch around the box)."""
        l, r, t, b = -7.0, 7.0, 3.12, -3.52
        nl, nr, nb = MOD_C[0] - MOD_W / 2 - 0.3, MOD_C[0] + MOD_W / 2 + 0.25, MOD_C[1] - MOD_H / 2 - 0.62
        pts = [[l, t], [nl, t], [nl, nb], [nr, nb], [nr, t], [r, t], [r, b], [l, b], [l, t]]
        p = VMobject(stroke_color=HARN, stroke_width=3).set_points_as_corners([np.array([x, y, 0]) for x, y in pts])
        return DashedVMobject(p, num_dashes=120, dashed_ratio=0.55)

    def base(self, stage):
        """The static diagram at the start of chapter `stage` (no context cards)."""
        g = [self.ctx, self.ctx_label, self.model, self.model_name, self.model_sub, self.a_cm]
        if stage >= 3:
            g += [self.prog, self.prog_name, self.tool_group, self.proj_label, self.file_group, self.a_ms, self.a_sp,
                  self.a_pj]
        if stage >= 4:
            g += [self.a_pc, self.res_label]
        return g


# --- the context column ---------------------------------------------------------------------------
class Column:
    """Cards stacked in the context panel, newest at the bottom. When they no longer fit, the oldest
    unpinned cards shrink to slivers (still there, still read), and the newest stay readable."""
    TOP = CTX_T - 0.5
    BOTTOM = CTX_B + 0.12
    GAP = 0.07
    SGAP = 0.035

    def __init__(self, scene):
        self.scene, self.items = scene, []

    def target(self, it, form, y_top):
        m = (it["full"] if form == "full" else it["sliver"]).copy()
        m.move_to([CTX_X, y_top - m.height / 2, 0])
        return m

    def plan(self, items):
        pinned = [it for it in items if it.get("pin")]
        rest = [it for it in items if not it.get("pin")]
        avail = self.TOP - self.BOTTOM - sum(it["full"].height + self.GAP for it in pinned)
        k = len(rest)
        while k > 0:
            h = sum(it["full"].height + self.GAP for it in rest[len(rest) - k:]) + \
                sum(it["sliver"].height + self.SGAP for it in rest[:len(rest) - k])
            if h <= avail:
                break
            k -= 1
        forms = {}
        for it in pinned:
            forms[id(it)] = "full"
        for j, it in enumerate(rest):
            forms[id(it)] = "full" if j >= len(rest) - k else "sliver"
        out, y = [], self.TOP
        for it in items:
            f = forms[id(it)]
            m = it["full"] if f == "full" else it["sliver"]
            out.append((it, f, y))
            y -= m.height + (self.GAP if f == "full" else self.SGAP)
        return out

    def anims(self, new=None, src=None, index=None):
        """Animations that move every card to its place, adding `new` (from `src`, a mobject, if given),
        at the end or at `index`."""
        items = list(self.items)
        if new:
            items.insert(len(items) if index is None else index, new)
        an = []
        for it, f, y in self.plan(items):
            tgt = self.target(it, f, y)
            if it is new:
                if src is not None:
                    an.append(ReplacementTransform(src, tgt))
                else:
                    an.append(FadeIn(tgt, shift=UP * 0.1))
                it["shown"], it["form"] = tgt, f
            elif it["form"] != f:
                an.append(ReplacementTransform(it["shown"], tgt))
                it["shown"], it["form"] = tgt, f
            elif np.linalg.norm(it["shown"].get_top() - tgt.get_top()) > 1e-3:
                an.append(it["shown"].animate.move_to(tgt))
        self.items = items
        return an

    def place(self, new_items):
        """Add cards at once, with no animation (to restore a state)."""
        self.items += new_items
        for it, f, y in self.plan(self.items):
            it["shown"], it["form"] = self.target(it, f, y), f
            self.scene.add(it["shown"])

    def item(self, lines, color, pin=False, **kw):
        c = card(lines, color, **kw)
        return {"full": c, "sliver": sliver(color), "pin": pin, "role": color}

    def remove_all(self):
        for it in self.items:
            self.scene.remove(it["shown"])
        self.items = []


def task_item(col, short=False):
    lines = TR["task_lines"] if not short else ["task: … no price for 'gadget' …"]
    return col.item(lines, INK, pin=True, size=14)


def instr_item(col, short=False):
    if short:
        return col.item(["instructions (request format)"], HARN, pin=True, size=14, tcolor=HARN)
    lines = ["instructions", "search: TEXT", "open file: NAME", "edit file: NAME …", "run tests"]
    it = col.item(lines, HARN, pin=True, size=14, tcolor=INK)
    it["full"][2][0].set_color(HARN)
    return it


class LScene(CueScene):
    """A chapter: fades in from the background, and fades out to it at the end."""

    def setup(self):
        super().setup()
        self.d = Diagram()
        self.col = Column(self)

    def lit(self, arr, color, t=0.3):
        return arr.animate(run_time=t).set_color(color)

    def fade_in_all(self, t=0.4):
        mobs = [m for m in self.mobjects]
        for m in mobs:
            m.save_state()
            m.set_opacity(0)
        self.play(*[Restore(m) for m in mobs], run_time=t)

    def end(self, t=0.3):
        self.until(self.dur - t - 0.02)
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=t)
        self.finish()

    def write_slot(self, s, color=MODEL, size=19, t=0.4):
        m = T(s, size, color, font=MONO).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
        self.play(FadeIn(m, shift=RIGHT * 0.15), run_time=t)
        return m

    def sweep(self, t=0.7):
        """A light band down the context panel: the model reading the whole context."""
        band = Rectangle(width=CTX_R - CTX_L - 0.1, height=0.35, stroke_width=0, fill_color=MODEL, fill_opacity=0.18)
        band.move_to([CTX_X, CTX_T - 0.2, 0])
        self.add(band)
        self.play(band.animate.move_to([CTX_X, CTX_B + 0.2, 0]), run_time=t, rate_func=linear)
        self.remove(band)
