from nkit import *


def node(name, path, x, y, color=AMBER):
    h = split_path(path)[1][:8]
    r = RoundedRectangle(corner_radius=0.1, width=2.8, height=1.1, stroke_color=TRAY_EDGE, stroke_width=2,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    n = mono(name, 18, INK).move_to(r.get_center() + 0.2 * UP)
    v = mono(h, 18, color).move_to(r.get_center() + 0.22 * DOWN)
    return VGroup(r, n, v)


class S4(CueScene):
    SEG = "s4"

    def construct(self):
        c = chip("Change an input, change the path")
        hello = node("hello", demo_path("hello"), -3.6, 1.2)
        greet = node("greet", demo_path("greet"), 1.0, 1.2)
        cow = node("cowsay", demo_path("cowsay"), -3.6, -1.3)
        e = arrow(hello[0].get_right(), greet[0].get_left())
        uses = mono("runs hello", 13, MUTED).next_to(e, UP, 0.08)
        self.at("01")
        self.play(FadeIn(c), FadeIn(hello), FadeIn(cow), run_time=0.6)

        # 02-03: one option of hello changes; new hash
        self.at("02")
        opt = mono("doCheck = false", 17, AMBER).next_to(hello, LEFT, 0.3).shift(0.9 * UP)
        oa = arrow(opt.get_bottom(), hello[0].get_top() + 0.6 * LEFT)
        self.play(FadeIn(opt), GrowArrow(oa), run_time=0.6)
        self.at("03")
        h2 = mono(split_path(demo_path("hello2"))[1][:8], 18, AMBER).move_to(hello[2])
        was = mono(f"was {split_path(demo_path('hello'))[1][:8]}", 13, FAINT).next_to(hello, DOWN, 0.12)
        self.play(FadeOut(hello[2], shift=0.2 * UP), FadeIn(h2, shift=0.2 * UP), FadeIn(was), run_time=0.6)
        hello[0].set_stroke(AMBER)

        # 04-06: greet runs hello, so greet changes too
        self.at("04")
        self.play(FadeIn(greet), GrowArrow(e), FadeIn(uses), run_time=0.6)
        self.at("05")
        g2 = mono(split_path(demo_path("greet2"))[1][:8], 18, AMBER).move_to(greet[2])
        gwas = mono(f"was {split_path(demo_path('greet'))[1][:8]}", 13, FAINT).next_to(greet, DOWN, 0.12)
        self.play(e.animate.set_color(AMBER), run_time=0.3)
        self.play(FadeOut(greet[2], shift=0.2 * UP), FadeIn(g2, shift=0.2 * UP), FadeIn(gwas),
                  greet[0].animate.set_stroke(AMBER), run_time=0.6)
        self.at("06")
        rip = mono("the change ripples downstream", 16, AMBER).move_to([1.0, 2.35, 0])
        self.play(FadeIn(rip), run_time=0.4)

        # 07: cowsay unchanged
        self.at("07")
        same = mono("unchanged", 15, GOOD).next_to(cow, RIGHT, 0.3)
        self.play(cow[2].animate.set_color(GOOD), cow[0].animate.set_stroke(GOOD), FadeIn(same), run_time=0.6)

        # 08-10: the store, both hellos side by side (real listing)
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        lines = [l for l in DEMO.split("both are now in the store, side by side")[1].splitlines()
                 if l.endswith("-hello-2.12.1")]
        listing = sorted(set(lines))
        t = terminal([("$ ls -d /nix/store/*-hello-2.12.1", MUTED)] + [store_path(p, 17) for p in listing],
                     width=9.5).move_to([0, 0.6, 0])
        self.play(FadeIn(t[0]), FadeIn(t[1][0]), run_time=0.5)
        self.at("09")
        self.play(LaggedStart(*[FadeIn(r) for r in t[1][1:]], lag_ratio=0.4), run_time=0.9)
        lab = VGroup(mono("doCheck = false", 14, AMBER), mono("original", 14, MUTED))
        for l, r in zip(lab, t[1][1:]):
            l.next_to(r, RIGHT, 0.35)
        self.play(FadeIn(lab), run_time=0.4)
        self.at("10")
        cap = mono("never the same path → never overwritten", 20, GOOD).next_to(t, DOWN, 0.5)
        self.play(FadeIn(cap), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
