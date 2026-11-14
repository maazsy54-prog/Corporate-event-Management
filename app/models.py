from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    Date,
    DateTime,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from datetime import datetime, timezone

from app.db import Base


class Event(Base):
    """Database model for corporate events."""

    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    event_date = Column(Date, nullable=False)
    location = Column(String(255), nullable=False)
    max_capacity = Column(Integer, nullable=False)

    # Relationship with event registrations
    registrations = relationship(
        "Registration", back_populates="event", cascade="all, delete-orphan"
    )


class Registration(Base):
    """Database model for employee event registrations."""

    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, index=True)

    event_id = Column(
        Integer, ForeignKey("events.id", ondelete="CASCADE"), nullable=False
    )

    employee_name = Column(String(150), nullable=False)
    employee_email = Column(String(255), nullable=False)

    registered_at = Column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )

    # Prevent the same employee from registering twice for one event
    __table_args__ = (
        UniqueConstraint("event_id", "employee_email", name="unique_event_employee"),
    )

    # Relationship with Event
    event = relationship("Event", back_populates="registrations")
