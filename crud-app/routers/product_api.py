from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from crud.product import (
    create_products,
    delete_product,
    get_all_products,
    get_product_by_id,
    update_product,
)
from db.database import get_db
from schemas.schema import ProductCreate

router = APIRouter(prefix="/api")


@router.post("/products/", response_model=list[ProductCreate])
async def create_new_products(
    products: list[ProductCreate], db: AsyncSession = Depends(get_db)
):
    return await create_products(db, products)


@router.put("/products/{product_id}", response_model=ProductCreate)
async def update_existing_product(
    product_id: int, product_data: ProductCreate, db: AsyncSession = Depends(get_db)
):
    await update_product(db, product_id, product_data)
    return await get_product_by_id(db, product_id)


@router.delete("/products/{product_id}")
async def delete_existing_product(product_id: int, db: AsyncSession = Depends(get_db)):
    await delete_product(db, product_id)
    return {"message": "Product deleted successfully"}


@router.get("/products/", response_model=list[ProductCreate])
async def get_products(db: AsyncSession = Depends(get_db)):
    return await get_all_products(db)


@router.get("/products/{product_id}", response_model=ProductCreate)
async def get_product(product_id: int, db: AsyncSession = Depends(get_db)):
    return await get_product_by_id(db, product_id)
