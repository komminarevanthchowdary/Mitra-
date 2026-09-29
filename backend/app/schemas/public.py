from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, EmailStr, Field, StringConstraints
from typing import Annotated


PhoneNumber = Annotated[str, StringConstraints(strip_whitespace=True, min_length=8, max_length=24, pattern=r"^[+\d][\d\s().-]{7,23}$")]


class ContactEnquiryCreate(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    customer_name: str = Field(min_length=2, max_length=120)
    mobile_number: PhoneNumber
    email: EmailStr | None = Field(default=None, max_length=254)
    city: str = Field(min_length=2, max_length=100)
    service_interest: str = Field(min_length=2, max_length=140)
    message: str = Field(min_length=10, max_length=2000)
    consent: bool
    website: str | None = Field(default=None, max_length=200)


class ContactReceipt(BaseModel):
    id: UUID | None = None
    message: str = "Thank you. Your enquiry has been received."


class ServiceRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    name: str
    slug: str
    category: str
    short_description: str
    description: str | None


class ProjectRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    title: str
    slug: str
    summary: str
    category: str
    city: str | None
    state: str | None
    image_url: str | None
    created_at: datetime
