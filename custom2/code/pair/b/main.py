from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import asyncio
import math  # 삼각함수 사용
import numpy as np  # 0에서 2π 범위를 생성하기 위해 사용

app = FastAPI()

semaphore = asyncio.Semaphore(50000)

# 전역 클라이언트 재사용
client = httpx.AsyncClient(http2=True, limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000))

# 10KB 문자열을 미리 생성해 재사용
TEN_KB_DATA = "X" * (10 * 1024)

def cpu_intensive_task():
    """안전한 범위에서 삼각함수 연산을 30000번 수행"""
    result = 0
    # 0에서 2π까지 10000개의 값을 생성
    x_values = np.linspace(0, 2 * math.pi, 30000)
    for x in x_values:
        # 안전한 삼각함수 연산 수행
        result += math.sin(x) + math.cos(x)  # 무한대 값이 발생하지 않는 연산
    return result

async def fetch_value(value: int):
    async with semaphore:
        # CPU 부하 작업 실행
        cpu_result = cpu_intensive_task()

        new_value = value + 1
        data_to_send = {
            "value": new_value,
            "data": TEN_KB_DATA,
            "cpu_result": cpu_result,  # CPU 연산 결과를 데이터에 포함 (선택사항)
        }
        response = await client.post("http://servicec:11002/c", json=data_to_send)
        response.raise_for_status()
        return response.json()

@app.get("/b")
async def b(value: int):
    try:
        result = await fetch_value(value)
        return result
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11001, workers=1)
