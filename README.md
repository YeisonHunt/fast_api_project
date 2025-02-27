# Energy Billing System

A system for calculating and analyzing energy billing using Python and PostgreSQL.

## Features

- Calculate energy invoice concepts (EA, EC, EE1, EE2)
- Calculate monthly invoices for clients
- Retrieve client consumption and injection statistics
- Monitor system load by hour

## Requirements

- Python 3.8+
- PostgreSQL 12+
- Dependencies listed in `requirements.txt`

## Project Structure

```
energy-billing/
│
├── alembic/                  # Database migrations
│   ├── versions/             # Migration versions
│   └── env.py                # Alembic environment configuration
│
├── app/                      # Application code
│   ├── models/               # SQLAlchemy models
│   │   ├── __init__.py
│   │   └── models.py         # Database models
│   │
│   ├── routes/               # API endpoints
│   │   ├── __init__.py
│   │   ├── items.py          # Energy billing endpoints
│   │   └── users.py          # User endpoints
│   │
│   ├── schemas/              # Pydantic models
│   │   ├── __init__.py
│   │   └── database.py       # Request/response schemas
│   │
│   └── utils/                # Utility functions
│       └── calculations.py   # Calculation logic
│
├── .env                      # Environment variables
├── alembic.ini               # Alembic configuration
├── database.py               # Database connection setup
├── main.py                   # FastAPI application
└── requirements.txt          # Project dependencies
```

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/energy-billing.git
   cd energy-billing
   ```

2. Create a virtual environment:
   ```
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Create a PostgreSQL database:
   ```
   createdb energy_billing
   ```

5. Update the `.env` file with your database connection URL:
   ```
   DATABASE_URL=postgresql://username:password@localhost/energy_billing
   ```

6. Run the migrations:
   ```
   alembic upgrade head
   ```

## Running the Application

Start the FastAPI server:
```
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

API Documentation will be available at http://localhost:8000/docs.

### Tests with CURL commands
# 1. Test the homepage
curl -X GET "http://localhost:8000/"

# 2. Calculate a complete invoice for a client (January 2023)
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "month": 1, "year": 2023}'

# 3. Calculate a complete invoice for a client (February 2023)
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "month": 2, "year": 2023}'

# 4. Get client statistics
curl -X GET "http://localhost:8000/api/v1/client-statistics/1"

# 5. Get system load for January 1, 2023
curl -X GET "http://localhost:8000/api/v1/system-load?date_str=2023-01-01"

# 6. Calculate EA (Active Energy) for January 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ea/1?year=2023&month=1"

# 7. Calculate EC (Energy Excess Commercialization) for January 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ec/1?year=2023&month=1"

# 8. Calculate EE1 (Energy Excess type 1) for January 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ee1/1?year=2023&month=1"

# 9. Calculate EE2 (Energy Excess type 2) for January 2023
curl -X GET "http://localhost:8000/api/v1/calculate-ee2/1?year=2023&month=1"

# 10. Get client basic information
curl -X GET "http://localhost:8000/api/v1/users/1"

# 11. Test a different client - client 2
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 2, "month": 1, "year": 2023}'

# 12. Test a different client - client 3
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 3, "month": 1, "year": 2023}'

# 13. Testing edge case: March data where injection = consumption
curl -X POST "http://localhost:8000/api/v1/calculate-invoice" \
  -H "Content-Type: application/json" \
  -d '{"client_id": 1, "month": 3, "year": 2023}'



## API Endpoints

- `POST /api/v1/calculate-invoice`: Calculate the invoice for a client and a specific month
- `GET /api/v1/client-statistics/{client_id}`: Get consumption and injection statistics for a client
- `GET /api/v1/system-load`: Get system load by hour based on consumption data
- `GET /api/v1/calculate-ea/{client_id}`: Calculate EA (Active Energy) for a client and month
- `GET /api/v1/calculate-ec/{client_id}`: Calculate EC (Energy Excess Commercialization) for a client and month
- `GET /api/v1/calculate-ee1/{client_id}`: Calculate EE1 (Energy Excess type 1) for a client and month
- `GET /api/v1/calculate-ee2/{client_id}`: Calculate EE2 (Energy Excess type 2) for a client and month
- `GET /api/v1/users/{client_id}`: Get basic information about a client

## Database Schema

The database schema includes the following tables:
- `services`: Information about client services
- `records`: Records of energy consumption and injection
- `consumption`: Energy consumption data
- `injection`: Energy injection data
- `tariffs`: Energy tariffs
- `xm_data_hourly_per_agent`: Hourly energy prices

## Calculation Logic

- **EA (Active Energy)**: Sum of consumption * CU rate
- **EC (Energy Excess Commercialization)**: Sum of injection * C rate
- **EE1 (Energy Excess type 1)**: Min(sum(injection), sum(consumption)) * (-CU rate)
- **EE2 (Energy Excess type 2)**: Calculated hourly when injection exceeds consumption