import sys
from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI
from loguru import logger

from logfparse.db.database import engine, init_db
from logfparse.routers import dhcp_request_data_api, parse_task_api

logger.remove()
logger.add(sys.stdout, level="INFO")


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await engine.dispose()


def get_app(lifespan=lifespan):
    app = FastAPI(lifespan=lifespan, title="LogfParse", version="0.0.1", debug=True)
    app.include_router(dhcp_request_data_api.dhcp_data_router)
    app.include_router(parse_task_api.parse_task_router)

    return app


app = get_app(lifespan=lifespan)


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
