import asyncio

from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from logfparse.db.models import ParseTask
from logfparse.service.log_parser_service import LogOptions, execute
from logfparse.settings import settings
from logfparse.utils.ssh_client import SSHOptions
from logfparse.utils.task_status import set_task_running_status


async def log_parser_task(
    task_id: int, db: AsyncSession, stop_event: asyncio.Event
) -> bool:
    try:
        task_options = await db.execute(
            select(ParseTask).where(ParseTask.id == task_id)
        )
        task_options = task_options.scalars().one()

        log_options = LogOptions(
            ssh_client=SSHOptions(
                # TODO: ssh info will be getting from db.
                host=settings.SSH_HOST,
                port=settings.SSH_PORT,
                username=settings.SSH_USERNAME,
                password=settings.SSH_PASSWORD,
            ),
            log_file=str(task_options.log_file_path),
            parse_template=str(task_options.parse_template_path),
            timeout=int(task_options.command_run_time),
            command=str(task_options.run_command),
        )
        logger.info(
            f"Task {task_options.task_name} started with options: {log_options}"
        )
        await execute(log_options, db, stop_event)
    except BaseException as e:
        await set_task_running_status(task_id, False, db)
        logger.error(f"Task {task_options.task_name} failed with error: {e}")
        return False
    return True
