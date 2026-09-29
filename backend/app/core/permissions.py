from sqlalchemy import Select, or_, select

from app.models.identity import Role, User
from app.models.lead import Lead


def visible_leads_statement(user: User) -> Select[tuple[Lead]]:
    """Build the server-side lead scope from the authenticated account."""
    statement = select(Lead)
    if user.role == Role.BRANCH:
        if user.branch_id is None:
            return statement.where(Lead.id.is_(None))
        return statement.where(Lead.branch_id == user.branch_id)
    if user.role == Role.STAFF:
        return statement.where(
            or_(Lead.created_by_id == user.id, Lead.assigned_staff_id == user.id)
        )
    return statement
