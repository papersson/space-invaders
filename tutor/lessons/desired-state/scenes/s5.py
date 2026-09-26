from dkit import *


class S5(CueScene):
    SEG = "s5"

    def construct(self):
        c = chip("Once, or forever")
        # 01-04: both reconcile; the difference is when
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        lp = Loop(("desired", "current", "act"), center=(0, 0.3), r=1.3, size=15)
        self.play(FadeIn(lp), lp.spin(1, 1.4), run_time=1.4)
        self.at("02")
        how = mono("how often does it run?", 22, AMBER).move_to([0, -2.0, 0])
        self.play(FadeIn(how), run_time=0.5)
        self.at("03")
        both = mono("both tools reconcile", 20, INK).move_to([0, 2.5, 0])
        self.play(FadeIn(both), run_time=0.4)
        self.at("04")
        when = mono("the difference is when", 20, AMBER).move_to(how)
        self.play(Transform(how, when), run_time=0.5)

        # 05-08: Terraform: compares when you run it, then stops; a server deleted by hand stays deleted
        self.at("05")
        self.play(FadeOut(lp), FadeOut(how), FadeOut(both), run_time=0.4)
        head = mono("terraform (command-line tool): compares when you run it, then stops", 17, INK).move_to([0, 2.7, 0])
        self.play(FadeIn(head), run_time=0.5)
        self.at("06")
        names = run_line("servers on disk: web-0 web-1 web-2 web-3 web-4").split(": ")[1].split()
        srv = [server(n, -4.4 + 2.2 * i, 1.2) for i, n in enumerate(names)]
        sim = mono("servers simulated as files", 13, MUTED).next_to(VGroup(*srv), DOWN, 0.2)
        self.play(LaggedStart(*[FadeIn(s) for s in srv], lag_ratio=0.15), FadeIn(sim), run_time=0.9)
        self.at("07")
        rm = terminal([("$ rm servers/web-1", AMBER)], width=4.0).move_to([-3.6, -0.6, 0])
        self.play(FadeIn(rm), run_time=0.4)
        x = cross(srv[1].get_center())
        self.play(Create(x), run_time=0.3)
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=1.35, height=0.8, stroke_color=FAINT,
                                                stroke_width=1.5).move_to(srv[1]), num_dashes=24)
        self.play(FadeOut(srv[1]), FadeOut(x), FadeIn(ghost), run_time=0.5)
        self.at("08")
        t = ValueTracker(0)
        idle = always_redraw(lambda: mono(f"terraform not running · {int(t.get_value())} min", 15, MUTED)
                             .move_to([2.6, -0.6, 0]))
        self.add(idle)
        self.play(t.animate.set_value(45), run_time=max(1.0, self.end_of("08") - self.now()), rate_func=linear)
        still = mono(run_line("servers on disk: web-0 web-2"), 15, BAD).move_to([2.6, -1.1, 0])
        self.play(FadeIn(still), run_time=0.4)

        # 09-10: its record, refreshed on the next plan
        self.at("09")
        rec = mono("its record: 5 servers created", 15, INK).move_to([-3.6, -1.6, 0])
        self.play(FadeIn(rec), run_time=0.4)
        self.at("10")
        self.remove(idle)
        plan = terminal([("$ terraform plan", MUTED), (run_line("# local_file.server[1]"), AMBER),
                         (run_line("Plan: 1 to add"), AMBER)], width=6.8).move_to([1.9, -2.3, 0])
        self.play(FadeOut(still), FadeIn(plan), run_time=0.7)

        # 11-13: the script picture fails
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        w1 = mono("apply = a script: run once, and it's done?", 20, MUTED).move_to([0, 1.2, 0])
        self.play(FadeIn(w1), run_time=0.4)
        self.play(Create(Line(w1.get_left(), w1.get_right(), stroke_color=BAD, stroke_width=3)), run_time=0.4)
        self.at("12")
        w2 = mono("applying didn't hold the system there", 20, INK).move_to([0, 0.3, 0])
        self.play(FadeIn(w2), run_time=0.4)
        self.at("13")
        w3 = mono("terraform checks only when you ask", 20, AMBER).move_to([0, -0.5, 0])
        self.play(FadeIn(w3), run_time=0.4)

        # 14-15: a Kubernetes loop has no end
        self.at("14")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        lk = Loop(("desired", "current", "act"), center=(-3.2, 0.2), r=1.3, size=15)
        kh = mono("Kubernetes controller: runs all the time", 17, INK).move_to([0, 2.7, 0])
        self.play(FadeIn(lk), FadeIn(kh), run_time=0.5)
        self.play(lk.spin(1, 1.2), run_time=1.2)
        self.at("15")
        ps = [pod([1.6 + 1.1 * i, 0.9, 0]) for i in range(3)]
        self.play(*[FadeIn(p) for p in ps], lk.spin(1, 1.0), run_time=1.0)
        self.play(ps[1].animate.set_color(BAD), run_time=0.3)
        self.play(FadeOut(ps[1]), run_time=0.3)
        rep = pod(ps[1].get_center())
        self.play(FadeIn(rep, scale=0.6), lk.spin(1, 0.9), run_time=0.9)
        sec = VGroup(mono("deleted copy → replaced within seconds", 15, ICE),
                     mono("dead machine → a few minutes (the grace period)", 15, MUTED)).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
        sec.move_to([2.4, -0.6, 0])
        self.play(FadeIn(sec[0]), run_time=0.4)
        self.play(FadeIn(sec[1]), lk.spin(1, 1.2), run_time=1.2)

        # 16-18: drift
        self.at("16")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        des = VGroup(mono("desired", 16, MUTED), mono("5 servers", 24, AMBER)).arrange(DOWN, buff=0.12).move_to([-3.0, 1.2, 0])
        cur = VGroup(mono("current", 16, MUTED), mono("4 servers", 24, BAD)).arrange(DOWN, buff=0.12).move_to([3.0, 1.2, 0])
        gap = DoubleArrow(des.get_right() + 0.3 * RIGHT, cur.get_left() + 0.3 * LEFT, buff=0.1, color=BAD, stroke_width=3)
        dr = T("drift", 30, BAD).next_to(gap, UP, 0.2)
        self.play(FadeIn(des), FadeIn(cur), GrowFromCenter(gap), FadeIn(dr), run_time=0.8)
        self.at("17")
        a = mono("terraform: drift waits for the next run", 20, AMBER).move_to([0, -0.6, 0])
        self.play(FadeIn(a), run_time=0.5)
        self.at("18")
        b = mono("continuous loop: repaired as soon as it's noticed", 20, ICE).move_to([0, -1.4, 0])
        self.play(FadeIn(b), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
