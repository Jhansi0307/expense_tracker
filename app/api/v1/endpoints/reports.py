from datetime import datetime
from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.api.deps import get_db, get_current_user
from app.models.user import User
from app.schemas.report import ReportSummary
from app.services.report_service import generate_report

router = APIRouter()


@router.get("/summary", response_model=ReportSummary)
def get_summary_report(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
    date_from: Optional[datetime] = Query(None),
    date_to: Optional[datetime] = Query(None),
):
    """
    General summary endpoint, can be used for monthly/yearly reports or chart data.
    Pass date_from/date_to from frontend as needed.
    """
    return generate_report(
        db=db,
        user_id=current_user.id,
        date_from=date_from,
        date_to=date_to,
    )
