"""Pieces shared by the Nix scenes: store paths with the hash picked out, boxes, a terminal,
and the real outputs from the demo runs."""
import re
from common import *

DEMO = (DATA / "nix_demo.txt").read_text()
NIXOS = (DATA / "nixos_demo.txt").read_text()
GOOD = ICE
BAD = CORAL


def demo_path(key):
    """The store path printed after 'key: ' in the demo output."""
    return re.search(rf"^{re.escape(key)}: (\S+)", DEMO, re.M).group(1)


def system_paths():
    return re.findall(r"^system: (\S+)", NIXOS, re.M)


def split_path(p):
    """'/nix/store/<hash>-name' -> ('/nix/store/', hash, '-name')."""
    m = re.match(r"(/nix/store/)([0-9a-z]{32})(-.*)", p)
    return m.group(1), m.group(2), m.group(3)


def store_path(p, size=18, hash_color=AMBER, color=INK, short=False):
    """A store path as one line of text, the hash coloured; short=True keeps 8 hash characters."""
    pre, h, name = split_path(p)
    if short:
        h = h[:8] + "…"
    parts = VGroup(mono(pre, size, MUTED), mono(h, size, hash_color), mono(name, size, color))
    parts.arrange(RIGHT, buff=0.02, aligned_edge=DOWN)
    return parts


def terminal(lines, width=6.0, size=16):
    """A dark terminal box; each line is (text, color) or a ready-made mobject."""
    rows = VGroup(*[l if isinstance(l, Mobject) else mono(l[0], size, l[1]) for l in lines])
    rows.arrange(DOWN, buff=0.14, aligned_edge=LEFT)
    box = RoundedRectangle(corner_radius=0.1, width=max(width, rows.width + 0.5), height=rows.height + 0.5,
                           stroke_color=DIM, stroke_width=1.5, fill_color="#0B0E12", fill_opacity=1)
    rows.move_to(box).align_to(box, LEFT).shift(0.25 * RIGHT)
    return VGroup(box, rows)


def box(text, x, y, w=2.4, h=0.7, color=INK, edge=TRAY_EDGE, size=17, dashed=False):
    r = RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=edge, stroke_width=2,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    if dashed:
        r = VGroup(RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_width=0, fill_color=TRAY_FILL,
                                    fill_opacity=1).move_to([x, y, 0]),
                   DashedVMobject(RoundedRectangle(corner_radius=0.08, width=w, height=h, stroke_color=edge,
                                                   stroke_width=2).move_to([x, y, 0]), num_dashes=40))
    return VGroup(r, mono(text, size, color).move_to([x, y, 0]))


def arrow(a, b, color=FAINT, buff=0.08):
    return Arrow(a, b, buff=buff, color=color, stroke_width=2.5, tip_length=0.15, max_tip_length_to_length_ratio=0.2)
