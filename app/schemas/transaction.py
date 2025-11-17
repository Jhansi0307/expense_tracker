from datetime import datetime

from pydantic import BaseModel


class TransactionBase(BaseModel):
    amount: float
    type: str  # "income" or "expense"
    description: str | None = None
    date: datetime | None = None
    category_id: int | None = None


class TransactionCreate(TransactionBase):
    pass


class TransactionUpdate(BaseModel):
    amount: float | None = None
    type: str | None = None
    description: str | None = None
    date: datetime | None = None
    category_id: int | None = None


class TransactionRead(TransactionBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
