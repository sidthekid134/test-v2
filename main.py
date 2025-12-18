from fastapi import FastAPI, Depends
import uvicorn
from sqlmodel import Session

from app.config.database import create_db_and_tables, get_session
from app.models.eleven import Eleven
from app.routers import eleven as eleven_router

app = FastAPI(
    title="11",
    description="Implementation of 11",
    version="1.0.0"
)

app.include_router(eleven_router.router)

@app.get("/")
async def root():
    return {"message": "Implementation of 11"}

@app.get("/11")
async def eleven_endpoint():
    return {"value": 11}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)