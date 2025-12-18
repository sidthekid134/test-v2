# 11 API

A FastAPI application that efficiently implements "11".

## Features

- GET /11 - Returns the value 11
- GET /eleven - Returns the value 11 via a router
- GET /eleven/db - Returns all 11 objects from the database
- POST /eleven - Creates a new 11 object in the database

## Installation

```bash
# Install dependencies
pip install -r requirements.txt
```

## Running the application

```bash
# Run the application with auto-reload
uvicorn main:app --reload
```

## API Documentation

Once the application is running, you can access the API documentation at:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
# Run tests
pytest
```