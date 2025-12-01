from fastapi import FastAPI
from app.database import create_db_and_tables
from app.routers import eleven, twelve

app = FastAPI(
    title="Test1",
    description="FastAPI application for Test1 project",
    version="0.1.0",
)

app.include_router(eleven.router)
app.include_router(twelve.router)

@app.get("/")
async def root():
    return {"message": "12"}

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)