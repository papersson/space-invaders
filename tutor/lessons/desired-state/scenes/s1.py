from dkit import *


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        # 01: three copies of a web app on three machines
        self.at("01")
        head = mono("Kubernetes:  replicas = 3", 22, INK).move_to([0, 2.6, 0])
        ms = [Machine(f"machine {i + 1}", x, 0.2) for i, x in enumerate((-3.6, 0, 3.6))]
        pods = [pod(m.slot(0, 1)) for m in ms]
        count = mono("running: 3", 20, ICE).move_to([0, -1.6, 0])
        self.play(FadeIn(head), *[FadeIn(m) for m in ms], run_time=0.7)
        self.play(LaggedStart(*[FadeIn(p, scale=0.8) for p in pods], lag_ratio=0.25), FadeIn(count), run_time=0.8)

        # 02: 03:00, machine 2 dies with its copy
        self.at("02")
        clock = mono("03:00", 26, AMBER).move_to([5.3, 2.6, 0])
        self.play(FadeIn(clock), run_time=0.4)
        self.play(ms[1].box.animate.set_stroke(DIM).set_fill(BG), ms[1].name.animate.set_color(DIM),
                  pods[1].animate.set_color(BAD), run_time=0.6)
        self.play(FadeOut(pods[1]), Transform(count, mono("running: 2", 20, BAD).move_to(count)), run_time=0.5)
        dead = mono("no longer reporting", 14, FAINT).next_to(ms[1].box, DOWN, 0.15)
        self.play(FadeIn(dead), run_time=0.3)

        # 03-04: the clock runs; nobody acts; a new copy appears
        self.at("03")
        t = ValueTracker(0)
        clk = always_redraw(lambda: mono(f"03:{int(t.get_value()):02d}", 26, AMBER).move_to([5.3, 2.6, 0]))
        self.remove(clock)
        self.add(clk)
        self.play(t.animate.set_value(6), run_time=max(1.0, self.start_of("04") - self.now() + 0.6), rate_func=linear)
        new = pod(ms[2].slot(1, 2), color=ICE)
        self.play(pods[2].animate.move_to(ms[2].slot(0, 2)), run_time=0.3)
        self.play(FadeIn(new, scale=0.6), Transform(count, mono("running: 3", 20, ICE).move_to(count)), run_time=0.6)
        nobody = mono("nobody touched anything", 16, MUTED).move_to([0, -2.3, 0])
        self.play(FadeIn(nobody), run_time=0.4)

        # 05-07: Terraform: five servers, one deleted by hand
        self.at("05")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.remove(clk)
        head2 = mono("Terraform:  servers = 5", 22, INK).move_to([0, 2.6, 0])
        self.play(FadeIn(head2), run_time=0.4)
        self.at("06")
        srv = [server(f"web-{i}", -4.4 + 2.2 * i, 0.4) for i in range(5)]
        self.play(LaggedStart(*[FadeIn(s, shift=0.2 * UP) for s in srv], lag_ratio=0.2), run_time=1.0)
        self.at("07")
        hand = Triangle(fill_color=INK, fill_opacity=1, stroke_width=0).scale(0.14).rotate(0.5)
        hand.move_to([-1.0, -1.6, 0])
        self.play(FadeIn(hand), run_time=0.2)
        self.play(hand.animate.move_to(srv[1].get_bottom() + 0.15 * DOWN), run_time=0.6)
        x = cross(srv[1].get_center())
        self.play(Create(x), run_time=0.3)
        self.play(FadeOut(srv[1]), FadeOut(x), FadeOut(hand), run_time=0.5)
        ghost = DashedVMobject(RoundedRectangle(corner_radius=0.08, width=1.35, height=0.8, stroke_color=FAINT,
                                                stroke_width=1.5).move_to(srv[1]), num_dashes=24)
        self.play(FadeIn(ghost), run_time=0.3)

        # 08-09: nothing happens until the next run
        self.at("08")
        four = mono("servers: 4", 20, BAD).move_to([0, -1.2, 0])
        self.play(FadeIn(four), run_time=0.4)
        self.at("09")
        until = mono("until the next terraform run", 16, MUTED).next_to(four, DOWN, 0.25)
        self.play(FadeIn(until), run_time=0.4)

        # 10-12: the question
        self.at("10")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        l0 = T("a description of what you want  →  reality", 26, MUTED).move_to([0, 1.6, 0])
        self.play(FadeIn(l0), run_time=0.5)
        self.at("11")
        q1 = T("How do they make it real, and keep it that way?", 34, INK).move_to([0, 0.3, 0])
        self.play(FadeIn(q1), run_time=0.6)
        self.at("12")
        q2 = T("Why does one repair things by itself, while the other waits for you?", 28, INK).next_to(q1, DOWN, 0.5)
        self.play(FadeIn(q2), run_time=0.6)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
