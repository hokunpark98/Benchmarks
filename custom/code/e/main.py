from fastapi import FastAPI, HTTPException
import uvicorn
import asyncio
from collections import deque

app = FastAPI()

# Request buffer
request_queue = deque()
max_queue_size = 10000  # Maximum size of the request queue

# Semaphore to limit concurrent tasks
semaphore = asyncio.Semaphore(1000) 

async def process_request(value: int):
    async with semaphore:
        new_value = value + 1
        return {"value": new_value}

@app.get("/e")
async def d(value: int):
    if len(request_queue) >= max_queue_size:
        raise HTTPException(status_code=503, detail="Service busy, please try again later.")
    
    # Add the request to the queue
    request_queue.append(value)
    
    while request_queue:
        value = request_queue.popleft()
        try:
            result = await process_request(value)
            return result
        except HTTPException as e:
            # Log the error
            print(f"Request failed with error: {e.detail}")
            await asyncio.sleep(1)  # Wait before retrying
            raise HTTPException(status_code=500, detail="Failed to process request")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=11004, workers=1)
