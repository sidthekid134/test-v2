from fastapi import FastAPI

app = FastAPI(
    title="11",
    description="FastAPI application that returns 11",
    version="0.1.0",
)

@app.get("/")
async def root():
    """Return the number 11."""
    return {"value": 11}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)