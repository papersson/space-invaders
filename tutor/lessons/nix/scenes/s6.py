from nkit import *


def generation(n, bins, x, y, color=INK):
    r = RoundedRectangle(corner_radius=0.1, width=3.7, height=1.5, stroke_color=TRAY_EDGE, stroke_width=2,
                         fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
    t = mono(f"generation {n}", 17, color).move_to(r.get_top() + 0.3 * DOWN)
    b = mono("bin: " + " ".join(bins), 13, MUTED).move_to(r.get_center() + 0.2 * DOWN)
    return VGroup(r, t, b)


class S6(CueScene):
    SEG = "s6"

    def construct(self):
        c = chip("Installing is switching a link")
        run = DEMO.split("=== a profile")[1]
        # 01-03: a generation is a directory of links; the profile links to one
        self.at("01")
        q = mono("what does \"installed\" mean?", 22, INK).move_to([0, 2.7, 0])
        self.play(FadeIn(c), FadeIn(q), run_time=0.6)
        self.at("02")
        store = RoundedRectangle(corner_radius=0.15, width=4.2, height=4.2, stroke_color=DIM, stroke_width=1.5).move_to([4.4, -0.3, 0])
        sl = label("/nix/store", 14).next_to(store, UP, 0.12)
        items = VGroup(*[mono(s, 14, MUTED) for s in ("…-hello-2.12.1", "…-cowsay-3.8.3", "…-glibc-2.40-66", "…")])
        items.arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(store)
        g1 = generation(1, ["hello"], -0.6, 0.9)
        l1 = arrow(g1[0].get_right(), items[0].get_left(), color=FAINT)
        self.play(FadeIn(store), FadeIn(sl), FadeIn(items), FadeIn(g1), GrowArrow(l1), run_time=0.8)
        self.at("03")
        prof = box("profile", -5.0, 0.9, w=2.0, color=AMBER, edge=AMBER)
        pa = arrow(prof.get_right(), g1[0].get_left(), color=AMBER)
        self.play(FadeIn(prof), GrowArrow(pa), run_time=0.6)

        # 04-07: install cowsay: generation 2, then one switch of the link
        self.at("04")
        pl1 = mono("profile -> profile-1-link", 15, MUTED).move_to([-3.4, -2.9, 0])
        self.play(FadeIn(pl1), run_time=0.4)
        self.at("05")
        g2 = generation(2, ["cowsay", "cowthink", "hello"], -0.6, -1.3)
        l2 = VGroup(arrow(g2[0].get_right(), items[0].get_left(), color=FAINT),
                    arrow(g2[0].get_right(), items[1].get_left(), color=FAINT))
        self.play(FadeIn(g2), *[GrowArrow(a) for a in l2], run_time=0.7)
        pa2 = arrow(prof.get_right(), g2[0].get_left(), color=AMBER)
        self.play(Transform(pa, pa2), run_time=0.5)
        pl2 = mono("profile -> profile-2-link", 15, AMBER).move_to(pl1)
        self.play(Transform(pl1, pl2), run_time=0.3)
        self.at("06")
        one = mono("one step: never half old, half new", 16, AMBER).move_to([-3.2, 2.0, 0])
        self.play(FadeIn(one), FadeOut(q), run_time=0.5)
        self.at("07")
        self.play(Indicate(pa, color=AMBER, scale_factor=1.05), run_time=0.8)

        # 08-09: roll back
        self.at("08")
        rb = mono([l for l in run.splitlines() if l.startswith("switching profile")][0], 15, ICE).move_to([-3.4, -3.35, 0])
        pa1 = arrow(prof.get_right(), g1[0].get_left(), color=AMBER)
        self.play(FadeIn(rb), run_time=0.3)
        self.play(Transform(pa, pa1), Transform(pl1, mono("profile -> profile-1-link", 15, ICE).move_to(pl1)), run_time=0.6)
        self.at("09")
        kept = mono("store: nothing deleted", 15, GOOD).next_to(store, DOWN, 0.15)
        self.play(g2.animate.set_opacity(0.4), l2.animate.set_opacity(0.4), FadeIn(kept), run_time=0.6)

        # 10-11: old generations, and the garbage collector
        self.at("10")
        stay = mono("old generations stay until you delete them", 16, MUTED).move_to([-2.2, 2.85, 0])
        self.play(FadeOut(one), FadeIn(stay), run_time=0.5)
        self.at("11")
        gc = mono("then: garbage collector removes paths nothing uses", 16, AMBER).next_to(stay, DOWN, 0.15).align_to(stay, LEFT)
        self.play(FadeIn(gc), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
