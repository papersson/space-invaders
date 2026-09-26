from nkit import *


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("The trouble with shared paths")
        # 01-03: shared places
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        self.at("02")
        bin_l = mono("/usr/bin", 20, MUTED).move_to([-5.2, 1.6, 0])
        a = box("program A", -2.4, 1.6, w=2.3)
        b = box("program B", 0.3, 1.6, w=2.3)
        self.play(FadeIn(bin_l), FadeIn(a), FadeIn(b), run_time=0.6)
        self.at("03")
        lib_l = mono("/usr/lib", 20, MUTED).move_to([-5.2, -0.6, 0])
        lib = box("libssl.so  v1", -1.05, -0.6, w=3.0, color=INK)
        aa = arrow(a.get_bottom(), lib.get_top() + 0.5 * LEFT)
        ba = arrow(b.get_bottom(), lib.get_top() + 0.5 * RIGHT)
        self.play(FadeIn(lib_l), FadeIn(lib), GrowArrow(aa), GrowArrow(ba), run_time=0.7)

        # 04-05: an upgrade overwrites it in place
        self.at("04")
        v3 = box("libssl.so  v3", -1.05, -0.6, w=3.0, color=AMBER, edge=AMBER)
        up = mono("upgrade: v3 written over v1", 16, AMBER).next_to(lib, DOWN, 0.3)
        self.play(FadeIn(up), run_time=0.3)
        self.play(Transform(lib, v3), run_time=0.7)
        self.at("05")
        bb = mono("built for v1", 14, BAD).next_to(b, RIGHT, 0.25)
        self.play(b[0].animate.set_stroke(BAD), b[1].animate.set_color(BAD), ba.animate.set_color(BAD), FadeIn(bb), run_time=0.6)

        # 06: two programs, two versions, one slot
        self.at("06")
        wa = mono("A wants v3", 16, AMBER).next_to(a, UP, 0.2)
        wb = mono("B wants v1", 16, BAD).next_to(b, UP, 0.2)
        one = mono("one path, one version", 16, BAD).move_to([3.9, -0.6, 0])
        self.play(FadeIn(wa), FadeIn(wb), FadeIn(one), run_time=0.6)

        # 07: versioned names, the exception
        self.at("07")
        g = VGroup(box("libssl.so.1.1", 2.1, -2.2, w=2.6, size=15, color=ICE, edge=ICE),
                   box("libssl.so.3", 4.9, -2.2, w=2.6, size=15, color=ICE, edge=ICE))
        gl = mono("versioned names: some libraries", 14, ICE).next_to(g, UP, 0.12)
        self.play(FadeIn(g), FadeIn(gl), run_time=0.6)
        self.wait(0.8)
        self.play(FadeOut(g), FadeOut(gl), run_time=0.5)

        # 08: a half-finished upgrade
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        files = VGroup(*[box(f"file {i + 1}", -5.25 + 1.5 * i, 0.4, w=1.3, h=0.9, size=14) for i in range(8)])
        self.play(FadeIn(files), run_time=0.5)
        new = [box(f"v3", -5.25 + 1.5 * i, 0.4, w=1.3, h=0.9, size=16, color=ICE, edge=ICE) for i in range(4)]
        self.play(LaggedStart(*[Transform(files[i], new[i]) for i in range(4)], lag_ratio=0.3), run_time=1.2)
        bolt = VMobject(fill_color=AMBER, fill_opacity=1, stroke_width=0).set_points_as_corners(
            [[0.1, 0.5, 0], [-0.2, -0.05, 0], [0.02, -0.05, 0], [-0.1, -0.5, 0], [0.22, 0.08, 0], [0.0, 0.08, 0], [0.1, 0.5, 0]])
        bolt.move_to([0.75, 1.6, 0])
        pw = mono("power out", 16, AMBER).next_to(bolt, RIGHT, 0.2)
        self.play(FadeIn(bolt), FadeIn(pw), run_time=0.4)
        old = VGroup(*[mono("v1", 16, MUTED).move_to(files[i]) for i in range(4, 8)])
        self.play(*[FadeOut(files[i][1]) for i in range(4, 8)], FadeIn(old), run_time=0.4)
        mix = mono("v1 and v3 files mixed", 20, BAD).move_to([0, -1.0, 0])
        self.play(FadeIn(mix), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
