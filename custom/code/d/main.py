from fastapi import FastAPI, HTTPException
import uvicorn
import httpx
import asyncio
from collections import deque

app = FastAPI()

# Request buffer
request_queue = deque()
max_queue_size = 10000  # Maximum size of the request queue

# Semaphore to limit concurrent tasks
semaphore = asyncio.Semaphore(1000)  # Limit to 1000 concurrent requests

async def fetch_value(new_value: int):
    async with semaphore:
        async with httpx.AsyncClient() as client:
            response = await client.get(f'http://service-e:11004/e?value={new_value}')
            response.raise_for_status()
            return response.json()

@app.get("/d")
async def a(value: int):
    if len(request_queue) >= max_queue_size:
        raise HTTPException(status_code=503, detail="Service busy, please try again later.")
    
    # Add the request to the queue
    request_queue.append(value)
    
    while request_queue:
        value = request_queue.popleft()
        try:
            result = await fetch_value(value)
            return result
        except httpx.HTTPStatusError as exc:
            raise HTTPException(status_code=exc.response.status_code, detail=str(exc))
        except httpx.RequestError as exc:
            raise HTTPException(status_code=500, detail=str(exc))

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11003, workers=1)
