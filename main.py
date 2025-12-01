from fastapi import FastAPI

app = FastAPI(
    title="12",
    description="FastAPI application that returns 12",
    version="0.1.0",
)

@app.get("/")
async def root():
    """Return the number 12."""
    return {"value": 12}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)