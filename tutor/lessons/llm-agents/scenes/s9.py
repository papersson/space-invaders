from skit import *
from s1 import A_Y, B_Y


class S9(CueScene):
    SEG = "s9"

    def construct(self):
        A = Strip("loop_1", A_Y, labels={18: "Fixed."})
        B = Strip("no_tests_1", B_Y, labels={10: "Fixed."})
        la = label("run A", 16, INK).next_to(A.cards[0], UP, 0.22).align_to(A.cards[0], LEFT)
        lb = label("run B", 16, INK).next_to(B.cards[0], UP, 0.22).align_to(B.cards[0], LEFT)

        # 01: the two strips from chapter 1, now with their colours named
        self.at("01", -0.3)
        self.play(FadeIn(VGroup(*A.cards, *B.cards, la, lb)), run_time=0.8)
        keys = VGroup()
        for col, txt, fill in [(OUR_GREY, "instructions", 1), (BLUE, "the model's writing", 0.92), (GREEN, "tool results", 0.88)]:
            sw = RoundedRectangle(corner_radius=0.04, width=0.28, height=0.28, stroke_width=0, fill_color=col, fill_opacity=fill)
            keys.add(VGroup(sw, mono(txt, 14, INK).next_to(sw, RIGHT, 0.12)))
        keys.arrange(RIGHT, buff=0.6).move_to([0, 2.3, 0]).align_to([X0, 0, 0], LEFT)
        self.play(FadeIn(keys), run_time=0.6)

        # 02-04: picks each step from its context; the loop writes results back
        self.at("03")
        greens = VGroup(*[c for c in A.cards if c.kind == "result"])
        self.play(LaggedStart(*[Indicate(g, color=GREEN, scale_factor=1.08) for g in greens], lag_ratio=0.08), run_time=1.6)

        # 05-07: A's context held ground truth from the test; B's held only its own fix
        self.at("05")
        ra = SurroundingRectangle(A.cards[11], color=CORAL, buff=0.06, corner_radius=0.08, stroke_width=3)
        self.play(Create(ra), run_time=0.5)
        self.at("06")
        hole = DashedVMobject(Rectangle(width=A.cards[11].width + 0.12, height=0.9, stroke_color=MUTED, stroke_width=2).move_to(
            [A.cards[11].get_x(), B_Y, 0]), num_dashes=20)
        rb = SurroundingRectangle(B.cards[10], color=BLUE, buff=0.06, corner_radius=0.08, stroke_width=3)
        self.play(Create(hole), Create(rb), run_time=0.6)

        # 08-09: the more capable model did better the same way: it read the data for itself
        self.at("08")
        r = "no_tests_strong_1"
        C = Strip(r, -3.35, labels={len(card_items(r)) - 1: "reply"})
        VGroup(*C.cards).scale(0.8, about_point=[X0, -3.35, 0])
        lc = label("more capable model", 14, INK).next_to(C.cards[0], UP, 0.16).align_to(C.cards[0], LEFT)
        self.play(FadeIn(VGroup(*C.cards, lc)), run_time=0.7)
        ci = next(i for i, c in enumerate(C.cards) if c.kind == "model" and c.data.get("sub") == "sales.csv")
        rc = SurroundingRectangle(VGroup(C.cards[ci], C.cards[ci + 1]), color=INK, buff=0.05, corner_radius=0.06, stroke_width=2.5)
        self.play(Create(rc), run_time=0.5)

        # 10-11: code comes with tests: A's two test calls and their answers
        self.at("11")
        tests = VGroup(A.cards[10], A.cards[11], A.cards[16], A.cards[17])
        self.play(FadeOut(ra), LaggedStart(*[Indicate(t, color=INK, scale_factor=1.1) for t in tests], lag_ratio=0.2), run_time=1.4)

        # 14-15: the end card
        self.at("14")
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.8)
        title = T("It Said It Was Fixed", 40, INK).move_to([0, 1.9, 0])
        take = T("An agent can be trusted as far as ground truth reaches its context.", 24, BLUE).next_to(title, DOWN, 0.5)
        refs = VGroup(*[mono(t, 13, MUTED) for t in [
            "Anthropic, “Building effective agents” (Schluntz and Zhang, 2024)",
            "Anthropic, “Effective context engineering for AI agents” (2025)",
            "Claude API docs, “How tool use works”; “Using the Messages API”",
            "Yao et al., “ReAct: Synergizing Reasoning and Acting in Language Models” (2022)",
            "Willison, “I think ‘agent’ may finally have a widely enough agreed upon definition to be useful jargon now” (2025)",
            "Hong, Troynikov and Huber, “Context Rot: How Increasing Input Tokens Impacts LLM Performance” (Chroma, 2025)",
            "Runs: sims/agent.py and Claude Code, captured 2026-09-26 (captures/)",
        ]]).arrange(DOWN, buff=0.14, aligned_edge=LEFT).next_to(take, DOWN, 0.8)
        refs.move_to([0, refs.get_center()[1], 0])
        self.play(FadeIn(title), run_time=0.8)
        self.play(FadeIn(take), run_time=0.8)
        self.at("15", 1.0)
        self.play(FadeIn(refs), run_time=1.0)
        self.until(self.dur - 0.6)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        self.finish()
