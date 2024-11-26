import asyncio

from logfparse.db.database import get_db

# from logfparse.utils.log_listener import LogListener, LogOptions
from logfparse.service.log_parser_service import LogOptions, execute
from logfparse.utils.ssh_client import SSHOptions


async def run() -> None:
    log_options = LogOptions(
        ssh_client=SSHOptions(
            host="127.0.0.1",
            port=2222,
            username="root",
            password="toor",
        ),
        log_file="/root/stream_demo.log",
        parse_template="logfparse/utils/parser_templates/dhcp_request.template",
        timeout=30,
        command="tail -f",
    )
    db = next(get_db())
    await execute(log_options, db)

    print("Listening for logs...\n")


def main():
    asyncio.run(run())


if __name__ == "__main__":
    main()
