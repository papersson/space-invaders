# Usage: python3 iosim.py 18   (N = 2^18 keys, memory M = N/16, blocks B = 64 and 256)
# Count block transfers (misses) under an LRU cache of M/B blocks.
import random, sys
from collections import OrderedDict

class LRU:
    def __init__(self, M, B):
        self.B, self.frames, self.c, self.io = B, M // B, OrderedDict(), 0
    def touch(self, blk):
        c = self.c
        if blk in c:
            c.move_to_end(blk); return
        self.io += 1
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

n = 1 << int(sys.argv[1]); M = n // 16
for B in (64, 256):
    random.seed(0); a = [random.random() for _ in range(n)]
    c = LRU(M, B); heapsort(a, c); assert all(a[i] <= a[i+1] for i in range(n-1)); h = c.io
    random.seed(0); a = [random.random() for _ in range(n)]
    c = LRU(M, B); s = mergesort(a, c); assert s == sorted(s); m = c.io
    ext = 4 * n // B  # external merge sort, 1 merge pass: read+write twice
    print(f"N=2^{sys.argv[1]} M=N/16 B={B}: heapsort {h:,}  2-way mergesort {m:,}  ext k-way {ext:,}  heap/merge {h/m:.1f}x  heap/ext {h/ext:.0f}x")
