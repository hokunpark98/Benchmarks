# c.py
from fastapi import FastAPI, HTTPException, Request
import uvicorn
import asyncio
import numpy as np
import httpx

app = FastAPI()
semaphore = asyncio.Semaphore(50000)

client = httpx.AsyncClient(
    http2=True,
    limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000)
)

def cpu_intensive_task():
    size = 100
    A = np.ones((size, size), dtype=float)
    B = np.ones((size, size), dtype=float)
    for _ in range(10):
        A = A.dot(B)
    return float(np.sum(A))

async def call_d(new_value: int):
    data_to_send = {
        "value": new_value  # TEN_KB_DATA 제거됨
    }
    # 서비스 D 호출
    response = await client.post("http://serviced.heart.svc.cluster.local:11004/d", json=data_to_send)
    response.raise_for_status()
    return response.json()

async def process_request(request_data: dict):
    async with semaphore:
        cpu_intensive_task()
        value = request_data.get("value", 0)
        value = value + 1
        result = await call_d(value)
        return result

@app.post("/c")
async def c_endpoint(request: Request):
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
    uvicorn.run(app, host="0.0.0.0", port=11003, workers=1)
