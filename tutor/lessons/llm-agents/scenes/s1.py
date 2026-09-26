from skit import *

A_Y, B_Y = -0.2, -1.95


def final_text(run):
    return S[run]["cards"][-1]["text"]


def pick(text, *parts):
    for p in parts:
        assert p in text, p
    return parts


class S1(CueScene):
    SEG = "s1"

    def construct(self):
        proj = Project()
        A = Strip("loop_1", A_Y, labels={len(card_items("loop_1")) - 1: "Fixed."})
        B = Strip("no_tests_1", B_Y, labels={len(card_items("no_tests_1")) - 1: "Fixed."})
        la = label("run A", 16, INK).next_to(A.cards[0], UP, 0.22).align_to(A.cards[0], LEFT)
        lb = label("run B", 16, INK).next_to(B.cards[0], UP, 0.22).align_to(B.cards[0], LEFT)

        # 01: the project
        self.at("01")
        self.play(FadeIn(proj), run_time=0.8)

        # 02-03: two runs: instructions and task in both
        self.at("02", 1.0)
        self.play(FadeIn(la), FadeIn(lb), *[FadeIn(A.cards[i]) for i in (0, 1)],
                  *[FadeIn(B.cards[i]) for i in (0, 1)], run_time=0.8)

        # 04-05: the same first four steps in both
        self.at("05")
        dur = (self.cues["05"][1] - self.cues["05"][0]) - 0.3
        per = dur / 8
        for k in range(2, 10):
            self.play(FadeIn(A.cards[k], shift=0.15 * DOWN), FadeIn(B.cards[k], shift=0.15 * DOWN),
                      run_time=max(per, 0.2))

        # 06: they split
        self.at("06")
        xs = (A.cards[9].get_right()[0] + A.cards[10].get_left()[0]) / 2
        split = DashedLine([xs, A_Y + 0.75, 0], [xs, B_Y - 0.6, 0], stroke_color=FAINT, stroke_width=2, dash_length=0.08)
        self.play(Create(split), run_time=0.5)

        # 07: A takes four more steps
        self.at("07")
        dur = (self.cues["07"][1] - self.cues["07"][0]) + 0.1
        for k in range(10, 18):
            self.play(FadeIn(A.cards[k], shift=0.15 * DOWN), run_time=max(dur / 8, 0.2))

        # 08: A's last reply
        self.at("08")
        ta = final_text("loop_1")
        pick(ta, "Fixed. The test was failing for two reasons in `report.py`:", "All tests now pass.")
        qa = quote(["Fixed. The test was failing for two reasons in `report.py`:", ("…", MUTED),
                    "All tests now pass."], 14).move_to([0, 1.55, 0]).align_to([X0, 0, 0], LEFT)
        self.play(FadeIn(A.cards[18], shift=0.15 * DOWN), run_time=0.4)
        self.play(FadeIn(qa), run_time=0.5)

        # 09-10: B stops, and says Fixed
        self.at("09")
        self.play(FadeIn(B.cards[10], shift=0.15 * DOWN), run_time=0.4)
        self.at("10")
        tb = final_text("no_tests_1")
        pick(tb, "Fixed. The bug was that revenue was being computed with `+`",
             "now returns the correct totals per region, matching the expected values in `test_report.py`.")
        qb = quote(["Fixed. The bug was that revenue was being computed with `+`", ("…", MUTED),
                    "… now returns the correct totals per region, matching",
                    "the expected values in `test_report.py`."], 13)
        qb.next_to(B.first(11), DOWN, 0.3).align_to([X0, 0, 0], LEFT)
        self.play(FadeIn(qb), run_time=0.5)

        # 11-13: our own test run after each
        self.at("11")
        ra_pos = qa.get_right() + RIGHT * 0.5
        hdr = mono("our test run:", 14, MUTED)
        ha = hdr.copy().next_to(qa, RIGHT, 0.45).align_to(qa, UP).shift(0.05 * DOWN)
        hb = hdr.copy().next_to(qb, RIGHT, 0.45).align_to(qb, UP).shift(0.05 * DOWN)
        self.play(FadeIn(ha), FadeIn(hb), run_time=0.4)
        self.at("12")
        ok_a = VGroup(check(ORIGIN, 1.0, GREEN, 6), mono("OK", 18, GREEN)).arrange(RIGHT, buff=0.2).next_to(ha, DOWN, 0.2).align_to(ha, LEFT)
        self.play(FadeIn(ok_a), run_time=0.4)
        self.at("13")
        err = S["no_tests_1"]["last_error"]
        assert err == "KeyError: 'region'", err
        bad_b = VGroup(cross(ORIGIN, 0.12, CORAL, 5), mono(err, 16, CORAL)).arrange(RIGHT, buff=0.2).next_to(hb, DOWN, 0.2).align_to(hb, LEFT)
        self.play(FadeIn(bad_b), run_time=0.4)

        # 14-17: three runs each
        self.at("15")
        # counts from data/runs.txt: loop 3 of 3 passed; no_tests 3 of 3 said Fixed and failed
        three_a = mono("3 of 3", 16, INK).next_to(ok_a, RIGHT, 0.4)
        three_b = mono("3 of 3", 16, INK).next_to(bad_b, RIGHT, 0.4)
        self.at("16")
        self.play(FadeIn(three_a), run_time=0.4)
        self.at("17")
        self.play(FadeIn(three_b), run_time=0.4)

        # 18: the one missing thing: the test tool (A's two "test" cards)
        self.at("18")
        tests = [c for c in A.cards if getattr(c, "kind", "") == "model" and c.data.get("label") == "test"]
        rings = VGroup(*[SurroundingRectangle(c, color=AMBER, buff=0.05, stroke_width=3, corner_radius=0.08) for c in tests])
        self.play(Create(rings), run_time=0.6)
        self.at("19")
        self.play(FadeOut(rings), run_time=0.5)

        # 20: the question; the two strips stay
        self.at("20")
        self.play(FadeOut(VGroup(qa, ha, ok_a, three_a, qb, hb, bad_b, three_b, split)), run_time=0.8)
        self.until(self.dur)
        self.finish()
