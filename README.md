# Corporate Event Management API

A REST API built using FastAPI, PostgreSQL, SQLAlchemy, and Pydantic for managing corporate events and employee registrations.

## 1. Features

- Create, retrieve, update, and delete corporate events.
- Register employees for events.
- View event registrations.
- Cancel employee registrations.
- Prevent duplicate employee registrations.
- Enforce maximum event capacity.
- Validate incoming data using Pydantic.
- Handle errors with appropriate HTTP status codes.
- Pagination using `skip` and `limit`.
- Interactive API documentation using Swagger UI.

## 2. Project Structure

```text
Corporate-event-Management/
│
├── app/
│   ├── __init__.py
│   ├── db.py
│   ├── main.py
│   ├── models.py
│   ├── schemas.py
│   └── services.py
│
├── tests/
│   ├── __init__.py
│   └── test_main.py
│
├── requirements.txt
└── README.md
```

## 3. Technologies Used

- Python
- FastAPI
- PostgreSQL
- SQLAlchemy
- Pydantic
- Pytest
- Git and GitHub

## 4. Installation

Clone the repository:

```bash
git clone https://github.com/maazsy54-prog/Corporate-event-Management.git
```

Navigate to the project directory:

```bash
cd Corporate-event-Management
```

Create a virtual environment:

```bash
python -m venv venv
```

Activate the virtual environment on Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 5. Database Configuration

This project uses PostgreSQL with SQLAlchemy.

Create a `.env` file in the project root directory and configure your database connection:

```env
DATABASE_URL=postgresql://USERNAME:PASSWORD@HOST:5432/DATABASE_NAME?sslmode=require
```

Replace the placeholders with your PostgreSQL database credentials.

**Important:** Keep your `.env` file private. Never upload database passwords or credentials to GitHub.

Ensure the PostgreSQL database is accessible and has the tables defined by the SQLAlchemy models.

## 6. Run the Application

Start the FastAPI development server:

```bash
uvicorn app.main:app --reload
```

The application will be available at:

```text
http://127.0.0.1:8000
```

## 7. API Documentation

FastAPI automatically generates interactive Swagger documentation.

Open:

```text
http://127.0.0.1:8000/docs
```

You can test all available API endpoints through Swagger UI.

## 8. Available API Endpoints

### Event Management

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events` | Create an event |
| GET | `/events` | Retrieve all events |
| GET | `/events/{event_id}` | Retrieve a specific event |
| PUT | `/events/{event_id}` | Update an event |
| DELETE | `/events/{event_id}` | Delete an event |

### Event Registration

| Method | Endpoint | Description |
|---|---|---|
| POST | `/events/{event_id}/registrations` | Register an employee |
| GET | `/events/{event_id}/registrations` | View event registrations |
| DELETE | `/registrations/{registration_id}` | Cancel registration |

### Pagination Example

```text
GET /events?skip=0&limit=10
```

## 9. Run Tests

The project uses pytest for automated testing.

Run:

```bash
pytest -v
```

The test suite uses a separate in-memory SQLite database for testing.

**Expected result:**

```text
18 passed
```

The tests cover event management, employee registrations, validation, duplicate registrations, capacity limits, and error handling.

## 10. Author

**Project:** Corporate Event Management API

**GitHub Repository:**

https://github.com/maazsy54-prog/Corporate-event-Management
