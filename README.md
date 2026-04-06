# Relay

A simple URL shortener service built with FastAPI, SQLModel, and PostgreSQL.

## Tech Stack
- **Language:** Python 3.11
- **Framework:** FastAPI
- **ORM/Validation:** SQLModel (SQLAlchemy + Pydantic v2)
- **Database:** PostgreSQL
- **Server:** Uvicorn

## Project Structure
```
url-shortener/
├── app/
│   ├── __init__.py
│   ├── models/           # Database models (SQLModel)
│   │   ├── __init__.py
│   │   ├── url.py        # URL model
│   │   └── click.py      # Click tracking model
│   └── core/             # Core utilities
│       ├── __init__.py
│       ├── database.py   # Database connection
│       ├── config.py     # Configuration
│       └── encoder.py    # Short code encoding/decoding
├── main.py               # Application entry point with all endpoints
├── pyproject.toml        # Project dependencies
└── README.md             # This file
```

## API Endpoints
- `POST /` - Create a short URL
- `GET /:shortCode` - Redirect to original URL
- `GET /health` - Health check

## Running Locally
```bash
# Install dependencies
pip install -e .

# Run the app
uvicorn main:app --reload
```

## Docker (Planned)
```bash
docker-compose up
```