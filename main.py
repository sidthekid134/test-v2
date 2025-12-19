from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import eleven
from app.config.database import create_db_and_tables

# Create FastAPI app
app = FastAPI(
    title="11 API",
    description="API for implementing '11' efficiently",
    version="0.1.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins in development
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(eleven.router)

@app.get("/")
async def root():
    return {"message": "Welcome to the 11 API"}

@app.on_event("startup")
def on_startup():
    """Create database tables on startup."""
    create_db_and_tables()

# Run with: uvicorn main:app --reload
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)