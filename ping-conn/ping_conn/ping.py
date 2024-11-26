import asyncio
import logging
import time

from icmplib import async_multiping

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

RUN_TIME_MULTPING = 10


async def multiping(
    addrs: list[str],
    count: int = 2,
    timeout: int = 2,
    concurrent_tasks=400,
    privileged=False,
) -> list:
    return await async_multiping(
        addrs,
        count=count,
        timeout=timeout,
        concurrent_tasks=concurrent_tasks,
        privileged=privileged,
    )


def inactive_pings_log(addrs_list: list) -> int:
    inactive_len: int = 0
    for addr in addrs_list:
        if not addr.is_alive:
            inactive_len += 1
            logging.info(f"{addr.address}: is not active.")

    return inactive_len


# NOTE: uvloop library alternatively can be used instead of the default asyncio event loop
async def do_multiping(addrs_list: list[str]):
    while True:
        start_time = time.time()
        ping_results = await multiping(addrs_list)
        # Only checks inactive addresss pings
        inactive_pings_len = inactive_pings_log(ping_results)
        end_time = time.time()
        logging.info(f"Multiping finished in {(end_time - start_time):.2f} seconds")
        logging.info(
            f"Average time: {(end_time - start_time) / len(addrs_list):.2f} seconds"
        )
        logging.info(f"Total pinged: {len(addrs_list)}")
        logging.info(f"Total inactive pings: {inactive_pings_len}")

        await asyncio.sleep(RUN_TIME_MULTPING)
