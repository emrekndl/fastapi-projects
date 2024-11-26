from sqlalchemy import delete, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from db.models import Product
from schemas.schema import ProductCreate


async def create_products(db: AsyncSession, products: list[ProductCreate]):
    db_products = [Product(**product.dict()) for product in products]
    db.add_all(db_products)
    await db.commit()
    return db_products


async def update_product(
    db: AsyncSession, product_id: int, product_data: ProductCreate
):
    await db.execute(
        update(Product).where(Product.id == product_id).values(**product_data.dict())
    )
    await db.commit()


async def delete_product(db: AsyncSession, product_id: int):
    await db.execute(delete(Product).where(Product.id == product_id))
    await db.commit()


async def get_all_products(db: AsyncSession):
    result = await db.execute(select(Product))
    return result.scalars().all()


async def get_product_by_id(db: AsyncSession, product_id: int):
    result = await db.execute(select(Product).where(Product.id == product_id))
    return result.scalar()
