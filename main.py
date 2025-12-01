from fastapi import FastAPI
import uvicorn

from app.database import create_db_and_tables
from app.routers import eleven, twelve

app = FastAPI(
    title="11 & 12 API",
    description="API implementing the 11 and 12 requirements",
    version="1.0.0"
)

# Include routers
app.include_router(eleven.router)
app.include_router(twelve.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the 11 & 12 API"}


@app.on_event("startup")
def on_startup():
    create_db_and_tables()


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)