"""
Service layer for the Corporate Event Management API.

This module contains all business logic and database operations.
API routes will call these functions from main.py.
"""

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func

from fastapi import HTTPException, status

from app import models
from app import schemas


# ==========================================
# 1. CREATE EVENT
# ==========================================


def create_event(db: Session, event: schemas.EventCreate):
    """Create a new corporate event."""

    db_event = models.Event(**event.model_dump())

    db.add(db_event)
    db.commit()
    db.refresh(db_event)

    return db_event


# ==========================================
# 2. GET ALL EVENTS
# ==========================================


def get_events(db: Session, skip: int = 0, limit: int = 100):
    """Retrieve all events with pagination."""

    return db.query(models.Event).offset(skip).limit(limit).all()


# ==========================================
# 3. GET EVENT BY ID
# ==========================================


def get_event(db: Session, event_id: int):
    """Retrieve a specific event."""

    event = db.query(models.Event).filter(models.Event.id == event_id).first()

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    return event


# ==========================================
# 4. UPDATE EVENT
# ==========================================


def update_event(db: Session, event_id: int, event_data: schemas.EventUpdate):
    """Update an existing event."""

    event = get_event(db, event_id)

    update_data = event_data.model_dump()

    for key, value in update_data.items():
        setattr(event, key, value)

    db.commit()
    db.refresh(event)

    return event


# ==========================================
# 5. DELETE EVENT
# ==========================================


def delete_event(db: Session, event_id: int):
    """Delete an existing event."""

    event = get_event(db, event_id)

    db.delete(event)
    db.commit()

    return None


# ==========================================
# 6. REGISTER EMPLOYEE FOR EVENT
# ==========================================


def register_employee(
    db: Session, event_id: int, registration: schemas.RegistrationCreate
):
    """Register an employee for an event."""

    # Check whether event exists
    event = (
        db.query(models.Event)
        .filter(models.Event.id == event_id)
        .with_for_update()
        .first()
    )

    if event is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Event not found"
        )

    # Check duplicate registration
    existing_registration = (
        db.query(models.Registration)
        .filter(
            models.Registration.event_id == event_id,
            models.Registration.employee_email == registration.employee_email,
        )
        .first()
    )

    if existing_registration:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Employee already registered for this event",
        )

    # Check event capacity
    total_registrations = (
        db.query(func.count(models.Registration.id))
        .filter(models.Registration.event_id == event_id)
        .scalar()
    )

    if total_registrations >= event.max_capacity:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Event has reached maximum capacity",
        )

    # Create registration
    db_registration = models.Registration(
        event_id=event_id, **registration.model_dump()
    )

    db.add(db_registration)

    try:
        db.commit()
        db.refresh(db_registration)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="Registration already exists"
        )

    return db_registration


# ==========================================
# 7. GET EVENT REGISTRATIONS
# ==========================================


def get_event_registrations(db: Session, event_id: int):
    """Retrieve all registrations for a specific event."""

    # Ensure event exists
    get_event(db, event_id)

    return (
        db.query(models.Registration)
        .filter(models.Registration.event_id == event_id)
        .all()
    )


# ==========================================
# 8. CANCEL REGISTRATION
# ==========================================


def cancel_registration(db: Session, registration_id: int):
    """Cancel an employee's event registration."""

    registration = (
        db.query(models.Registration)
        .filter(models.Registration.id == registration_id)
        .first()
    )

    if registration is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Registration not found"
        )

    db.delete(registration)
    db.commit()

    return None
