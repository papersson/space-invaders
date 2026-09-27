from skit import *

TOOL_OF = {"search": "search", "open_file": "open file", "edit_file": "edit file", "run_tests": "run tests"}


def start_s5(sc):
    """The end of chapter 4: result pasted back; the model's next request is out."""
    d, col = sc.d, sc.col
    sc.add(chip("5 · the loop"), *d.base(4), d.tag_claude)
    col.place([instr_item(col), task_item(col), col.item([TR["steps"][0]["request"]], MODEL, size=15),
               col.item(["prices.py:8:", 'raise LookupError(f"no price for {product!r}")'], HARN, size=14)])
    nxt = T(TR["steps"][1]["request"], 19, MODEL, font=MONO).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
    sc.add(nxt)
    return nxt


class S5(LScene):
    SEG = "s5"

    def counter(self, n):
        return T(f"requests: {n}", 16, NUM, font=MONO).move_to([CTX_R - 0.2, CTX_T - 0.24, 0], aligned_edge=RIGHT)

    def construct(self):
        d, col = self.d, self.col
        nxt = start_s5(self)
        self.fade_in_all(0.3)
        arrows = [d.a_cm, d.a_ms, d.a_sp, d.a_pc]

        # 01: one step won't fix a bug
        self.at("01", 0.3)
        self.play(FadeOut(nxt), run_time=0.4)

        # 02-04: so repeat: the loop, a dot running round it
        self.at("02")
        self.play(*[self.lit(a, INK, 0.4) for a in arrows], FadeIn(d.loop_label), run_time=0.4)
        path = d.loop_path()
        dot = Dot(radius=0.085, color=INK).move_to(path.get_start())
        self.add(dot)
        s, e = self.cues["03"]
        self.until(s)
        self.play(MoveAlongPath(dot, path), run_time=e - s, rate_func=linear)
        self.at("04")
        self.play(MoveAlongPath(dot, path), run_time=1.3, rate_func=linear)

        # 05-06: until a reply with no request in it; then the loop stops
        self.at("05", 0.6)
        reply = card(["a reply, with no request in it"], MUTED, w=4.3, size=15, font=SANS)
        reply.move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
        seg = VMobject().set_points_as_corners([path.get_start(), np.array([SLOT_L - 0.05, SLOT_Y, 0])])
        self.play(MoveAlongPath(dot, seg), run_time=0.6, rate_func=linear)
        self.play(FadeIn(reply, shift=RIGHT * 0.1), run_time=0.4)
        s, e = self.cues["05"]
        self.until(e - 0.9)
        nothing = tag("no request: stop", MUTED, 15).next_to(d.a_sp, RIGHT, buff=0.12)
        self.play(FadeIn(nothing), run_time=0.4)
        self.at("06", 0.8)
        self.play(FadeOut(dot), *[self.lit(a, FAINT, 0.6) for a in arrows], run_time=0.6)

        # 07: a model in a loop like this, using tools, is called an agent
        self.at("07", 1.6)
        ag = T("agent", 30, INK, weight=BOLD).move_to([2.6, 3.5, 0])
        rule = Line([-3.1, 3.5, 0], [7.0, 3.5, 0], stroke_color=FAINT, stroke_width=1.5)
        rl, rr = rule.copy().put_start_and_end_on([-3.1, 3.5, 0], [1.95, 3.5, 0]), \
            rule.copy().put_start_and_end_on([3.25, 3.5, 0], [7.0, 3.5, 0])
        self.play(FadeIn(ag, scale=1.2), Create(rl), Create(rr), run_time=0.7)

        # 08: here's how the whole run went: the context starts again from the task
        self.at("08")
        olds = [it["shown"] for it in col.items]
        col.items = []
        self.play(*[FadeOut(m) for m in olds], FadeOut(reply), FadeOut(nothing), FadeOut(d.loop_label), run_time=0.5)
        ins, task = instr_item(col, short=True), task_item(col, short=True)
        cnt = self.counter(0)
        self.play(*col.anims(ins), *col.anims(task), FadeIn(cnt), run_time=0.4)
        self.cnt = cnt

        c = self.cues
        self.step(1, c["08"][0] + 1.0, c["09"][0] + 0.9)
        self.step(2, c["09"][0] + 0.95, c["09"][0] + 2.4)
        self.step(3, c["09"][0] + 2.5, c["09"][0] + 4.3)
        self.step(4, c["09"][0] + 4.35, c["09"][1] + 0.7)

        # 10: the price list spells it "Gadget", with a capital G
        self.at("10")
        res2 = col.items[5]["shown"][2][0]
        tsk = col.items[1]["shown"][2][0]
        u1 = Underline(glyphs(res2, "Gadget"), color=NUM, buff=0.03, stroke_width=3)
        u2 = Underline(glyphs(tsk, "gadget"), color=NUM, buff=0.03, stroke_width=3)
        self.play(Create(u2), run_time=0.4)
        self.play(Create(u1), run_time=0.4)

        # 11: so it edits the lookup: now "gadget" finds "Gadget"
        self.at("11")
        self.play(FadeOut(u1), FadeOut(u2), run_time=0.2)
        self.step(5, c["11"][0] + 0.2, c["11"][1] + 0.5)

        # 12-13: it runs the tests; they fail
        self.step(6, c["12"][0], c["13"][1] + 0.15, fail_at=c["13"][0])

        # 14-15: Ben's bill: 37.00 expected, 39.50 computed
        self.at("14", 0.2)
        ben1 = T("Ben: expected 37.00", 17, INK, font=MONO)
        ben2 = T("got 39.50", 17, FAIL, font=MONO)
        ben = VGroup(ben1, ben2).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([PROJ_L + 0.05, -2.85, 0], aligned_edge=LEFT)
        self.play(FadeIn(ben1), run_time=0.4)
        self.at("15", 0.1)
        self.play(FadeIn(ben2), run_time=0.4)

        # 16: the failure goes into the context and changes the next step
        self.at("16")
        fail_card = col.items[-1]["shown"]
        box = SurroundingRectangle(fail_card, color=FAIL, buff=0.05, corner_radius=0.07, stroke_width=2.4)
        self.play(Create(box), run_time=0.5)
        self.play(self.lit(d.a_cm, MODEL), run_time=0.3)
        self.sweep(1.0)
        self.play(Indicate(d.model, color=MODEL, scale_factor=1.05), run_time=0.6)
        self.play(FadeOut(box), self.lit(d.a_cm, FAINT), FadeOut(ben), run_time=0.4)

        # 17: looks at the test and at Ben's orders (requests 7 to 10)
        s, e = c["17"][0], c["17"][1] + 1.45
        w = (e - s) / 4
        for k, n in enumerate([7, 8, 9, 10]):
            self.step(n, s + k * w, s + (k + 1) * w - 0.05)

        # 18-19: the discount kicked in at eleven, should start at ten: request 11
        self.step(11, c["18"][0], c["18"][1] + 0.1)
        self.at("19")
        lab = T("discount from 10, not 11", 16, NUM, font=MONO).move_to([PROJ_L + 0.05, -3.2, 0], aligned_edge=LEFT)
        self.play(FadeIn(lab), run_time=0.4)

        # 20-21: runs the tests again; they pass
        self.at("20")
        self.play(FadeOut(lab), FadeOut(self.last_tag), run_time=0.3)
        self.last_tag = None
        self.step(12, c["20"][0] + 0.35, c["21"][1] + 0.3, pass_at=c["21"][0])

        # 22: it writes its answer, and the loop stops
        self.at("22")
        ans = T(TR["reply_excerpt"], 17, MUTED, font=MONO).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
        self.play(FadeIn(ans, shift=RIGHT * 0.1), run_time=0.4)
        it = col.item([TR["reply_excerpt"]], MUTED, size=14)
        self.play(*col.anims(it, src=ans), run_time=0.6)
        stop = tag("no request: stop", MUTED, 15).next_to(d.a_sp, RIGHT, buff=0.12)
        self.play(FadeIn(stop), run_time=0.3)

        # 23: twelve requests
        self.at("23")
        reqs = VGroup(*[i["shown"] for i in col.items if i["role"] == MODEL])
        self.play(Circumscribe(self.cnt, color=NUM, buff=0.06), reqs.animate.set_opacity(1).set_color(MODEL), run_time=0.9)
        self.play(Indicate(reqs, color=MODEL, scale_factor=1.02), run_time=0.8)
        self.end()

    # --- one request of the real run, from the model writing it to its result in the context ------
    last_tag = None

    def step(self, n, t0, t1, fail_at=None, pass_at=None):
        d, col = self.d, self.col
        st = TR["steps"][n - 1]
        self.until(t0)
        dur = max(t1 - self.now(), 0.9)
        k = st["kind"]
        chipm = d.tools[TOOL_OF[k]]
        req = T(st["request"], 19, MODEL, font=MONO).move_to([SLOT_L, SLOT_Y, 0], aligned_edge=LEFT)
        self.play(FadeIn(req, shift=RIGHT * 0.1), run_time=0.18 * dur)
        # the program spots the request and carries it out
        target = []
        if k in ("open_file", "edit_file"):
            target = [d.files[st["request"].split(":", 1)[1].strip()]]
        elif k == "search":
            target = list(d.files.values())
        elif k == "run_tests":
            target = [d.files["test_invoice.py"]]
        on = [chipm[0].animate.set_fill(HARN, 0.4), self.lit(d.a_sp, HARN), self.lit(d.a_pj, HARN)]
        on += [f[0].animate.set_stroke(HARN, 2.4) for f in target]
        r_item = col.item([st["request"]], MODEL, size=14)
        self.play(*on, *col.anims(r_item, src=req), run_time=0.24 * dur)
        self.remove(self.cnt)
        self.cnt = self.counter(n)
        self.add(self.cnt)
        # the result
        if fail_at is not None:
            self.until(fail_at)
        if pass_at is not None:
            self.until(pass_at)
        color = HARN
        if st["status"] == "fail":
            color = FAIL
        elif st["status"] == "pass":
            color = PASS
        text = st["result_excerpt"]
        res = card([text], color, w=4.3, size=14)
        res.move_to([PROG_C[0], PROG_C[1] - PROG_H / 2 - 0.35, 0])
        extra = []
        if st["status"] == "pass":
            extra = [ReplacementTransform(d.badge_fail, d.badge_pass)]
        elif st["status"] == "fail":
            extra = [Indicate(d.badge_fail, color=FAIL, scale_factor=1.06)]
        tg = []
        if st["tag"]:
            if self.last_tag is not None:
                tg.append(FadeOut(self.last_tag))
            self.last_tag = T(st["tag"], 17, NUM, font=MONO).move_to([PROJ_L + 0.05, -2.75, 0], aligned_edge=LEFT)
            tg.append(FadeIn(self.last_tag))
        self.play(FadeIn(res, shift=DOWN * 0.08), self.lit(d.a_pc, color), *extra, *tg,
                  run_time=max(0.2 * (t1 - t0), 0.2))
        x_item = col.item([text], color, size=14)
        left = max(t1 - self.now(), 0.25)
        off = [chipm[0].animate.set_fill(HARN, 0), self.lit(d.a_sp, FAINT), self.lit(d.a_pj, FAINT),
               self.lit(d.a_pc, FAINT)]
        off += [f[0].animate.set_stroke(FAINT, 1.4) for f in target]
        self.play(*col.anims(x_item, src=res), *off, run_time=left * 0.9)
