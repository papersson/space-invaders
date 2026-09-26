"""Pieces shared by the query-planner scenes: numbers and plan lines parsed from the real runs,
the table drawn as a grid of its 12,739 pages, plan-tree nodes and a code card."""
import re
from common import *
from PIL import Image

RUNS = (DATA / "runs.txt").read_text()
PAGES_TXT = (DATA / "pages.txt").read_text()
GOOD = ICE
BAD = CORAL


def part(n):
    """The text of one numbered part of runs.txt ('=== 4b. ...' -> part('4b'))."""
    m = re.search(rf"^=== {re.escape(n)}\. .*?(?=^=== |\Z)", RUNS, re.M | re.S)
    return m.group(0)


def medians(n):
    """Median execution times (ms) printed in part n, in order."""
    return [float(x) for x in re.findall(r"median_ms_of_7_runs\s*\n-+\n\s*([\d.]+)", part(n))]


def est_rows(text, node):
    """Estimated rows on the first plan line containing node."""
    line = next(l for l in text.splitlines() if node in l)
    return int(re.search(r"rows=(\d+) width", line).group(1))


def total_cost(text):
    """Total cost of the plan's top node."""
    line = next(l for l in text.splitlines() if "cost=" in l)
    return float(re.search(r"cost=[\d.]+\.\.([\d.]+)", line).group(1))


RELPAGES = int(re.search(r"relpages\s*\n-+\n\s*(\d+)", RUNS).group(1))
PAGES_4242 = [int(x) for x in re.findall(r"^\s*\d+ \|\s*(\d+)\s*$", PAGES_TXT.split("=== pages holding")[0], re.M)]


def ms(x):
    return f"{x:,.3f} ms" if x < 1 else f"{x:,.1f} ms"


# --- the table as a grid of pages --------------------------------------------------
COLS = 139
ROWS = (RELPAGES + COLS - 1) // COLS
PITCH = 4          # pixels per page cell


def page_grid(lit=(), all_color=None, w=8.6):
    """An image of every page of the table, one small cell each; lit pages in ICE."""
    img = Image.new("RGBA", (COLS * PITCH, ROWS * PITCH), (0, 0, 0, 0))
    px = img.load()
    base = (0x2B, 0x33, 0x3C, 255) if all_color is None else all_color
    lit = set(lit)
    for p in range(RELPAGES):
        r, c = divmod(p, COLS)
        col = (0x8F, 0xD3, 0xFF, 255) if p in lit else base
        for dy in range(PITCH - 1):
            for dx in range(PITCH - 1):
                px[c * PITCH + dx, r * PITCH + dy] = col
    m = ImageMobject(img)
    m.set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
    m.width = w
    return m


def page_pos(grid, p):
    """Scene position of page p's cell on a grid image."""
    r, c = divmod(p, COLS)
    x0, y0 = grid.get_corner(UL)[0], grid.get_corner(UL)[1]
    cell = grid.width / COLS
    return np.array([x0 + (c + 0.4) * cell, y0 - (r + 0.4) * cell, 0])


def code_card(text, size=18, color=INK):
    t = mono(text, size, color)
    b = SurroundingRectangle(t, buff=0.28, color=DIM, stroke_width=1.5, corner_radius=0.1)
    b.set_fill("#0B0E12", 1)
    return VGroup(b, t)


def node(title, detail="", color=INK, w=4.6):
    """A plan-tree node: the operator and a line of detail."""
    t = mono(title, 16, color)
    d = mono(detail, 13, MUTED) if detail else VGroup()
    inner = VGroup(t, d).arrange(DOWN, buff=0.08, aligned_edge=LEFT) if detail else t
    r = RoundedRectangle(corner_radius=0.08, width=max(w, inner.width + 0.4), height=inner.height + 0.3,
                         stroke_color=TRAY_EDGE, stroke_width=1.8, fill_color=TRAY_FILL, fill_opacity=1)
    inner.move_to(r).align_to(r, LEFT).shift(0.2 * RIGHT)
    return VGroup(r, inner)


def tree(nodes, x, y, gap=0.25, indent=0.5):
    """Stack plan nodes top to bottom, each child indented, with a short elbow line."""
    g = VGroup()
    for i, n in enumerate(nodes):
        n.move_to([x, y, 0], aligned_edge=UL).shift(i * indent * RIGHT)
        if i:
            n.next_to(g[-1], DOWN, gap).align_to(g[-1], LEFT).shift(indent * RIGHT)
        g.add(n)
    return g
