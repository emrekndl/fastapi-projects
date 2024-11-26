from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.category import (
    create_category,
    delete_category,
    get_all_categories,
    get_category_by_id,
    update_category,
)
from db.database import get_db
from schemas.schema import CategoryCreate

router = APIRouter(prefix="/api")


@router.post("/categories/", response_model=CategoryCreate)
async def create_new_category(
    category: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    return await create_category(db, category)


@router.put("/categories/{category_id}", response_model=CategoryCreate)
async def update_existing_category(
    category_id: int, category_data: CategoryCreate, db: AsyncSession = Depends(get_db)
):
    await update_category(db, category_id, category_data)
    return await get_category_by_id(db, category_id)


@router.delete("/categories/{category_id}")
async def delete_existing_category(
    category_id: int, db: AsyncSession = Depends(get_db)
):
    await delete_category(db, category_id)
    return {"message": "Category deleted successfully"}


@router.get("/categories/", response_model=list[CategoryCreate])
async def get_categories(db: AsyncSession = Depends(get_db)):
    return await get_all_categories(db)


@router.get("/categories/{category_id}", response_model=CategoryCreate)
async def get_category(category_id: int, db: AsyncSession = Depends(get_db)):
    return await get_category_by_id(db, category_id)
