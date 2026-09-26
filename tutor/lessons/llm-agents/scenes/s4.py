from skit import *


def loop_arrows(model, code):
    a = CurvedArrow(model[0].get_right() + DOWN * 0.1, code[0].get_top() + LEFT * 0.3, angle=-TAU / 5,
                    color=BLUE, stroke_width=3, tip_length=0.18)
    b = CurvedArrow(code[0].get_left() + DOWN * 0.1, model[0].get_bottom() + RIGHT * 0.5 + DOWN * 0.35, angle=-TAU / 6,
                    color=GREEN, stroke_width=3, tip_length=0.18)
    return VGroup(a, b)


def line_marker(text_mob, src_line, sub, color, nth=1):
    """A thin underline under the nth occurrence of `sub` in a mono line of text."""
    i = -1
    for _ in range(nth):
        i = src_line.index(sub, i + 1)
    cw = text_mob.width / len(src_line)
    x0 = text_mob.get_left()[0] + i * cw
    return Line([x0, text_mob.get_bottom()[1] - 0.06, 0], [x0 + cw * len(sub), text_mob.get_bottom()[1] - 0.06, 0],
                stroke_color=color, stroke_width=4)


BUG_LINE = 'totals[region] = totals.get(region, 0) + int(row["units"]) + float(row["unit_price"])'
FIX_LINE = 'totals[region] = totals.get(region, 0) + int(row["units"]) * float(row["unit_price"])'


class S4(AgentScene):
    SEG = "s4"

    def construct(self):
        # the end of chapter 3: one tool call answered, the second left waiting
        self.picture("one_tool_1", 5, tag=True)
        ring = DashedVMobject(SurroundingRectangle(self.strip.cards[4], color=AMBER, buff=0.06, corner_radius=0.08), num_dashes=24)
        self.code.set_opacity(0.45)
        self.add(ring)

        # 01: therefore, a loop
        self.at("01")
        arrows = loop_arrows(self.model, self.code)
        self.play(FadeOut(ring), self.code.animate.set_opacity(1), run_time=0.4)
        self.play(Create(arrows[0]), Create(arrows[1]), run_time=0.8)

        # 02-05: the loop, as it ran (sims/agent.py, agent())
        card = code_lines(AGENT_SRC, 15).move_to([0, 0.05, 0]).align_to([X0, 0, 0], LEFT)
        rows = card[1]
        src = AGENT_SRC.rstrip("\n").split("\n")

        def hl(*idx):
            g = VGroup()
            for i in idx:
                r = rows[i]
                g.add(Rectangle(width=card[0].width - 0.25, height=r.height + 0.12, stroke_width=0, fill_color=BLUE,
                                fill_opacity=0.16).move_to([card[0].get_center()[0], r.get_center()[1], 0]))
            return g

        def find(sub):
            return next(i for i, l in enumerate(src) if sub in l)

        self.at("02", -0.2)
        self.play(FadeIn(card), run_time=0.6)
        h = hl(find("reply = call_model"))
        self.play(FadeIn(h), run_time=0.3)
        self.at("03")
        h2 = hl(find("request = parse_tool_call"), find('context.append(("result"'))
        self.play(ReplacementTransform(h, h2), run_time=0.4)
        self.at("04")
        h3 = hl(find("for _ in range"), find("reply = call_model"))
        self.play(ReplacementTransform(h2, h3), run_time=0.4)
        self.at("05")
        h4 = hl(find("if request is None"), find("return context"), 0)
        self.play(ReplacementTransform(h3, h4), run_time=0.4)

        # 06-07: that loop is an agent: a dot runs the loop
        self.at("06")
        self.play(FadeOut(h4), run_time=0.3)
        dot = Dot(color=INK, radius=0.07)
        for _ in range(2):
            self.play(MoveAlongPath(dot, arrows[0]), run_time=0.7, rate_func=linear)
            self.play(MoveAlongPath(dot, arrows[1]), run_time=0.7, rate_func=linear)
        self.remove(dot)

        # 08: run A from its first call (captures/loop_1.json)
        self.at("08")
        old = VGroup(*self.strip.cards[2:5])
        self.play(FadeOut(card), FadeOut(old), run_time=0.6)
        A = Strip("loop_1", STRIP_Y, labels={18: "Fixed."})
        self.remove(*self.strip.cards[:2])
        self.add(*A.cards[:2])
        self.strip, self.shown = A, 2

        # 09: lists the files, reads the test, reads the code
        self.at("09")
        t = (self.cues["09"][1] - self.now() + 0.4) / 3
        for _ in range(3):
            self.step(tool_file(self.strip.cards[self.shown]), t=t)

        # 10: the bug: adds where it should multiply (the report.py result, as read)
        self.at("10")
        rtext = self.strip.cards[7].data["text"]
        assert BUG_LINE in rtext
        panel = quote([BUG_LINE], 14, title="report.py, as read")
        op = callout(self.strip.cards[7], panel, UP, 0.35)
        keep_on_screen(op)
        mark = line_marker(panel[1][0], BUG_LINE, "+", CORAL, nth=2)
        self.play(FadeIn(op), run_time=0.4)
        self.play(Create(mark), run_time=0.4)

        # 11: rewrites the line, then asks to run the test
        self.at("11")
        wtext = self.strip.cards[8].data["text"]
        assert FIX_LINE.replace('"', '\\"') in wtext, "fix line in write_file"
        self.step("report.py", t=1.3)
        panel2 = quote([FIX_LINE], 14, title="report.py, as written")
        panel2.move_to(panel)
        mark2 = line_marker(panel2[1][0], FIX_LINE, "*", BLUE)
        self.play(FadeOut(op), FadeIn(panel2), FadeIn(mark2), run_time=0.4)
        self.read(0.35)
        self.model_writes(0.35)

        # 12-14: pause and predict
        self.at("12")
        self.play(FadeOut(panel2), FadeOut(mark2), run_time=0.5)
        q = T("?", 40, AMBER).next_to(self.proj.badge, LEFT, 0.25)
        self.at("14")
        self.play(FadeIn(q), run_time=0.4)
        self.until(self.dur - 0.4)
        self.play(FadeOut(q), run_time=0.35)
        self.finish()
