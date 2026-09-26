"""Change propagation on a small dependency graph, three ways, logging every recomputation.

naive: when a value changes, immediately recompute each dependent (depth-first), which
       in turn recomputes its dependents. This is the observer pattern. The order in which
       dependents are notified is whatever order they subscribed in; both orders are recorded.
height: mark everything downstream as out of date, then recompute in order of height
       (inputs are height 0; a formula is 1 + the highest of its inputs), each at most once.
cutoff: height order, and if a recomputed value is unchanged, don't mark its dependents.
Writes data/propagate.json with the traces and the counts used in the lesson.
"""
import json
from pathlib import Path


class Graph:
    def __init__(self):
        self.f, self.deps, self.val, self.users = {}, {}, {}, {}

    def input(self, name, v):
        self.val[name] = v; self.deps[name] = []; self.users.setdefault(name, [])

    def formula(self, name, deps, f):
        self.f[name], self.deps[name] = f, deps
        self.users.setdefault(name, [])
        for d in deps:
            self.users[d].append(name)
        self.val[name] = f(*[self.val[d] for d in deps])

    def height(self, n):
        return 0 if not self.deps[n] else 1 + max(self.height(d) for d in self.deps[n])

    def compute(self, n, log):
        v = self.f[n](*[self.val[d] for d in self.deps[n]])
        log.append((n, v))
        changed = v != self.val[n]
        self.val[n] = v
        return changed

    def set_naive(self, name, v, latest_first=False):
        log = []
        self.val[name] = v
        def push(n):
            for u in (reversed(self.users[n]) if latest_first else self.users[n]):
                self.compute(u, log)
                push(u)
        push(name)
        return log

    def set_height(self, name, v, cutoff=False):
        log = []
        self.val[name] = v
        dirty = set(self.users[name])
        while dirty:
            n = min(dirty, key=self.height)          # lowest height first
            dirty.remove(n)
            if self.compute(n, log) or not cutoff:
                dirty.update(self.users[n])
        return log


def cart():
    g = Graph()
    g.input("price", 20); g.input("qty", 2)
    g.formula("subtotal", ["price", "qty"], lambda p, q: p * q)
    g.formula("tax", ["subtotal"], lambda s: s * 10 // 100)
    g.formula("total", ["subtotal", "tax"], lambda s, t: s + t)
    g.formula("free_shipping", ["total"], lambda t: t >= 50)
    g.formula("banner", ["free_shipping"], lambda f: "Free shipping!" if f else "Spend $50 for free shipping")
    return g


def stacked(k):
    """k diamonds in a row: x -> (a1, b1) -> d1 -> (a2, b2) -> d2 ... ; count recomputations of the last node."""
    g = Graph(); g.input("x", 0); prev = "x"
    for i in range(1, k + 1):
        g.formula(f"a{i}", [prev], lambda v: v + 1)
        g.formula(f"b{i}", [prev], lambda v: v + 2)
        g.formula(f"d{i}", [f"a{i}", f"b{i}"], lambda a, b: a + b)
        prev = f"d{i}"
    return g, prev


out = {}
g = cart(); out["before"] = dict(g.val)
out["naive"] = cart().set_naive("qty", 3)
out["naive_total_first"] = cart().set_naive("qty", 3, latest_first=True)
out["height"] = cart().set_height("qty", 3)
g = cart(); g.set_height("qty", 3); out["after"] = dict(g.val)
out["cutoff_qty4"] = (lambda g: (g.set_height("qty", 3, True), g.set_height("qty", 4, True))[1])(cart())
out["nocutoff_qty4"] = (lambda g: (g.set_height("qty", 3), g.set_height("qty", 4))[1])(cart())
counts = []
for k in (1, 2, 3, 5, 10, 20):
    g, last = stacked(k); n_naive = sum(1 for n, _ in g.set_naive("x", 1) if n == last)
    g, last = stacked(k); n_height = sum(1 for n, _ in g.set_height("x", 1) if n == last)
    g, _ = stacked(k); total_naive = len(g.set_naive("x", 1))
    g, _ = stacked(k); total_height = len(g.set_height("x", 1))
    counts.append({"diamonds": k, "last_naive": n_naive, "last_height": n_height,
                   "all_naive": total_naive, "all_height": total_height})
out["stacked"] = counts
Path("data").mkdir(exist_ok=True)
Path("data/propagate.json").write_text(json.dumps(out, indent=1))
for k in ("before", "naive", "naive_total_first", "height", "after", "nocutoff_qty4", "cutoff_qty4"):
    print(k, out[k])
for c in counts:
    print(c)
