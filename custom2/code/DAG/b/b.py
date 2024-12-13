from fastapi import FastAPI, Request
import math
import httpx

app = FastAPI()

B_ITER = 4000
DATA_SIZE_B_TO_C = 1024 * 4  # 4KB

async def heavy_trig_computation(iterations: int):
    result = 0.0
    for i in range(iterations):
        # 모든 값이 주기적으로 변화하고, 발산하지 않도록 안전한 연산 사용
        angle = (i % 360) * (math.pi / 180)  # [0, 2π] 범위로 정규화
        result += math.sin(angle) * math.cos(angle) * (1 / (math.sqrt(i % 100 + 1)))
    return result

@app.post("/process")
async def process_from_a(request: Request):
    received_data = await request.body()
    await heavy_trig_computation(B_ITER)
    data = "Y" * DATA_SIZE_B_TO_C
    async with httpx.AsyncClient() as client:
        response = await client.post("http://servicec:11002/process", data=data)
        return {"b_result": "done", "c_response": response.json()}
