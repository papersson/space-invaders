"""Generate the data behind the video's "real" visuals into data/.

- race_*.png / race.json: every block transfer (I/O) heapsort and 2-way merge sort
  make under an LRU cache (iosim.py: 261,120 items, memory 21,760 items = 1/12 of
  the file, 256-item blocks), plotted as position-in-file against time; plus both
  algorithms' comparison counts and the pass counts 18 -> 5 -> 2.
- strip.json: 1,000,000 random keys sorted by external merge sort in the same
  proportions as the hook (memory = 16% of the file, so 7 runs). One sampled key
  per pixel column, before, after each run is formed, and fully sorted.
- toy.json: the 48-card toy (B = 4, M = 16): its shuffled deck and the event log
  of the 3-way merge that the animation replays.
"""
import heapq
import json
import math
import random
from pathlib import Path

import numpy as np
from PIL import Image

import iosim

OUT = Path(__file__).parent / "data"
AMBER = (242, 169, 59)


def race():
    # a file twelve memories long, like the sort demo (1,000 MB against an 86 MB buffer makes 12 runs)
    B = 256
    M = 85 * B
    n = 12 * M
    ch, cm, ext = iosim.run_all(n, B, trace=True, M=M)
    W, H = 1400, 300
    nblocks = n // B
    random.seed(0)
    a = [random.random() for _ in range(n)]
    heap_cmp, merge_cmp = iosim.comparisons(a)
    p2, io2 = iosim.external_passes(a, M, B, 2)
    pk, iok = iosim.external_passes(a, M, B, M // B - 1)
    meta = {"n": n, "M": M, "B": B, "external_mergesort": ext,
            "comparisons": {"heapsort": heap_cmp, "mergesort": merge_cmp},
            "passes": {"mergesort": math.ceil(math.log2(n)), "runs_then_two_way": p2, "runs_then_multiway": pk},
            "pass_ios": {"runs_then_two_way": io2, "runs_then_multiway": iok},
            "pieces_below_memory": int(math.log2(M))}
    print(f"comparisons heapsort {heap_cmp:,} merge {merge_cmp:,}; passes 18? {meta['passes']}; ios {meta['pass_ios']}")
    for name, cache in (("heapsort", ch), ("mergesort", cm)):
        tr = np.array(cache.trace, dtype=np.int64)
        x = np.minimum((tr[:, 0] - 1) * W // cache.steps, W - 1)
        y = (tr[:, 1] % nblocks) * H // nblocks          # merge sort ping-pongs between two arrays
        y = H - 1 - y                                     # start of the file at the bottom
        img = np.zeros((H, W), np.float32)
        np.add.at(img, (y, x), 1.0)
        # a trip is a dot; soft saturation keeps density visible
        from scipy.ndimage import maximum_filter
        img = maximum_filter(img, size=2)                 # 2 px dots, same for both panels
        alpha = np.clip(img / 8.0, 0, 1) ** 0.5
        rgba = np.zeros((H, W, 4), np.uint8)
        rgba[..., :3] = AMBER
        rgba[..., 3] = (alpha * 255).astype(np.uint8)
        Image.fromarray(rgba, "RGBA").save(OUT / f"race_{name}.png")
        cum = np.searchsorted(np.sort(x), np.arange(W), side="right")
        meta[name] = {"trips": cache.io, "steps": cache.steps, "cum_by_column": cum.tolist()}
        print(f"{name}: {cache.io:,} trips over {cache.steps:,} accesses")
    print(f"external merge sort: {ext:,} trips")
    (OUT / "race.json").write_text(json.dumps(meta))


def strip():
    rng = np.random.default_rng(7)
    N, M, W = 1_000_000, 160_000, 1600
    keys = rng.random(N)
    cols = (np.arange(W) * N) // W + N // (2 * W)
    states = [keys[cols].round(4).tolist()]
    work = keys.copy()
    bounds = []
    for lo in range(0, N, M):
        work[lo:lo + M] = np.sort(work[lo:lo + M])
        bounds.append(int(lo * W // N))
        states.append(work[cols].round(4).tolist())
    states.append(np.sort(keys)[cols].round(4).tolist())
    (OUT / "strip.json").write_text(json.dumps({
        "N": N, "M": M, "runs": len(bounds), "run_start_columns": bounds + [W], "states": states}))
    print(f"strip: {len(bounds)} runs")


def merge_events(runs, B):
    """k-way merge with one input block per run and one output block."""
    ev = [{"t": "load", "run": r, "block": 0} for r in range(len(runs))]
    pos = [0] * len(runs)
    heap = [(run[0], r) for r, run in enumerate(runs)]
    heapq.heapify(heap)
    out = 0
    while heap:
        v, r = heapq.heappop(heap)
        ev.append({"t": "pop", "run": r, "value": v, "slot": pos[r] % B, "out": out % B})
        out += 1
        if out % B == 0:
            ev.append({"t": "flush", "block": out // B - 1})
        pos[r] += 1
        if pos[r] < len(runs[r]):
            if pos[r] % B == 0:
                ev.append({"t": "refill", "run": r, "block": pos[r] // B})
            heapq.heappush(heap, (runs[r][pos[r]], r))
    return ev


def toy():
    N, B, M = 48, 4, 16
    best = None
    for seed in range(400):
        deck = list(range(1, N + 1))
        random.Random(seed).shuffle(deck)
        runs = [sorted(deck[i:i + M]) for i in range(0, N, M)]
        ev = merge_events(runs, B)
        kinds = [e["t"] for e in ev]
        first_flush, first_refill = kinds.index("flush"), kinds.index("refill")
        pops = [e for e in ev if e["t"] == "pop"]
        first4 = {e["run"] for e in pops[:4]}
        switches = sum(a["run"] != b["run"] for a, b in zip(pops, pops[1:]))
        # teachable: the first output block mixes all three runs, the flush comes
        # before the first refill, and runs interleave a lot
        if len(first4) == 3 and first_flush < first_refill:
            score = switches
            if best is None or score > best[0]:
                best = (score, seed, deck, runs, ev)
    score, seed, deck, runs, ev = best
    trips = sum(e["t"] in ("load", "flush", "refill") for e in ev)
    (OUT / "toy.json").write_text(json.dumps(
        {"N": N, "B": B, "M": M, "seed": seed, "deck": deck, "runs": runs, "events": ev,
         "merge_trips": trips}, indent=0))
    print(f"toy: seed {seed}, {score} run switches, merge trips {trips}")


if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    toy()
    strip()
    race()
