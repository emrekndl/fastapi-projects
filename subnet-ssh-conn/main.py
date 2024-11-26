import asyncio
import logging

import uvicorn
from fastapi import BackgroundTasks, FastAPI

from ip_ping import get_active_ip
from ssh_conn import run

app = FastAPI(debug=True)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


async def execute_task():
    logging.info("Active IP task started...")
    # NOTE: ip should be getting from api post request
    active_ips: set = await get_active_ip("172.29.0.1/16")
    if not active_ips:
        logging.error("No active IP found.")
        return
        # raise Exception("No active IP found.")
    logging.info("SSH Connection task started...")
    # NOTE: username and password should be getting from database or other source
    tasks = [run(str(ip), "test_user", "test_pass") for ip in active_ips]
    await asyncio.gather(*tasks)


@app.get("/")
async def root(background_tasks: BackgroundTasks):
    background_tasks.add_task(execute_task)
    return {"message": "Task is started."}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
