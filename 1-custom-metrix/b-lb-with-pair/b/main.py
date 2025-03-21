from fastapi import FastAPI, HTTPException, Request
import uvicorn
import asyncio
import math
import numpy as np  # 0에서 2π 범위를 생성하기 위해 사용

app = FastAPI()

semaphore = asyncio.Semaphore(50000)

def cpu_intensive_task():
    # 대규모 행렬 연산을 통한 CPU 부하
    size = 150
    A = np.ones((size, size), dtype=float)
    B = np.ones((size, size), dtype=float)
    for _ in range(10):
        A = A.dot(B)
    return float(np.sum(A))

async def process_request(request_data: dict):
    async with semaphore:
        # CPU 부하 작업 실행
        _ = cpu_intensive_task()

        # 요청 데이터 처리
        value = request_data.get("value", 0)
        value = value + 1
        return {
            "value": value,
        }

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
