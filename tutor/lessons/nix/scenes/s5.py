from nkit import *

REFS = (DATA / "closure_refs.txt").read_text()


def short(name):
    """'5m9amsvv…-glibc-2.40-66' -> 'glibc-2.40-66'."""
    return name.split("-", 1)[1]


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("The closure")
        # 01-03: Hello needs the C library; where is it?
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        hello = box("hello-2.12.1", -4.9, 1.8, w=3.0, color=INK)
        self.play(FadeIn(hello), run_time=0.4)
        self.at("02")
        need = mono("needs: the C library", 17, MUTED).next_to(hello, DOWN, 0.2)
        self.play(FadeIn(need), run_time=0.4)
        self.at("03")
        ul = mono("/usr/lib ?", 20, MUTED).move_to([0.5, 1.8, 0])
        self.play(FadeIn(ul), run_time=0.3)
        self.play(Create(Line(ul.get_left(), ul.get_right(), stroke_color=BAD, stroke_width=3)), run_time=0.3)

        # 04-05: full store paths inside its files, found by scanning
        self.at("04")
        self.play(FadeOut(ul), FadeOut(need), *[FadeOut(m) for m in self.mobjects if isinstance(m, Line)], run_time=0.3)
        inside = VGroup(mono("inside hello's files:", 14, MUTED),
                        store_path(demo_ref("glibc"), 15)).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        inside.move_to([1.2, 1.8, 0])
        self.play(FadeIn(inside), run_time=0.6)
        self.at("05")
        scan = mono("found by scanning the output for store paths", 15, ICE).next_to(inside, DOWN, 0.25).align_to(inside, LEFT)
        self.play(FadeIn(scan), run_time=0.5)

        # 06-07: follow the references: the closure (real run)
        self.at("06")
        self.play(FadeOut(inside), FadeOut(scan), run_time=0.3)
        pos = {"hello-2.12.1": (-4.9, 1.8), "glibc-2.40-66": (-1.5, 1.8), "libidn2-2.3.7": (1.9, 2.5),
               "libunistring-1.2": (4.9, 2.5), "xgcc-13.3.0-libgcc": (1.9, 1.0)}
        boxes = {"hello-2.12.1": hello}
        for k, (x, y) in pos.items():
            if k not in boxes:
                boxes[k] = box(k, x, y, w=2.8 if "xgcc" not in k else 3.2, size=15)
        edges = []
        cur = None
        for line in REFS.splitlines()[1:]:
            if line.endswith(":"):
                cur = short(line[:-1])
            elif "->" in line:
                edges.append((cur, short(line.split("-> ")[1])))
        arrs = {e: arrow(boxes[e[0]].get_right() if pos[e[1]][1] == pos[e[0]][1] else boxes[e[0]].get_right(),
                         boxes[e[1]].get_left()) for e in edges}
        order = ["glibc-2.40-66", "libidn2-2.3.7", "xgcc-13.3.0-libgcc", "libunistring-1.2"]
        for k in order:
            ins = [a for (s, d), a in arrs.items() if d == k]
            self.play(*[GrowArrow(a) for a in ins], FadeIn(boxes[k]), run_time=0.5)
        self.at("07")
        rt = VGroup(mono("the compiler's runtime library", 13, MUTED), mono("(not the compiler)", 13, MUTED))
        rt.arrange(DOWN, buff=0.06).next_to(boxes["xgcc-13.3.0-libgcc"], DOWN, 0.12)
        clo = SurroundingRectangle(VGroup(*boxes.values(), rt), buff=0.3, color=ICE, stroke_width=2, corner_radius=0.12)
        cl = mono("closure: 5 paths (nix-store -qR)", 17, ICE).next_to(clo, DOWN, 0.15).align_to(clo, LEFT)
        self.play(Create(clo), FadeIn(cl), run_time=0.8)

        # 08: copy them, and it runs
        self.at("08")
        cp = mono("copy these 5 to another machine of the same kind → hello runs", 16, INK).move_to([0, -1.75, 0])
        self.play(FadeIn(cp), run_time=0.5)

        # 09: the compiler itself is not in it
        self.at("09")
        gcc = box("compiler: gcc 13", -3.6, -2.7, w=3.4, size=15, color=FAINT, edge=FAINT, dashed=True)
        gl = mono("build-time only, not in the closure", 14, FAINT).next_to(gcc, RIGHT, 0.3)
        self.play(FadeIn(gcc), FadeIn(gl), FadeIn(rt), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()


def demo_ref(name):
    """The full store path of a closure member, from the demo's closure listing."""
    return next(l for l in DEMO.splitlines() if l.startswith("/nix/store/") and name in l)
