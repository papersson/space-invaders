from skit import *
from s6 import staircase, counts, SCALE, BOT, ROW_GAP

CC = S["claude_code_1"]
SINCE = "#6FB7B7"    # Claude Code: everything added after its first call (not split by kind)


class S8(CueScene):
    SEG = "s8"

    def construct(self):
        rows = staircase()
        cnt = counts(rows)
        A = VGroup(*rows)

        # 01-03: the second way: the context only grows (run A's staircase)
        self.at("01", -0.2)
        w2 = mono("the context grows", 18, INK).to_corner(UL, buff=0.45)
        self.play(FadeIn(w2), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.12), run_time=1.2)
        self.play(FadeIn(VGroup(*cnt)), run_time=0.5)
        self.at("03")
        for r in rows[-3:]:
            band, anim = band_sweep(r, 0.35)
            self.add(band)
            self.play(anim)
            self.remove(band)

        # 04-05: Claude Code: the same command-line tool, running its own loop
        self.at("04")
        name = T("Claude Code", 26, INK).move_to([3.6, 3.45, 0])
        self.play(FadeIn(name), run_time=0.5)
        self.at("05", 1.0)
        tag = mono("claude -p, its own loop · tools: Read, Edit, python3 -m unittest", 13, MUTED).next_to(name, DOWN, 0.12)
        keep_on_screen(tag)
        self.play(FadeIn(tag), run_time=0.5)

        # 06: its first call read 11,597 tokens: at run A's scale it runs off the frame
        self.at("06")
        first = CC["calls"][0]
        y0 = BOT - 0.55
        big = Rectangle(width=first * SCALE, height=TOK_H, stroke_width=0, fill_color=OUR_GREY, fill_opacity=0.95)
        big.move_to([X0 + first * SCALE / 2, y0, 0])
        self.play(FadeOut(VGroup(*cnt)), run_time=0.3)
        self.play(A.animate.set_opacity(0.5), GrowFromEdge(big, LEFT), run_time=1.2, rate_func=linear)
        # zoom out along x, so Claude Code's largest call fits in 11 units
        f = 2745 / CC["calls"][-1]     # Claude Code's largest call gets the width run A's largest had
        self.play(big.animate.stretch(f, 0, about_point=[X0, y0, 0]),
                  A.animate.stretch(f, 0, about_point=[X0, 0, 0]).set_opacity(1), run_time=1.2)
        s2 = SCALE * f
        ca = mono_b(f"{first:,}", 16, AMBER).next_to(big, RIGHT, 0.2)
        la = VGroup(mono("run A", 13, MUTED), mono_b(f"{sum(S['loop_1']['calls']):,}", 13, AMBER)).arrange(RIGHT, buff=0.2)
        self.play(FadeIn(ca), run_time=0.4)

        # 07-08: nine calls, each re-reading its first call's context; 123,192 in all
        self.at("07")
        gap = 0.4
        top_y = -0.2
        A_small = A.copy().stretch(0.35, 1).move_to([0, 1.4, 0]).align_to([X0, 0, 0], LEFT)
        la.next_to(A_small, RIGHT, 0.3)
        cc_rows, cc_cnt = VGroup(), []
        n = len(CC["calls"])
        for i, c in enumerate(CC["calls"]):
            y = top_y - i * gap
            g = Rectangle(width=first * s2, height=0.3, stroke_width=0, fill_color=OUR_GREY, fill_opacity=0.95)
            g.move_to([X0 + first * s2 / 2, y, 0])
            row = VGroup(g)
            if c > first:
                w = (c - first) * s2
                row.add(Rectangle(width=w, height=0.3, stroke_width=0, fill_color=SINCE, fill_opacity=0.95).move_to(
                    [X0 + first * s2 + w / 2, y, 0]))
            cc_rows.add(row)
            strong = i in (0, n - 1)
            cc_cnt.append(mono_b(f"{c:,}", 14 if strong else 11, AMBER if strong else "#B98A45").next_to(row, RIGHT, 0.15))
        self.play(ReplacementTransform(A, A_small), FadeIn(la), ReplacementTransform(big, cc_rows[0]),
                  ca.animate.move_to(cc_cnt[0]), run_time=0.8)
        self.remove(ca)
        self.add(cc_cnt[0])
        dur = self.cues["07"][1] - self.now()
        self.play(LaggedStart(*[AnimationGroup(FadeIn(cc_rows[i]), FadeIn(cc_cnt[i])) for i in range(1, n)], lag_ratio=0.3),
                  run_time=max(dur, 1.0))
        gl = mono("its first call's context", 13, MUTED).next_to(cc_rows[0][0], UP, 0.1).align_to(cc_rows[0], LEFT)
        sl = mono("everything since", 13, SINCE).next_to(cc_rows[-1][1], DOWN, 0.1).align_to(cc_rows[-1][1], LEFT)
        self.play(FadeIn(gl), FadeIn(sl), run_time=0.4)
        self.at("08")
        greys = VGroup(*[r[0] for r in cc_rows])
        self.play(LaggedStart(*[Indicate(g, color=INK, scale_factor=1.02) for g in greys], lag_ratio=0.1), run_time=1.4)
        total = CC["total"]
        assert total == sum(CC["calls"]) == 123192
        br = Brace(VGroup(*cc_cnt), RIGHT, buff=0.15, color=AMBER)
        tt = VGroup(mono_b(f"{total:,}", 22, AMBER), mono("tokens read", 15, AMBER)).arrange(DOWN, buff=0.08).next_to(br, RIGHT, 0.15)
        keep_on_screen(tt)
        self.play(GrowFromCenter(br), FadeIn(tt), run_time=0.6)

        # 09-10: a longer task: twice the calls, more than twice the reading (Claude Code's own counts)
        self.at("09")
        since = VGroup(*[r[1] for r in cc_rows if len(r) > 1])
        self.play(LaggedStart(*[Indicate(s_, color=INK, scale_factor=1.04) for s_ in since], lag_ratio=0.12), run_time=1.6)
        self.at("10")
        s4, s8 = sum(CC["calls"][:4]), sum(CC["calls"][:8])
        assert (s4, s8) == (49369, 107572)
        self.play(FadeOut(VGroup(br, tt)), run_time=0.3)
        x = max(c.get_right()[0] for c in cc_cnt) + 0.2
        def bracket(n, dx, val):
            top, bot = cc_rows[0].get_top()[1], cc_rows[n - 1].get_bottom()[1]
            ln = VGroup(Line([x + dx, top, 0], [x + dx, bot, 0], stroke_color=AMBER, stroke_width=2.5),
                        Line([x + dx - 0.1, top, 0], [x + dx, top, 0], stroke_color=AMBER, stroke_width=2.5),
                        Line([x + dx - 0.1, bot, 0], [x + dx, bot, 0], stroke_color=AMBER, stroke_width=2.5))
            t = VGroup(mono(f"{n} calls", 13, AMBER), mono_b(f"{val:,}", 15, AMBER)).arrange(DOWN, buff=0.04, aligned_edge=LEFT)
            t.next_to(ln, RIGHT, 0.12).align_to(ln, DOWN)
            return VGroup(ln, t)
        b4, b8 = bracket(4, 0.0, s4), bracket(8, 1.25, s8)
        keep_on_screen(b8)
        self.play(FadeIn(b4), run_time=0.5)
        self.play(FadeIn(b8), run_time=0.5)

        # 11-14: context rot (cited; not shown by these runs)
        self.at("12")
        rot = VGroup(mono("context rot", 17, INK), mono("Hong, Troynikov and Huber (Chroma), 2025", 13, MUTED)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        rot.next_to(w2, DOWN, 0.25).align_to(w2, LEFT)
        self.play(FadeIn(rot), run_time=0.5)
        self.at("13")
        self.play(Indicate(rot[0], color=INK, scale_factor=1.08), run_time=0.8)
        self.at("14")
        ns = mono("not shown by these runs", 12, MUTED).next_to(rot, DOWN, 0.1).align_to(rot, LEFT)
        self.play(FadeIn(ns), run_time=0.4)

        # 15-18: compaction: the context folded into a summary (a picture of the idea, not a run)
        self.at("15")
        self.play(FadeOut(VGroup(cc_rows, *cc_cnt, b4, b8, gl, sl, A_small, la, name, tag, ns)), run_time=0.6)
        strip = token_bars("loop_1", SCALE, -0.6)
        self.play(FadeIn(strip), run_time=0.6)
        self.at("16")
        head, tail = VGroup(*strip[:3]), VGroup(*strip[3:])
        summ_w = tail.width * 0.3
        summ = Rectangle(width=summ_w, height=TOK_H, stroke_color=INK, stroke_width=1.5, fill_color="#8FA3B5",
                         fill_opacity=0.9).move_to([head.get_right()[0] + summ_w / 2, -0.6, 0])
        sl2 = mono("summary", 14, INK).next_to(summ, DOWN, 0.12)
        pic = mono("a picture of the idea, not a run", 12, MUTED).next_to(summ, UP, 0.14)
        comp = VGroup(mono("compaction", 17, INK), mono("Anthropic, 2025", 13, MUTED)).arrange(DOWN, buff=0.08, aligned_edge=LEFT)
        comp.next_to(rot, DOWN, 0.3).align_to(rot, LEFT)
        self.play(ReplacementTransform(tail, summ), FadeIn(sl2), FadeIn(pic), FadeIn(comp), run_time=1.2)
        self.at("17")
        more = VGroup()
        x = summ.get_right()[0]
        for w, col in [(0.25, BLUE), (0.55, GREEN), (0.2, BLUE), (0.45, GREEN)]:
            more.add(Rectangle(width=w, height=TOK_H, stroke_width=0.6, stroke_color=BG, fill_color=col, fill_opacity=0.95).move_to([x + w / 2, -0.6, 0]))
            x += w
        self.play(LaggedStart(*[FadeIn(m) for m in more], lag_ratio=0.3), run_time=1.2)
        self.at("18")
        self.play(Indicate(summ, color=INK, scale_factor=1.08), run_time=1.0)
        self.until(self.dur - 0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.finish()
