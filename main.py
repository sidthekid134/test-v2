from fastapi import FastAPI
import uvicorn

from app.database import create_db_and_tables
from app.routers import eleven

app = FastAPI(
    title="11 API",
    description="API implementing the 11 requirement",
    version="1.0.0"
)

# Include routers
app.include_router(eleven.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the 11 API"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)