from nkit import *

INPUTS = ["source", "build script", "compiler", "libraries", "options"]


class S9(CueScene):
    SEG = "s9"

    def construct(self):
        c = chip("The answer")
        hp = demo_path("hello")
        # 01-02: the hash names everything that went in
        self.at("01")
        p = store_path(hp, 20).move_to([0, 2.4, 0])
        self.play(FadeIn(c), FadeIn(p), run_time=0.6)
        self.at("02")
        ins = VGroup(*[mono(t, 16, AMBER) for t in INPUTS]).arrange(RIGHT, buff=0.5).move_to([0, 1.3, 0])
        arrs = VGroup(*[arrow(p[1].get_bottom(), i.get_top(), color=AMBER) for i in ins])
        self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(i)) for a, i in zip(arrs, ins)], lag_ratio=0.15),
                  run_time=1.0)

        # 03-06: three consequences
        self.at("03")
        lines = [("04", "no overwriting → versions side by side"), ("05", "exact paths → exact dependencies"),
                 ("06", "switch one link → upgrade, rollback")]
        shown = VGroup()
        for i, (cue, text) in enumerate(lines):
            self.at(cue)
            t = mono(text, 20, ICE).move_to([0, 0.1 - 0.6 * i, 0])
            shown.add(t)
            self.play(FadeIn(t), run_time=0.5)

        # 07-09: what it fixes, and what it doesn't
        self.at("07")
        fx = mono("the hash fixes the inputs: pin them", 18, AMBER).move_to([0, -2.1, 0])
        self.play(FadeIn(fx), run_time=0.5)
        self.at("08")
        by = mono("the bytes usually, but not always, follow", 16, MUTED).next_to(fx, DOWN, 0.15)
        self.play(FadeIn(by), run_time=0.4)
        self.at("09")
        bk = mono("back up your data", 16, BAD).next_to(by, DOWN, 0.15)
        self.play(FadeIn(bk), run_time=0.4)

        # end card
        self.until(self.end_of("09", 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("A Hash in Every Path", 40, INK, weight=SEMIBOLD).move_to([0, 2.5, 0])
        s1 = T("Nix names every build by a hash of everything that went into it, so nothing is overwritten:", 22, INK).next_to(name, DOWN, 0.5)
        s1b = T("versions coexist, dependencies are exact, and upgrades and rollbacks switch one link.", 22, INK).next_to(s1, DOWN, 0.12)
        refs = VGroup(T("Further reading", 17, MUTED, weight=MEDIUM),
                      T("Dolstra, The Purely Functional Software Deployment Model, PhD thesis, Utrecht (2006)", 16, MUTED),
                      T("Dolstra, de Jonge & Visser, \"Nix: A Safe and Policy-Free System for Software Deployment\", LISA (2004)", 16, MUTED),
                      T("Dolstra & Löh, \"NixOS: A Purely Functional Linux Distribution\", ICFP (2008) · Bruno, Nix Pills", 16, MUTED),
                      T("Malka, Zacchiroli & Zimmermann, \"Does Functional Package Management Enable Reproducible Builds at Scale? Yes.\", MSR (2025)", 16, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s1b, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(s1), FadeIn(s1b), run_time=0.7)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
