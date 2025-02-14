# main.py
from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import asyncio

app = FastAPI()

# 동시성 제한
semaphore = asyncio.Semaphore(50000)

# 전역 HTTP 클라이언트 (커넥션 풀 재사용)
client = httpx.AsyncClient(
    http2=True,
    limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000)
)

async def fetch_value(new_value: int):
    async with semaphore:
        data_to_send = {
            "value": new_value  # TEN_KB_DATA 제거됨
        }
        # 서비스 A의 /a 엔드포인트 호출
        response = await client.post("http://servicea.heart.svc.cluster.local:11001/a", json=data_to_send)
        response.raise_for_status()
        return response.json()

@app.get("/lb")
async def lb(value: int):
    try:
        # timeout을 10초로 설정 (오류 메시지 상 1초라고 되어 있으나, 기존 코드대로 10초 유지)
        result = await asyncio.wait_for(fetch_value(value), timeout=10.0)
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=500, detail="Request timed out after 1 second")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11000, workers=4)
