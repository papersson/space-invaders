"""Fan-out and hedging simulations behind the lesson's numbers (python3 sim.py).

A backend call takes about 10 ms (log-normal, median 10 ms) and, independently with probability 1%,
hits a hiccup that makes it take a full second. A page calls N backends in parallel and waits for all.
Hedging: if a call hasn't answered by the backend's 95th-percentile time, send a copy to a second
backend (independent) and take whichever answers first. Writes data/fanout.json.
"""
import json
import math
import random

P_SLOW, SLOW_MS = 0.01, 1000.0


def backend(rng):
    fast = math.exp(rng.gauss(math.log(10.0), 0.25))
    return SLOW_MS + fast if rng.random() < P_SLOW else fast


def pct(xs, q):
    s = sorted(xs)
    return s[min(len(s) - 1, int(q * len(s)))]


if __name__ == "__main__":
    rng = random.Random(42)
    one = [backend(rng) for _ in range(1_000_000)]
    mean, p50, p95, p99, p999 = sum(one) / len(one), pct(one, .5), pct(one, .95), pct(one, .99), pct(one, .999)
    print(f"one backend: mean {mean:.1f} ms, p50 {p50:.1f}, p95 {p95:.1f}, p99 {p99:.1f}, p99.9 {p999:.1f}")
    exact = {n: 1 - (1 - P_SLOW) ** n for n in (1, 10, 50, 70, 100, 1000)}
    print("P(page slow) exact:", {k: round(v, 4) for k, v in exact.items()})
    pages, slow_pages, hedged_pages, extra, calls = 200_000, 0, [], 0, 0
    plain = []
    for _ in range(pages):
        lat, hl = [], []
        for _ in range(100):
            x = backend(rng)
            lat.append(x)
            calls += 1
            if x > p95:
                extra += 1
                y = p95 + backend(rng)
                hl.append(min(x, y))
            else:
                hl.append(x)
        plain.append(max(lat))
        hedged_pages.append(max(hl))
    frac_slow = sum(1 for x in plain if x >= SLOW_MS) / pages
    frac_slow_h = sum(1 for x in hedged_pages if x >= SLOW_MS) / pages
    print(f"pages of 100 calls: slow (>= 1 s) {frac_slow:.3f}; hedged at p95: slow {frac_slow_h:.4f}; "
          f"extra requests {extra / calls:.3f}")
    print(f"page p50 {pct(plain, .5):.0f} ms, p99 {pct(plain, .99):.0f}; hedged p50 {pct(hedged_pages, .5):.0f}, "
          f"p99 {pct(hedged_pages, .99):.0f}")
    grid = [[1 if rng.random() < P_SLOW else 0 for _ in range(100)] for _ in range(20)]
    json.dump({"backend": {"mean": mean, "p50": p50, "p95": p95, "p99": p99, "p999": p999},
               "exact": exact, "sim": {"pages": pages, "slow": frac_slow, "slow_hedged": frac_slow_h,
                                       "extra": extra / calls, "p50": pct(plain, .5), "p99": pct(plain, .99),
                                       "p50_hedged": pct(hedged_pages, .5), "p99_hedged": pct(hedged_pages, .99)},
               "grid": grid, "hist": sorted(one[:20000])}, open("data/fanout.json", "w"))
