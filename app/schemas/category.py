from pydantic import BaseModel


class CategoryBase(BaseModel):
    name: str
    type: str  # "income" or "expense"


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: str | None = None
    type: str | None = None


class CategoryRead(CategoryBase):
    id: int

    class Config:
        orm_mode = True
