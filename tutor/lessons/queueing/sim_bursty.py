"""Burstier arrivals for chapter 6 (python3 sim_bursty.py): one FIFO server, exponential work with
mean S = 10 ms, interarrival times from a two-phase hyperexponential with squared coefficient of
variation 3 (three times as variable as Poisson arrivals, balanced means). Compared with Kingman's
approximation T = S + ((Ca^2 + Cs^2) / 2) * rho / (1 - rho) * S. Adds "bursty" to data/queue.json."""
import json
import math
import random

S, CA2, N = 0.010, 3.0, 5_000_000


def h2_gap(rng, lam):
    p1 = 0.5 * (1 + math.sqrt((CA2 - 1) / (CA2 + 1)))
    if rng.random() < p1:
        return rng.expovariate(2 * p1 * lam)
    return rng.expovariate(2 * (1 - p1) * lam)


def run(rho, seed):
    rng = random.Random(seed)
    lam = rho / S
    t = free = total = 0.0
    for _ in range(N):
        t += h2_gap(rng, lam)
        start = max(t, free)
        free = start + rng.expovariate(1 / S)
        total += free - t
    return total / N


if __name__ == "__main__":
    q = json.load(open("data/queue.json"))
    sim, king = {}, {}
    for rho in (0.3, 0.5, 0.6, 0.7, 0.8, 0.85, 0.9):
        sim[f"{rho:.2f}"] = run(rho, int(rho * 977)) * 1000
        king[f"{rho:.2f}"] = (S + (CA2 + 1) / 2 * rho / (1 - rho) * S) * 1000
        print(f"rho {rho:.2f}: simulated {sim[f'{rho:.2f}']:7.2f} ms   Kingman {king[f'{rho:.2f}']:7.2f} ms")
    q["bursty"] = {"ca2": CA2, "N": N, "sim_ms": sim, "kingman_ms": king}
    json.dump(q, open("data/queue.json", "w"))
