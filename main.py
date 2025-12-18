from fastapi import FastAPI
import uvicorn
from app.database.db import create_db_and_tables
from app.routers import items, users

# Create FastAPI app instance
app = FastAPI(
    title="11",
    description="FastAPI application for '11' project",
    version="0.1.0"
)

# Include routers
app.include_router(items.router)
app.include_router(users.router)

# Setup events
@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to 11 API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)