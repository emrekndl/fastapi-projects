from fastapi import HTTPException, status
from loguru import logger
from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from logfparse.db.models import DHCPRequestData
from logfparse.schemas.schema import (
    DHCPRequestDataCreate,
    DHCPRequestDataRead,
    DHCPRequestDataUpdate,
)
from logfparse.utils.foo_bar_baz import convert_to_read_model


async def create_dhcp_request_data(
    dhcp_request_data: DHCPRequestDataCreate, db: AsyncSession
) -> DHCPRequestDataRead:
    try:
        db_dhcp_request_data = DHCPRequestData(**dhcp_request_data.model_dump())
        db.add(db_dhcp_request_data)
        await db.commit()
        await db.refresh(db_dhcp_request_data)
        return convert_to_read_model(db_dhcp_request_data, DHCPRequestDataRead)
    except Exception as e:
        await db.rollback()
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def get_dhcp_request_data_by_id(
    dhcp_request_data_id: int, db: AsyncSession
) -> DHCPRequestDataRead:
    try:
        result = await db.execute(
            select(DHCPRequestData).where(DHCPRequestData.id == dhcp_request_data_id)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    if result:
        return convert_to_read_model(result.scalars().one(), DHCPRequestDataRead)
    else:
        logger.error(f"Not Found with id: {dhcp_request_data_id}")
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Not Found with id: {dhcp_request_data_id}",
        )


async def get_all_dhcp_request_data(db: AsyncSession) -> list[DHCPRequestDataRead]:
    try:
        result = await db.execute(select(DHCPRequestData))
    except Exception as e:
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
    return [
        convert_to_read_model(item, DHCPRequestDataRead)
        for item in result.scalars().all()
    ]

    # return list(
    #     map(
    #         lambda x: convert_to_read_model(x, DHCPRequestDataRead),
    #         result.scalars().all(),
    #     )
    # )
    # return map(convert_to_read_model, result.scalars().all())


async def update_dhcp_request_data(
    dhcp_request_data_id: int,
    dhcp_request_data: DHCPRequestDataUpdate,
    db: AsyncSession,
) -> DHCPRequestDataRead:
    try:
        result = await db.execute(
            select(DHCPRequestData).where(DHCPRequestData.id == dhcp_request_data_id)
        )
        db_dhcp_request_data = result.scalars().first()
        if db_dhcp_request_data is None:
            logger.error(f"Not Found with id: {dhcp_request_data_id}")
            raise HTTPException(status_code=404, detail="Not Found")
        result = (
            update(DHCPRequestData)
            .where(DHCPRequestData.id == dhcp_request_data_id)
            .values(dhcp_request_data.model_dump())
        )
        await db.execute(result)
        await db.commit()
        return convert_to_read_model(result, DHCPRequestDataRead)
    except Exception as e:
        await db.rollback()
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


async def delete_dhcp_request_data(dhcp_request_data_id: int, db: AsyncSession) -> bool:
    try:
        result = await db.execute(
            select(DHCPRequestData).where(DHCPRequestData.id == dhcp_request_data_id)
        )
        db_dhcp_request_data = result.scalars().first()
        if db_dhcp_request_data is None:
            logger.error(f"Not Found with id: {dhcp_request_data_id}")
            raise HTTPException(status_code=404, detail="Not Found")
        await db.execute(
            delete(DHCPRequestData).where(DHCPRequestData.id == dhcp_request_data_id)
        )
        await db.commit()
        return True
    except Exception as e:
        await db.rollback()
        logger.error(f"Exception: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )
