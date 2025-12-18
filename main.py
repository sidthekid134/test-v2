from fastapi import FastAPI
from typing import Dict

from app.database import create_db_and_tables
from app.routers import eleven

# Create a FastAPI instance
app = FastAPI(
    title="11 API",
    description="API that efficiently implements 11",
    version="1.0.0",
)

# Include routers
app.include_router(eleven.router)

# Startup event
@app.on_event("startup")
def on_startup():
    create_db_and_tables()

# Root endpoint
@app.get("/", response_model=Dict[str, str])
def read_root():
    """
    Root endpoint that returns basic API information.
    """
    return {
        "message": "Welcome to the 11 API",
        "documentation": "/docs",
        "eleven": "/eleven",
    }

# The core "11" endpoint - top level for maximum efficiency
@app.get("/11", response_model=Dict[str, int])
def get_eleven():
    """
    Returns the number 11.
    
    This endpoint efficiently implements "11" as requested.
    """
    return {"value": 11}

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)