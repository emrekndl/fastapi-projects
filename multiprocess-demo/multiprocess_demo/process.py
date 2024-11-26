import asyncio
import logging
from concurrent.futures import ProcessPoolExecutor
from time import sleep

import psutil
import uvloop
from db import ProcessStatus, update_or_create_process_status

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


def run_process(process_id):
    cpu_usage = 0
    memory_usage = 0
    p = psutil.Process()

    process_task()

    while p.is_running():
        cpu_usage = p.cpu_percent(interval=1)
        memory_usage = p.memory_info().rss / (1024 * 1024)  # MB

        asyncio.run(
            update_process_status(process_id, cpu_usage, memory_usage, "Running")
        )

        logging.info(
            f"Process ID: {process_id}, Status: Running, CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage} MB"
        )

        sleep(1)

    asyncio.run(update_process_status(process_id, cpu_usage, memory_usage, "Finished"))

    logging.info(
        f"Process ID: {process_id}, Status: Finished, CPU Usage: {cpu_usage}%, Memory Usage: {memory_usage} MB"
    )


def process_task():
    sum(i * i for i in range(100))
    # sum(i * i for i in range(1000000))


async def update_process_status(process_id, cpu_usage, memory_usage, status):
    process_status = ProcessStatus(
        process_id=process_id,
        status=status,
        cpu_usage=cpu_usage,
        memory_usage=memory_usage,
    )
    await update_or_create_process_status(process_status)


# async def start_process_in_executor(executor, process_id):
#     loop = asyncio.get_event_loop()
#     await loop.run_in_executor(executor, run_process, process_id)


async def start_process_with_timeout(executor, process_id, timeout=60):
    loop = asyncio.get_event_loop()
    try:
        await asyncio.wait_for(
            loop.run_in_executor(executor, run_process, process_id), timeout
        )
    except asyncio.TimeoutError:
        print(f"Process {process_id} timed out.")


async def multiprocess_run():
    executor = ProcessPoolExecutor(max_workers=10)

    tasks = []
    for i in range(100):
        # for i in range(1000):
        task = asyncio.create_task(start_process_with_timeout(executor, i, timeout=10))
        tasks.append(task)

    await asyncio.gather(*tasks)
