from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from logfparse.crud.dhcp_request_data import (
    create_dhcp_request_data,
    delete_dhcp_request_data,
    get_all_dhcp_request_data,
    get_dhcp_request_data_by_id,
    update_dhcp_request_data,
)
from logfparse.db.database import get_db
from logfparse.schemas.schema import (
    DHCPRequestDataCreate,
    DHCPRequestDataRead,
    DHCPRequestDataUpdate,
)

dhcp_data_router = APIRouter(prefix="/api")


@dhcp_data_router.get("/data", response_model=list[DHCPRequestDataRead])
async def get_data(db: AsyncSession = Depends(get_db)) -> list[DHCPRequestDataRead]:
    return await get_all_dhcp_request_data(db=db)


@dhcp_data_router.get("/data/{data_id}", response_model=DHCPRequestDataRead)
async def get_data_by_id(
    data_id: int, db: AsyncSession = Depends(get_db)
) -> DHCPRequestDataRead:
    return await get_dhcp_request_data_by_id(dhcp_request_data_id=data_id, db=db)


@dhcp_data_router.post("/data", response_model=DHCPRequestDataRead)
async def create_data(
    dhcp_request_data: DHCPRequestDataCreate,
    db: AsyncSession = Depends(get_db),
) -> DHCPRequestDataRead:
    return await create_dhcp_request_data(dhcp_request_data=dhcp_request_data, db=db)


@dhcp_data_router.put("/data/{data_id}", response_model=DHCPRequestDataRead)
async def update__data(
    dhcp_request_data_id: int,
    dhcp_request_data: DHCPRequestDataUpdate,
    db: AsyncSession = Depends(get_db),
) -> DHCPRequestDataRead:
    return await update_dhcp_request_data(
        dhcp_request_data_id=dhcp_request_data_id,
        dhcp_request_data=dhcp_request_data,
        db=db,
    )


@dhcp_data_router.delete("/data/{data_id}")
async def delete_data(
    dhcp_request_data_id: int, db: AsyncSession = Depends(get_db)
) -> bool:
    return await delete_dhcp_request_data(
        dhcp_request_data_id=dhcp_request_data_id, db=db
    )
