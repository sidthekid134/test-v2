from fastapi import FastAPI
from sqlmodel import SQLModel
from contextlib import asynccontextmanager

from app.config.database import engine
from app.models.models import Item

# Create tables on startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield
    
# Initialize FastAPI app
app = FastAPI(
    title="11",
    description="FastAPI application for implementing 11",
    version="1.0.0",
    lifespan=lifespan
)

# Include routers
from app.routers import items

app.include_router(items.router)

# Root endpoint
@app.get("/")
async def root():
    return {"message": "Welcome to 11 API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)