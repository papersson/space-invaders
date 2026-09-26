from skit import *
from s4 import loop_arrows, line_marker

OPEN_LINE = 'with open(path, newline="", encoding="utf-8-sig") as f:'


class S5(AgentScene):
    SEG = "s5"

    def construct(self):
        # the end of chapter 4: run A up to its first run_tests request
        self.picture("loop_1", 11, tag=True, labels={18: "Fixed."})
        arrows = loop_arrows(self.model, self.code)
        self.add(arrows)
        cards = self.strip.cards

        # 01: it doesn't
        self.at("01")
        self.tool_runs("test_report.py", 0.3)

        # 02: the key error (captures/loop_1.json, the run_tests result)
        self.at("02")
        res = cards[11].data["text"].rstrip().split("\n")
        tail = [l for l in res if l.startswith("KeyError") or l.startswith("FAILED")]
        assert tail == ["KeyError: 'region'", "FAILED (errors=1)"], tail
        panel = quote([('    region = row["region"]', MUTED), ("KeyError: 'region'", CORAL), ("FAILED (errors=1)", CORAL)], 15,
                      title="tool result: run_tests")
        op = keep_on_screen(callout(cards[11], panel, UP, 0.35))
        self.play(FadeIn(op), run_time=0.5)

        # 03-04: it joins the context: ground truth
        self.at("03")
        self.play(Indicate(cards[11], color=GREEN, scale_factor=1.12), run_time=0.8)
        self.at("04", 1.0)
        gt = mono("ground truth", 16, GREEN).next_to(cards[11], DOWN, 0.18)
        self.play(FadeIn(gt), run_time=0.5)

        # 05: the next call reads it, and asks for the data file
        self.at("05")
        self.play(FadeOut(op), run_time=0.3)
        self.read(0.5)
        self.model_writes(0.45)

        # 06: the byte order mark, glued to "region" (the sales.csv result, as read)
        self.at("06")
        self.tool_runs("sales.csv", 0.35)
        csv = cards[13].data["text"]
        assert csv.startswith("﻿region,product,units,unit_price\n"), repr(csv[:40])
        l1 = mono("region,product,units,unit_price", 16, INK)
        l2 = mono(csv.split("\n")[1], 16, MUTED)
        rows = VGroup(l1, l2).arrange(DOWN, buff=0.12, aligned_edge=LEFT)
        box = RoundedRectangle(corner_radius=0.1, width=rows.width + 1.0, height=rows.height + 0.5, stroke_color=DIM,
                               stroke_width=1.5, fill_color="#0B0E12", fill_opacity=1)
        rows.move_to(box).align_to(box, LEFT).shift(0.6 * RIGHT)
        bom = Rectangle(width=0.1, height=l1.height + 0.06, stroke_width=0, fill_color=CORAL, fill_opacity=1)
        bom.next_to(l1, LEFT, 0.06)
        bl = mono("byte order mark (U+FEFF)", 14, CORAL).next_to(box, UP, 0.12).align_to(box, LEFT)
        panel2 = VGroup(box, rows, bom, label("tool result: sales.csv", 13).next_to(box, UP, 0.12).align_to(box, RIGHT), bl)
        op2 = keep_on_screen(callout(cards[13], panel2, UP, 0.5))
        self.play(FadeIn(op2[0]), FadeIn(VGroup(box, rows, panel2[3])), run_time=0.5)
        self.play(FadeIn(bom), FadeIn(bl, shift=0.1 * UP), Flash(bom, color=CORAL, line_length=0.15, flash_radius=0.2), run_time=0.7)

        # 07: the code was only half the problem
        self.at("07")

        # 08: it changes how the file is opened
        self.at("08")
        self.play(FadeOut(op2), run_time=0.3)
        wtext = cards[14].data["text"]
        assert OPEN_LINE.replace('"', '\\"') in wtext
        self.step("report.py", t=1.4)
        panel3 = quote([OPEN_LINE], 15, title="report.py, as written")
        op3 = keep_on_screen(callout(cards[15], panel3, UP, 0.35))
        m3 = line_marker(panel3[1][0], OPEN_LINE, 'encoding="utf-8-sig"', BLUE)
        self.play(FadeIn(op3), Create(m3), run_time=0.5)

        # 09: runs the test again: it passes
        self.at("09")
        self.play(FadeOut(op3), FadeOut(m3), run_time=0.3)
        self.step("test_report.py", t=1.3)
        assert "pass" in cards[17].data["marks"]
        ok = self.proj.passing()
        self.play(ReplacementTransform(self.proj.badge, ok), run_time=0.5)
        self.proj.badge = ok

        # 10: no tool call: the loop ends
        self.at("10")
        self.read(0.4)
        self.model_writes(0.4)

        # 11-13: who chose to read the data file
        self.at("11")
        ring = SurroundingRectangle(cards[12], color=INK, buff=0.06, corner_radius=0.08, stroke_width=3)
        self.play(Create(ring), run_time=0.5)

        # 14-16: a scripted version: read, fix, test, then nothing (not run)
        self.at("14")
        chips = VGroup()
        for w in ["read", "fix", "test"]:
            b = RoundedRectangle(corner_radius=0.08, width=0.9, height=0.42, stroke_color=MUTED, stroke_width=1.5,
                                 fill_color=PANEL, fill_opacity=1)
            chips.add(VGroup(b, mono(w, 15, MUTED).move_to(b)))
        chips.arrange(RIGHT, buff=0.35).move_to([0, -1.25, 0]).align_to([X0 + 1.4, 0, 0], LEFT)
        arrs = VGroup(*[Arrow(chips[i].get_right(), chips[i + 1].get_left(), buff=0.05, color=MUTED, stroke_width=2,
                              max_tip_length_to_length_ratio=0.3) for i in range(2)])
        tag = mono("scripted (not run)", 13, MUTED).next_to(chips, UP, 0.15).align_to(chips, LEFT)
        dur = self.cues["14"][1] - self.now()
        for i in range(3):
            self.play(FadeIn(chips[i]), *([GrowArrow(arrs[i - 1])] if i else [FadeIn(tag)]), run_time=max(0.25, dur / 3.5))
        self.at("15")
        self.at("16")
        stop = cross(chips[2].get_right() + RIGHT * 0.45, 0.13, CORAL, 5)
        self.play(FadeIn(stop), run_time=0.4)

        # 17-18: the agent's own path after the key error
        self.at("17")
        path = SurroundingRectangle(VGroup(*cards[12:18]), color=BLUE, buff=0.08, corner_radius=0.1, stroke_width=3)
        self.play(ReplacementTransform(ring, path), run_time=0.6)
        self.at("18")
        self.play(Indicate(cards[11], color=GREEN, scale_factor=1.12), run_time=0.8)
        self.until(self.dur - 0.6)
        self.play(FadeOut(VGroup(chips, arrs, tag, stop, path, gt)), run_time=0.5)
        self.finish()
