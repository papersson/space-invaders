from dkit import *

LX, RX = -3.5, 3.4


class S2(CueScene):
    SEG = "s2"

    def construct(self):
        c = chip("Say what, not how")
        # 01-03: two ways to say it
        self.at("01")
        self.play(FadeIn(c), run_time=0.4)
        self.at("02")
        lh = mono("list the steps", 18, MUTED).move_to([LX, 2.5, 0])
        lc = mono("start 2 more servers", 22, AMBER).move_to([LX, 1.85, 0])
        self.play(FadeIn(lh), FadeIn(lc), run_time=0.6)
        self.at("03")
        rh = mono("describe the end state", 18, MUTED).move_to([RX, 2.5, 0])
        rc = mono("servers = 3", 22, ICE).move_to([RX, 1.85, 0])
        self.play(FadeIn(rh), FadeIn(rc), run_time=0.6)
        div = Line([0, 2.8, 0], [0, -3.0, 0], stroke_color=DIM, stroke_width=1.5)
        self.play(Create(div), run_time=0.4)

        # 04-08: the script, run twice
        self.at("04")
        twice = mono("run it twice", 16, MUTED).move_to([0, 3.2, 0])
        self.play(FadeIn(twice), run_time=0.4)
        self.at("05")
        imp = [l for l in RUN.splitlines() if l.startswith("after run")]
        lt = terminal([("$ ./start-two-more.sh", MUTED), (imp[0], INK), ("$ ./start-two-more.sh", MUTED),
                       (imp[1], BAD)], width=5.8, size=17).move_to([LX, 0.2, 0])
        rows = lt[1]
        self.play(FadeIn(lt[0]), run_time=0.4)
        self.at("06")
        self.play(FadeIn(rows[0]), FadeIn(rows[1]), run_time=0.5)
        self.at("07")
        self.play(FadeIn(rows[2]), FadeIn(rows[3]), run_time=0.5)
        self.at("08")
        rep = mono("every run repeats its work", 16, BAD).next_to(lt, DOWN, 0.3)
        self.play(FadeIn(rep), run_time=0.4)

        # 09-13: Terraform, run twice, then 3 -> 5 (real run)
        self.at("09")
        nc = run_line("No changes.")
        rt = terminal([("$ terraform apply", MUTED), (run_line("Plan: 3 to add"), INK),
                       ("$ terraform apply", MUTED), (nc.split(". ")[0] + ".", GOOD),
                       ("  " + nc.split(". ", 1)[1], GOOD)], width=6.3, size=16).move_to([RX, 0.35, 0])
        r = rt[1]
        self.play(FadeIn(rt[0]), run_time=0.4)
        self.at("10")
        self.play(FadeIn(r[0]), FadeIn(r[1]), run_time=0.5)
        self.at("11")
        self.play(FadeIn(r[2]), run_time=0.3)
        self.play(FadeIn(r[3]), FadeIn(r[4]), run_time=0.5)
        self.at("12")
        rc5 = mono("servers = 5", 22, ICE).move_to(rc)
        self.play(Transform(rc, rc5), run_time=0.5)
        self.at("13")
        p2 = terminal([("$ terraform plan", MUTED), (run_line("Plan: 2 to add"), AMBER)], width=6.3, size=16)
        p2.next_to(rt, DOWN, 0.2)
        self.play(FadeIn(p2), run_time=0.6)
        self.play(Circumscribe(p2[1][1], color=AMBER, stroke_width=2), run_time=0.8)

        # 14-17: the names, and the job
        self.at("14")
        n_imp = mono("imperative", 22, AMBER).move_to(lh)
        self.play(Transform(lh, n_imp), run_time=0.5)
        self.at("15")
        n_dec = mono("declarative", 22, ICE).move_to(rh)
        self.play(Transform(rh, n_dec), run_time=0.5)
        self.at("16")
        self.play(FadeOut(rep), FadeOut(lt), FadeOut(rt), FadeOut(p2), FadeOut(twice), FadeOut(div),
                  FadeOut(lh), FadeOut(lc), FadeOut(rh), FadeOut(rc), run_time=0.5)
        des = VGroup(mono("desired state", 18, MUTED), mono("servers = 5", 26, AMBER)).arrange(DOWN, buff=0.15)
        cur = VGroup(mono("current state", 18, MUTED), mono("3 servers exist", 26, INK)).arrange(DOWN, buff=0.15)
        des.move_to([-3.9, 0.9, 0])
        cur.move_to([3.9, 0.9, 0])
        self.play(FadeIn(des), run_time=0.5)
        self.play(FadeIn(cur), run_time=0.5)
        self.at("17")
        arr = Arrow(cur.get_left() + 0.4 * LEFT, des.get_right() + 0.4 * RIGHT, buff=0.1, color=ICE, stroke_width=3)
        job = mono("make current match desired", 18, ICE).next_to(arr, DOWN, 0.45)
        self.play(GrowArrow(arr), FadeIn(job), run_time=0.7)

        # 18-21: the wrong picture
        self.at("18")
        wrong = mono("apply = a script: run once, and it's done?", 20, MUTED).move_to([0, -1.2, 0])
        self.play(FadeIn(wrong), run_time=0.5)
        self.at("19")
        again = mono("run again:  No changes.", 20, GOOD).move_to([0, -1.9, 0])
        self.play(FadeIn(again), run_time=0.5)
        self.at("20")
        ran = mono("already ran", 24, MUTED).move_to([-2.2, -2.8, 0])
        self.play(FadeIn(ran), run_time=0.4)
        self.play(Create(Line(ran.get_left(), ran.get_right(), stroke_color=BAD, stroke_width=3)), run_time=0.3)
        self.at("21")
        matches = mono("already matches", 24, GOOD).move_to([2.2, -2.8, 0])
        self.play(FadeIn(matches), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
