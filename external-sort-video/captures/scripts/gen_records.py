#!/usr/bin/env python3
"""Generate 100-byte text records: 10 random uppercase key chars, a space,
88 random alphanumeric payload chars, newline.  Fixed seed, stdlib only.

usage: gen_records.py OUT N_RECORDS [SEED]
"""
import random
import sys

UPPER = b"ABCDEFGHIJKLMNOPQRSTUVWXYZ"
ALNUM = b"ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789"


def table(alphabet):
    # Keep only byte values < k*len(alphabet) (rejection sampling -> uniform),
    # then map byte b -> alphabet[b % len(alphabet)].
    n = len(alphabet)
    keep = (256 // n) * n
    trans = bytes(alphabet[b % n] for b in range(256))
    drop = bytes(range(keep, 256))
    return trans, drop


def draw(rng, count, trans, drop):
    out = bytearray()
    while len(out) < count:
        raw = rng.randbytes(int((count - len(out)) * 1.15) + 64)
        out += raw.translate(trans, drop)
    return bytes(out[:count])


def main():
    out_path = sys.argv[1]
    n_total = int(sys.argv[2])
    seed = int(sys.argv[3]) if len(sys.argv) > 3 else 20260925
    rng = random.Random(seed)
    kt, kd = table(UPPER)
    pt, pd = table(ALNUM)
    chunk = 200_000
    with open(out_path, "wb", buffering=0) as f:
        done = 0
        while done < n_total:
            n = min(chunk, n_total - done)
            keys = draw(rng, 10 * n, kt, kd)
            pay = draw(rng, 88 * n, pt, pd)
            buf = bytearray(100 * n)
            for i in range(10):
                buf[i::100] = keys[i::10]
            buf[10::100] = b" " * n
            for i in range(88):
                buf[11 + i::100] = pay[i::88]
            buf[99::100] = b"\n" * n
            f.write(buf)
            done += n


if __name__ == "__main__":
    main()
