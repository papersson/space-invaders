from dkit import *


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("The answer")
        # 01-03: declare; a loop compares and fixes, like a thermostat
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        self.at("02")
        dec = mono("you declare:  replicas = 3", 22, AMBER).move_to([0, 2.6, 0])
        self.play(FadeIn(dec), run_time=0.5)
        self.at("03")
        l1 = Loop(("measure", "compare", "act"), center=(-3.0, 0.2), r=1.2, size=14)
        l2 = Loop(("desired", "current", "act"), center=(3.0, 0.2), r=1.2, size=14)
        t1 = label("thermostat", 14).next_to(l1, DOWN, 0.3)
        t2 = label("controller", 14).next_to(l2, DOWN, 0.3)
        self.play(FadeIn(l1), FadeIn(l2), FadeIn(t1), FadeIn(t2), run_time=0.6)
        self.play(l1.spin(1, 1.4), l2.spin(1, 1.4), run_time=1.4)

        # 04-06: level-triggered; absolute target
        self.at("04")
        self.play(FadeOut(t1), FadeOut(t2), FadeOut(l1), FadeOut(l2), run_time=0.4)
        a1 = mono("compares whole states: level-triggered, not edge-triggered", 20, ICE).move_to([0, 0.9, 0])
        self.play(FadeIn(a1), run_time=0.5)
        self.at("05")
        a2 = mono("a missed event is caught on the next pass", 18, MUTED).next_to(a1, DOWN, 0.3)
        self.play(FadeIn(a2), run_time=0.4)
        self.at("06")
        a3 = mono("an absolute target: running it again does no harm", 18, MUTED).next_to(a2, DOWN, 0.6)
        self.play(FadeIn(a3), run_time=0.4)

        # 07-08: continuous vs when you run it
        self.at("07")
        self.play(FadeOut(a1), FadeOut(a2), FadeOut(a3), FadeOut(dec), run_time=0.4)
        k = VGroup(mono("Kubernetes", 26, INK), mono("continuous", 22, ICE)).arrange(DOWN, buff=0.2).move_to([-3.2, 0.8, 0])
        self.play(FadeIn(k), run_time=0.5)
        self.at("08")
        tf = VGroup(mono("Terraform CLI", 26, INK), mono("when you run it", 22, AMBER)).arrange(DOWN, buff=0.2).move_to([3.2, 0.8, 0])
        self.play(FadeIn(tf), run_time=0.5)

        # 09: eventual agreement
        self.at("09")
        ev = mono("eventual agreement, not an instant guarantee", 20, INK).move_to([0, -1.2, 0])
        chk = mono("check the status · watch what no tool manages", 16, MUTED).next_to(ev, DOWN, 0.2)
        self.play(FadeIn(ev), run_time=0.5)
        self.play(FadeIn(chk), run_time=0.4)

        # end card
        self.until(self.end_of("09", 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("Make It So", 40, INK, weight=SEMIBOLD).move_to([0, 2.5, 0])
        s1 = T("Declare the state you want. A loop compares it with what exists and fixes the difference.", 22, INK).next_to(name, DOWN, 0.5)
        s1b = T("Kubernetes runs that loop all the time; Terraform's command-line tool, when you run it.", 22, INK).next_to(s1, DOWN, 0.12)
        refs = VGroup(T("Further reading", 17, MUTED, weight=MEDIUM),
                      T("Kubernetes documentation, \"Controllers\"; design principles and API conventions (level-based logic)", 16, MUTED),
                      T("Burns, Grant, Oppenheimer, Brewer & Wilkes, \"Borg, Omega, and Kubernetes\", ACM Queue (2016)", 16, MUTED),
                      T("Brikman, Terraform: Up & Running, 3rd ed. (2022), ch. 1-3 · Terraform documentation, \"plan\" and \"apply\"", 16, MUTED),
                      T("Åström & Murray, Feedback Systems (2008), ch. 1", 16, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s1b, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(s1), FadeIn(s1b), run_time=0.7)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
