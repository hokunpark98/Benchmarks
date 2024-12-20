from fastapi import FastAPI, HTTPException, Request
import uvicorn
import httpx
import asyncio
import numpy as np

app = FastAPI()

semaphore = asyncio.Semaphore(50000)
client = httpx.AsyncClient(http2=True, limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000))

FIFTY_KB_DATA = "X" * (500 * 1024)

def cpu_intensive_task():
    # 대규모 행렬 연산을 통한 CPU 부하
    size = 100
    A = np.ones((size, size), dtype=float)
    B = np.ones((size, size), dtype=float)
    for _ in range(10):
        A = A.dot(B)
    return float(np.sum(A))

async def call_service_b(value: int):
    async with semaphore:
        # CPU 연산 수행
        cpu_result = cpu_intensive_task()
        new_value = value + 1
        data_to_send = {
            "value": new_value,
            "data": FIFTY_KB_DATA,
            "cpu_result": cpu_result,
        }
        # b -> c로 POST 요청
        response = await client.post("http://serviceb:11002/b", json=data_to_send)
        response.raise_for_status()
        return response.json()

@app.post("/a")
async def a_endpoint(request: Request):
    try:
        request_data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON data")

    # a로부터 받은 데이터
    value = request_data.get("value", 0)
    input_data = request_data.get("data", "")  # 10KB 데이터

    # c 서비스 호출
    try:
        result_from_c = await call_service_b(value)
        # c 결과를 그대로 a에게 반환
        return result_from_c
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    # CPU 바운드 작업 때문에 단일 worker 유지 가능
    uvicorn.run(app, host="0.0.0.0", port=11001, workers=1)
