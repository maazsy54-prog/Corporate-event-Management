"""
Main application file for Corporate Event Management API.

This file defines API endpoints and connects them
with the service layer and PostgreSQL database.
"""

from fastapi import FastAPI, Depends, status, Query
from sqlalchemy.orm import Session

from app.db import get_db
from app import models, schemas, services

# ==========================================
# INITIALIZE FASTAPI APPLICATION
# ==========================================

app = FastAPI(
    title="Corporate Event Management API",
    description="API for managing corporate events and employee registrations.",

)


# ==========================================
# ROOT ENDPOINT
# ==========================================


@app.get("/")
def home():
    """Welcome endpoint."""

    return {"message": "Welcome to Corporate Event Management API", "docs": "/docs"}


# ==========================================
# 1. CREATE EVENT
# POST /events
# ==========================================


@app.post(
    "/events",
    response_model=schemas.EventResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Events"]
)

def create_event(event: schemas.EventCreate, db: Session = Depends(get_db)):
    """Create a new corporate event."""

    return services.create_event(db, event)


# ==========================================
# 2. GET ALL EVENTS
# GET /events
# ==========================================


@app.get("/events", response_model=list[schemas.EventResponse])
def get_events(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=100),
    db: Session = Depends(get_db)
):
    """Retrieve all events."""

    return services.get_events(db, skip, limit)


# ==========================================
# 3. GET EVENT BY ID
# GET /events/{event_id}
# ==========================================


@app.get("/events/{event_id}", response_model=schemas.EventResponse)
def get_event(event_id: int, db: Session = Depends(get_db)):
    """Retrieve a specific event."""

    return services.get_event(db, event_id)


# ==========================================
# 4. UPDATE EVENT
# PUT /events/{event_id}
# ==========================================


@app.put("/events/{event_id}", response_model=schemas.EventResponse)
def update_event(
    event_id: int, event_data: schemas.EventUpdate, db: Session = Depends(get_db)
):
    """Update an existing event."""

    return services.update_event(db, event_id, event_data)


# ==========================================
# 5. DELETE EVENT
# DELETE /events/{event_id}
# ==========================================


@app.delete("/events/{event_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_event(event_id: int, db: Session = Depends(get_db)):
    """Delete an event."""

    services.delete_event(db, event_id)

    return None


# ==========================================
# 6. REGISTER EMPLOYEE
# POST /events/{event_id}/registrations
# ==========================================


@app.post(
    "/events/{event_id}/registrations",
    response_model=schemas.RegistrationResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Registrations"]
)
def register_employee(
    event_id: int,
    registration: schemas.RegistrationCreate,
    db: Session = Depends(get_db),
):
    """Register an employee for an event."""

    return services.register_employee(db, event_id, registration)


# ==========================================
# 7. GET EVENT REGISTRATIONS
# GET /events/{event_id}/registrations
# ==========================================


@app.get(
    "/events/{event_id}/registrations",
    response_model=list[schemas.RegistrationResponse],
)
def get_event_registrations(event_id: int, db: Session = Depends(get_db)):
    """Retrieve all registrations for an event."""

    return services.get_event_registrations(db, event_id)


# ==========================================
# 8. CANCEL REGISTRATION
# DELETE /registrations/{registration_id}
# ==========================================


@app.delete("/registrations/{registration_id}", status_code=status.HTTP_204_NO_CONTENT)
def cancel_registration(registration_id: int, db: Session = Depends(get_db)):
    """Cancel an employee registration."""

    services.cancel_registration(db, registration_id)

    return None
