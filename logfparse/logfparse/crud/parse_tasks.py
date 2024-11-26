from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from logfparse.db.models import ParseTask
from logfparse.schemas.schema import (
    ParseTaskCreate,
    ParseTaskRead,
    ParseTaskUpdate,
)
from logfparse.utils.foo_bar_baz import convert_to_read_model


# task_filter: ParseTaskReadFilter
async def get_all_parse_tasks(db: AsyncSession) -> list[ParseTaskRead]:
    try:
        # query = task_filter.filter(select(ParseTask))
        result = await db.execute(select(ParseTask))
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return list(
        map(
            lambda x: convert_to_read_model(x, ParseTaskRead),
            result.scalars().all(),
        )
    )


async def get_parse_task_by_id(parse_task_id: int, db: AsyncSession) -> ParseTaskRead:
    try:
        result = await db.execute(
            select(ParseTask).where(ParseTask.id == parse_task_id)
        )
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    if result:
        return convert_to_read_model(result.scalars().one(), ParseTaskRead)
    else:
        logger.error(f"Not Found with id: {parse_task_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not Found with id: {parse_task_id}",
        )


async def create_parse_task(
    parse_task: ParseTaskCreate, db: AsyncSession
) -> ParseTaskRead:
    try:
        db_parse_task = ParseTask(**parse_task.model_dump())
        db.add(db_parse_task)
        await db.commit()
        await db.refresh(db_parse_task)
        return convert_to_read_model(db_parse_task, ParseTaskRead)
    except Exception as e:
        logger.error(f"Exception: {e}")
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def delete_parse_task(parse_task_id: int, db: AsyncSession) -> bool:
    try:
        result = await db.execute(
            select(ParseTask).where(ParseTask.id == parse_task_id)
        )
        db_parse_task = result.scalars().first()
        if db_parse_task is None:
            logger.error(f"Not Found with id: {parse_task_id}")
            raise HTTPException(status_code=404, detail="Not Found")
        await db.execute(delete(ParseTask).where(ParseTask.id == parse_task_id))
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def update_parse_task(
    parse_task_id: int, parse_task: ParseTaskUpdate, db: AsyncSession
) -> ParseTaskRead:
    try:
        result = await db.execute(
            select(ParseTask).where(ParseTask.id == parse_task_id)
        )
        db_parse_task = result.scalars().first()
        if db_parse_task is None:
            logger.error(f"Not Found with id: {parse_task_id}")
            raise HTTPException(status_code=404, detail="Not Found")
        result = (
            update(ParseTask)
            .where(ParseTask.id == parse_task_id)
            .values(parse_task.model_dump())
        )
        await db.execute(result)
        await db.commit()
        return convert_to_read_model(result, ParseTaskRead)
    except Exception as e:
        await db.rollback()
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
