import aiosqlite
from pydantic import BaseModel

DATABASE_URL = "processes.db"


async def get_db():
    conn = await aiosqlite.connect(DATABASE_URL)
    return conn


async def init_db():
    conn = await get_db()
    try:
        await conn.execute(
            """
            CREATE TABLE IF NOT EXISTS process_status (
                process_id INTEGER PRIMARY KEY,
                status TEXT,
                cpu_usage REAL,
                memory_usage REAL
            )
            """
        )
        await conn.commit()
    finally:
        await conn.close()


class ProcessStatus(BaseModel):
    process_id: int
    status: str
    cpu_usage: float
    memory_usage: float

    class Config:
        from_attributes = True


async def update_or_create_process_status(process_status: ProcessStatus):
    conn = await get_db()
    try:
        await conn.execute(
            """
            INSERT OR REPLACE INTO process_status (process_id, status, cpu_usage, memory_usage)
            VALUES (?, ?, ?, ?)
            """,
            (
                process_status.process_id,
                process_status.status,
                process_status.cpu_usage,
                process_status.memory_usage,
            ),
        )
        await conn.commit()
    finally:
        await conn.close()
