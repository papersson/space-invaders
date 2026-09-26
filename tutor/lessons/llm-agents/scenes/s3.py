from skit import *


class S3(AgentScene):
    SEG = "s3"

    def construct(self):
        # the end of chapter 2: model (tagged), project, and the bare strip with its text reply
        bare = Strip("bare_1", STRIP_Y, labels={2: "text"})
        self.picture("one_tool_1", 2, tag=True, code=False)
        self.add(bare.cards[2])

        # 01: act for it: the reply goes, our code appears
        self.at("01")
        self.play(FadeOut(bare.cards[2]), run_time=0.5)
        self.play(FadeIn(self.code, shift=0.2 * LEFT), run_time=0.6)

        # 02-05: the tool list and the format, in the instructions (sims/agent.py system prompt)
        self.at("02")
        rows = [(name, INK) for name in AGENT.TOOL_DOCS]
        panel = quote(rows, 14, title="instructions: the tools")
        panel.move_to([0, -0.55, 0]).align_to([X0, 0, 0], LEFT)
        link = Line(self.strip.cards[0].get_top(), panel.get_bottom(), stroke_color=FAINT, stroke_width=1.5)
        self.play(Create(link), FadeIn(panel[0]), FadeIn(panel[2]), run_time=0.4)
        dur = self.cues["02"][1] - self.now() - 0.2
        for r in panel[1]:
            self.play(FadeIn(r, shift=0.1 * RIGHT), run_time=max(dur / 4, 0.25))
        self.at("03")
        self.play(Indicate(self.code[0], color=INK, scale_factor=1.06), run_time=0.8)

        self.at("04")
        fmt = mono('{"tool": "read_file", "path": "report.py"}', 16, BLUE)
        note = mono("a line of JSON here; real APIs give tool calls a structured form", 13, MUTED)
        grp = VGroup(fmt, note).arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(panel, UP, 0.55).align_to(panel, LEFT)
        self.play(FadeIn(fmt), run_time=0.5)
        self.play(FadeIn(note), run_time=0.4)
        self.at("05")
        tc = mono("tool call", 17, BLUE).next_to(fmt, RIGHT, 0.4)
        self.play(FadeIn(tc), run_time=0.4)

        # 06: the first reply is a tool call: list the files (captures/one_tool_1.json)
        self.at("06")
        self.play(FadeOut(VGroup(panel, link, grp, tc)), run_time=0.4)
        self.read(0.5)
        c = self.model_writes(0.45)
        op = callout(c, mono(S["one_tool_1"]["cards"][3]["text"], 15, BLUE), UP, 0.3)
        self.play(FadeIn(op), run_time=0.3)

        # 07-08: our code runs it, and the result joins the context
        self.at("07")
        self.play(FadeOut(op), run_time=0.2)
        self.play(Indicate(self.proj, color=INK, scale_factor=1.03), run_time=0.4)
        r, flow = self.tool_runs(None, 0.5, keep=True)
        res_txt = S["one_tool_1"]["cards"][4]["text"].split("\n")
        rp = callout(r, quote(res_txt, 14), UP, 0.3)
        self.play(FadeIn(rp), run_time=0.4)
        self.at("08")
        tr = mono("tool result", 17, GREEN).next_to(rp, RIGHT, 0.3).align_to(rp, DOWN)
        self.play(FadeIn(tr), run_time=0.4)

        # 09-12: who ran it: our code, not the model
        self.at("09")
        self.play(Circumscribe(self.code[0], color=INK, time_width=0.6), run_time=1.0)
        self.at("10")
        self.play(self.model.animate.set_opacity(0.35), run_time=0.4)
        self.at("11")
        self.play(self.model.animate.set_opacity(1), run_time=0.4)
        self.at("12")
        src = mono("Claude API docs, “How tool use works”", 13, MUTED).next_to(self.model, DOWN, 0.55)
        self.play(FadeIn(src), run_time=0.4)

        # 13: called again, it asks for a second tool: read the test
        self.at("13")
        self.play(FadeOut(VGroup(rp, tr, src, flow)), run_time=0.3)
        self.read(0.5)
        c2 = self.model_writes(0.45)
        op2 = callout(c2, mono(S["one_tool_1"]["cards"][5]["text"], 15, BLUE), UP, 0.3)
        self.play(FadeIn(op2), run_time=0.3)

        # 14-15: our code stops: the request waits, unanswered
        self.at("14")
        ring = DashedVMobject(SurroundingRectangle(c2, color=AMBER, buff=0.06, corner_radius=0.08), num_dashes=24)
        self.play(Create(ring), self.code.animate.set_opacity(0.45), run_time=0.6)
        self.at("15")
        self.play(ring.animate.set_stroke(opacity=0.4), run_time=0.6)
        self.play(ring.animate.set_stroke(opacity=1), run_time=0.6)
        self.until(self.dur - 0.6)
        self.play(FadeOut(op2), run_time=0.5)
        self.finish()
