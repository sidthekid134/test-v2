import uvicorn
from fastapi import FastAPI
from app.routers import twelve
from app.config.database import create_db_and_tables

app = FastAPI(
    title="Twelve API",
    description="API for managing twelve items",
    version="0.1.0"
)

app.include_router(twelve.router)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def read_root():
    return {"message": "Welcome to Twelve API"}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)