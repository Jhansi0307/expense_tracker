from dataclasses import dataclass
from typing import List

from app.schemas.report import ReportSummary


@dataclass
class Alert:
    message: str
    level: str  # info/warning/danger


def check_spending_limits(
    report: ReportSummary, monthly_limit: float
) -> List[Alert]:
    alerts: List[Alert] = []
    if report.total_expense > monthly_limit:
        alerts.append(
            Alert(
                message=(
                    f"You exceeded your monthly limit "
                    f"({report.total_expense:.2f} > {monthly_limit:.2f})"
                ),
                level="danger",
            )
        )
    return alerts
