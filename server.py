from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def simulate_buses():
    return {"Hello": "World"}
