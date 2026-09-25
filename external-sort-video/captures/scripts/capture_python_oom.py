#!/usr/bin/env python3
"""Run `sorted(open('records.txt'))` in python3 under `ulimit -v LIMIT_KB`,
sampling its RSS (and virtual size) every ~0.05 s until it dies.

usage: capture_python_oom.py WORKDIR LIMIT_KB OUT_JSON
"""
import json
import os
import subprocess
import sys
import threading
import time

INTERVAL = 0.05


def read_status(pid):
    vals = {}
    try:
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                k = line.split(":", 1)[0]
                if k in ("VmRSS", "VmSize", "VmHWM", "VmPeak"):
                    vals[k] = int(line.split()[1])
    except (FileNotFoundError, ProcessLookupError):
        pass
    return vals


def main():
    work, limit_kb, out_json = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    py = "lines = sorted(open('records.txt'))"
    shell = f'ulimit -v {limit_kb}; exec python3 -c "{py}"'
    argv = ["bash", "-c", shell]

    samples = []
    peaks = {}
    t0 = time.monotonic()
    proc = subprocess.Popen(argv, cwd=work, stderr=subprocess.PIPE,
                            stdout=subprocess.PIPE)
    done = {}

    def waiter():
        _, status, ru = os.wait4(proc.pid, 0)
        done["t"] = time.monotonic() - t0
        done["status"] = status
        done["maxrss"] = ru.ru_maxrss

    th = threading.Thread(target=waiter)
    th.start()
    next_t = t0
    while "t" not in done:
        t = time.monotonic() - t0
        v = read_status(proc.pid)
        if "VmRSS" in v:
            samples.append({"t": round(t, 3), "rss_kb": v["VmRSS"],
                            "vmsize_kb": v["VmSize"]})
            for k in ("VmHWM", "VmPeak"):
                peaks[k] = max(peaks.get(k, 0), v.get(k, 0))
        next_t += INTERVAL
        time.sleep(max(0.0, next_t - time.monotonic()))
    th.join()
    stderr = proc.stderr.read().decode(errors="replace")
    stdout = proc.stdout.read().decode(errors="replace")
    status = done["status"]
    rc = os.waitstatus_to_exitcode(status)
    result = {
        # the exact argv, written as a valid shell command line
        "command": 'bash -c "ulimit -v %d; exec python3 -c '
                   '\\"%s\\""' % (limit_kb, py),
        "limit_kb": limit_kb,
        "samples": samples,
        "stderr": stderr,
        "returncode": rc,
        # extras
        "killed_by_signal": os.WIFSIGNALED(status),
        "signal": os.WTERMSIG(status) if os.WIFSIGNALED(status) else None,
        "stdout": stdout,
        "duration_s": round(done["t"], 3),
        "peak_rss_kb_vmhwm": peaks.get("VmHWM"),
        "peak_vmsize_kb_vmpeak": peaks.get("VmPeak"),
        "peak_rss_kb_ru_maxrss": done["maxrss"],
        "input_bytes": os.path.getsize(os.path.join(work, "records.txt")),
        "python_version": sys.version.split()[0],
        "sample_interval_s": INTERVAL,
    }
    with open(out_json, "w") as f:
        json.dump(result, f, separators=(",", ":"))
    print(json.dumps({k: v for k, v in result.items() if k != "samples"},
                     indent=1))
    print("samples:", len(samples), "json bytes:", os.path.getsize(out_json))
    print("first/last samples:", samples[:3], samples[-3:])


if __name__ == "__main__":
    main()
