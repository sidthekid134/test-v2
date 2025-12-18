from fastapi import FastAPI
from app.database import create_db_and_tables

app = FastAPI(
    title="11",
    description="Implementation of 11 using FastAPI and SQLModel",
    version="0.1.0",
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
async def root():
    return {"message": "Welcome to 11"}

# Import and include routers
from app.routers import items_router
app.include_router(items_router.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)