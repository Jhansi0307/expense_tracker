from sqlalchemy.orm import Session

from app.models.user import User
from app.core.security import get_password_hash


def init_db(db: Session) -> None:
    # Example: create a default user if none exists
    user = db.query(User).filter(User.email == "admin@example.com").first()
    if not user:
        user = User(
            email="admin@example.com",
            hashed_password=get_password_hash("admin123"),
            is_active=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)
