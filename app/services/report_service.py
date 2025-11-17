from datetime import datetime
from typing import Optional, List

import pandas as pd
from sqlalchemy.orm import Session

from app.models.transaction import Transaction
from app.models.category import Category
from app.schemas.report import CategorySummary, ReportSummary


def generate_report(
    db: Session,
    user_id: int,
    date_from: Optional[datetime] = None,
    date_to: Optional[datetime] = None,
) -> ReportSummary:
    q = db.query(Transaction, Category).join(
        Category, Transaction.category_id == Category.id, isouter=True
    )
    q = q.filter(Transaction.user_id == user_id)

    if date_from:
        q = q.filter(Transaction.date >= date_from)
    if date_to:
        q = q.filter(Transaction.date <= date_to)

    rows = q.all()
    if not rows:
        return ReportSummary(
            total_income=0.0, total_expense=0.0, net=0.0, by_category=[]
        )

    # Build DataFrame
    data = []
    for tx, cat in rows:
        data.append(
            {
                "amount": tx.amount,
                "type": tx.type,
                "category_id": cat.id if cat else None,
                "category_name": cat.name if cat else None,
            }
        )

    df = pd.DataFrame(data)

    # Total income/expense
    total_income = (
        df.loc[df["type"] == "income", "amount"].sum()
        if "income" in df["type"].values
        else 0.0
    )
    total_expense = (
        df.loc[df["type"] == "expense", "amount"].sum()
        if "expense" in df["type"].values
        else 0.0
    )
    net = total_income - total_expense

    # Group by category
    group_cols = ["category_id", "category_name", "type"]
    category_groups = df.groupby(group_cols)["amount"].sum().reset_index()

    by_category: List[CategorySummary] = []
    for _, row in category_groups.iterrows():
        by_category.append(
            CategorySummary(
                category_id=int(row["category_id"])
                if row["category_id"] is not None
                else None,
                category_name=row["category_name"],
                total_amount=float(row["amount"]),
                type=row["type"],
            )
        )

    return ReportSummary(
        total_income=float(total_income),
        total_expense=float(total_expense),
        net=float(net),
        by_category=by_category,
    )
