from ckit import *


class S8(CueScene):
    SEG = "s8"

    def construct(self):
        c = chip("The answer")
        actor = Actor(0.8, 0.3)
        ma, mb = machine("A", -5.3, 1.3), machine("B", -5.3, -1.1)
        self.at("01")
        self.play(FadeIn(c), FadeIn(actor), FadeIn(ma), FadeIn(mb), run_time=0.6)
        self.at("03")
        ea, eb = envelope("deposit 50", AMBER), envelope("deposit 50", AMBER)
        ea.move_to(ma.get_right() + 0.7 * RIGHT); eb.move_to(mb.get_right() + 0.7 * RIGHT)
        self.play(FadeIn(ea), FadeIn(eb), run_time=0.3)
        self.play(ea.animate.move_to(actor.slot(0)), eb.animate.move_to(actor.slot(1)), run_time=0.7)
        self.play(FadeOut(ea), actor.set("$150"), run_time=0.4)
        self.play(FadeOut(eb), actor.set("$200", GOOD), run_time=0.4)
        # 04-07: the table
        self.at("04")
        self.play(*[FadeOut(m) for m in self.mobjects if m is not c], run_time=0.4)
        cols = ["threads + locks", "actors", "channels"]
        rows = [("data race", ["only if every access\ntakes the lock", "ruled out for its own state\n(enforced in Erlang;\nconvention in Akka)",
                               "ruled out for the owner's\nstate (convention in Go)"], [AMBER, GOOD, GOOD]),
                ("race condition\n(check, then act)", ["possible"] * 3, [BAD] * 3),
                ("deadlock", ["possible"] * 3, [BAD] * 3)]
        xs, y0 = [-1.6, 1.6, 4.8], 2.4
        head = VGroup(*[mono(t, 18, INK).move_to([x, y0, 0]) for t, x in zip(cols, xs)])
        grid = VGroup(head)
        for i, (name, cells, colors) in enumerate(rows):
            y = y0 - 1.1 - 1.2 * i
            row = VGroup(mono(name, 17, MUTED).move_to([-5.0, y, 0]))
            for t, x, col in zip(cells, xs, colors):
                row.add(mono(t, 14, col).move_to([x, y, 0]))
            grid.add(row)
        self.play(FadeIn(grid[0]), FadeIn(grid[1]), run_time=0.8)
        self.play(FadeIn(grid[2]), FadeIn(grid[3]), run_time=0.8)
        # 08-10: two decisions
        self.at("08")
        self.play(FadeOut(grid), run_time=0.4)
        d = VGroup(T("Two decisions, in every one of these models:", 28, INK),
                   mono("1. which steps must happen as one", 22, AMBER),
                   mono("2. no cycle of waits", 22, AMBER)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([0, 0.6, 0])
        self.play(FadeIn(d[0]), run_time=0.5)
        self.at("09")
        self.play(FadeIn(d[1]), run_time=0.4)
        self.at("10")
        self.play(FadeIn(d[2]), run_time=0.4)
        self.at("11")
        ns = mono("neither model is simply the safe one", 20, ICE).move_to([0, -1.4, 0])
        self.play(FadeIn(ns), run_time=0.5)
        self.at("14")
        adv = mono("Go wiki: channels to hand data along · a lock to guard a piece of state", 17, MUTED).move_to([0, -2.2, 0])
        self.play(FadeIn(adv), run_time=0.5)

        # end card
        self.until(self.end_of("14", 0.7))
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.5)
        name = T("Share Memory, or Pass Messages?", 38, INK, weight=SEMIBOLD).move_to([0, 2.5, 0])
        s1 = T("One owner per piece of state rules out data races on it.", 24, INK).next_to(name, DOWN, 0.5)
        s2 = T("It doesn't rule out race conditions or deadlock: you still choose what happens as one step,", 20, MUTED).next_to(s1, DOWN, 0.18)
        s3 = T("and keep waits from forming a cycle.", 20, MUTED).next_to(s2, DOWN, 0.1)
        refs = VGroup(T("Further reading", 18, MUTED, weight=MEDIUM),
                      T("Butcher, Seven Concurrency Models in Seven Weeks (2014), ch. 2, 5, 6", 17, MUTED),
                      T("Hoare, \"Communicating Sequential Processes\", CACM (1978) · Hewitt, Bishop & Steiger, IJCAI (1973)", 17, MUTED),
                      T("Goetz et al., Java Concurrency in Practice (2006), ch. 2, 10", 17, MUTED),
                      T("Tu et al., \"Understanding Real-World Concurrency Bugs in Go\", ASPLOS (2019)", 17, MUTED),
                      T("Lauer & Needham, \"On the Duality of Operating System Structures\" (1979) · Go wiki, \"Use a sync.Mutex or a channel?\"", 17, MUTED))
        refs.arrange(DOWN, buff=0.1).next_to(s3, DOWN, 0.6)
        self.play(FadeIn(name), FadeIn(s1), run_time=0.6)
        self.play(FadeIn(s2), FadeIn(s3), run_time=0.5)
        self.play(FadeIn(refs), run_time=0.5)
        self.until(self.dur - 0.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
