import asyncio
from datetime import datetime, timedelta
from io import StringIO
from typing import Annotated, Callable, TypedDict

import paramiko
from loguru import logger


class SSHOptions(TypedDict, total=False):
    host: Annotated[str, "SSH server hostname or IP address"]
    port: Annotated[int, "SSH server port"]
    username: Annotated[str, "SSH username"]
    password: Annotated[str, "SSH password"]


# NOTE: paramiko instead of asyncssh usable.
class SSHClient:
    def __init__(self, options: SSHOptions) -> None:
        # TODO: options default values will be getting from config, env.
        self.host = options.get("host", "localhost")
        self.port = options.get("port", 22)
        self.username = options.get("username", "testuser")
        self.password = options.get("password", "testpassword")
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    def connect(self, timeout: int = 10) -> None:
        try:
            self.client.connect(
                self.host,
                port=self.port,
                username=self.username,
                password=self.password,
                timeout=timeout,
            )
        except Exception as e:
            logger.error(f"SSH connection failed: {e}")
            raise ConnectionError(f"SSH connection failed: {e}")

    def execute_command(self, command: str, timeout: int = 10) -> str:
        _, stdout, stderr = self.client.exec_command(command, timeout=timeout)
        output = stdout.read().decode("utf-8")
        error = stderr.read().decode("utf-8")
        if error:
            logger.error(f"Command execution failed: {error}")
            raise Exception(f"Command execution failed: {error}")
        return output

    async def stream_command(
        self, command: str, callback: Callable, timeout: int
    ) -> None:
        channel = self.client.get_transport().open_session()
        channel.exec_command(command)
        start_time = datetime.now()
        buffer = StringIO()

        try:
            while True:
                if channel.recv_ready():
                    buffer.write(channel.recv(1024).decode("utf-8"))
                if datetime.now() - start_time >= timedelta(seconds=timeout):
                    break

            if buffer.tell() > 0:
                # buffer.seek(0)
                await callback(buffer.getvalue())
                await asyncio.sleep(1)
        finally:
            buffer.close()
            channel.close()

    def is_connected(self) -> bool:
        transport = self.client.get_transport()
        if not transport or not transport.is_active():
            return False
        return True

    def close(self) -> None:
        self.client.close()
