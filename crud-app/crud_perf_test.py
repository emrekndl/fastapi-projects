import asyncio
import time

from faker import Faker
from sqlalchemy.ext.asyncio import AsyncSession

from crud.category import create_category
from crud.product import create_products, delete_product, update_product
from db.database import get_db
from schemas.schema import CategoryCreate, ProductCreate

fake = Faker()


async def generate_test_data(db: AsyncSession, count: int = 100_000):
    products = [
        ProductCreate(
            name=fake.name(),
            description=fake.text(),
            price=round(fake.random_number(digits=5), 2),
            category_id=fake.random_int(min=1, max=10),
        )
        for _ in range(count)
    ]
    categories = [
        CategoryCreate(
            name=fake.name(),
            description=fake.text(),
        )
        for _ in range(10)
    ]
    for category in categories:
        await create_category(db, category)
    await create_products(db, products)
    # await create_category(db, categories)


async def test_insert_performance():
    async with get_db() as db:
        start_time = time.time()
        await generate_test_data(db)
        end_time = time.time()
        print(
            f"100,000 record added, time : {time.strftime('%H:%M:%S', time.gmtime(end_time - start_time))}"
        )


async def test_update_and_delete_performance():
    async with get_db() as db:
        start_update = time.time()
        for i in range(1, 100_001):
            await update_product(
                db,
                product_id=i,
                product_data=ProductCreate(
                    name=fake.name(),
                    description=fake.text(),
                    price=round(fake.random_number(digits=5), 2),
                    category_id=fake.random_int(min=1, max=10),
                ),
            )
        end_update = time.time()
        print(
            f"100,000 record updated, time : {time.strftime('%H:%M:%S', time.gmtime(end_update - start_update))}"
        )

        start_delete = time.time()
        for i in range(1, 100_001):
            await delete_product(db, product_id=i)
        end_delete = time.time()
        print(
            f"100,000 record deleted, time : {time.strftime('%H:%M:%S', time.gmtime(end_delete - start_delete))}"
        )


async def main():
    await test_insert_performance()
    await test_update_and_delete_performance()


if __name__ == "__main__":
    asyncio.run(main())
