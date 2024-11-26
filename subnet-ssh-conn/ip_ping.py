import asyncio
import logging

from icmplib import async_ping
from netaddr import IPNetwork

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


# NOTE: Just use reguler ping method and with asyncio.to_thread() method
async def do_ping(address: str, count: int = 1, timeout: int = 3) -> bool:
    try:
        # NOTE: privileged=True is needed for sudo(root) on linux
        # host = await async_ping(address, timeout=timeout, count=count)
        host = await async_ping(address, timeout=timeout, count=count, privileged=False)
        if host.is_alive:
            logging.info(f"{host.address} active.")
            return True

        logging.info(f"{host.address} inactive.")
        return False

    except Exception as e:
        logging.error(f"{address} - Ping error: {e}")
        return False


def get_chunk_size(total_ips: int) -> int:
    if total_ips <= 1000:
        return max(50, total_ips // 20)
    elif total_ips <= 10000:
        return max(100, total_ips // 20)
    else:
        return max(500, total_ips // 66)  # 65


async def process_chunk(chunk: list) -> list:
    ping_tasks = [do_ping(str(ip)) for ip in chunk]
    results = await asyncio.gather(*ping_tasks)
    return results


async def get_active_ip(ip_str: str) -> set:
    # ip_str = "172.18.0.1/28"
    # ip_str = "172.29.0.1/16"

    ip = IPNetwork(ip_str)
    ip_size = ip.size
    active_ips = set()

    # inactive_ips = set()

    logging.info(
        f"""
        ip network : {ip.network}
        ip broadcast : {ip.broadcast}
        ip version : {ip.version}
        ip netmask : {ip.netmask}
        ip prefixlen : {ip.prefixlen}
        ip hostmask : {ip.hostmask}
        ip size : {ip_size}"""
    )

    # NOTE: ulimit -a increase or use semaphore
    chunck_size = get_chunk_size(ip_size)

    logging.info(f"Chunck size: {chunck_size}")
    ip_chunks = [list(ip)[i : i + chunck_size] for i in range(0, ip_size, chunck_size)]

    task = [process_chunk(chunk) for chunk in ip_chunks]
    results = await asyncio.gather(*task)

    for result, chunk in zip(results, ip_chunks):
        for i, res in zip(chunk, result):
            if res:
                active_ips.add(str(i))
            else:
                # inactive_ips.add(str(ip[i]))
                continue
    logging.info(f"Active IPs ({len(active_ips)}): {list(active_ips)}")
    # logging.info(f"Inactive IPs ({len(inactive_ips)}): {list(inactive_ips)}")

    return active_ips
