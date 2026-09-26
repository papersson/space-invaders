from qkit import *


class S7(CueScene):
    SEG = "s7"

    def construct(self):
        c = chip("The answer")
        fast, slow = medians("1")
        # 01-02: who decides
        self.at("01")
        q = T("Who decides how a query runs?", 30, INK).move_to([0, 2.6, 0])
        self.play(FadeIn(c), FadeIn(q), run_time=0.6)
        self.at("02")
        a = mono("the query planner (SQL says only what)", 20, ICE).next_to(q, DOWN, 0.3)
        self.play(FadeIn(a), run_time=0.5)

        # 03-06: rows and pages, from statistics
        self.at("03")
        k1 = VGroup(mono("customer 4242", 16, MUTED), mono(ms(fast), 22, GOOD), mono("10 pages", 16, GOOD)).arrange(DOWN, buff=0.1)
        k2 = VGroup(mono("customer 1", 16, MUTED), mono(ms(slow), 22, BAD), mono(f"{RELPAGES:,} pages", 16, BAD)).arrange(DOWN, buff=0.1)
        VGroup(k1, k2).arrange(RIGHT, buff=2.0).move_to([0, 0.5, 0])
        self.play(FadeIn(k1), FadeIn(k2), run_time=0.6)
        lines = [("04", "rare → index → 10 pages", GOOD), ("05", "common → every page, whatever the plan", BAD),
                 ("06", "few matches + an index → nested loop · many → hash join", AMBER)]
        for i, (cue, text, col) in enumerate(lines):
            self.at(cue)
            self.play(FadeIn(mono(text, 17, col).move_to([0, -0.9 - 0.45 * i, 0])), run_time=0.4)

        # 07-09: the data, the belief, and what to do
        self.at("07")
        stale = mono("stale statistics → wrong plan → ANALYZE", 17, INK).move_to([0, -2.3, 0])
        self.play(FadeIn(stale), run_time=0.4)
        self.at("08")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        dont = mono("slow query? don't guess, don't just add an index", 20, MUTED).move_to([0, 0.9, 0])
        self.play(FadeIn(dont), run_time=0.4)
        self.at("09")
        do = mono("EXPLAIN ANALYZE: compare expected rows with actual rows", 20, AMBER).move_to([0, 0.0, 0])
        self.play(FadeIn(do), run_time=0.5)

        # end card
        self.until(self.end_of("09", 0.8))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("Same Query, Different Plan", 40, INK, weight=SEMIBOLD).move_to([0, 2.5, 0])
        s1 = T("You say what; the planner decides how, by estimating how many rows each step will touch.", 22, INK).next_to(name, DOWN, 0.5)
        s1b = T("When a query is slow, compare the estimated rows with the actual rows in EXPLAIN ANALYZE.", 22, INK).next_to(s1, DOWN, 0.12)
        refs = VGroup(T("Further reading", 17, MUTED, weight=MEDIUM),
                      T("Selinger et al., \"Access Path Selection in a Relational Database Management System\", SIGMOD (1979)", 16, MUTED),
                      T("PostgreSQL documentation, §14.1 \"Using EXPLAIN\" and §14.2 \"Statistics Used by the Planner\"", 16, MUTED),
                      T("Kleppmann, Designing Data-Intensive Applications (2017), ch. 2 · Winand, Use The Index, Luke", 16, MUTED),
                      T("Leis et al., \"How Good Are Query Optimizers, Really?\", PVLDB (2015)", 16, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s1b, DOWN, 0.7)
        self.play(FadeIn(name), FadeIn(s1), FadeIn(s1b), run_time=0.7)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
