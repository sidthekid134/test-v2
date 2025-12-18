from fastapi import FastAPI
import uvicorn
from fastapi.middleware.cors import CORSMiddleware

from app.core.database import create_db_and_tables
from app.routers.items import router as items_router

# Create FastAPI app
app = FastAPI(
    title="Item Management API",
    description="API for managing items",
    version="0.1.0"
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(items_router)

@app.on_event("startup")
def on_startup():
    """Create database tables on startup"""
    create_db_and_tables()

@app.get("/")
def read_root():
    """Root endpoint"""
    return {"message": "Welcome to the Item Management API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)