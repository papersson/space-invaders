# Usage: python3 iosim.py 18   (N = 2^18 keys, memory M = N/16, blocks B = 64 and 256)
# Count block transfers (misses) under an LRU cache of M/B blocks.
import random, sys
from collections import OrderedDict

class LRU:
    def __init__(self, M, B, trace=False):
        self.B, self.frames, self.c, self.io = B, M // B, OrderedDict(), 0
        self.steps = 0                      # every access, hit or miss
        self.trace = [] if trace else None  # (step, block) for each miss
    def touch(self, blk):
        self.steps += 1
        c = self.c
        if blk in c:
            c.move_to_end(blk); return
        self.io += 1
        if self.trace is not None:
            self.trace.append((self.steps, blk))
        c[blk] = True
        if len(c) > self.frames:
            c.popitem(last=False)

def heapsort(a, cache):
    B, t = cache.B, cache.touch
    n = len(a)
    def sift(i, end):
        while True:
            l = 2*i+1
            if l >= end: return
            t(l//B)
            r = l+1
            m = l
            if r < end:
                t(r//B)
                if a[r] > a[l]: m = r
            t(i//B)
            if a[m] <= a[i]: return
            a[i], a[m] = a[m], a[i]
            i = m
    for i in range(n//2-1, -1, -1): sift(i, n)
    for end in range(n-1, 0, -1):
        t(0); t(end//B)
        a[0], a[end] = a[end], a[0]
        sift(0, end)

def mergesort(a, cache):
    # bottom-up 2-way, ping-pong between two arrays (second array offset by n)
    B, t, n = cache.B, cache.touch, len(a)
    src, dst, so, do = a, [0]*n, 0, n
    w = 1
    while w < n:
        for lo in range(0, n, 2*w):
            i, mid, hi = lo, min(lo+w, n), min(lo+2*w, n)
            j, k = mid, lo
            while i < mid or j < hi:
                if j >= hi or (i < mid and src[i] <= src[j]):
                    t((so+i)//B); dst[k] = src[i]; i += 1
                else:
                    t((so+j)//B); dst[k] = src[j]; j += 1
                t((do+k)//B); k += 1
        src, dst, so, do = dst, src, do, so
        w *= 2
    return src

def external_mergesort(a, M, B):
    """External merge sort with explicit buffers. Returns (sorted list, block transfers)."""
    import heapq
    n, io = len(a), 0
    runs = []
    for lo in range(0, n, M):                 # phase 1: memory-sized sorted runs
        chunk = a[lo:lo+M]
        io += -(-len(chunk) // B)             # read
        runs.append(sorted(chunk))
        io += -(-len(chunk) // B)             # write
    k = M // B - 1                            # one input block per run + one output block
    while len(runs) > 1:                      # phase 2: k-way merge passes
        nxt = []
        for g in range(0, len(runs), k):
            group = runs[g:g+k]
            pos = [0] * len(group)
            heap = []
            for r, run in enumerate(group):
                io += 1                       # first block of each run
                heap.append((run[0], r))
            heapq.heapify(heap)
            out, outbuf = [], 0
            while heap:
                v, r = heapq.heappop(heap)
                out.append(v); outbuf += 1
                if outbuf == B:
                    io += 1; outbuf = 0       # flush a full output block
                pos[r] += 1
                if pos[r] < len(group[r]):
                    if pos[r] % B == 0:
                        io += 1               # input buffer ran dry: fetch next block
                    heapq.heappush(heap, (group[r][pos[r]], r))
            if outbuf:
                io += 1
            nxt.append(out)
        runs = nxt
    return runs[0], io

def external_passes(a, M, B, fanin):
    """External merge sort with a given merge width. Returns (passes, block transfers)."""
    n, io, runs = len(a), 0, []
    for lo in range(0, n, M):
        c = a[lo:lo + M]
        io += 2 * -(-len(c) // B)
        runs.append(sorted(c))
    passes = 1
    while len(runs) > 1:
        nxt = []
        for g in range(0, len(runs), fanin):
            grp = runs[g:g + fanin]
            io += 2 * -(-sum(len(r) for r in grp) // B)
            nxt.append(sorted(x for r in grp for x in r))
        runs = nxt
        passes += 1
    return passes, io

def comparisons(a):
    """Comparisons made by the heapsort and bottom-up merge sort above, on copies of a."""
    k = [0]
    def lt(x, y):
        k[0] += 1
        return x < y
    h = list(a); n = len(h)
    def sift(i, end):
        while True:
            l = 2 * i + 1
            if l >= end: return
            r, m = l + 1, l
            if r < end and lt(h[l], h[r]): m = r
            if not lt(h[i], h[m]): return
            h[i], h[m] = h[m], h[i]; i = m
    for i in range(n // 2 - 1, -1, -1): sift(i, n)
    for end in range(n - 1, 0, -1):
        h[0], h[end] = h[end], h[0]; sift(0, end)
    heap_k = k[0]; k[0] = 0
    src, w = list(a), 1
    while w < n:
        dst = [0] * n
        for lo in range(0, n, 2 * w):
            i, mid, hi = lo, min(lo + w, n), min(lo + 2 * w, n); j, t = mid, lo
            while i < mid and j < hi:
                if lt(src[j], src[i]): dst[t] = src[j]; j += 1
                else: dst[t] = src[i]; i += 1
                t += 1
            dst[t:hi] = src[i:mid] + src[j:hi]
        src, w = dst, w * 2
    return heap_k, k[0]

def run_all(n, B, trace=False, M=None):
    M = M or n // 16
    random.seed(0); a = [random.random() for _ in range(n)]
    ch = LRU(M, B, trace); heapsort(a, ch); assert all(a[i] <= a[i+1] for i in range(n-1))
    random.seed(0); a = [random.random() for _ in range(n)]
    cm = LRU(M, B, trace); s = mergesort(a, cm); assert s == sorted(s)
    random.seed(0); a = [random.random() for _ in range(n)]
    s, ext = external_mergesort(a, M, B); assert s == sorted(a)
    return ch, cm, ext

if __name__ == "__main__":
    n = 1 << int(sys.argv[1]); M = n // 16
    for B in (64, 256):
        if M // B < 3:  # a 2-way merge needs two input blocks and one output block in memory
            print(f"N=2^{sys.argv[1]} B={B}: skipped, memory holds only {M // B} block(s)"); continue
        ch, cm, ext = run_all(n, B)
        h, m = ch.io, cm.io
        print(f"N=2^{sys.argv[1]} M=N/16 B={B}: heapsort {h:,}  2-way mergesort {m:,}  ext k-way {ext:,}  heap/merge {h/m:.1f}x  heap/ext {h/ext:.0f}x")
