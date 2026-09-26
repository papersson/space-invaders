from rkit import *

AFTER = {"subtotal": "$60", "tax": "$6", "total": "$66", "free": "yes", "banner": "Free shipping!"}


class S8(CueScene):
    SEG = "s8"

    def construct(self):
        c = chip("The answer")
        g = Graph()
        n = g.n
        self.at("01")
        self.play(FadeIn(c), FadeIn(g), run_time=0.7)
        self.at("02")
        self.play(n["qty"].set("3", AMBER), run_time=0.4)
        for k in ["subtotal", "tax", "total", "free", "banner"]:
            self.play(n[k].set(AFTER[k], GREEN), run_time=0.35)

        # 03-05: two questions, two answers
        self.at("03")
        q = VGroup(mono("what is out of date?", 22, INK), mono("in what order?", 22, INK)).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        q.move_to([-2.4, -2.3, 0])
        self.play(FadeIn(q), run_time=0.6)
        self.at("04")
        a1 = mono("→ everything downstream, nothing else", 20, GREEN).next_to(q[0], RIGHT, 0.3)
        self.play(FadeIn(a1), run_time=0.5)
        self.at("05")
        a2 = mono("→ by height, once each, stop where unchanged", 20, GREEN).next_to(q[1], RIGHT, 0.3)
        self.play(FadeIn(a2), run_time=0.5)

        # 06: get it wrong: 64
        self.at("06")
        ghost = mono("$64", 22, CORAL).next_to(n["total"], UP, 0.2)
        self.play(FadeIn(ghost), run_time=0.4)
        self.play(FadeOut(ghost), run_time=0.6)

        # 08: the same machine in three places
        self.at("08")
        self.play(FadeOut(q), FadeOut(a1), FadeOut(a2), run_time=0.4)
        where = VGroup(mono("cells: Excel", 20, ICE), mono("files: Make, Bazel", 20, ICE),
                       mono("UI state: Vue, Solid, Angular signals", 20, ICE)).arrange(RIGHT, buff=0.8).move_to([0, -2.3, 0])
        self.play(LaggedStart(*[FadeIn(w) for w in where], lag_ratio=0.5), run_time=1.6)

        # end card
        self.until(self.end_of("08", 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("What the Spreadsheet Knows", 40, INK, weight=SEMIBOLD).move_to([0, 2.4, 0])
        s1 = T("Keep a dependency graph. After a change, mark everything downstream,", 24, INK).next_to(name, DOWN, 0.5)
        s1b = T("then recompute in height order, each value once, and stop where nothing changed.", 24, INK).next_to(s1, DOWN, 0.12)
        refs = VGroup(T("Further reading", 18, MUTED, weight=MEDIUM),
                      T("Bainomugisha et al., \"A Survey on Reactive Programming\", ACM Computing Surveys (2013)", 18, MUTED),
                      T("Mokhov, Mitchell & Peyton Jones, \"Build Systems à la Carte\", ICFP (2018)", 18, MUTED),
                      T("Cooper & Krishnamurthi, \"Embedding Dynamic Dataflow in a Call-by-Value Language\", ESOP (2006)", 18, MUTED),
                      T("Microsoft, \"Excel Recalculation\" · Minsky, \"Seven Implementations of Incremental\" (2016)", 18, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s1b, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(s1), FadeIn(s1b), run_time=0.7)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
