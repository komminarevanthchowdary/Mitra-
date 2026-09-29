from datetime import UTC, datetime
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, require_roles
from app.db.session import get_db
from app.models.audit import AuditLog
from app.models.identity import Role, User
from app.models.lead import Lead, LeadStatus, LeadStatusHistory
from app.repositories.leads import get_visible_lead, list_visible_leads
from app.schemas.leads import AdminLeadRead, BranchLeadRead, LeadCreate, LeadPage, LeadStatusUpdate, StaffLeadRead

router = APIRouter(prefix="/leads", tags=["leads"])
ManagementLead = AdminLeadRead | StaffLeadRead | BranchLeadRead


def _read_model(user: User) -> type[AdminLeadRead] | type[StaffLeadRead] | type[BranchLeadRead]:
    if user.role in (Role.SUPER_ADMIN, Role.ADMIN):
        return AdminLeadRead
    if user.role == Role.BRANCH:
        return BranchLeadRead
    return StaffLeadRead


@router.get("", response_model=LeadPage)
def list_leads(
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
    limit: Annotated[int, Query(ge=1, le=100)] = 25,
    offset: Annotated[int, Query(ge=0)] = 0,
) -> LeadPage:
    rows, total = list_visible_leads(db, user, limit=limit, offset=offset)
    schema = _read_model(user)
    return LeadPage(
        items=[schema.model_validate(row) for row in rows],
        total=total,
        limit=limit,
        offset=offset,
    )


@router.post("", response_model=ManagementLead, status_code=status.HTTP_201_CREATED)
def create_lead(
    payload: LeadCreate,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Lead:
    if user.role == Role.BRANCH and user.branch_id is None:
        raise HTTPException(status_code=403, detail="This branch account is not assigned to a branch.")
    lead = Lead(
        lead_number=f"MIT-{datetime.now(UTC):%Y%m}-{uuid4().hex[:8].upper()}",
        **payload.model_dump(),
        branch_id=user.branch_id,
        created_by_id=user.id,
        status=LeadStatus.NEW,
    )
    db.add(lead)
    db.flush()
    db.add(
        LeadStatusHistory(
            lead_id=lead.id,
            from_status=None,
            to_status=LeadStatus.NEW,
            changed_by_id=user.id,
            note="Lead created",
        )
    )
    db.commit()
    db.refresh(lead)
    schema = _read_model(user)
    return schema.model_validate(lead)


@router.get("/{lead_id}", response_model=ManagementLead)
def get_lead(
    lead_id: UUID,
    user: Annotated[User, Depends(get_current_user)],
    db: Annotated[Session, Depends(get_db)],
) -> Lead:
    lead = get_visible_lead(db, user, lead_id)
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found.")
    return _read_model(user).model_validate(lead)


@router.patch("/{lead_id}/status", response_model=AdminLeadRead)
def update_lead_status(
    lead_id: UUID,
    payload: LeadStatusUpdate,
    request: Request,
    user: Annotated[User, Depends(require_roles(Role.ADMIN, Role.SUPER_ADMIN))],
    db: Annotated[Session, Depends(get_db)],
) -> Lead:
    lead = db.scalar(select(Lead).where(Lead.id == lead_id).with_for_update())
    if lead is None:
        raise HTTPException(status_code=404, detail="Lead not found.")
    if lead.status == payload.status:
        raise HTTPException(status_code=409, detail="The lead already has this status.")
    old_status = lead.status
    lead.status = payload.status
    lead.updated_at = datetime.now(UTC)
    db.add(
        LeadStatusHistory(
            lead_id=lead.id,
            from_status=old_status,
            to_status=payload.status,
            changed_by_id=user.id,
            note=payload.note,
        )
    )
    db.add(
        AuditLog(
            actor_user_id=user.id,
            action="lead.status.updated",
            entity_type="lead",
            entity_id=str(lead.id),
            request_id=getattr(request.state, "request_id", None),
            details={"from_status": old_status.value, "to_status": payload.status.value},
        )
    )
    db.commit()
    db.refresh(lead)
    return lead
