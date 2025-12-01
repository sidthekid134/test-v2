# Eleven API

A FastAPI application that implements the "11" requirement.

## Features

- RESTful API for accessing the number 11
- SQLModel integration for database operations
- Complete CRUD operations for Eleven resources

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the application:

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000

API Documentation will be available at:
- http://localhost:8000/docs
- http://localhost:8000/redoc

## API Endpoints

- `GET /`: Welcome message
- `GET /eleven/`: List all eleven records
- `GET /eleven/value`: Get the value 11
- `GET /eleven/{eleven_id}`: Get a specific eleven record
- `POST /eleven/`: Create a new eleven record