from qkit import *

ROW0, ROWH, NROWS = 1.9, 0.3, 13
X_LEFT, X_RIGHT = -5.6, 6.2


def gantt(arrivals, starts, ends, t_max, cursor):
    """One row per request: grey from arrival to start of work, amber while being worked on.
    Drawn up to the cursor time (ms)."""
    sc = (X_RIGHT - X_LEFT) / t_max
    g = VGroup()
    t = cursor.get_value()
    for k, (a, s, e) in enumerate(zip(arrivals, starts, ends)):
        if a > t:
            break
        y = ROW0 - ROWH * k
        g.add(Dot([X_LEFT + a * sc, y, 0], radius=0.05, color=ICE))
        if s > a:
            g.add(Rectangle(width=(min(s, t) - a) * sc, height=0.18, stroke_width=0, fill_color=WAIT,
                            fill_opacity=0.9).move_to([X_LEFT + a * sc, y, 0], aligned_edge=LEFT))
        if t > s:
            g.add(Rectangle(width=max((min(e, t) - s) * sc, 0.001), height=0.18, stroke_width=0, fill_color=AMBER,
                            fill_opacity=0.95).move_to([X_LEFT + s * sc, y, 0], aligned_edge=LEFT))
    g.add(Line([X_LEFT + t * sc, ROW0 + 0.3, 0], [X_LEFT + t * sc, ROW0 - ROWH * (NROWS - 1) - 0.25, 0],
               stroke_color=ICE, stroke_width=2, stroke_opacity=0.6))
    return g


def waiting_at(arrivals, starts, t):
    return sum(1 for a, s in zip(arrivals, starts) if a <= t < s)


def clumpy_window(trace, n=NROWS):
    """A window of n consecutive requests from the 90% trace that includes a clear clump."""
    arr = [x * 1000 for x in trace["arrivals"]]
    dep = [x * 1000 for x in trace["departures"]]
    best, best_w = 0, None
    for w in range(1, 250):
        if dep[w - 1] > arr[w]:          # start the window with an idle server
            continue
        a, d = arr[w:w + n], dep[w:w + n]
        s = [max(a[0], a[0])] + [max(a[i], d[i - 1]) for i in range(1, n)]
        qmax = max(waiting_at(a, s, x) for x in a)
        if 4 <= qmax <= 6 and (best_w is None or qmax > best):
            best, best_w = qmax, w
    w = best_w
    a, d = arr[w:w + n], dep[w:w + n]
    s = [a[0]] + [max(a[i], d[i - 1]) for i in range(1, n)]
    t0 = a[0] - 5
    return [x - t0 for x in a], [x - t0 for x in s], [x - t0 for x in d]


class S3(CueScene):
    SEG = "s3"

    def construct(self):
        c = chip("Where queues come from")
        axis = Line([X_LEFT, ROW0 + 0.45, 0], [X_RIGHT, ROW0 + 0.45, 0], stroke_color=FAINT, stroke_width=1.5)
        tl = mono("time →", 16, FAINT).next_to(axis, UP, 0.08).align_to(axis, RIGHT)
        rows = mono("one row per request", 16, FAINT).next_to(axis, UP, 0.08).align_to(axis, LEFT)
        counter = Counter(0, title="WAITING NOW", size=40, anchor=[6.5, 3.35, 0], color=INK)

        # 01-04: evenly spaced, fixed work: nobody waits
        self.at("01")
        gap = S_MS / 0.9
        arr = [2 + k * gap for k in range(NROWS)]
        st, en = arr, [a + S_MS for a in arr]
        t_max = en[-1] + 4
        cur = ValueTracker(0.0)
        g = always_redraw(lambda: gantt(arr, st, en, t_max, cur))
        head = T("evenly spaced, exactly 10 ms of work each", 24, INK).move_to([1.3, 3.3, 0])
        self.play(FadeIn(c), FadeIn(head), FadeIn(axis), FadeIn(tl), FadeIn(rows), FadeIn(counter), run_time=0.6)
        self.add(g)
        v_rate = t_max / max(self.start_of("04") - self.now(), 3.0)

        def sweep(tracker, until, rate, *anims):
            d = until - self.now()
            if d > 1 / 30:
                self.play(tracker.animate.set_value(tracker.get_value() + d * rate), *anims, run_time=d,
                          rate_func=linear)
        sweep(cur, self.start_of("02", 1.5), v_rate)
        gl = mono("a new request every 11.1 ms (10 ms ÷ 0.9)", 18, ICE).move_to([2.3, -2.5, 0])
        sweep(cur, self.now() + 0.5, v_rate, FadeIn(gl))
        sweep(cur, self.start_of("04"), v_rate)
        cur.set_value(t_max)
        self.at("04")
        ok = mono("nobody waits: every response 10 ms", 22, INK).next_to(gl, DOWN, 0.3)
        self.play(FadeIn(ok), run_time=0.5)

        # 05-08: random arrivals and random work: a clump builds a queue
        self.at("05")
        g.clear_updaters()
        self.play(FadeOut(g), FadeOut(gl), FadeOut(ok), FadeOut(head), run_time=0.4)
        arr2, st2, en2 = clumpy_window(Q["trace"]["0.90"])
        t_max2 = en2[-1] + 4
        cur2 = ValueTracker(0.0)
        g2 = always_redraw(lambda: gantt(arr2, st2, en2, t_max2, cur2))
        head2 = T("real traffic: random arrivals, random work (90% busy)", 24, INK).move_to([1.2, 3.3, 0])
        self.play(FadeIn(head2), run_time=0.4)
        self.add(g2)
        counter.tracker.add_updater(lambda m: m.set_value(waiting_at(arr2, st2, cur2.get_value())))
        self.add(counter.tracker)
        span2 = self.start_of("09") - self.now() - 0.3
        self.play(cur2.animate.set_value(t_max2), run_time=max(span2, 5.0), rate_func=linear)
        counter.tracker.clear_updaters()

        # 09-10: queues come from variability
        self.at("09")
        var = T("Queues come from variability.", 30, ICE).move_to([2.0, -2.55, 0])
        self.play(FadeIn(var), run_time=0.5)
        self.at("10")
        how = T("What decides how long they last?", 26, MUTED).next_to(var, DOWN, 0.25)
        self.play(FadeIn(how), run_time=0.5)
        self.until(self.dur - 0.5)
        g2.clear_updaters()
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.45)
        self.finish()
