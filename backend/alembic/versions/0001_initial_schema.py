"""Initial Mitra Solar schema.

Revision ID: 0001_initial_schema
Revises:
Create Date: 2026-09-29
"""
from typing import Sequence

from alembic import op
import sqlalchemy as sa

revision: str = "0001_initial_schema"
down_revision: str | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None

user_role = sa.Enum(
    "SUPER_ADMIN", "ADMIN", "STAFF", "BRANCH",
    name="user_role", native_enum=False, create_constraint=True,
)
lead_status = sa.Enum(
    "NEW", "CONTACTED", "SITE_VISIT", "QUOTATION", "FOLLOW_UP", "WON", "LOST", "CANCELLED",
    name="lead_status", native_enum=False, create_constraint=True,
)


def upgrade() -> None:
    op.create_table(
        "branches",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("code", sa.String(length=32), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_branches")),
        sa.UniqueConstraint("code", name=op.f("uq_branches_code")),
    )
    op.create_table(
        "users",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=False),
        sa.Column("full_name", sa.String(length=120), nullable=False),
        sa.Column("hashed_password", sa.String(length=255), nullable=False),
        sa.Column("role", user_role, nullable=False),
        sa.Column("branch_id", sa.Uuid(), nullable=True),
        sa.Column("is_active", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"], name=op.f("fk_users_branch_id_branches"), ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_users")),
        sa.UniqueConstraint("email", name=op.f("uq_users_email")),
    )
    op.create_index(op.f("ix_users_branch_id"), "users", ["branch_id"], unique=False)
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=False)

    op.create_table(
        "services",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("name", sa.String(length=140), nullable=False),
        sa.Column("slug", sa.String(length=160), nullable=False),
        sa.Column("category", sa.String(length=80), nullable=False),
        sa.Column("short_description", sa.String(length=400), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("is_published", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_services")),
        sa.UniqueConstraint("slug", name=op.f("uq_services_slug")),
    )

    op.create_table(
        "projects",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("title", sa.String(length=180), nullable=False),
        sa.Column("slug", sa.String(length=200), nullable=False),
        sa.Column("summary", sa.String(length=500), nullable=False),
        sa.Column("category", sa.String(length=100), nullable=False),
        sa.Column("city", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=True),
        sa.Column("image_url", sa.String(length=2048), nullable=True),
        sa.Column("is_demo", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("is_published", sa.Boolean(), server_default=sa.text("false"), nullable=False),
        sa.Column("sort_order", sa.Integer(), server_default="0", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_projects")),
        sa.UniqueConstraint("slug", name=op.f("uq_projects_slug")),
    )

    op.create_table(
        "contact_enquiries",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("customer_name", sa.String(length=120), nullable=False),
        sa.Column("mobile_number", sa.String(length=24), nullable=False),
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("service_interest", sa.String(length=140), nullable=False),
        sa.Column("message", sa.Text(), nullable=False),
        sa.Column("consent", sa.Boolean(), nullable=False),
        sa.Column("status", sa.String(length=24), server_default="NEW", nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_contact_enquiries")),
        sa.CheckConstraint("consent IS TRUE", name=op.f("ck_contact_enquiries_consent_required")),
    )
    op.create_index(op.f("ix_contact_enquiries_status"), "contact_enquiries", ["status"], unique=False)

    op.create_table(
        "leads",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("lead_number", sa.String(length=32), nullable=False),
        sa.Column("customer_name", sa.String(length=120), nullable=False),
        sa.Column("mobile_number", sa.String(length=24), nullable=False),
        sa.Column("alternate_mobile", sa.String(length=24), nullable=True),
        sa.Column("email", sa.String(length=254), nullable=True),
        sa.Column("address", sa.String(length=500), nullable=True),
        sa.Column("city", sa.String(length=100), nullable=False),
        sa.Column("district", sa.String(length=100), nullable=True),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("pincode", sa.String(length=12), nullable=True),
        sa.Column("service_interest", sa.String(length=140), nullable=False),
        sa.Column("property_type", sa.String(length=80), nullable=True),
        sa.Column("estimated_requirement", sa.String(length=140), nullable=True),
        sa.Column("source", sa.String(length=80), server_default="PORTAL", nullable=False),
        sa.Column("internal_notes", sa.Text(), nullable=True),
        sa.Column("status", lead_status, server_default="NEW", nullable=False),
        sa.Column("branch_id", sa.Uuid(), nullable=True),
        sa.Column("created_by_id", sa.Uuid(), nullable=False),
        sa.Column("assigned_staff_id", sa.Uuid(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["assigned_staff_id"], ["users.id"], name=op.f("fk_leads_assigned_staff_id_users"), ondelete="SET NULL"),
        sa.ForeignKeyConstraint(["branch_id"], ["branches.id"], name=op.f("fk_leads_branch_id_branches"), ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["created_by_id"], ["users.id"], name=op.f("fk_leads_created_by_id_users"), ondelete="RESTRICT"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_leads")),
        sa.UniqueConstraint("lead_number", name=op.f("uq_leads_lead_number")),
    )
    op.create_index(op.f("ix_leads_assigned_staff_id"), "leads", ["assigned_staff_id"], unique=False)
    op.create_index(op.f("ix_leads_branch_id"), "leads", ["branch_id"], unique=False)
    op.create_index("ix_leads_branch_created_at", "leads", ["branch_id", "created_at"], unique=False)
    op.create_index(op.f("ix_leads_created_by_id"), "leads", ["created_by_id"], unique=False)
    op.create_index("ix_leads_creator_created_at", "leads", ["created_by_id", "created_at"], unique=False)
    op.create_index(op.f("ix_leads_status"), "leads", ["status"], unique=False)

    op.create_table(
        "refresh_tokens",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("user_id", sa.Uuid(), nullable=False),
        sa.Column("token_hash", sa.String(length=64), nullable=False),
        sa.Column("expires_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("revoked_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"], name=op.f("fk_refresh_tokens_user_id_users"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_refresh_tokens")),
        sa.UniqueConstraint("token_hash", name=op.f("uq_refresh_tokens_token_hash")),
    )
    op.create_index(op.f("ix_refresh_tokens_expires_at"), "refresh_tokens", ["expires_at"], unique=False)
    op.create_index(op.f("ix_refresh_tokens_user_id"), "refresh_tokens", ["user_id"], unique=False)

    op.create_table(
        "lead_status_history",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("lead_id", sa.Uuid(), nullable=False),
        sa.Column("from_status", sa.Enum("NEW", "CONTACTED", "SITE_VISIT", "QUOTATION", "FOLLOW_UP", "WON", "LOST", "CANCELLED", name="lead_status", native_enum=False, create_constraint=False), nullable=True),
        sa.Column("to_status", sa.Enum("NEW", "CONTACTED", "SITE_VISIT", "QUOTATION", "FOLLOW_UP", "WON", "LOST", "CANCELLED", name="lead_status", native_enum=False, create_constraint=False), nullable=False),
        sa.Column("changed_by_id", sa.Uuid(), nullable=False),
        sa.Column("note", sa.String(length=1000), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["changed_by_id"], ["users.id"], name=op.f("fk_lead_status_history_changed_by_id_users"), ondelete="RESTRICT"),
        sa.ForeignKeyConstraint(["lead_id"], ["leads.id"], name=op.f("fk_lead_status_history_lead_id_leads"), ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_lead_status_history")),
    )
    op.create_index("ix_lead_status_history_lead_created", "lead_status_history", ["lead_id", "created_at"], unique=False)

    op.create_table(
        "audit_logs",
        sa.Column("id", sa.Uuid(), nullable=False),
        sa.Column("actor_user_id", sa.Uuid(), nullable=True),
        sa.Column("action", sa.String(length=100), nullable=False),
        sa.Column("entity_type", sa.String(length=80), nullable=False),
        sa.Column("entity_id", sa.String(length=80), nullable=False),
        sa.Column("request_id", sa.String(length=36), nullable=True),
        sa.Column("details", sa.JSON(), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.ForeignKeyConstraint(["actor_user_id"], ["users.id"], name=op.f("fk_audit_logs_actor_user_id_users"), ondelete="SET NULL"),
        sa.PrimaryKeyConstraint("id", name=op.f("pk_audit_logs")),
    )
    op.create_index(op.f("ix_audit_logs_action"), "audit_logs", ["action"], unique=False)
    op.create_index(op.f("ix_audit_logs_actor_user_id"), "audit_logs", ["actor_user_id"], unique=False)
    op.create_index(op.f("ix_audit_logs_created_at"), "audit_logs", ["created_at"], unique=False)


def downgrade() -> None:
    op.drop_index(op.f("ix_audit_logs_created_at"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_actor_user_id"), table_name="audit_logs")
    op.drop_index(op.f("ix_audit_logs_action"), table_name="audit_logs")
    op.drop_table("audit_logs")
    op.drop_index("ix_lead_status_history_lead_created", table_name="lead_status_history")
    op.drop_table("lead_status_history")
    op.drop_index(op.f("ix_refresh_tokens_user_id"), table_name="refresh_tokens")
    op.drop_index(op.f("ix_refresh_tokens_expires_at"), table_name="refresh_tokens")
    op.drop_table("refresh_tokens")
    op.drop_index(op.f("ix_leads_status"), table_name="leads")
    op.drop_index("ix_leads_creator_created_at", table_name="leads")
    op.drop_index(op.f("ix_leads_created_by_id"), table_name="leads")
    op.drop_index("ix_leads_branch_created_at", table_name="leads")
    op.drop_index(op.f("ix_leads_branch_id"), table_name="leads")
    op.drop_index(op.f("ix_leads_assigned_staff_id"), table_name="leads")
    op.drop_table("leads")
    op.drop_index(op.f("ix_contact_enquiries_status"), table_name="contact_enquiries")
    op.drop_table("contact_enquiries")
    op.drop_table("projects")
    op.drop_table("services")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.drop_index(op.f("ix_users_branch_id"), table_name="users")
    op.drop_table("users")
    op.drop_table("branches")
