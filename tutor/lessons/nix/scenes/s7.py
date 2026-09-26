from nkit import *


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("A whole system")
        base = NIXOS.split("=== configuration.nix (base):")[1].split("system:")[0].strip().splitlines()
        p0, p1, p2 = system_paths()
        # 01-03: one file describes the system; one store path
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        os_l = mono("NixOS: the same idea, for a whole operating system", 18, INK).move_to([0, 2.8, 0])
        self.play(FadeIn(os_l), run_time=0.5)
        self.at("02")
        code = VGroup(*[mono(l, 16, INK) for l in base]).arrange(DOWN, buff=0.1, aligned_edge=LEFT)
        fb = SurroundingRectangle(code, buff=0.3, color=DIM, stroke_width=1.5, corner_radius=0.1)
        fl = mono("configuration.nix  (can import other files)", 14, MUTED).next_to(fb, UP, 0.12).align_to(fb, LEFT)
        cfg = VGroup(fb, code, fl).move_to([-2.6, 1.0, 0])
        self.play(FadeIn(cfg), run_time=0.6)
        self.at("03")
        what = mono("programs · configuration files · start-up scripts", 14, MUTED).move_to([-2.6, -0.4, 0])
        self.play(FadeIn(what), run_time=0.4)
        out = store_path(p0, 15, short=True).move_to([0, -1.5, 0])
        oa = arrow(what.get_bottom(), out.get_top() + 0.3 * LEFT)
        self.play(GrowArrow(oa), FadeIn(out), run_time=0.6)

        # 04-07: evaluated here: add nginx -> new path; remove -> the first path again (real run)
        self.at("04")
        ev = mono("evaluated on this machine (nixpkgs 50ab793786d9)", 14, MUTED).next_to(out, DOWN, 0.2)
        self.play(FadeIn(ev), run_time=0.4)
        self.at("05")
        self.play(Indicate(out[1], color=AMBER, scale_factor=1.1), run_time=0.8)
        self.at("06")
        add = mono("services.nginx.enable = true;", 16, AMBER).next_to(code, DOWN, 0.1).align_to(code, LEFT)
        self.play(FadeIn(add, shift=0.3 * RIGHT), fb.animate.stretch_to_fit_height(fb.height + 0.4).shift(0.2 * DOWN), run_time=0.6)
        out2 = store_path(p1, 15, short=True).move_to(out)
        out2[1].set_color(AMBER)
        self.play(FadeOut(out, shift=0.2 * UP), FadeIn(out2, shift=0.2 * UP), run_time=0.6)
        self.at("07")
        self.play(FadeOut(add, shift=0.3 * RIGHT), fb.animate.stretch_to_fit_height(fb.height - 0.4).shift(0.2 * UP), run_time=0.6)
        out3 = store_path(p2, 15, short=True, hash_color=GOOD).move_to(out)
        same = mono("same as before", 15, GOOD).next_to(out3, RIGHT, 0.3)
        self.play(FadeOut(out2, shift=0.2 * UP), FadeIn(out3, shift=0.2 * UP), FadeIn(same), run_time=0.6)

        # 08-09: generations in the boot menu (illustration)
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        menu_r = DashedVMobject(RoundedRectangle(corner_radius=0.1, width=6.4, height=2.6, stroke_color=MUTED,
                                                 stroke_width=1.8), num_dashes=60).move_to([0, 0.6, 0])
        ill = mono("illustration", 14, MUTED).next_to(menu_r, UP, 0.12).align_to(menu_r, RIGHT)
        rows = VGroup(*[mono(t, 18, INK) for t in ("NixOS - Configuration 42", "NixOS - Configuration 41",
                                                     "NixOS - Configuration 40")]).arrange(DOWN, buff=0.3, aligned_edge=LEFT)
        rows.move_to(menu_r)
        sel = Rectangle(width=5.8, height=0.5, stroke_width=0, fill_color=ICE, fill_opacity=0.25).move_to(rows[0])
        self.play(Create(menu_r), FadeIn(ill), FadeIn(sel), FadeIn(rows), run_time=0.7)
        self.at("09")
        self.play(sel.animate.move_to(rows[1]), run_time=0.6)
        rb = mono("or:  nixos-rebuild switch --rollback", 16, MUTED).next_to(menu_r, DOWN, 0.3)
        self.play(FadeIn(rb), run_time=0.4)

        # 10-11: the link switches at once; the running machine catches up
        self.at("10")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        one = mono("link to the new system generation: switches in one step", 18, AMBER).move_to([0, 0.8, 0])
        self.play(FadeIn(one), run_time=0.5)
        self.at("11")
        slow = VGroup(mono("the running machine: takes longer", 18, INK),
                      mono("services restart one by one", 16, MUTED),
                      mono("a new kernel needs a reboot", 16, MUTED)).arrange(DOWN, buff=0.15, aligned_edge=LEFT)
        slow.move_to([0, -0.8, 0])
        self.play(FadeIn(slow[0]), run_time=0.4)
        self.play(FadeIn(slow[1]), run_time=0.4)
        self.play(FadeIn(slow[2]), run_time=0.4)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
