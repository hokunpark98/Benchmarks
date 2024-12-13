from fastapi import FastAPI, Request
import math
import httpx

app = FastAPI()

D_ITER = 3000
DATA_SIZE_D_TO_E = 1024 * 3  # 3KB

async def heavy_trig_computation(iterations: int):
    result = 0.0
    for i in range(iterations):
        # 모든 값이 주기적으로 변화하고, 발산하지 않도록 안전한 연산 사용
        angle = (i % 360) * (math.pi / 180)  # [0, 2π] 범위로 정규화
        result += math.sin(angle) * math.cos(angle) * (1 / (math.sqrt(i % 100 + 1)))
    return result

@app.post("/process")
async def process_from_c(request: Request):
    received_data = await request.body()
    await heavy_trig_computation(D_ITER)
    data = "W" * DATA_SIZE_D_TO_E
    async with httpx.AsyncClient() as client:
        response = await client.post("http://servicee:11004/process", data=data)
        return {"d_result": "done", "e_response": response.json()}
