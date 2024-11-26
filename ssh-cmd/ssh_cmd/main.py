import logging

import uvicorn
from fastapi import BackgroundTasks, FastAPI
from network_scanner import NetworkScanner
from pydantic import BaseModel

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

app = FastAPI()


class CommandRequest(BaseModel):
    network: str
    command: str
    username: str
    password: str


async def ssh_cmd_run(request: CommandRequest) -> None:
    # user and password should be encrypted and getted from database
    scanner = NetworkScanner(request.network, request.username, request.password)
    results = await scanner.scan_and_run_command(request.command)
    for result in results:
        logging.info(result)


@app.post("/execute-command/")
async def execute_command(
    background_tasks: BackgroundTasks, request: CommandRequest
) -> dict:
    print(request)
    background_tasks.add_task(ssh_cmd_run, request)
    return {
        "status": f"'{request.command}' command is running for {request.network} subnets"
    }


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8001)

"""
{
    "network": "172.18.0/29",
    "command": "ip a",
    "username": "root",
    "password": "toor"
}
"""
