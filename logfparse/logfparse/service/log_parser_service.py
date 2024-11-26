import asyncio
from typing import Any, Dict, TypedDict

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from textfsm import TextFSM, re

from logfparse.db.models import DHCPRequestData
from logfparse.schemas.schema import DHCPRequestDataCreate
from logfparse.utils.foo_bar_baz import convert_parsed_data_to_schema
from logfparse.utils.ssh_client import SSHClient, SSHOptions


class LogOptions(TypedDict, total=False):
    ssh_client: SSHOptions
    log_file: str
    parse_template: str
    command: str
    timeout: int


class LogParserService:
    def __init__(self, log_options: LogOptions, db: AsyncSession):
        # TODO: log_options default values will be getting from config, env.
        self.ssh_client = SSHClient(log_options.get("ssh_client", {}))
        self.log_file = log_options.get("log_file", "/var/log/syslog")
        self.parse_template = log_options.get(
            "parse_template", "utils/parser_templates/dhcp_request.template"
        )
        self.timeout = log_options.get("timeout", 300)
        self.command = log_options.get("command", "tail -f /var/log/syslog")
        self.db = db

    async def listen_for_logs(self) -> None:
        if not self.ssh_client.is_connected():
            self.ssh_client.connect()

        try:
            await self.ssh_client.stream_command(
                command=f"{self.command} { self.log_file}",
                callback=self.parse_and_store_logs,
                timeout=self.timeout,
            )
            await asyncio.sleep(1)
        except Exception as e:
            logger.error(f"Exception: {e}. Reconnecting for in 10 seconds...")
            print(f"Exception: {e}. Reconnecting for in 10 seconds...")
            await asyncio.sleep(10)
        finally:
            if self.ssh_client.is_connected():
                self.ssh_client.close()

    async def parse_and_store_logs(self, logs: str) -> None:
        blocked_logs = re.split(r"\n-{2,}\n", logs)
        for block in blocked_logs:
            parsed_data = self.parse_logs(block.strip())
            # self.print_logs(parsed_data)
            # TODO:
            await self.store_to_db(parsed_data)

    # NOTE: this process will be multiprocessed, it will be more efficient, cpu bound...
    def parse_logs(self, logs: str) -> list[Dict[str, Any]]:
        with open(self.parse_template, "r") as template_file:
            template = TextFSM(template_file)
            parsed_data = template.ParseText(logs)
            return parsed_data

    async def check_client_id(self, client_id: str) -> bool:
        result = await self.db.execute(
            select(DHCPRequestData).where(
                DHCPRequestData.client_identifier == client_id
            )
        )
        return not result.scalars().first()

    async def store_to_db(self, parsed_data: list) -> None:
        for data in parsed_data:
            # ??? parsed data list convert to tuple for duplicate entry?
            if await self.check_client_id(data[0]):
                schema_instance = convert_parsed_data_to_schema(
                    data, DHCPRequestDataCreate
                )
                # TODO: Converting the schema isntance into a model instance should be a more general structure. For different types of tasks.
                model_instance = DHCPRequestData(**schema_instance.model_dump())
                # try:
                self.db.add(model_instance)
                await self.db.commit()
                logger.info(f"Added entry: {model_instance}")
                # except IntegrityError as e:
                #     logger.error(
                #         f"IntegrityError: Duplicate entry {model_instance} -- {e}"
                #     )
                #     await self.db.rollback()
            else:
                logger.debug(f"Duplicate entry {data}")

    def print_logs(self, parsed_data: list) -> None:
        for data in parsed_data:
            logger.debug("----------------------")
            logger.debug(f"ClientIdentifier: {data[0]}")
            logger.debug(f"RequestIPAddress: {data[1]}")
            logger.debug(f"VendorClassIdentifier: {data[2]}")
            logger.debug(f"HostName: {data[3]}")
            logger.debug("----------------------")


async def execute(
    log_options: LogOptions, db: AsyncSession, stop_event: asyncio.Event
) -> None:
    log_parser_service = LogParserService(log_options, db)
    while not stop_event.is_set():
        await log_parser_service.listen_for_logs()
