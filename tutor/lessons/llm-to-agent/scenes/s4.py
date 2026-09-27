from skit import *


def start_s4(sc):
    """The end of chapter 3: the program has searched; its result waits; the model's request is out."""
    d, col = sc.d, sc.col
    sc.add(chip("4 · the result goes back in"), *d.base(3), d.tag_claude)
    d.tools["search"][0].set_fill(HARN, 0.35)
    d.a_pj.set_color(HARN)
    d.files["prices.py"][0].set_stroke(HARN, 2.4)
    col.place([instr_item(col), task_item(col)])
    req = T(TR["steps"][0]["request"], 19, MODEL, font=MONO).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
    sc.add(req)
    return req


class S4(LScene):
    SEG = "s4"

    def construct(self):
        d, col = self.d, self.col
        req = start_s4(self)
        self.fade_in_all(0.3)

        # 01: the search found something: its result waits at the program
        self.at("01")
        res_lines = ["prices.py:8:", 'raise LookupError(f"no price for {product!r}")']
        res = card(res_lines, HARN, w=5.2, size=14)
        res.move_to([PROG_C[0] + 0.5, -2.95, 0])
        self.play(FadeIn(res, shift=DOWN * 0.1), run_time=0.5)

        # 02-03: the model can't see it; it knows only its context
        self.at("02")
        self.play(Indicate(res, color=HARN, scale_factor=1.04), run_time=0.7)
        self.at("03", 0.3)
        self.play(d.ctx.animate.set_stroke(MODEL, width=2.6), run_time=0.4)
        self.play(d.ctx.animate.set_stroke(FAINT, width=2), run_time=0.4)

        # 04: the program pastes the result into the context (after the model's own request)
        self.at("04")
        r_item = col.item([TR["steps"][0]["request"]], MODEL, size=15)
        self.play(*col.anims(r_item, src=req), d.tools["search"][0].animate.set_fill(HARN, 0),
                  d.files["prices.py"][0].animate.set_stroke(FAINT, 1.4), self.lit(d.a_pj, FAINT), run_time=0.6)
        self.play(GrowArrow(d.a_pc), FadeIn(d.res_label), run_time=0.5)
        self.play(self.lit(d.a_pc, HARN, 0.2), run_time=0.2)
        x_item = col.item(res_lines, HARN, size=14)
        self.play(*col.anims(x_item, src=res), run_time=0.9)
        self.play(self.lit(d.a_pc, FAINT, 0.2), run_time=0.2)

        # 05: one match: line 8 of prices.py
        self.at("05")
        first = x_item["shown"][2][0]
        u = Underline(first, color=HARN, buff=0.03, stroke_width=3)
        self.play(Create(u), run_time=0.5)

        # 06: then it runs the model again, on the whole context
        self.at("06")
        self.play(FadeOut(u), self.lit(d.a_cm, MODEL), run_time=0.3)
        self.sweep(1.2)
        self.play(Indicate(d.model, color=MODEL, scale_factor=1.05), run_time=0.6)

        # 07-08: the result in view; it knows where the error comes from
        self.at("07")
        box = SurroundingRectangle(x_item["shown"], color=MODEL, buff=0.05, corner_radius=0.07, stroke_width=2.2)
        self.play(Create(box), run_time=0.5)
        self.at("08", 1.2)
        self.play(Indicate(d.files["prices.py"], color=MODEL, scale_factor=1.05), run_time=0.8)

        # 09: so it writes its next request: open that file
        self.at("09", 1.0)
        self.play(FadeOut(box), self.lit(d.a_cm, FAINT), run_time=0.3)
        nxt = self.write_slot(TR["steps"][1]["request"])

        # 10-14: web search in chat assistants, 2023: the same trick (an illustration)
        self.at("10", 0.2)
        inset = rbox(7.2, 4.1, FAINT, fill=BG, fo=0.97, sw=1.6, r=0.12).move_to([3.3, -1.3, 0])
        title = label("2023 · chat assistants", 18, INK).move_to(inset.get_corner(UL) + np.array([0.3, -0.35, 0]), aligned_edge=LEFT)
        ill = tag("illustration", FAINT, 14).move_to(inset.get_corner(UR) + np.array([-0.3, -0.35, 0]), aligned_edge=RIGHT)
        self.play(FadeIn(inset), run_time=0.4)
        self.at("11")
        self.play(FadeIn(title), FadeIn(ill), run_time=0.5)

        def mini(s, color, x, y, w=2.1):
            b = rbox(w, 0.6, color, fill=PANEL, sw=1.8, r=0.08).move_to([x, y, 0])
            return VGroup(b, T(s, 16, INK if color != HARN else HARN, font=MONO).move_to(b))
        y1, y2 = -0.75, -2.45
        q = mini("a question", INK, 0.95, y1, 1.9)
        sr = mini("search: …", MODEL, 3.35, y1, 1.9)
        ws = mini("web search", HARN, 5.55, y1, 1.9)
        wp = mini("web pages", HARN, 5.55, y2, 1.9)
        ans = mini("an answer, with sources", MODEL, 1.8, y2, 3.6)
        a1 = arrow(q.get_right() + RIGHT * 0.05, sr.get_left() + LEFT * 0.05)
        a2 = arrow(sr.get_right() + RIGHT * 0.05, ws.get_left() + LEFT * 0.05, color=HARN)
        a3 = arrow(ws.get_bottom() + DOWN * 0.05, wp.get_top() + UP * 0.05, color=HARN)
        a4 = arrow(wp.get_left() + LEFT * 0.05, ans.get_right() + RIGHT * 0.05, color=HARN)
        s, e = self.cues["13"]
        self.at("13")
        self.play(FadeIn(q), GrowArrow(a1), FadeIn(sr), run_time=0.6)
        self.until(s + (e - s) * 0.4)
        self.play(GrowArrow(a2), FadeIn(ws), run_time=0.5)
        self.until(s + (e - s) * 0.7)
        self.play(GrowArrow(a3), FadeIn(wp), run_time=0.5)
        self.at("14")
        self.play(GrowArrow(a4), FadeIn(ans), run_time=0.6)
        self.end()
