from pydantic import BaseModel
from typing import List


class CategorySummary(BaseModel):
    category_id: int | None
    category_name: str | None
    total_amount: float
    type: str  # "income" or "expense"


class ReportSummary(BaseModel):
    total_income: float
    total_expense: float
    net: float
    by_category: List[CategorySummary]
