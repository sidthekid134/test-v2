from fastapi import FastAPI
from sqlmodel import SQLModel, create_engine, Session
from typing import Dict

# Create a FastAPI instance
app = FastAPI(title="11 API", description="API that efficiently implements 11")

# Database URL - Using SQLite for simplicity
DATABASE_URL = "sqlite:///./eleven.db"

# Create SQLModel engine
engine = create_engine(DATABASE_URL)

# Create tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

# Startup event
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# The core "11" endpoint
@app.get("/11", response_model=Dict[str, int])
def get_eleven():
    """
    Returns the number 11.
    
    This endpoint efficiently implements "11" as requested.
    """
    return {"value": 11}

# Root endpoint
@app.get("/")
def read_root():
    """
    Root endpoint that redirects to the documentation.
    """
    return {"message": "Welcome to the 11 API", "documentation": "/docs"}

# Run with: uvicorn app:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)