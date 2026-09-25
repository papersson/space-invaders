#!/usr/bin/env python3
"""Run GNU sort with a small buffer and a dedicated temp dir, sampling the temp
dir listing, the output size and sort's RSS roughly every 0.1 s.

usage: capture_gnu_sort.py WORKDIR BUFFER OUT_JSON [extra sort args...]
"""
import json
import os
import shutil
import subprocess
import sys
import threading
import time

INTERVAL = 0.1      # sampling period (s)
KEEP_EVERY = 0.5    # keep an unchanged sample at least this often (s)


def read_status(pid):
    rss = hwm = None
    try:
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    rss = int(line.split()[1])
                elif line.startswith("VmHWM:"):
                    hwm = int(line.split()[1])
    except (FileNotFoundError, ProcessLookupError):
        pass
    return rss, hwm


def read_state(pid):
    try:
        with open(f"/proc/{pid}/stat") as f:
            return f.read().rsplit(")", 1)[1].split()[0]
    except (FileNotFoundError, ProcessLookupError, IndexError):
        return None


def list_tmp(tmpdir):
    files = []
    try:
        with os.scandir(tmpdir) as it:
            for e in it:
                try:
                    files.append({"name": e.name, "bytes": e.stat().st_size})
                except FileNotFoundError:
                    pass
    except FileNotFoundError:
        pass
    files.sort(key=lambda d: d["name"])
    return files


def main():
    work, buf, out_json = sys.argv[1], sys.argv[2], sys.argv[3]
    extra = sys.argv[4:]
    inp = os.path.join(work, "records.txt")
    out = os.path.join(work, "sorted.txt")
    tmpdir = os.path.join(work, "sort-tmp")
    shutil.rmtree(tmpdir, ignore_errors=True)
    os.makedirs(tmpdir)
    if os.path.exists(out):
        os.remove(out)

    version = subprocess.run(["sort", "--version"], capture_output=True,
                             text=True).stdout.splitlines()[0]
    argv = ["sort", "-S", buf, "-T", tmpdir, *extra, inp, "-o", out]
    shown = ["sort", "-S", buf, "-T", "sort-tmp", *extra, "records.txt",
             "-o", "sorted.txt"]
    env = dict(os.environ, LC_ALL="C")

    samples = []
    last_key = None
    last_kept_t = -1e9
    n_max = 0
    names_seen = []
    peak_hwm = 0

    t0 = time.monotonic()
    proc = subprocess.Popen(argv, env=env, stderr=subprocess.PIPE)
    # Reap the child in a thread with wait4() so we get the exact exit time
    # and the kernel's own peak-RSS figure (ru_maxrss).
    done = {}

    def waiter():
        _, status, ru = os.wait4(proc.pid, 0)
        done["t"] = time.monotonic() - t0
        done["rc"] = os.waitstatus_to_exitcode(status)
        done["maxrss"] = ru.ru_maxrss
    th = threading.Thread(target=waiter)
    th.start()
    next_t = t0
    while True:
        running = "t" not in done
        t = time.monotonic() - t0
        tmp = list_tmp(tmpdir)
        try:
            out_bytes = os.stat(out).st_size
        except FileNotFoundError:
            out_bytes = 0
        rss, hwm = read_status(proc.pid) if running else (None, None)
        if hwm:
            peak_hwm = max(peak_hwm, hwm)
        n_max = max(n_max, len(tmp))
        for f in tmp:
            if f["name"] not in names_seen:
                names_seen.append(f["name"])
        state = read_state(proc.pid) if running else "exited"
        s = {"t": round(t, 3), "tmp_files": tmp, "output_bytes": out_bytes,
             "sort_rss_kb": rss if rss is not None else 0, "state": state}
        key = (tuple((f["name"], f["bytes"]) for f in tmp), out_bytes, rss,
               state)
        if key != last_key or t - last_kept_t >= KEEP_EVERY or not running:
            samples.append(s)
            last_key = key
            last_kept_t = t
        if not running:
            break
        next_t += INTERVAL
        time.sleep(max(0.0, next_t - time.monotonic()))
    th.join()
    duration = done["t"]
    proc.returncode = done["rc"]
    stderr = proc.stderr.read().decode(errors="replace")

    result = {
        "command": "LC_ALL=C " + " ".join(shown),
        "input_bytes": os.path.getsize(inp),
        "sort_version": version,
        "buffer": buf,
        "samples": samples,
        "n_temp_files_max": n_max,
        "duration_s": round(duration, 3),
        # extras (not in the requested schema, but useful):
        "returncode": proc.returncode,
        "stderr": stderr,
        "sort_peak_rss_kb_vmhwm": peak_hwm,
        "sort_peak_rss_kb_ru_maxrss": done["maxrss"],
        "sort_peak_rss_kb_sampled": max(x["sort_rss_kb"] for x in samples),
        "temp_file_names_in_order_seen": names_seen,
        "output_bytes_final": os.path.getsize(out),
        "sample_interval_s": INTERVAL,
        "nproc": os.cpu_count(),
    }
    with open(out_json, "w") as f:
        json.dump(result, f, separators=(",", ":"))
    print(json.dumps({k: v for k, v in result.items() if k != "samples"},
                     indent=1))
    print("samples kept:", len(samples), "json bytes:", os.path.getsize(out_json))


if __name__ == "__main__":
    main()
