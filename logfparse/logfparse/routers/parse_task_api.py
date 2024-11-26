import asyncio
from typing import Dict

from fastapi import APIRouter, Depends
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from logfparse.crud.parse_tasks import (
    create_parse_task,
    delete_parse_task,
    get_all_parse_tasks,
    get_parse_task_by_id,
    update_parse_task,
)
from logfparse.db.database import get_db
from logfparse.schemas.schema import (
    ParseTaskCreate,
    ParseTaskRead,
    ParseTaskUpdate,
)
from logfparse.tasks.log_parser_task import log_parser_task
from logfparse.utils.task_status import get_task_running_status, set_task_running_status

parse_task_router = APIRouter(prefix="/api")

stop_signals: Dict[int, asyncio.Event] = {}


@parse_task_router.post("/tasks", response_model=ParseTaskRead)
async def create_task(
    parse_task: ParseTaskCreate, db: AsyncSession = Depends(get_db)
) -> ParseTaskRead:
    return await create_parse_task(parse_task=parse_task, db=db)


# parse_task_filter: ParseTaskReadFilter = FilterDepends(ParseTaskReadFilter),
@parse_task_router.get("/tasks", response_model=list[ParseTaskRead])
async def get_task_all(
    db: AsyncSession = Depends(get_db),
) -> list[ParseTaskRead]:
    return await get_all_parse_tasks(db=db)


@parse_task_router.get("/tasks/{task_id}", response_model=ParseTaskRead)
async def get_task_by_id(
    task_id: int, db: AsyncSession = Depends(get_db)
) -> ParseTaskRead:
    return await get_parse_task_by_id(parse_task_id=task_id, db=db)


@parse_task_router.put("/tasks/{task_id}", response_model=ParseTaskRead)
async def update_task(
    task_id: int,
    parse_task: ParseTaskUpdate,
    db: AsyncSession = Depends(get_db),
) -> ParseTaskRead:
    return await update_parse_task(parse_task_id=task_id, parse_task=parse_task, db=db)


@parse_task_router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, db: AsyncSession = Depends(get_db)) -> bool:
    return await delete_parse_task(parse_task_id=task_id, db=db)


# We can use celery, rabbitmq instead of background tasks as Asyncio (or Fastfapi Background task).
@parse_task_router.get("/tasks/{task_id}/start")
async def start_task(
    task_id: int,
    db: AsyncSession = Depends(get_db),
):
    running = await get_task_running_status(task_id=task_id, db=db)
    if running:
        logger.info(f"Task {task_id} is already running.")
        return {"message": f"Task {task_id} is already running."}

    result = await set_task_running_status(task_id=task_id, running_status=True, db=db)
    if not result:
        logger.info(f"Task {task_id} not started.")
        return {"message": f"Task {task_id} not started."}

    stop_signals[task_id] = asyncio.Event()
    _ = asyncio.create_task(
        log_parser_task(task_id=task_id, db=db, stop_event=stop_signals[task_id])
    )

    logger.info(f"Task {task_id} started.")
    return {"message": f"Task {task_id} started."}


@parse_task_router.get("/tasks/{task_id}/stop")
async def stop_task(task_id: int, db: AsyncSession = Depends(get_db)):
    running = await get_task_running_status(task_id=task_id, db=db)
    if not running:
        logger.info(f"Task {task_id} is not running.")
        return {"message": f"Task {task_id} is not running."}

    stop_signals[task_id].set()
    result = await set_task_running_status(task_id=task_id, running_status=False, db=db)
    if not result:
        logger.info(f"Task {task_id} not stopped.")
        return {"message": f"Task {task_id} not stopped."}
    logger.info(f"Task {task_id} stopped.")
    return {"message": f"Task {task_id} stopped."}
