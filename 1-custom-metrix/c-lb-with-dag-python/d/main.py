# d.py
from fastapi import FastAPI, HTTPException, Request
import uvicorn
import asyncio
import numpy as np

app = FastAPI()
semaphore = asyncio.Semaphore(50000)

def cpu_intensive_task():
    size = 100
    A = np.ones((size, size), dtype=float)
    B = np.ones((size, size), dtype=float)
    for _ in range(10):
        A = A.dot(B)
    return float(np.sum(A))

async def process_request(request_data: dict):
    async with semaphore:
        cpu_intensive_task()
        value = request_data.get("value", 0)
        value = value + 1
        return {
            "value": value,
        }

@app.post("/d")
async def d_endpoint(request: Request):
    try:
        request_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON data")
    try:
        result = await process_request(request_data)
        return result
    except HTTPException:
        raise HTTPException(status_code=500, detail="Failed to process request")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11004, workers=1)
