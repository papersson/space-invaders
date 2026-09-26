from rkit import *

MAKE = (DATA / "make_stale.txt").read_text().splitlines()


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("Where do the arrows come from?")
        g = Graph().scale(0.8).move_to([0, 0.3, 0])
        self.at("01")
        self.play(FadeIn(c), FadeIn(g), run_time=0.6)
        self.at("02")
        self.play(*[a.animate.set_color(ICE).set_stroke(width=4) for a in g.e.values()], run_time=0.8)
        self.at("03")
        self.play(FadeOut(g), run_time=0.4)

        # 03-07: dependencies that change with the data; recorded on each run
        self.at("04")
        tag = label("another cart", 16).move_to([-4.6, 2.6, 0])
        f = mono("total = subtotal + tax − IF(has_coupon, coupon, 0)", 20, INK).move_to([0.4, 2.6, 0])
        self.play(FadeIn(tag), FadeIn(f), run_time=0.6)

        def small(name, x, y):
            b = RoundedRectangle(corner_radius=0.08, width=1.9, height=0.6, stroke_color=TRAY_EDGE, stroke_width=1.8,
                                 fill_color=TRAY_FILL, fill_opacity=1).move_to([x, y, 0])
            return VGroup(b, mono(name, 16, INK).move_to(b))
        tot = small("total", 2.4, 0.9)
        ins = [small(nm, -3.2, y) for nm, y in (("subtotal", 1.6), ("tax", 0.9), ("has_coupon", 0.2), ("coupon", -0.5))]
        arrows = [Arrow(b.get_right(), tot.get_left(), buff=0.08, color=FAINT, stroke_width=2.2, tip_length=0.14)
                  for b in ins]
        self.play(FadeIn(tot), *[FadeIn(b) for b in ins], *[GrowArrow(a) for a in arrows[:3]], run_time=0.8)
        self.at("05")
        no = mono("has_coupon = no → coupon not read", 16, MUTED).next_to(ins[3], DOWN, 0.2).align_to(ins[3], LEFT)
        self.play(FadeIn(no), run_time=0.4)
        yes = mono("has_coupon = yes → coupon read", 16, ICE).move_to(no, aligned_edge=LEFT)
        arrows[3].set_color(ICE)
        self.play(Transform(no, yes), GrowArrow(arrows[3]), run_time=0.7)
        self.at("06")
        rec = mono("recorded on the last run: subtotal, tax, has_coupon, coupon", 16, GREEN).move_to([0.4, -1.5, 0])
        self.play(FadeIn(rec), run_time=0.6)

        # 08-14: Make with a missing prerequisite (real run)
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        mk = mono("Make: the dependencies are listed by hand, in a Makefile", 20, INK).to_edge(UP, buff=0.9)
        self.play(FadeIn(mk), run_time=0.5)
        colors = []
        for line in MAKE[:-3]:
            if "up to date" in line or ("free shipping" in line and len(colors) > 3):
                colors.append((line.replace("\t", "  "), CORAL))
            elif line.startswith("---"):
                colors.append((line, MUTED))
            else:
                colors.append((line.replace("\t", "  "), INK))
        term = terminal(colors, width=10.0).move_to([0, -0.6, 0])
        rows = term[1]
        self.at("09")
        self.play(FadeIn(term[0]), FadeIn(rows[:3]), run_time=0.8)
        self.at("11")
        self.play(FadeIn(rows[3]), run_time=0.5)
        self.at("12")
        self.play(FadeIn(rows[4]), run_time=0.4)
        self.at("13")
        self.play(FadeIn(rows[5]), run_time=0.4)
        self.play(FadeIn(rows[6]), run_time=0.4)
        self.at("14")
        fix = terminal([(MAKE[-3], MUTED), (MAKE[-2], INK), (MAKE[-1], GREEN)], width=10.0).next_to(term, DOWN, 0.15)
        self.play(FadeIn(fix), run_time=0.7)

        # 15-18: a cycle can't be ordered
        self.at("15")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        pts = [np.array([-1.6, 0.3, 0]), np.array([1.6, 0.3, 0]), np.array([0, -2.1, 0])]
        cyc = VGroup(*[Circle(radius=0.45, stroke_color=TRAY_EDGE, stroke_width=2.5, fill_color=TRAY_FILL,
                              fill_opacity=1).move_to(p) for p in pts])
        names = VGroup(*[mono(t, 20, INK).move_to(p) for t, p in zip("ABC", pts)])
        links = VGroup(*[Arrow(pts[i], pts[(i + 1) % 3], buff=0.5, color=CORAL, stroke_width=3, tip_length=0.18)
                         for i in range(3)])
        self.play(FadeIn(cyc), FadeIn(names), run_time=0.5)
        self.at("16")
        self.play(LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.4), run_time=1.2)
        first = mono("which comes first?", 20, CORAL).move_to([0, 1.5, 0])
        self.play(FadeIn(first), run_time=0.4)
        self.at("17")
        cr = mono("Excel: circular reference", 22, AMBER).move_to([3.7, -0.9, 0])
        self.play(FadeIn(cr), run_time=0.5)
        self.at("18")
        cr2 = mono("warns by default · can iterate if asked", 16, MUTED).next_to(cr, DOWN, 0.15)
        self.play(FadeIn(cr2), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
