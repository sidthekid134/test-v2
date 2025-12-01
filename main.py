from fastapi import FastAPI

app = FastAPI(title="Test1", description="FastAPI application for Test1")

@app.get("/11")
def eleven():
    return {"result": 11}

@app.get("/")
def root():
    return {"message": "Welcome to Test1", "endpoints": ["/11"]}