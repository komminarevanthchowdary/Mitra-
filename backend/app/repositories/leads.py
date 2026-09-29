from uuid import UUID

from sqlalchemy import Select, func, select
from sqlalchemy.orm import Session

from app.core.permissions import visible_leads_statement
from app.models.identity import User
from app.models.lead import Lead


def list_visible_leads(
    db: Session, user: User, *, limit: int, offset: int
) -> tuple[list[Lead], int]:
    scoped: Select[tuple[Lead]] = visible_leads_statement(user)
    total = db.scalar(select(func.count()).select_from(scoped.subquery())) or 0
    items = list(
        db.scalars(scoped.order_by(Lead.created_at.desc()).offset(offset).limit(limit)).all()
    )
    return items, total


def get_visible_lead(db: Session, user: User, lead_id: UUID) -> Lead | None:
    return db.scalar(visible_leads_statement(user).where(Lead.id == lead_id))
