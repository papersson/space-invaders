from skit import *
from s4 import loop_arrows

SCALE = 10 / 2745          # tokens -> scene units: run A's last call (2,745 tokens) is 10 units
BOT = -3.25
ROW_GAP = 0.6


def row_y(n):
    return BOT + (9 - n) * ROW_GAP


def staircase(run="loop_1", scale=SCALE, bot=BOT, gap=ROW_GAP, x0=X0):
    """Row n is what call n read: the bars of the first row_cards(n) messages, at row n's height."""
    calls = S[run]["calls"]
    rows = []
    for n in range(1, len(calls) + 1):
        r = token_bars(run, scale, bot + (len(calls) - n) * gap, x0, n_cards=row_cards(n))
        assert abs(r.width - calls[n - 1] * scale) < 0.02, (n, r.width, calls[n - 1] * scale)
        rows.append(r)
    return rows


def counts(rows, run="loop_1", size=16):
    calls = S[run]["calls"]
    out = []
    for i, (r, c) in enumerate(zip(rows, calls)):
        strong = i in (0, len(calls) - 1)
        out.append(mono_b(f"{c:,}", size if strong else size - 3, AMBER if strong else "#B98A45").next_to(r, RIGHT, 0.2))
    return out


def keyerror_bar_index():
    cs = [c for c in S["loop_1"]["cards"] if c["tokens"] > 0]
    return next(i for i, c in enumerate(cs) if c["kind"] == "result" and "fail" in c.get("marks", []))


class S6(AgentScene):
    SEG = "s6"

    def construct(self):
        # the end of chapter 5: run A complete
        self.picture("loop_1", 19, tag=True, failing=False, labels={18: "Fixed."})
        arrows = loop_arrows(self.model, self.code)
        self.add(arrows)
        cards = self.strip.cards

        # 01: nine calls: eight tool calls, then the final reply
        self.at("01")
        blues = [c for c in cards if c.kind == "model"]
        assert len(blues) == 9
        nums = VGroup(*[mono(str(i + 1), 14, BLUE).next_to(c, UP, 0.1) for i, c in enumerate(blues)])
        self.play(LaggedStart(*[FadeIn(n, shift=0.1 * DOWN) for n in nums], lag_ratio=0.15), run_time=1.6)

        # 02-04: it looks as if it remembers; each call started from nothing
        self.at("04")
        self.play(FadeOut(self.model[1]), run_time=0.4)
        self.play(FadeIn(self.model[1]), run_time=0.4)

        # 05-06: every call gets the whole context
        self.at("06")
        for _ in range(2):
            band, anim = band_sweep(self.visible(), 1.0)
            self.add(band)
            self.play(anim)
            self.remove(band)

        # 07: counted in tokens: the cards become bars sized by what they add
        self.at("07")
        bars = token_bars("loop_1", SCALE, BOT)
        self.play(FadeOut(VGroup(self.model, self.code, self.proj, arrows, nums)), run_time=0.5)
        tr = [ReplacementTransform(cards[0], VGroup(bars[0], bars[1])), ReplacementTransform(cards[1], bars[2])]
        tr += [ReplacementTransform(cards[k], bars[k + 1]) for k in range(2, 18)]
        tr += [FadeOut(cards[18])]
        self.play(*tr, run_time=1.4)
        tok = mono("tokens", 15, MUTED).next_to(bars, DOWN, 0.12).align_to(bars, LEFT)
        self.play(FadeIn(tok), run_time=0.3)

        # 08: call 1 read 1,423 tokens
        rows = staircase()
        cnt = counts(rows)
        self.at("08")
        r1 = VGroup(*[b.copy() for b in bars[:3]])
        self.play(r1.animate.move_to(rows[0]), run_time=0.7)
        self.remove(r1)
        self.add(rows[0])
        band, anim = band_sweep(rows[0], 0.4)
        self.add(band)
        self.play(anim, FadeIn(cnt[0]), run_time=0.4)
        self.remove(band)

        # 09: most of it fixed text: the tool's notes and our instructions (data/overhead.txt)
        self.at("09")
        cli, ours = rows[0][0], VGroup(rows[0][1], rows[0][2])
        b1 = Brace(cli, UP, buff=0.06, color=MUTED)
        t1 = mono("notes added by claude -p ≈1,180", 13, MUTED).next_to(b1, UP, 0.06)
        b2 = Brace(ours, UP, buff=0.06, color=MUTED)
        t2 = mono("our instructions + task ≈240", 13, MUTED).next_to(b2, UP, 0.06).align_to(b2, LEFT)
        self.play(GrowFromCenter(b1), FadeIn(t1), run_time=0.5)
        self.play(GrowFromCenter(b2), FadeIn(t2), run_time=0.5)

        # 10: every row: call n reads everything call n-1 read, and more
        self.at("10")
        dur = self.cues["10"][1] - self.now() - 0.2
        per = max(dur / 8, 0.3)
        for n in range(2, 10):
            src = VGroup(*[b.copy() for b in bars[:row_cards(n)]])
            if n < 9:
                self.play(src.animate.move_to(rows[n - 1]), FadeIn(cnt[n - 1]), run_time=per)
                self.remove(src)
                self.add(rows[n - 1])
            else:
                self.remove(src)
                self.play(FadeIn(cnt[8]), run_time=per)
        self.remove(bars)
        self.add(rows[8])

        # 11: in all, 18,537 tokens read
        self.at("11")
        total = sum(S["loop_1"]["calls"])
        assert total == 18537
        br = Brace(VGroup(*cnt), RIGHT, buff=0.15, color=AMBER)
        tt = VGroup(mono_b(f"{total:,}", 22, AMBER), mono("tokens read", 15, AMBER)).arrange(DOWN, buff=0.08)
        tt.next_to(br, RIGHT, 0.15)
        keep_on_screen(tt)
        self.play(GrowFromCenter(br), FadeIn(tt), run_time=0.6)

        # 16-17: what came back, it knows only from its context: the key error, in every row after it arrived
        self.at("16")
        k = keyerror_bar_index()
        outs = VGroup(*[SurroundingRectangle(rows[n][k], color=CORAL, buff=0.03, stroke_width=3)
                        for n in range(9) if len(rows[n]) > k])
        self.play(LaggedStart(*[Create(o) for o in outs], lag_ratio=0.2), run_time=1.2)
        self.until(self.dur)
        self.finish()
