from skit import *


def start_s3(sc):
    """The diagram at the start of chapter 3: context panel, the LLM box (GPT-2 tag), no cards."""
    d = sc.d
    sc.add(chip("3 · text that is an action"), d.ctx, d.ctx_label, d.model, d.model_name, d.model_sub, d.tag_gpt2, d.a_cm)


class S3(LScene):
    SEG = "s3"

    def construct(self):
        d, col = self.d, self.col
        start_s3(self)
        self.fade_in_all(0.3)

        # 01: here's a task: the project, its tests failing
        self.at("01")
        self.play(FadeIn(d.proj_label), LaggedStart(*[FadeIn(f) for f in d.file_group], lag_ratio=0.15),
                  FadeIn(d.badge_fail), run_time=0.8)
        # 02: the task card
        self.at("02", 0.3)
        task = task_item(col)
        self.play(*col.anims(task), run_time=0.6)

        # 03: you might picture the model reaching into the files itself
        self.at("03", 0.4)
        reach = DashedLine(d.model.get_right() + DOWN * 0.3, d.files["prices.py"].get_left() + LEFT * 0.1,
                           color=MODEL, stroke_width=2.5, dash_length=0.12)
        self.play(Create(reach), run_time=0.8)
        self.play(reach.animate.set_opacity(0), run_time=0.8)
        self.remove(reach)

        # 04: not the small one, but a large model
        self.at("04", 1.6)
        self.play(ReplacementTransform(d.tag_gpt2, d.tag_claude), run_time=0.6)

        # 05: in one try it wrote that it would explore the project, and wrote out a command
        self.at("05")
        b = TR["bare"]
        l1 = T("I'll start by exploring the project", 17, MODEL).move_to([SLOT_L, SLOT_Y + 0.22, 0], aligned_edge=LEFT)
        l2 = T("structure to find the relevant code.", 17, MODEL).next_to(l1, DOWN, buff=0.1, aligned_edge=LEFT)
        l3 = T(b["tool"], 15, MODEL, font=MONO).next_to(l2, DOWN, buff=0.18, aligned_edge=LEFT).set_opacity(0.8)
        src = tag("the model on its own, one try", FAINT, 13).next_to(l1, UP, buff=0.14, aligned_edge=LEFT)
        self.play(GrowArrow(d.a_ms), FadeIn(src), FadeIn(VGroup(l1, l2), shift=RIGHT * 0.15), run_time=0.6)
        s, e = self.cues["05"]
        self.until(s + (e - s) * 0.6)
        self.play(FadeIn(l3, shift=RIGHT * 0.1), run_time=0.4)

        # 06: nothing there to carry it out; the tests still failed
        self.at("06")
        dead = DashedLine(l3.get_bottom() + DOWN * 0.08, l3.get_bottom() + DOWN * 1.0 + RIGHT * 0.9, color=FAINT,
                          stroke_width=2.5, dash_length=0.1)
        cross = VGroup(Line(UL, DR), Line(UR, DL)).scale(0.12).set_stroke(FAINT, 3).move_to(dead.get_end())
        self.play(Create(dead), run_time=0.5)
        self.play(FadeIn(cross), run_time=0.2)
        s, e = self.cues["06"]
        self.until(s + (e - s) * 0.6)
        self.play(Indicate(d.badge_fail, color=FAIL, scale_factor=1.06), run_time=0.8)

        # 07: text on its own doesn't do anything
        self.at("07", 0.4)
        self.play(FadeOut(VGroup(l1, l2, l3, src, dead, cross)), run_time=0.5)

        # 08: a program next to the model, watching what it writes
        self.at("08", 0.3)
        self.play(FadeIn(d.prog), FadeIn(d.prog_name), run_time=0.5)
        self.play(GrowArrow(d.a_sp), run_time=0.5)

        # 09: a format for requests, at the top of the context
        self.at("09", 0.4)
        ins = instr_item(col)
        self.play(*col.anims(ins, index=0), run_time=0.8)

        # 10-11: "search:", "open file:"
        def mark(i):
            line = ins["shown"][2][i]
            return SurroundingRectangle(line, color=HARN, buff=0.05, corner_radius=0.04, stroke_width=2)
        self.at("10", 0.2)
        m = mark(1)
        self.play(Create(m), run_time=0.4)
        self.at("11")
        m2 = mark(2)
        self.play(ReplacementTransform(m, m2), run_time=0.4)
        self.at("12", 0.5)
        self.play(FadeOut(m2), run_time=0.4)

        # 13: the model writes a line: search: no price for
        self.at("13", 0.9)
        req = self.write_slot(TR["steps"][0]["request"])

        # 14: the program spots the request and searches the project's files
        self.at("14")
        spot = SurroundingRectangle(req, color=HARN, buff=0.08, corner_radius=0.05, stroke_width=2)
        self.play(Create(spot), self.lit(d.a_sp, HARN), run_time=0.5)
        chips = d.tool_group
        self.play(FadeIn(chips), run_time=0.4)
        sch = d.tools["search"]
        self.play(sch[0].animate.set_fill(HARN, 0.35), GrowArrow(d.a_pj), run_time=0.4)
        self.play(self.lit(d.a_pj, HARN), run_time=0.2)
        for f in FILES:
            self.play(d.files[f][0].animate.set_stroke(HARN, 2.4), run_time=0.14)
            if f != "prices.py":
                self.play(d.files[f][0].animate.set_stroke(FAINT, 1.4), run_time=0.1)
        l8 = tag("line 8", HARN, 15).move_to(d.files["prices.py"][0].get_right() + LEFT * 0.5)
        self.play(FadeIn(l8), run_time=0.3)

        # 15: each thing the program can do is a tool
        self.at("15")
        br = Brace(d.prog, DOWN, buff=0.08, color=HARN)
        tl = T("tools", 20, HARN, weight=MEDIUM).next_to(br, DOWN, buff=0.08)
        self.play(GrowFromCenter(br), FadeIn(tl), run_time=0.5)
        s, e = self.cues["15"]
        names = ["search", "open file", "edit file", "run tests"]
        for i, n in enumerate(names):
            self.until(s + (e - s) * (0.52 + 0.12 * i))
            self.play(Indicate(d.tools[n], color=HARN, scale_factor=1.1), run_time=0.45)

        # 16-18: who did the searching: the program, not the model
        self.at("16")
        self.play(VGroup(d.model, d.model_name).animate.set_opacity(0.3), run_time=0.5)
        self.at("18")
        self.play(Indicate(d.prog, color=HARN, scale_factor=1.03), self.lit(d.a_pj, INK, 0.3), run_time=0.8)
        self.play(VGroup(d.model, d.model_name).animate.set_opacity(1), self.lit(d.a_pj, HARN, 0.3), run_time=0.5)
        self.end()
