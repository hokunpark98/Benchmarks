from fastapi import FastAPI, HTTPException, Request
import uvicorn
import asyncio
import math
import numpy as np  # 0에서 2π 범위를 생성하기 위해 사용

app = FastAPI()

semaphore = asyncio.Semaphore(50000)

def cpu_intensive_task():
    """안전한 범위에서 삼각함수 연산을 3만 번 수행"""
    result = 0
    # 0에서 2π까지 1만 개의 값을 생성
    x_values = np.linspace(0, 2 * math.pi, 30000)
    for x in x_values:
        # 안전한 삼각함수 연산 수행
        result += math.sin(x) + math.cos(x)  # 무한대 값이 발생하지 않는 연산
    return result

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
    uvicorn.run(app, host="0.0.0.0", port=11002, workers=1)
