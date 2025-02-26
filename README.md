# FastAPI PostgreSQL Application

A simple FastAPI backend with PostgreSQL database, using SQLAlchemy ORM and Alembic for migrations.

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- PostgreSQL

## Installation Steps

### 1. Clone the repository (or create your project structure)

```bash
git clone <repository-url>
# or create your own structure as shown in the project files
cd fastapi-postgresql-app
```

### 2. Create and activate virtual environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up PostgreSQL using Docker

```bash
# Start PostgreSQL container
docker-compose up -d
```

### 5. Configure environment variables

Create a `.env` file in the project root with:

```
DATABASE_URL=postgresql://myuser:mypassword@localhost:5432/mydatabase
```

### 6. Run database migrations

```bash
# Initialize Alembic (if not already initialized)
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Create users and items tables"

# Run migrations
alembic upgrade head
```

### 7. Start the application

```bash
uvicorn app.main:app --reload
```

The application will be available at `http://127.0.0.1:8000`

## API Documentation

Access the interactive API documentation at:
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## Testing with curl

### Create a user

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "name": "John Doe",
  "email": "john@example.com"
}'
```

Expected response:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "id": 1,
  "items": []
}
```

### Get all users

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/' \
  -H 'accept: application/json'
```

Expected response:
```json
[
  {
    "name": "John Doe",
    "email": "john@example.com",
    "id": 1,
    "items": []
  }
]
```

### Get a specific user

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/1' \
  -H 'accept: application/json'
```

Expected response:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "id": 1,
  "items": []
}
```

### Create an item for a user

```bash
curl -X 'POST' \
  'http://127.0.0.1:8000/users/1/items/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "First Item",
  "description": "Description of the first item"
}'
```

Expected response:
```json
{
  "title": "First Item",
  "description": "Description of the first item",
  "id": 1,
  "owner_id": 1
}
```

### Get an item by ID

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/items/1' \
  -H 'accept: application/json'
```

Expected response:
```json
{
  "title": "First Item",
  "description": "Description of the first item",
  "id": 1,
  "owner_id": 1
}
```

### Get a user with items (after creating items)

```bash
curl -X 'GET' \
  'http://127.0.0.1:8000/users/1' \
  -H 'accept: application/json'
```

Expected response:
```json
{
  "name": "John Doe",
  "email": "john@example.com",
  "id": 1,
  "items": [
    {
      "title": "First Item",
      "description": "Description of the first item",
      "id": 1,
      "owner_id": 1
    }
  ]
}
```

## Project Structure

```
fastapi-postgresql-app/
├── alembic/
│   └── versions/
├── app/
│   ├── models/
│   │   └── models.py
│   ├── routes/
│   │   ├── items.py
│   │   └── users.py
│   ├── schemas/
│   │   └── schemas.py
│   ├── database.py
│   └── main.py
├── .env
├── docker-compose.yml
└── requirements.txt
```