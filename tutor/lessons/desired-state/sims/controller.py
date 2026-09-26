"""Two controllers keeping 3 replicas running, on the same timeline of events.

edge:  acts on each event it receives: "a pod died" -> start one pod. Events that arrive
       while it is down (restarting) are lost.
level: on every pass (each tick, and whenever it wakes), counts the pods that exist and
       starts or stops the difference from the desired count. It never looks at events.

Timeline (ticks are seconds): desired = 3; a pod crashes at t=10; the controller restarts
from t=20 to t=26; another pod crashes at t=22, while it is down. A new pod takes 2 s to start.
Writes data/controller.json with both pod-count timelines.
"""
import json
from pathlib import Path

DESIRED, T_END, START_DELAY = 3, 40, 2
CRASHES = {10: "pod-1", 22: "pod-2"}
DOWN = range(20, 27)


def run(kind):
    pods = {"pod-0": 0, "pod-1": 0, "pod-2": 0}      # name -> tick it became ready
    starting, n_new, events, timeline, log = {}, 3, [], [], []
    for t in range(T_END + 1):
        for name, ready in list(starting.items()):     # finish starting pods
            if ready <= t:
                pods[name] = t; del starting[name]
        if t in CRASHES:                                # a pod crashes; an event is emitted
            del pods[CRASHES[t]]
            events.append((t, "pod died"))
            log.append((t, f"{CRASHES[t]} crashed"))
        up = t not in DOWN
        if kind == "edge":
            if up:
                for (te, e) in events:
                    if e == "pod died":
                        name = f"pod-{n_new}"; n_new += 1
                        starting[name] = t + START_DELAY
                        log.append((t, f"event '{e}' (t={te}) -> start {name}"))
            else:
                for (te, e) in events:
                    log.append((t, f"event '{e}' (t={te}) lost: controller down"))
            events = []
        else:
            events = []                                 # level: events are only wake-ups
            if up:
                have = len(pods) + len(starting)
                for _ in range(DESIRED - have):
                    name = f"pod-{n_new}"; n_new += 1
                    starting[name] = t + START_DELAY
                    log.append((t, f"counted {have}, want {DESIRED} -> start {name}"))
        timeline.append(len(pods))
    return {"timeline": timeline, "log": log, "final": len(pods)}


out = {"desired": DESIRED, "crashes": CRASHES, "down": [DOWN.start, DOWN.stop - 1], "start_delay": START_DELAY,
       "edge": run("edge"), "level": run("level")}
Path("data").mkdir(exist_ok=True)
Path("data/controller.json").write_text(json.dumps(out, indent=1))
for k in ("edge", "level"):
    print(k, "final running pods:", out[k]["final"])
    for t, m in out[k]["log"]:
        print(f"  t={t:2d}  {m}")
    print("  running pods over time:", "".join(str(n) for n in out[k]["timeline"]))
