# b.py
from fastapi import FastAPI, HTTPException, Request
import uvicorn
import asyncio
import numpy as np
import httpx

app = FastAPI()
semaphore = asyncio.Semaphore(50000)

# 전역 HTTP 클라이언트 (서비스 호출 용도)
client = httpx.AsyncClient(
    http2=True,
    limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000)
)

def cpu_intensive_task():
    # 대규모 행렬 연산을 통한 CPU 부하
    size = 120
    A = np.ones((size, size), dtype=float)
    B = np.ones((size, size), dtype=float)
    for _ in range(10):
        A = A.dot(B)
    return float(np.sum(A))

async def call_b(new_value: int):
    data_to_send = {
        "value": new_value  # TEN_KB_DATA 제거됨
    }
    # 서비스 C 호출
    response = await client.post("http://servicec.heart.svc.cluster.local:11003/c", json=data_to_send)
    response.raise_for_status()
    return response.json()

async def process_request(request_data: dict):
    async with semaphore:
        cpu_intensive_task()  # CPU 부하 작업 실행
        value = request_data.get("value", 0)
        value = value + 1  # value를 1 증가
        # 다음 서비스 호출
        result = await call_b(value)
        return result

@app.post("/b")
async def b_endpoint(request: Request):
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
    uvicorn.run(app, host="0.0.0.0", port=11002, workers=1)
