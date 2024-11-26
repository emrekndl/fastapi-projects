from contextlib import asynccontextmanager

import uvicorn
from db import init_db
from fastapi import BackgroundTasks, FastAPI
from process import multiprocess_run


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(lifespan=lifespan)


async def execute_process():
    await multiprocess_run()


@app.get("/")
async def root(background_tasks: BackgroundTasks):
    background_tasks.add_task(execute_process)
    return {"message": "Multiple Process started."}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
