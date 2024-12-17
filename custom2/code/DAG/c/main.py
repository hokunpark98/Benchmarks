from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import asyncio
import numpy as np
import math

app = FastAPI()
semaphore = asyncio.Semaphore(50000)
client = httpx.AsyncClient(http2=True, limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000))
TEN_KB_DATA = "X" * (60 * 1024)

def cpu_intensive_task():
    # 대규모 행렬 연산을 통한 CPU 부하
    size = 150
    A = np.ones((size, size), dtype=float)
    B = np.ones((size, size), dtype=float)
    for _ in range(10):
        A = A.dot(B)
    return float(np.sum(A))

async def fetch_value(value: int):
    async with semaphore:
        cpu_result = cpu_intensive_task()
        new_value = value + 1
        data_to_send = {
            "value": new_value,
            "data": TEN_KB_DATA,
            "cpu_result": cpu_result,
        }
        response = await client.post("http://servicec:11003/d", json=data_to_send)
        response.raise_for_status()
        return response.json()

@app.get("/c")
async def b(value: int):
    try:
        result = await fetch_value(value)
        return result
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    # CPU 바운드 태스크가 있기 때문에 workers=1로 유지하는 것도 전략일 수 있음
    # Kubernetes에서 replica를 늘려 CPU를 분산할 예정
    uvicorn.run(app, host="0.0.0.0", port=11002, workers=1)
