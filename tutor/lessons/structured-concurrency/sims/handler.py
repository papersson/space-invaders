"""The request handler from the lesson, run for real with asyncio (Python 3.11+).

A handler fetches a user and the user's orders concurrently. fetch_user takes 1.0 s;
fetch_orders fails after 0.1 s. The handler is written two ways: with asyncio.gather,
and with asyncio.TaskGroup. Every event is timestamped from the start of the request.
Usage: python3 handler.py > ../data/handler_runs.txt   (also writes ../data/timeline.json)
"""
import asyncio, gc, json, sys, time
from pathlib import Path

EVENTS = []
T0 = 0.0
QUIET = False


def log(who, what):
    if QUIET:
        return
    t = time.monotonic() - T0
    EVENTS.append({"t": round(t, 3), "who": who, "what": what})
    print(f"  {t:5.2f}s  {who:<14} {what}", flush=True)


async def fetch_user(fail_late=False):
    log("fetch_user", "started")
    try:
        await asyncio.sleep(1.0)
    except asyncio.CancelledError:
        log("fetch_user", "cancelled")
        raise
    if fail_late:
        log("fetch_user", "raises TimeoutError")
        raise TimeoutError("user service timed out")
    log("fetch_user", "finished")
    return "ada"


async def fetch_orders(fails=True):
    log("fetch_orders", "started")
    try:
        await asyncio.sleep(0.1 if fails else 1.0)
    except asyncio.CancelledError:
        log("fetch_orders", "cancelled")
        raise
    if fails:
        log("fetch_orders", "raises ConnectionError")
        raise ConnectionError("orders service down")
    log("fetch_orders", "finished")
    return ["book"]


async def fetch_user_retrying():
    """A retry loop with a bare except: it catches cancellation too, and tries again."""
    log("fetch_user", "started")
    for attempt in (1, 2):
        try:
            await asyncio.sleep(1.0)
            log("fetch_user", "finished")
            return "ada"
        except BaseException as e:
            log("fetch_user", f"caught {type(e).__name__}, retrying")


async def handler_sequential(fail_late=False):
    try:
        user = await fetch_user(fail_late)
        orders = await fetch_orders()
    except Exception as e:
        log("handler", f"returns error: {type(e).__name__}")
        return "error"


async def handler_gather(fail_late=False):
    try:
        user, orders = await asyncio.gather(fetch_user(fail_late), fetch_orders())
    except Exception as e:
        log("handler", f"returns error: {type(e).__name__}")
        return "error"


async def handler_taskgroup(fail_late=False):
    try:
        async with asyncio.TaskGroup() as tg:
            user = tg.create_task(fetch_user(fail_late))
            orders = tg.create_task(fetch_orders())
    except* Exception as eg:            # TaskGroup raises an ExceptionGroup
        names = ", ".join(type(e).__name__ for e in eg.exceptions)
        log("handler", f"returns error: {names}")


async def one_request(handler, label, fail_late=False):
    global T0
    EVENTS.clear()
    print(f"=== {label}")
    T0 = time.monotonic()
    await handler(fail_late)
    log("handler", "has returned")
    log("server", f"tasks still running: {len(asyncio.all_tasks()) - 1}")
    await asyncio.sleep(1.3)                        # the server keeps running afterwards
    gc.collect()                                    # an unretrieved task error would be logged here, to stderr
    await asyncio.sleep(0.05)
    alive = len(asyncio.all_tasks()) - 1
    log("server", f"tasks still running: {alive}")
    return list(EVENTS)


async def many_requests(handler, label, n=1000):
    global QUIET
    print(f"=== {label}: {n} requests at once")
    start = time.monotonic()
    before = len(asyncio.all_tasks())
    QUIET = True
    await asyncio.gather(*[handler() for _ in range(n)])
    took = time.monotonic() - start
    alive = len(asyncio.all_tasks()) - before
    print(f"  all {n} handlers returned after {took:.2f}s; tasks still running: {alive}")
    await asyncio.sleep(1.2)
    later = len(asyncio.all_tasks()) - before
    QUIET = False
    print(f"  1.2 s later, tasks still running: {later}")
    return {"n": n, "returned_after": round(took, 2), "alive": alive, "alive_later": later}


async def caller_gives_up(handler, label):
    """The client gives up after 0.5 s: asyncio.timeout around the handler. Both calls are slow."""
    global T0
    EVENTS.clear()
    print(f"=== {label}")
    T0 = time.monotonic()
    try:
        async with asyncio.timeout(0.5):
            await handler()
    except TimeoutError:
        log("caller", "gave up at the timeout")
    await asyncio.sleep(1.3)
    log("server", f"tasks still running: {len(asyncio.all_tasks()) - 1}")
    return list(EVENTS)


async def gather_both_slow():
    await asyncio.gather(fetch_user(), fetch_orders(fails=False))


async def taskgroup_both_slow():
    async with asyncio.TaskGroup() as tg:
        tg.create_task(fetch_user())
        tg.create_task(fetch_orders(fails=False))


async def create_task_both_slow():
    """Start both with create_task, then await them one after the other."""
    u = asyncio.create_task(fetch_user())
    o = asyncio.create_task(fetch_orders(fails=False))
    await u
    await o


async def handler_taskgroup_retrying(fail_late=False):
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_user_retrying())
            tg.create_task(fetch_orders())
    except* Exception as eg:
        log("handler", f"returns error: {', '.join(type(e).__name__ for e in eg.exceptions)}")


async def main():
    out = {}
    out["sequential"] = await one_request(handler_sequential, "sequential: fetch_user, then fetch_orders, which fails after 0.1 s")
    out["gather"] = await one_request(handler_gather, "gather: fetch_orders fails at 0.1 s")
    out["taskgroup"] = await one_request(handler_taskgroup, "TaskGroup: fetch_orders fails at 0.1 s")
    out["gather_late"] = await one_request(handler_gather, "gather: and fetch_user fails later, at 1.0 s", True)
    out["taskgroup_late"] = await one_request(handler_taskgroup, "TaskGroup: and fetch_user would fail later, at 1.0 s", True)
    out["many_gather"] = await many_requests(handler_gather, "gather")
    out["many_taskgroup"] = await many_requests(handler_taskgroup, "TaskGroup")
    out["cancel_taskgroup"] = await caller_gives_up(taskgroup_both_slow, "TaskGroup: the caller gives up at 0.5 s")
    out["cancel_gather"] = await caller_gives_up(gather_both_slow, "gather: the caller gives up at 0.5 s")
    out["cancel_create_task"] = await caller_gives_up(create_task_both_slow, "create_task, awaited in turn: the caller gives up at 0.5 s")
    out["retrying"] = await one_request(handler_taskgroup_retrying, "TaskGroup, fetch_user retries with a bare except: fetch_orders fails at 0.1 s")
    Path(__file__).resolve().parent.parent.joinpath("data", "timeline.json").write_text(json.dumps(out, indent=1))


asyncio.run(main())
print(f"=== Python {sys.version.split()[0]}")
