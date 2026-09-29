from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.content import ContactEnquiry, Project, Service
from app.schemas.public import ContactEnquiryCreate, ContactReceipt, ProjectRead, ServiceRead

router = APIRouter(tags=["public"])


@router.get("/services", response_model=list[ServiceRead])
def list_services(db: Annotated[Session, Depends(get_db)]) -> list[Service]:
    return list(db.scalars(select(Service).where(Service.is_published.is_(True)).order_by(Service.sort_order, Service.name)).all())


@router.get("/projects", response_model=list[ProjectRead])
def list_projects(db: Annotated[Session, Depends(get_db)]) -> list[Project]:
    return list(
        db.scalars(
            select(Project)
            .where(Project.is_published.is_(True), Project.is_demo.is_(False))
            .order_by(Project.sort_order, Project.created_at.desc())
        ).all()
    )


@router.post("/contact", response_model=ContactReceipt, status_code=status.HTTP_201_CREATED)
def create_contact_enquiry(
    payload: ContactEnquiryCreate,
    db: Annotated[Session, Depends(get_db)],
) -> ContactReceipt:
    if not payload.consent:
        raise HTTPException(status_code=422, detail="Please confirm that we may contact you about this enquiry.")
    # A filled honeypot is acknowledged without storing the submission. Do not
    # reveal that it was filtered to automated form submitters.
    if payload.website:
        return ContactReceipt()
    enquiry = ContactEnquiry(
        customer_name=payload.customer_name,
        mobile_number=payload.mobile_number,
        email=str(payload.email) if payload.email else None,
        city=payload.city,
        service_interest=payload.service_interest,
        message=payload.message,
        consent=payload.consent,
    )
    db.add(enquiry)
    db.commit()
    db.refresh(enquiry)
    return ContactReceipt(id=enquiry.id)
