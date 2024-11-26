from typing import Optional

from pydantic import BaseModel


class CategoryCreate(BaseModel):
    name: str
    description: Optional[str] = None

    class Config:
        # orm_mode = True
        from_attributes = True


class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

    class Config:
        # orm_mode = True
        from_attributes = True
