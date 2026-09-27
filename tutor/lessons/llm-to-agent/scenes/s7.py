from skit import *


def step_items(col, n):
    st = TR["steps"][n - 1]
    color = {"fail": FAIL, "pass": PASS}.get(st["status"], HARN)
    return [col.item([st["request"]], MODEL, size=14), col.item([st["result_excerpt"]], color, size=14)]


def start_s7(sc):
    d, col = sc.d, sc.col
    sc.add(chip("7 · the harness"), *d.base(4), d.tag_claude)
    items = [instr_item(col), task_item(col)]
    for n in range(1, 5):
        items += step_items(col, n)
    col.place(items)


class S7(LScene):
    SEG = "s7"

    def construct(self):
        d, col = self.d, self.col
        start_s7(self)
        self.fade_in_all(0.3)
        c = self.cues

        # 02: the LLM is the model
        self.at("02")
        mbox = SurroundingRectangle(d.model, color=MODEL, buff=0.1, corner_radius=0.16, stroke_width=2.5)
        self.play(Create(mbox), Indicate(d.model_name, color=MODEL, scale_factor=1.15), run_time=0.7)

        # 03: everything around it is the harness
        self.at("03", 0.3)
        out = d.harness_outline()
        hl = T("harness", 26, HARN, weight=BOLD).move_to([6.95, 3.45, 0], aligned_edge=RIGHT)
        self.play(FadeOut(mbox), Create(out), run_time=1.3)
        self.play(FadeIn(hl, shift=DOWN * 0.1), run_time=0.4)

        # 04: it writes the starting instructions, with the request format
        self.at("04", 0.4)
        ins = col.items[0]["shown"]
        old = ins[2][0]
        new = T("starting instructions", 14, HARN, font=MONO).move_to(old, aligned_edge=LEFT)
        self.play(Transform(old, new), Indicate(ins, color=HARN, scale_factor=1.03), run_time=0.8)

        # 05: the tools, the program that carries out each request, and the loop
        s, e = c["05"]
        self.until(s + (e - s) * 0.12)
        br = Brace(d.prog, DOWN, buff=0.08, color=HARN)
        tl = T("tools", 18, HARN, weight=MEDIUM).next_to(br, DOWN, buff=0.06)
        self.play(GrowFromCenter(br), FadeIn(tl), Indicate(d.tool_group, color=HARN, scale_factor=1.05), run_time=0.6)
        self.until(s + (e - s) * 0.4)
        self.play(Indicate(VGroup(d.prog, d.prog_name, d.tool_group), color=HARN, scale_factor=1.03), run_time=0.7)
        self.until(s + (e - s) * 0.8)
        arrows = [d.a_cm, d.a_ms, d.a_sp, d.a_pc]
        self.play(FadeIn(d.loop_label), *[self.lit(a, HARN, 0.4) for a in arrows], run_time=0.5)
        path = d.loop_path()
        dot = Dot(radius=0.08, color=INK).move_to(path.get_start())
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=1.6, rate_func=linear)
        self.remove(dot)
        self.play(*[self.lit(a, FAINT, 0.4) for a in arrows], run_time=0.4)

        # 07: before an edit, it can check permission, sometimes by asking you
        self.at("07")
        gx = (PROG_C[0] + PROG_W / 2 + PROJ_L) / 2
        gate = VGroup(Line([gx, PJ_Y - 0.28, 0], [gx, PJ_Y + 0.28, 0]),
                      Line([gx - 0.12, PJ_Y + 0.28, 0], [gx + 0.12, PJ_Y + 0.28, 0]),
                      Line([gx - 0.12, PJ_Y - 0.28, 0], [gx + 0.12, PJ_Y - 0.28, 0])).set_stroke(NUM, 4)
        pl = T("permission check", 15, NUM, font=MONO).move_to([PROJ_L - 0.1, 0.08, 0], aligned_edge=RIGHT)
        lead = Line([gx, pl.get_bottom()[1] - 0.05, 0], gate.get_top(), stroke_color=NUM, stroke_width=1.5)
        self.play(Create(gate), FadeIn(pl), Create(lead), run_time=0.6)
        req = T(TR["steps"][4]["request"], 18, MODEL, font=MONO).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
        self.play(FadeIn(req, shift=RIGHT * 0.1), run_time=0.4)
        mini = req.copy()
        self.play(mini.animate.scale(0.75).move_to([SP_X, PROG_C[1] + PROG_H / 2 + 0.02, 0]),
                  self.lit(d.a_sp, HARN), run_time=0.7)
        self.play(mini.animate.move_to([PROG_C[0] + PROG_W / 2 - 0.12, PJ_Y - 0.22, 0], aligned_edge=RIGHT),
                  self.lit(d.a_pj, HARN), run_time=0.6)
        s, e = c["07"]
        self.until(s + (e - s) * 0.72)
        ask = VGroup(rbox(1.55, 0.44, NUM, fill=PANEL, sw=1.6, r=0.08), T("allow?", 15, NUM, font=MONO))
        ask[1].move_to(ask[0])
        ask.move_to([gx - 0.75, 0.62, 0])
        self.play(FadeIn(ask), Indicate(gate, color=NUM, scale_factor=1.2), run_time=0.6)
        self.until(e + 0.3)
        self.play(FadeOut(ask), FadeOut(mini), FadeOut(req), self.lit(d.a_sp, FAINT), self.lit(d.a_pj, FAINT),
                  Indicate(d.files["prices.py"], color=HARN, scale_factor=1.05), run_time=0.5)

        # 08: every result makes the context longer
        self.at("08")
        s, e = c["08"]
        news = []
        for n in range(5, 13):
            news += step_items(col, n)
        dt = max((e + 0.1 - self.now()) / len(news), 0.1)
        for it in news:
            self.play(*col.anims(it), run_time=dt)

        # 09: when it fills up, the harness trims it: old results dropped, older steps summarized
        self.at("09", 0.2)
        s, e = c["09"]
        slivers = [it for it in col.items if it["form"] == "sliver"]
        res_sl = [it for it in slivers if it["role"] != MODEL]
        self.play(*[FadeOut(it["shown"]) for it in res_sl], run_time=0.6)
        col.items = [it for it in col.items if it not in res_sl]
        self.play(*col.anims(), run_time=0.5)
        self.until(s + (e - s) * 0.62)
        req_sl = [it for it in col.items if it["form"] == "sliver"]
        summ = col.item(["summary of earlier steps"], MUTED, size=14)
        idx = col.items.index(req_sl[0])
        col.items = [it for it in col.items if it not in req_sl]
        group = VGroup(*[it["shown"] for it in req_sl])
        self.play(*col.anims(summ, src=group, index=idx), run_time=0.8)
        tt = VGroup(T("trim the", 15, MUTED, font=MONO), T("context", 15, MUTED, font=MONO)).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        tt.move_to([CTX_R + 0.45, summ["shown"].get_center()[1], 0], aligned_edge=LEFT)
        at = arrow(tt.get_left() + LEFT * 0.05, [CTX_R - 0.05, tt.get_center()[1], 0], color=MUTED, sw=2)
        self.play(FadeIn(tt), GrowArrow(at), run_time=0.5)

        # 10: so an agent is an LLM plus a harness
        self.at("10")
        eq = VGroup(T("agent", 30, INK, weight=BOLD), T("=", 30, MUTED), T("LLM", 30, MODEL, weight=BOLD),
                    T("+", 30, MUTED), T("harness", 30, HARN, weight=BOLD)).arrange(RIGHT, buff=0.22)
        eq.move_to([0.9, 3.5, 0])
        self.play(FadeIn(eq, shift=DOWN * 0.1), run_time=0.7)

        # 11: five words to keep (the glossary card)
        self.at("11")
        self.play(*[FadeOut(m) for m in self.mobjects[1:]], run_time=0.5)
        rows = [("LLM", MODEL, "predicts the next word"),
                ("context", INK, "the text in front of it: all it sees"),
                ("tool", HARN, "something the program does when the model asks"),
                ("harness", HARN, "everything around the model"),
                ("agent", INK, "LLM + harness")]
        g = VGroup()
        for i, (term, col_, defi) in enumerate(rows):
            a = T(term, 30, col_, weight=BOLD).move_to([-4.2, 1.9 - 0.95 * i, 0], aligned_edge=RIGHT)
            b = T(defi, 26, INK).move_to([-3.6, 1.9 - 0.95 * i, 0], aligned_edge=LEFT)
            g.add(VGroup(a, b))
        s, e = c["11"]
        fr = [0.42, 0.56, 0.68, 0.79, 0.92]
        for i, r in enumerate(g):
            self.until(s + (e - s) * fr[i] - 0.1)
            self.play(FadeIn(r, shift=RIGHT * 0.1), run_time=0.35)
        self.end()
