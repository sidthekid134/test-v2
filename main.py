from fastapi import FastAPI
from app.models.models import create_db_and_tables
from app.routers import items

app = FastAPI(title="11", description="Implementation of '11' using FastAPI and SQLModel")

@app.on_event("startup")
async def startup():
    create_db_and_tables()

app.include_router(items.router)

@app.get("/")
async def root():
    return {"message": "Welcome to 11"}