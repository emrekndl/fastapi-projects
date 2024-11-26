from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from db.database import init_db
from routers import category_api, product_api


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


def get_app(lifespan=lifespan):
    app = FastAPI(lifespan=lifespan)
    app.include_router(product_api.router)
    app.include_router(category_api.router)

    return app


app = get_app(lifespan=lifespan)


# @app.on_event("startup")
# async def on_startup():
#     await init_db()


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000)
