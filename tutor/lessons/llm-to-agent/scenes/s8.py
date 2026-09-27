from skit import *
from s1 import mbox, tcard, question_box, MX, TOP_Y, BOT_Y


def start_s8(sc):
    d, col = sc.d, sc.col
    sc.add(chip("8 · the answer"), *d.base(4), d.tag_claude, d.loop_label)
    out = d.harness_outline()
    hl = T("harness", 26, HARN, weight=BOLD).move_to([6.95, 3.45, 0], aligned_edge=RIGHT)
    sc.add(out, hl)
    col.place([instr_item(col, short=True), task_item(col, short=True)])


class S8(LScene):
    SEG = "s8"

    def construct(self):
        d, col = self.d, self.col
        start_s8(self)
        self.fade_in_all(0.3)
        c = self.cues

        # 02-03: the model still predicts the next word
        self.at("02")
        self.play(Indicate(VGroup(d.model, d.model_name), color=MODEL, scale_factor=1.08), run_time=0.7)
        self.at("03")
        nw = TR["next_word"][:2]
        bars = VGroup()
        for i, (w, p) in enumerate(nw):
            word = T(w, 18, INK, font=MONO).move_to([SLOT_L + 0.95, SLOT_Y + 0.22 - 0.42 * i, 0], aligned_edge=RIGHT)
            bar = Rectangle(width=2.2 * p / nw[0][1], height=0.22, stroke_width=0, fill_color=NUM, fill_opacity=0.95)
            bar.move_to([SLOT_L + 1.1, word.get_center()[1], 0], aligned_edge=LEFT)
            val = T(f"{p * 100:.0f}%", 16, NUM, font=MONO).next_to(bar, RIGHT, buff=0.1)
            bars.add(VGroup(word, bar, val))
        self.play(FadeIn(bars), run_time=0.4)
        self.until(c["03"][1] + 0.1)
        self.play(FadeOut(bars), run_time=0.4)

        # 04: the harness turns text into actions, and pastes the results back
        self.at("04")
        s, e = c["04"]
        req = T("edit file: invoice.py", 18, MODEL, font=MONO).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
        self.play(FadeIn(req), self.lit(d.a_sp, HARN), run_time=0.4)
        self.play(self.lit(d.a_pj, HARN), Indicate(d.files["invoice.py"], color=HARN, scale_factor=1.05),
                  Indicate(VGroup(d.prog, d.prog_name, d.tool_group), color=HARN, scale_factor=1.02), run_time=0.8)
        self.until(s + (e - s) * 0.6)
        self.play(self.lit(d.a_pc, HARN), FadeIn(d.res_label.copy().set_color(INK)), run_time=0.4)
        res = card(["edited invoice.py"], HARN, w=3.0, size=14).move_to([PROG_C[0] - 0.3, PROG_C[1] - PROG_H / 2 - 0.35, 0])
        self.play(FadeIn(res), run_time=0.3)
        it = col.item(["edited invoice.py"], HARN, size=14)
        r_it = col.item(["edit file: invoice.py"], MODEL, size=14)
        self.play(*col.anims(r_it, src=req), run_time=0.5)
        self.play(*col.anims(it, src=res), run_time=0.6)

        # 05: the loop turns single steps into a whole job
        self.at("05")
        arrows = [d.a_cm, d.a_ms, d.a_sp, d.a_pc]
        self.play(*[self.lit(a, HARN, 0.3) for a in arrows], self.lit(d.a_pj, FAINT, 0.3), run_time=0.3)
        path = d.loop_path()
        dot = Dot(radius=0.08, color=INK).move_to(path.get_start())
        self.add(dot)
        self.play(MoveAlongPath(dot, path), run_time=max(c["05"][1] - self.now() + 0.6, 1.2), rate_func=linear)
        self.remove(dot)

        # 06-08: back to the opening picture: ChatGPT talked; an agent is still talking; the harness acts
        self.at("06")
        self.play(*[FadeOut(m) for m in self.mobjects[1:]], run_time=0.5)
        top = label("Nov 2022 · ChatGPT", 18, MUTED).move_to([-6.6, TOP_Y + 1.0, 0], aligned_edge=LEFT)
        msg = tcard("your message", INK, -5.35, TOP_Y)
        m1 = mbox(MX, TOP_Y)
        rep = tcard("its reply", MODEL, 0.25, TOP_Y)
        a1 = arrow(msg.get_right() + RIGHT * 0.08, m1.get_left() + LEFT * 0.08)
        a2 = arrow(m1.get_right() + RIGHT * 0.08, rep.get_left() + LEFT * 0.08)
        self.play(FadeIn(VGroup(top, msg, m1, rep, a1, a2)), run_time=0.6)
        self.at("07")
        bot = label("today · an agent", 18, MUTED).move_to([-6.6, BOT_Y + 1.0, 0], aligned_edge=LEFT)
        bug = tcard("a bug in some code", INK, -5.35, BOT_Y, w=2.5)
        m2 = mbox(MX, BOT_Y)
        qf, qq = question_box(0.55, BOT_Y)
        acts = VGroup(*[tcard(s_, INK, 4.6, BOT_Y + 0.75 - 0.75 * i, w=2.4) for i, s_ in
                        enumerate(["read files", "run tests", "fix the bug"])])
        b1 = arrow(bug.get_right() + RIGHT * 0.05, m2.get_left() + LEFT * 0.08)
        b2 = arrow(m2.get_right() + RIGHT * 0.08, qf.get_left() + LEFT * 0.06)
        b3 = VGroup(*[arrow(qf.get_right() + RIGHT * 0.06, a.get_left() + LEFT * 0.08) for a in acts])
        tx = tcard("text", MODEL, MX, BOT_Y, w=1.0).scale(0.8).move_to(b2.get_center() + UP * 0.45)
        self.play(FadeIn(VGroup(bot, bug, m2, qf, qq, acts, b1, b2, b3)), run_time=0.6)
        self.play(FadeIn(tx, shift=RIGHT * 0.2), run_time=0.4)
        self.at("08", 0.3)
        hb = rbox(2.2, 1.25, HARN, fill=PANEL, sw=2.6).move_to(qf)
        hw = T("harness", 24, HARN, weight=BOLD).move_to(hb)
        self.play(ReplacementTransform(qf, hb), ReplacementTransform(qq, hw), run_time=0.8)
        s, e = c["08"]
        self.until(s + (e - s) * 0.75)
        self.play(*[Indicate(a, color=HARN, scale_factor=1.04) for a in acts], *[self.lit(a, HARN, 0.5) for a in b3],
                  run_time=0.9)

        # end card: the takeaway and the references
        self.until(e + 1.2)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.6)
        t1 = T("An agent is an LLM plus a harness.", 36, INK, weight=MEDIUM)
        t2 = T("The model only writes text; the harness carries out its requests", 24, MUTED)
        t3 = T("and feeds the results back, in a loop.", 24, MUTED)
        take = VGroup(t1, t2, t3).arrange(DOWN, buff=0.22).move_to([0, 1.6, 0])
        refs = ["Anthropic, “Building effective agents” (Schluntz and Zhang, 2024)",
                "Claude Code docs, “How Claude Code works”",
                "Latent Space, “Claude Code: Anthropic's Agent in Your Terminal” (2025)",
                "Weng, “LLM Powered Autonomous Agents” (2023)",
                "Radford et al., “Language Models are Unsupervised Multitask Learners” (GPT-2, 2019)"]
        rg = VGroup(label("references", 15, FAINT), *[T(r, 16, MUTED) for r in refs]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        rg.move_to([0, -1.75, 0])
        self.play(FadeIn(take, shift=UP * 0.1), run_time=0.7)
        self.play(FadeIn(rg), run_time=0.6)
        self.end(0.5)
