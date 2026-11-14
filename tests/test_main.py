import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.main import app
from app.db import Base, get_db

# Separate in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)

TestingSessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)

# Create test database tables
Base.metadata.create_all(bind=engine)


# Override the production database dependency
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(autouse=True)
def reset_database():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


client = TestClient(app)


def test_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"


def test_create_event():
    event_data = {
        "title": "Corporate Technology Conference",
        "description": "Annual technology and innovation conference",
        "event_date": "2027-01-15",
        "location": "Islamabad",
        "max_capacity": 100,
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 201

    data = response.json()

    assert data["title"] == event_data["title"]
    assert data["description"] == event_data["description"]
    assert data["event_date"] == event_data["event_date"]
    assert data["location"] == event_data["location"]
    assert data["max_capacity"] == event_data["max_capacity"]
    assert "id" in data


def test_get_all_events():
    event_data = {
        "title": "Annual Corporate Meeting",
        "description": "Annual company meeting",
        "event_date": "2027-02-10",
        "location": "Peshawar",
        "max_capacity": 150,
    }

    client.post("/events", json=event_data)

    response = client.get("/events")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["title"] == "Annual Corporate Meeting"
    assert data[0]["location"] == "Peshawar"


def test_get_event_by_id():
    event_data = {
        "title": "Project Management Seminar",
        "description": "Seminar for project managers",
        "event_date": "2027-03-15",
        "location": "Islamabad",
        "max_capacity": 80,
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    response = client.get(f"/events/{event_id}")

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == event_id
    assert data["title"] == "Project Management Seminar"
    assert data["location"] == "Islamabad"


def test_update_event():
    event_data = {
        "title": "Original Corporate Event",
        "description": "Original description",
        "event_date": "2027-04-10",
        "location": "Peshawar",
        "max_capacity": 100,
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    updated_data = {
        "title": "Updated Corporate Conference",
        "description": "Updated event description",
        "event_date": "2027-05-15",
        "location": "Islamabad",
        "max_capacity": 200,
    }

    response = client.put(f"/events/{event_id}", json=updated_data)

    assert response.status_code == 200

    data = response.json()

    assert data["id"] == event_id
    assert data["title"] == "Updated Corporate Conference"
    assert data["description"] == "Updated event description"
    assert data["location"] == "Islamabad"
    assert data["max_capacity"] == 200


def test_delete_event():
    event_data = {
        "title": "Event to Delete",
        "description": "Testing event deletion",
        "event_date": "2027-06-20",
        "location": "Peshawar",
        "max_capacity": 50,
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    response = client.delete(f"/events/{event_id}")

    assert response.status_code == 204

    # Verify that the event no longer exists
    get_response = client.get(f"/events/{event_id}")

    assert get_response.status_code == 404


def test_register_employee():
    event_data = {
        "title": "Corporate Training Workshop",
        "description": "Employee training session",
        "event_date": "2027-07-15",
        "location": "Islamabad",
        "max_capacity": 100,
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Ali Khan",
        "employee_email": "ali@example.com",
    }

    response = client.post(f"/events/{event_id}/registrations", json=registration_data)

    assert response.status_code == 201

    data = response.json()

    assert data["employee_name"] == "Ali Khan"
    assert data["employee_email"] == "ali@example.com"
    assert data["event_id"] == event_id
    assert "id" in data
    assert "registered_at" in data


def test_get_event_registrations():
    event_data = {
        "title": "Employee Development Workshop",
        "description": "Professional development training",
        "event_date": "2027-08-10",
        "location": "Peshawar",
        "max_capacity": 100,
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Ahmed Khan",
        "employee_email": "ahmed@example.com",
    }

    client.post(f"/events/{event_id}/registrations", json=registration_data)

    response = client.get(f"/events/{event_id}/registrations")

    assert response.status_code == 200

    data = response.json()

    assert len(data) == 1
    assert data[0]["employee_name"] == "Ahmed Khan"
    assert data[0]["employee_email"] == "ahmed@example.com"
    assert data[0]["event_id"] == event_id


def test_cancel_registration():
    event_data = {
        "title": "Annual Employee Gathering",
        "description": "Corporate employee gathering",
        "event_date": "2027-09-15",
        "location": "Islamabad",
        "max_capacity": 100,
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Usman Khan",
        "employee_email": "usman@example.com",
    }

    registration_response = client.post(
        f"/events/{event_id}/registrations", json=registration_data
    )

    registration_id = registration_response.json()["id"]

    response = client.delete(f"/registrations/{registration_id}")

    assert response.status_code == 204

    # Verify registration has been cancelled
    get_response = client.get(f"/events/{event_id}/registrations")

    assert get_response.status_code == 200
    assert len(get_response.json()) == 0


def test_create_event_empty_title():
    event_data = {
        "title": "",
        "description": "Invalid event",
        "event_date": "2027-10-15",
        "location": "Islamabad",
        "max_capacity": 100,
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 422


def test_create_event_zero_capacity():
    event_data = {
        "title": "Invalid Event",
        "description": "Testing capacity validation",
        "event_date": "2027-10-15",
        "location": "Peshawar",
        "max_capacity": 0,
    }

    response = client.post("/events", json=event_data)

    assert response.status_code == 422

def test_register_employee_invalid_email():
    event_data = {
        "title": "Employee Training",
        "description": "Email validation test",
        "event_date": "2027-11-15",
        "location": "Islamabad",
        "max_capacity": 100
    }

    create_response = client.post("/events", json=event_data)

    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Ali Khan",
        "employee_email": "invalid-email"
    }

    response = client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    assert response.status_code == 422


def test_duplicate_registration():
    event_data = {
        "title": "Corporate Leadership Workshop",
        "description": "Leadership training",
        "event_date": "2027-12-10",
        "location": "Islamabad",
        "max_capacity": 10
    }

    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]

    registration_data = {
        "employee_name": "Ali Khan",
        "employee_email": "ali@example.com"
    }

    # First registration
    first_response = client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    assert first_response.status_code == 201

    # Attempt duplicate registration
    second_response = client.post(
        f"/events/{event_id}/registrations",
        json=registration_data
    )

    assert second_response.status_code == 409

def test_event_maximum_capacity():
    event_data = {
        "title": "Limited Capacity Conference",
        "description": "Only one employee can register",
        "event_date": "2027-12-20",
        "location": "Peshawar",
        "max_capacity": 1
    }

    create_response = client.post("/events", json=event_data)
    event_id = create_response.json()["id"]

    # First employee registration
    first_employee = {
        "employee_name": "Ahmed Khan",
        "employee_email": "ahmed@example.com"
    }

    first_response = client.post(
        f"/events/{event_id}/registrations",
        json=first_employee
    )

    assert first_response.status_code == 201

    # Second employee registration
    second_employee = {
        "employee_name": "Usman Khan",
        "employee_email": "usman@example.com"
    }

    second_response = client.post(
        f"/events/{event_id}/registrations",
        json=second_employee
    )

    assert second_response.status_code == 409

# ==========================================
# 15. GET NON-EXISTENT EVENT
# ==========================================

def test_get_nonexistent_event():
    response = client.get("/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


# ==========================================
# 16. UPDATE NON-EXISTENT EVENT
# ==========================================

def test_update_nonexistent_event():
    event_data = {
        "title": "Updated Event",
        "description": "Testing missing event",
        "event_date": "2027-01-15",
        "location": "Islamabad",
        "max_capacity": 100
    }

    response = client.put("/events/999", json=event_data)

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


# ==========================================
# 17. DELETE NON-EXISTENT EVENT
# ==========================================

def test_delete_nonexistent_event():
    response = client.delete("/events/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Event not found"


# ==========================================
# 18. CANCEL NON-EXISTENT REGISTRATION
# ==========================================

def test_cancel_nonexistent_registration():
    response = client.delete("/registrations/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Registration not found"