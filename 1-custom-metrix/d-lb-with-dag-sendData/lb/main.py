from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import asyncio
import numpy as np

app = FastAPI()

# 넉넉한 동시성 허용
semaphore = asyncio.Semaphore(50000)

# 전역 클라이언트 (커넥션 풀 재사용)
client = httpx.AsyncClient(http2=True, limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000))

TEN_KB_DATA = "X" * (10 * 1024)  # 100KB 데이터 생성

async def fetch_value(new_value: int):
    async with semaphore:
        # 이전에는 GET으로 b 호출했으나, 이제 POST로 10KB 데이터 전달
        data_to_send = {
            "value": new_value,
            "data": TEN_KB_DATA
        }
        response = await client.post("http://servicea.heart.svc.cluster.local:11001/a", json=data_to_send)
        response.raise_for_status()
        return response.json()

@app.get("/lb")
async def lb(value: int):
    try:
        # 5초 내에 fetch_value 완료해야 함
        result = await asyncio.wait_for(fetch_value(value), timeout=10.0)
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=500, detail="Request timed out after 10 second")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    # 여기서 workers와 uvloop, httptools 사용 권장
    uvicorn.run(app, host="0.0.0.0", port=11000, workers=4)
