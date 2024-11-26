import uvicorn
from fastapi import FastAPI
from fastapi.background import BackgroundTasks
from ping import do_multiping

# NOTE: ORJSON library alternatively can be used instead of the default JSON for faster performance
# app = FastAPI(default_response_class=ORJSONResponse)
app = FastAPI()


async def execute():
    list_of_addrs = [
        "8.8.8.8",
        "8.8.4.4",
        "1.1.1.1",
        "1.0.0.1",
        "127.0.0.1",
        "237.84.2.178",
        "38.0.101.76",
        "192.168.1.1",
    ] * 64
    await do_multiping(list_of_addrs)


@app.get("/")
async def root(background_tasks: BackgroundTasks):
    background_tasks.add_task(execute)
    return {"message": "Ping Connection Test Started."}


if __name__ == "__main__":
    uvicorn.run(app="main:app", host="0.0.0.0", port=8000, reload=True)
