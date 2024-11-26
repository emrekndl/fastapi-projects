import asyncio
from typing import List

from netaddr import IPNetwork
from ssh_client import SSHClient


class NetworkScanner:
    def __init__(self, network: str, username: str, password: str):
        self.network = IPNetwork(network)
        self.username = username
        self.password = password

    async def scan_and_run_command(self, command: str) -> List[str]:
        tasks = []
        port = 0
        # NOTE: Are we just trying to connect to the IP list or subnets?
        for ip in self.network:
            client = SSHClient(
                str(ip), self.username, self.password, port=f"300{(port := port+1)}"
            )
            tasks.append(client.run_ssh_command(command))

        results = await asyncio.gather(*tasks)
        return results
