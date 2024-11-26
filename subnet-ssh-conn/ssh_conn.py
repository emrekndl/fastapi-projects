import asyncio
import logging

import paramiko

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# asyncssh alternatively for paramiko
def ssh_connect(
    ip: str, username: str, password: str, port: int = 22, timeout: int = 10
) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(ip, username=username, password=password, port=port, timeout=timeout)
    return client


def close_connection(client):
    client.close()
    return


def execute_command(client, command, timeout: int = 10) -> str:
    _, stdout, _ = client.exec_command(command, timeout=timeout)
    return stdout.read.decode("utf-8")


async def run(
    ip: str,
    username: str,
    password: str,
    command: str | None = "ping",
    timeout: int = 10,
    port: int = 22,
):
    looping = asyncio.get_running_loop()
    client = None
    try:
        # asyncio.to_thread() alternatively for run_in_executor
        client = await looping.run_in_executor(
            None, ssh_connect, ip, username, password, port, timeout
        )
        if command:
            result = await looping.run_in_executor(
                None, execute_command, client, command, timeout
            )
            logging.info(f"SSH Test command {command} for {ip} result: {result}")

    except Exception as e:
        logging.error(f"SSH Connection error for {ip}: {e}")
        return

    finally:
        if client:
            await looping.run_in_executor(None, close_connection, client)
