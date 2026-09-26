"""Queueing simulations behind the lesson's numbers (python3 sim.py).

One FIFO server, work per request exponential with mean S = 10 ms, arrivals Poisson at rate lam
(an M/M/1 queue), plus the evenly spaced, fixed-work foil (D/D/1) and a multi-server check (M/M/c).
Writes data/queue.json.
"""
import heapq
import json
import random

S = 0.010


def mm1(rho, n, seed, S=S):
    rng = random.Random(seed)
    lam = rho / S
    t = free = 0.0
    total = 0.0
    for _ in range(n):
        t += rng.expovariate(lam)
        start = max(t, free)
        free = start + rng.expovariate(1 / S)
        total += free - t
    return total / n


def mmc(rho, c, n, seed, S=S):
    """c servers sharing one FIFO queue, utilization rho per server."""
    rng = random.Random(seed)
    lam = rho * c / S
    t = 0.0
    frees = [0.0] * c
    total = 0.0
    for _ in range(n):
        t += rng.expovariate(lam)
        f = heapq.heappop(frees)
        start = max(t, f)
        end = start + rng.expovariate(1 / S)
        heapq.heappush(frees, end)
        total += end - t
    return total / n


def dd1(rho, n, S=S):
    gap = S / rho
    t = free = total = 0.0
    for _ in range(n):
        t += gap
        start = max(t, free)
        free = start + S
        total += free - t
    return total / n


def trace(rho, n, seed=7, S=S):
    """Queue length (requests in the system) at every arrival and departure, for the animation.
    The same random draws at every load: interarrival and work are unit exponentials, scaled."""
    rng = random.Random(seed)
    ia = [rng.expovariate(1.0) for _ in range(n)]
    wk = [rng.expovariate(1.0) for _ in range(n)]
    lam = rho / S
    t = free = 0.0
    arr, dep = [], []
    for a, w in zip(ia, wk):
        t += a / lam
        start = max(t, free)
        free = start + w * S
        arr.append(t)
        dep.append(free)
    events = sorted([(x, +1) for x in arr] + [(x, -1) for x in dep])
    q, pts = 0, [(0.0, 0)]
    for x, d in events:
        q += d
        pts.append((round(x, 5), q))
    return {"arrivals": [round(x, 5) for x in arr], "departures": [round(x, 5) for x in dep], "queue": pts,
            "resp_mean": sum(d - a for a, d in zip(arr, dep)) / n}


if __name__ == "__main__":
    N = 20_000_000
    rhos = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95]
    sim = {f"{r:.2f}": mm1(r, N, seed=int(r * 1000)) * 1000 for r in rhos}
    theory = {f"{r:.2f}": S / (1 - r) * 1000 for r in rhos}
    for k in sim:
        print(f"rho {k}: simulated {sim[k]:7.2f} ms   formula {theory[k]:7.2f} ms")
    dd = {f"{r:.2f}": dd1(r, 10_000) * 1000 for r in (0.5, 0.8, 0.9, 0.95)}
    print("evenly spaced, fixed work:", dd)
    c8 = {f"{r:.2f}": mmc(r, 8, N, seed=5) * 1000 for r in (0.5, 0.8, 0.9, 0.95)}
    print("8 servers, one queue:", c8)
    tr = {f"{r:.2f}": trace(r, 400) for r in (0.8, 0.9)}
    for k, v in tr.items():
        print(f"trace {k}: mean response {v['resp_mean'] * 1000:.1f} ms, max queue {max(q for _, q in v['queue'])}")
    json.dump({"S_ms": S * 1000, "N": N, "mm1_sim_ms": sim, "mm1_formula_ms": theory, "dd1_ms": dd,
               "mmc8_sim_ms": c8, "trace": tr}, open("data/queue.json", "w"))
