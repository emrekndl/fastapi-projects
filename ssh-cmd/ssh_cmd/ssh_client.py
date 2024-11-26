import asyncssh


class SSHClient:
    def __init__(self, host: str, username: str, password: str, port: int = 22):
        self.host = host
        self.username = username
        self.password = password
        self.port = port

    async def run_ssh_command(self, command: str) -> asyncssh.BytesOrStr | None:
        try:
            async with asyncssh.connect(
                self.host,
                username=self.username,
                password=self.password,
                port=self.port,
            ) as conn:
                result = await conn.run(command)
                return result.stdout
        except Exception as e:
            return f"Error connecting to {self.host}: {str(e)}"
