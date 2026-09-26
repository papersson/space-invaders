"""Which except clauses catch a task group's error (Python 3.11+)? The group raises an
ExceptionGroup even for one failed task."""
import asyncio, sys


async def fetch_orders():
    await asyncio.sleep(0.1)
    raise ConnectionError("orders service down")


async def run(label, handler):
    try:
        await handler()
        print(f"{label:<34} caught inside the handler")
    except BaseException as e:
        print(f"{label:<34} NOT caught: {type(e).__name__}")


async def plain_connectionerror():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_orders())
    except ConnectionError:
        pass


async def plain_exception():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_orders())
    except Exception as e:
        assert type(e).__name__ == "ExceptionGroup"


async def star_connectionerror():
    try:
        async with asyncio.TaskGroup() as tg:
            tg.create_task(fetch_orders())
    except* ConnectionError:
        pass


async def main():
    await run("except ConnectionError:", plain_connectionerror)
    await run("except Exception:  (gets the group)", plain_exception)
    await run("except* ConnectionError:", star_connectionerror)
    print(f"Python {sys.version.split()[0]}")

asyncio.run(main())
