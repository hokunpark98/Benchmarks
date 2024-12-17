from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import asyncio

app = FastAPI()

# 넉넉한 동시성 허용
semaphore = asyncio.Semaphore(50000)

# 전역 클라이언트 (커넥션 풀 재사용)
client = httpx.AsyncClient(http2=True, limits=httpx.Limits(max_keepalive_connections=1000, max_connections=2000))

async def fetch_value(new_value: int):
    async with semaphore:
        # HTTP 요청 처리
        response = await client.get(f'http://serviceb:11001/b?value={new_value}')
        response.raise_for_status()
        return response.json()

@app.get("/a")
async def a(value: int):
    try:
        # 1초 내에 fetch_value 완료해야 함
        result = await asyncio.wait_for(fetch_value(value), timeout=5.0)
        return result
    except asyncio.TimeoutError:
        raise HTTPException(status_code=500, detail="Request timed out after 5 second")
    except httpx.HTTPStatusError as exc:
        raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
    except httpx.RequestError as exc:
        raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    # 여기서 workers와 uvloop, httptools 사용 권장
    uvicorn.run(app, host="0.0.0.0", port=11000, workers=4)
