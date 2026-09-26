from skit import *
from s1 import A_Y, B_Y


class S2(AgentScene):
    SEG = "s2"

    def construct(self):
        # the end of chapter 1: project and the two strips
        proj0 = Project()
        A = Strip("loop_1", A_Y, labels={18: "Fixed."})
        B = Strip("no_tests_1", B_Y, labels={10: "Fixed."})
        la = label("run A", 16, INK).next_to(A.cards[0], UP, 0.22).align_to(A.cards[0], LEFT)
        lb = label("run B", 16, INK).next_to(B.cards[0], UP, 0.22).align_to(B.cards[0], LEFT)
        self.add(proj0, *A.cards, *B.cards, la, lb)

        self.picture("bare_1", 0, tag=False, code=False, add=False, labels={2: "text"})
        self.add(self.proj)
        self.remove(proj0)

        # 01: start again, from the model on its own
        self.at("01")
        self.play(FadeOut(VGroup(*A.cards, *B.cards, la, lb), shift=0.3 * DOWN), run_time=0.8)
        self.play(FadeIn(self.model), run_time=0.6)

        # 02-03: text in, text out
        self.at("02")
        tin = Arrow(self.model[0].get_left() + LEFT * 1.6, self.model[0].get_left(), buff=0.1, color=MUTED, stroke_width=3)
        tout = Arrow(self.model[0].get_right(), self.model[0].get_right() + RIGHT * 1.6, buff=0.1, color=BLUE, stroke_width=3)
        lin, lout = mono("text", 16, MUTED).next_to(tin, UP, 0.1), mono("text", 16, BLUE).next_to(tout, UP, 0.1)
        self.play(GrowArrow(tin), FadeIn(lin), run_time=0.5)
        self.at("03")
        self.play(GrowArrow(tout), FadeIn(lout), run_time=0.5)

        # 04-05: its context: instructions and our task
        self.at("04")
        self.play(FadeOut(VGroup(tin, tout, lin, lout)), run_time=0.3)
        c0, c1 = self.strip.cards[0], self.strip.cards[1]
        self.play(FadeIn(c0, shift=0.2 * UP), FadeIn(c1, shift=0.2 * UP), run_time=0.6)
        self.shown = 2
        br = Brace(VGroup(c0, c1), DOWN, buff=0.08, color=MUTED)
        ctx = mono("context", 16, MUTED).next_to(br, DOWN, 0.06)
        self.play(GrowFromCenter(br), FadeIn(ctx), run_time=0.5)
        self.at("05")
        self.play(Indicate(c0, color=INK, scale_factor=1.06), run_time=0.6)
        self.play(Indicate(c1, color=INK, scale_factor=1.1), run_time=0.6)

        # 06: through the command-line tool, its own tools off
        self.at("06")
        tag = mono("claude -p, tools off", 13, MUTED).next_to(self.model[0], DOWN, 0.1)
        self.play(FadeIn(tag), run_time=0.5)
        self.model.add(tag)

        # 07: it reads everything, and replies with text
        self.at("07")
        self.play(FadeOut(br), FadeOut(ctx), run_time=0.3)
        self.read(0.6)
        reply = self.model_writes(0.5)

        # 08: the reply, opened: it writes out a shell command (captures/bare_1.json)
        self.at("08")
        text = S["bare_1"]["cards"][-1]["text"]
        cmd = '{"command":"find /home/user/space-invaders -maxdepth 3 -iname \'*report*\' 2>/dev/null; echo ---; pwd; ls"}'
        first = "I'll look at the test and the report.py file to understand what's failing."
        for part in (first, "**Tool: bash**", "Parameters:", cmd):
            assert part in text, part
        panel = quote([first, "", "**Tool: bash**", "Parameters:",
                       ('{"command":"find /home/user/space-invaders -maxdepth 3', AMBER),
                       ("  -iname '*report*' 2>/dev/null; echo ---; pwd; ls\"}", AMBER)], 14,
                      title="the model's reply")
        panel.move_to([-1.4, -0.3, 0])
        keep_on_screen(panel)
        link = Line(reply.get_top(), panel.get_bottom(), stroke_color=FAINT, stroke_width=1.5)
        self.play(Create(link), FadeIn(panel), run_time=0.6)

        # 09: nothing runs text
        self.at("09")
        tgt = self.proj.get_left() + LEFT * 0.2
        start = panel[1][4].get_right() + RIGHT * 0.15
        stop = start + (tgt - start) * 0.55
        dash = DashedLine(start, stop, stroke_color=AMBER, stroke_width=2.5, dash_length=0.1)
        end = cross(stop, 0.1, MUTED, 4)
        self.play(Create(dash), run_time=0.7)
        self.play(FadeIn(end), run_time=0.3)

        # 10: the test still fails
        self.at("10", 1.2)
        self.play(Indicate(self.proj.badge, color=CORAL, scale_factor=1.6), run_time=0.9)

        # 11: something else has to act on it
        self.at("11")
        self.play(FadeOut(VGroup(dash, end, link, panel)), run_time=0.8)
        self.until(self.dur)
        self.finish()
