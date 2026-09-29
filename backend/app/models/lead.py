import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, ForeignKey, Index, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.identity import Branch, User


class LeadStatus(str, enum.Enum):
    NEW = "NEW"
    CONTACTED = "CONTACTED"
    SITE_VISIT = "SITE_VISIT"
    QUOTATION = "QUOTATION"
    FOLLOW_UP = "FOLLOW_UP"
    WON = "WON"
    LOST = "LOST"
    CANCELLED = "CANCELLED"


class Lead(Base):
    __tablename__ = "leads"
    __table_args__ = (
        Index("ix_leads_branch_created_at", "branch_id", "created_at"),
        Index("ix_leads_creator_created_at", "created_by_id", "created_at"),
    )

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_number: Mapped[str] = mapped_column(String(32), nullable=False, unique=True)
    customer_name: Mapped[str] = mapped_column(String(120), nullable=False)
    mobile_number: Mapped[str] = mapped_column(String(24), nullable=False)
    alternate_mobile: Mapped[str | None] = mapped_column(String(24), nullable=True)
    email: Mapped[str | None] = mapped_column(String(254), nullable=True)
    address: Mapped[str | None] = mapped_column(String(500), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=False)
    district: Mapped[str | None] = mapped_column(String(100), nullable=True)
    state: Mapped[str] = mapped_column(String(100), nullable=False)
    pincode: Mapped[str | None] = mapped_column(String(12), nullable=True)
    service_interest: Mapped[str] = mapped_column(String(140), nullable=False)
    property_type: Mapped[str | None] = mapped_column(String(80), nullable=True)
    estimated_requirement: Mapped[str | None] = mapped_column(String(140), nullable=True)
    source: Mapped[str] = mapped_column(String(80), nullable=False, default="PORTAL", server_default="PORTAL")
    internal_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, name="lead_status", native_enum=False, create_constraint=True),
        nullable=False,
        default=LeadStatus.NEW,
        server_default=LeadStatus.NEW.value,
        index=True,
    )
    branch_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("branches.id", ondelete="RESTRICT"), nullable=True, index=True)
    created_by_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False, index=True)
    assigned_staff_id: Mapped[uuid.UUID | None] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    branch: Mapped[Branch | None] = relationship()
    created_by: Mapped[User] = relationship(foreign_keys=[created_by_id])
    assigned_staff: Mapped[User | None] = relationship(foreign_keys=[assigned_staff_id])
    status_history: Mapped[list["LeadStatusHistory"]] = relationship(
        back_populates="lead", cascade="all, delete-orphan", order_by="LeadStatusHistory.created_at"
    )


class LeadStatusHistory(Base):
    __tablename__ = "lead_status_history"
    __table_args__ = (Index("ix_lead_status_history_lead_created", "lead_id", "created_at"),)

    id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), primary_key=True, default=uuid.uuid4)
    lead_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("leads.id", ondelete="CASCADE"), nullable=False)
    from_status: Mapped[LeadStatus | None] = mapped_column(
        Enum(LeadStatus, name="lead_status", native_enum=False, create_constraint=False), nullable=True
    )
    to_status: Mapped[LeadStatus] = mapped_column(
        Enum(LeadStatus, name="lead_status", native_enum=False, create_constraint=False), nullable=False
    )
    changed_by_id: Mapped[uuid.UUID] = mapped_column(Uuid(as_uuid=True), ForeignKey("users.id", ondelete="RESTRICT"), nullable=False)
    note: Mapped[str | None] = mapped_column(String(1000), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False, server_default=func.now())

    lead: Mapped[Lead] = relationship(back_populates="status_history")
    changed_by: Mapped[User] = relationship()
