"""Control for the lost-error check: asyncio does log an error from a plain task that nobody
awaits ("Task exception was never retrieved"), so the absence of that message in the gather
run means the error really was dropped, not that such messages are hidden."""
import asyncio, gc


async def boom():
    raise TimeoutError("user service timed out")


async def main():
    t = asyncio.create_task(boom())
    await asyncio.sleep(0.1)
    del t
    gc.collect()
    await asyncio.sleep(0.05)

asyncio.run(main())
