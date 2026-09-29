from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field

from app.models.lead import LeadStatus
from app.schemas.public import PhoneNumber


class LeadCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    customer_name: str = Field(min_length=2, max_length=120)
    mobile_number: PhoneNumber
    alternate_mobile: PhoneNumber | None = None
    email: EmailStr | None = Field(default=None, max_length=254)
    address: str | None = Field(default=None, max_length=500)
    city: str = Field(min_length=2, max_length=100)
    district: str | None = Field(default=None, max_length=100)
    state: str = Field(min_length=2, max_length=100)
    pincode: str | None = Field(default=None, min_length=4, max_length=12, pattern=r"^[A-Za-z0-9 -]+$")
    service_interest: str = Field(min_length=2, max_length=140)
    property_type: str | None = Field(default=None, max_length=80)
    estimated_requirement: str | None = Field(default=None, max_length=140)


class LeadStatusUpdate(BaseModel):
    status: LeadStatus
    note: str | None = Field(default=None, max_length=1000)


class StaffLeadRead(BaseModel):
    """Staff-safe output: no internal status, branch, assignment or notes fields."""
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    lead_number: str
    customer_name: str
    mobile_number: str
    alternate_mobile: str | None
    email: EmailStr | None
    address: str | None
    city: str
    district: str | None
    state: str
    pincode: str | None
    service_interest: str
    property_type: str | None
    estimated_requirement: str | None
    created_at: datetime
    updated_at: datetime


class BranchLeadRead(StaffLeadRead):
    """Branch-safe output intentionally has the same restricted fields as Staff."""


class AdminLeadRead(StaffLeadRead):
    """Management output includes fields that must never be returned to Staff/Branch."""

    status: LeadStatus
    branch_id: UUID | None
    created_by_id: UUID
    assigned_staff_id: UUID | None
    internal_notes: str | None


class LeadPage(BaseModel):
    items: list[AdminLeadRead | StaffLeadRead | BranchLeadRead]
    total: int
    limit: int
    offset: int
