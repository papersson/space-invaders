from nkit import *


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        # 01: a normal package manager
        self.at("01")
        l1 = label("a normal package manager", 15).move_to([0, 2.7, 0])
        t1 = terminal([("/usr/bin/hello", INK)], width=9.8, size=22).move_to([0, 1.9, 0])
        self.play(FadeIn(l1), FadeIn(t1), run_time=0.7)

        # 02-03: Nix, and the hash
        self.at("02")
        l2 = label("nix", 15).move_to([0, 0.75, 0])
        p = store_path(demo_path("hello"), 22, hash_color=INK)
        t2 = terminal([p], width=9.8).move_to([0, -0.05, 0])
        self.play(FadeIn(l2), FadeIn(t2), run_time=0.7)
        self.at("03")
        h = p[1]
        self.play(h.animate.set_color(AMBER), run_time=0.5)
        br = Brace(h, DOWN, buff=0.12, color=AMBER)
        bl = mono("a hash: 32 characters", 16, AMBER).next_to(br, DOWN, 0.1)
        self.play(GrowFromCenter(br), FadeIn(bl), run_time=0.6)

        # 04-07: the promises
        self.at("04")
        self.play(FadeOut(l1), FadeOut(t1), FadeOut(l2), VGroup(t2, br, bl).animate.shift(1.9 * UP), run_time=0.6)
        nixos = mono("NixOS: a Linux distribution built on Nix", 16, MUTED).move_to([0, -0.2, 0])
        self.play(FadeIn(nixos), run_time=0.4)
        cards = []
        for i, (cue, text) in enumerate((("05", "same build, same result"), ("06", "versions side by side"),
                                         ("07", "roll back: a program or a machine"))):
            self.at(cue)
            cd = box(text, -4.55 + 4.55 * i, -1.5, w=4.4, h=0.9, color=ICE, size=14)
            cards.append(cd)
            self.play(FadeIn(cd, shift=0.2 * UP), run_time=0.5)

        # 08-09: the question
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        q1 = T("Why is there a hash in every path?", 36, INK).move_to([0, 0.5, 0])
        self.play(FadeIn(q1), run_time=0.6)
        self.at("09")
        q2 = T("And how does that one idea deliver all of that?", 28, MUTED).next_to(q1, DOWN, 0.5)
        self.play(FadeIn(q2), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
