from fastapi import FastAPI, HTTPException, Request
import uvicorn
import asyncio
import numpy as np

app = FastAPI()
semaphore = asyncio.Semaphore(50000)

def cpu_intensive_task():
    # 대규모 행렬 연산을 통한 CPU 부하
    size = 100
    A = np.ones((size, size), dtype=float)
    B = np.ones((size, size), dtype=float)
    for _ in range(10):
        A = A.dot(B)
    return float(np.sum(A))

async def process_request(request_data: dict):
    async with semaphore:
        # CPU 부하 작업 실행
        cpu_result = cpu_intensive_task()

        # 요청 데이터 처리
        value = request_data.get("value", 0)

        # value를 1 증가
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
    # CPU 바운드 태스크가 있기 때문에 workers=1로 유지할 수도 있음
    uvicorn.run(app, host="0.0.0.0", port=11001, workers=1)