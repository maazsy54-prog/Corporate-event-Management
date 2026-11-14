from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, EmailStr, Field


# -------------------------
# Event Schemas
# -------------------------


class EventCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str | None = None
    event_date: date
    location: str = Field(..., min_length=1, max_length=255)
    max_capacity: int = Field(..., gt=0)

    model_config = ConfigDict(str_strip_whitespace=True)


class EventUpdate(EventCreate):
    pass


class EventResponse(EventCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -------------------------
# Registration Schemas
# -------------------------


class RegistrationCreate(BaseModel):
    employee_name: str = Field(..., min_length=1, max_length=150)
    employee_email: EmailStr


class RegistrationResponse(RegistrationCreate):
    id: int
    event_id: int
    registered_at: datetime

    model_config = ConfigDict(from_attributes=True)
