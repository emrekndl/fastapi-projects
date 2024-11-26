from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import Category
from schemas.schema import CategoryCreate


async def create_category(db: AsyncSession, category: CategoryCreate):
    db_category = Category(**category.dict())
    db.add(db_category)
    await db.commit()
    return db_category


async def update_category(
    db: AsyncSession, category_id: int, category_data: CategoryCreate
):
    await db.execute(
        update(Category)
        .where(Category.id == category_id)
        .values(**category_data.dict())
    )
    await db.commit()


async def delete_category(db: AsyncSession, category_id: int):
    await db.execute(delete(Category).where(Category.id == category_id))
    await db.commit()


async def get_all_categories(db: AsyncSession):
    result = await db.execute(select(Category))
    return result.scalars().all()


async def get_category_by_id(db: AsyncSession, category_id: int):
    result = await db.execute(select(Category).where(Category.id == category_id))
    return result.scalar()
