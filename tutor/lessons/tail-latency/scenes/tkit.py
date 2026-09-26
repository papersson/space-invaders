"""Pieces shared by the tail latency scenes: the page fanning out to a 10 x 10 grid of servers."""
from common import *

F = json.loads((DATA / "fanout.json").read_text())
FAST = "#3B6E8C"          # a fast call (dim ice)
CELL, GAP = 0.44, 0.08
GRID_X, GRID_Y = 2.0, -0.1  # grid centre


def cell_center(i):
    r, c = divmod(i, 10)
    step = CELL + GAP
    return np.array([GRID_X + (c - 4.5) * step, GRID_Y + (4.5 - r) * step, 0])


def server_grid(color=PANEL):
    return VGroup(*[RoundedRectangle(corner_radius=0.05, width=CELL, height=CELL, stroke_color=DIM, stroke_width=1.2,
                                     fill_color=color, fill_opacity=1).move_to(cell_center(i)) for i in range(100)])


def page_box(x=-4.2, y=-0.1):
    r = RoundedRectangle(corner_radius=0.14, width=1.9, height=1.2, stroke_color=TRAY_EDGE, stroke_width=2.5,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    t = label("user's page", 18, INK).move_to(r)
    return VGroup(r, t)


def fan_lines(page, grid):
    left = grid.get_left()[0] - 0.15
    ys = [cell_center(10 * r)[1] for r in range(10)]
    return VGroup(*[Line(page.get_right(), [left, y, 0], stroke_color=FAINT, stroke_width=1.2) for y in ys])


def color_grid(grid, slow_row):
    for i, s in enumerate(slow_row):
        grid[i].set_fill(CORAL if s else FAST, 1)
    return grid
