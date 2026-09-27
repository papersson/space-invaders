from skit import *

BAR_X = 2.55          # left end of the bars
BAR_MAX = 3.2         # length of a bar at probability 0.308 (tea)
ROW_Y = [2.75, 2.3, 1.85, 1.4, 0.95]


def pct(p):
    return f"{p * 100:.0f}%" if p >= 0.05 else f"{p * 100:.1f}%"


class S2(LScene):
    SEG = "s2"

    def construct(self):
        d = self.d
        ch = chip("2 · what an LLM is")
        self.add(ch)
        self.fade_in_all(0.3)

        # 01: the model
        self.at("01")
        self.play(FadeIn(d.model), FadeIn(d.model_word), run_time=0.5)
        # 02: it's called an LLM
        self.at("02", 0.3)
        self.play(ReplacementTransform(d.model_word, d.model_name), FadeIn(d.model_sub), run_time=0.6)

        # 03: a small, freely available model; the words in front of it
        self.at("03")
        words = ["I", "made", "a", "cup", "of"]
        text = T(" ".join(words), 22, INK).move_to([CTX_L + 0.3, CTX_T - 0.75, 0], aligned_edge=LEFT)
        self.play(FadeIn(d.ctx), FadeIn(d.tag_gpt2), run_time=0.5)
        self.play(FadeIn(text, shift=RIGHT * 0.1), GrowArrow(d.a_cm), run_time=0.6)

        # 04: a probability for every word: bars
        self.at("04")
        nw = TR["next_word"]
        rows = VGroup()
        for i, (w, p) in enumerate(nw):
            strong = i < 2
            word = T(w, 22, INK if strong else MUTED, font=MONO).move_to([BAR_X - 0.15, ROW_Y[i], 0], aligned_edge=RIGHT)
            bar = Rectangle(width=max(BAR_MAX * p / nw[0][1], 0.04), height=0.26, stroke_width=0,
                            fill_color=NUM, fill_opacity=0.95 if strong else 0.4)
            bar.move_to([BAR_X, ROW_Y[i], 0], aligned_edge=LEFT)
            val = T(pct(p), 20, NUM if strong else FAINT, font=MONO).next_to(bar, RIGHT, buff=0.12)
            rows.add(VGroup(word, bar, val))
        src = tag("GPT-2, next word after “I made a cup of”", FAINT, 13).move_to([BAR_X - 1.0, ROW_Y[-1] - 0.45, 0], aligned_edge=LEFT)
        self.play(LaggedStart(*[FadeIn(r[0]) for r in rows], lag_ratio=0.1), run_time=0.5)
        self.play(*[GrowFromEdge(r[1], LEFT) for r in rows], *[FadeIn(r[2]) for r in rows], FadeIn(src), run_time=0.8)

        # 05-07: tea, coffee, everything else
        self.at("05")
        box_tea = SurroundingRectangle(rows[0], color=NUM, buff=0.08, corner_radius=0.06, stroke_width=2)
        self.play(Create(box_tea), run_time=0.4)
        self.at("06")
        box_cof = SurroundingRectangle(rows[1], color=NUM, buff=0.08, corner_radius=0.06, stroke_width=2)
        self.play(ReplacementTransform(box_tea, box_cof), run_time=0.4)
        self.at("07")
        self.play(FadeOut(box_cof), *[Indicate(r, color=MUTED, scale_factor=1.03) for r in rows[2:]], run_time=0.7)

        # 08: pick one of the likely words, add it to the text
        self.at("08")
        picked = SurroundingRectangle(rows[0], color=NUM, buff=0.08, corner_radius=0.06, stroke_width=2.5)
        ptag = tag("picked", NUM, 15).next_to(picked, LEFT, buff=0.15)
        self.play(Create(picked), FadeIn(ptag), run_time=0.4)
        t2 = T("I made a cup of tea", 22, INK).move_to(text, aligned_edge=LEFT)
        fly = rows[0][0].copy()
        self.play(Transform(fly, t2[-3:].copy()), run_time=0.7)
        self.remove(fly)
        self.remove(text)
        text = t2
        self.add(text)

        # 09: then predict again: and, then I (the likeliest each time)
        self.at("09")
        self.play(FadeOut(rows), FadeOut(picked), FadeOut(ptag), FadeOut(src), run_time=0.3)
        s, e = self.cues["09"]
        acc = "I made a cup of tea"
        for j, (w, p) in enumerate(TR["then"]):
            self.until(s + (e - s) * (0.35 + 0.3 * j))
            one = VGroup(T(w, 22, INK, font=MONO), Rectangle(width=BAR_MAX * p / nw[0][1], height=0.26,
                                                                 stroke_width=0, fill_color=NUM, fill_opacity=0.95))
            one[0].move_to([BAR_X - 0.15, ROW_Y[2], 0], aligned_edge=RIGHT)
            one[1].move_to([BAR_X, ROW_Y[2], 0], aligned_edge=LEFT)
            one.add(T(pct(p), 20, NUM, font=MONO).next_to(one[1], RIGHT, buff=0.12))
            self.play(*[FadeIn(m) for m in one], run_time=0.3)
            acc = acc + " " + w
            t2 = T(acc, 22, INK).move_to(text, aligned_edge=LEFT)
            n = len(w)
            fly = one[0].copy()
            self.play(Transform(fly, t2[-n:].copy()), FadeOut(one[1]), FadeOut(one[2]), run_time=0.5)
            self.remove(fly, *one, text)
            text = t2
            self.add(text)

        # 10-11: over and over
        self.at("10")
        for _ in range(2):
            self.play(self.lit(d.a_cm, MODEL, 0.25), Indicate(d.model, color=MODEL, scale_factor=1.04), run_time=0.45)
            self.play(self.lit(d.a_cm, FAINT, 0.25), run_time=0.25)

        # 12-13: only the text in front of it: its context
        self.at("12")
        self.play(d.ctx.animate.set_stroke(INK, width=2.5), run_time=0.4)
        self.at("13")
        self.play(FadeIn(d.ctx_label, shift=DOWN * 0.1), d.ctx.animate.set_stroke(FAINT, width=2), run_time=0.5)

        # 14: no memory from one use to the next
        self.at("14")
        self.play(text.animate.set_opacity(0.15), run_time=0.5)
        self.play(Indicate(d.model, color=MUTED, scale_factor=1.0), run_time=0.6)
        self.play(text.animate.set_opacity(1), run_time=0.5)

        # 15-18: two facts
        self.at("16")
        out_tag = tag("out: text", MODEL, 17).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
        a_out = arrow([MOD_C[0] + MOD_W / 2, SLOT_Y, 0], [SLOT_L - 0.05, SLOT_Y, 0], color=MODEL)
        self.play(GrowArrow(a_out), FadeIn(out_tag, shift=RIGHT * 0.1), run_time=0.5)
        self.at("18")
        k_tag = tag("knows: its context", MODEL, 17).move_to([CTX_L + 0.3, CTX_B + 0.35, 0], aligned_edge=LEFT)
        self.play(FadeIn(k_tag), d.ctx.animate.set_stroke(MODEL, width=2.5), run_time=0.5)
        self.end()
