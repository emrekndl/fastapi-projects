from sqlalchemy import update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from logfparse.db.models import ParseTask


async def get_task_running_status(task_id: int, db: AsyncSession):
    result = await db.execute(
        select(ParseTask.is_running).where(ParseTask.id == task_id)
    )
    running_status = result.scalar_one_or_none()

    if running_status is None:
        raise ValueError(f"Task with id {task_id} not found.")

    return running_status


async def set_task_running_status(
    task_id: int, running_status: bool, db: AsyncSession
) -> bool:
    try:
        await db.execute(
            update(ParseTask)
            .where(ParseTask.id == task_id)
            .values(is_running=running_status)
        )
        await db.commit()
    except Exception as e:
        raise e

    return True
