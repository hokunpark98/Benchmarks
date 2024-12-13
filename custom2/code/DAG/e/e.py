from fastapi import FastAPI, Request
import math

app = FastAPI()

E_ITER = 1000

async def heavy_trig_computation(iterations: int):
    result = 0.0
    for i in range(iterations):
        # 모든 값이 주기적으로 변화하고, 발산하지 않도록 안전한 연산 사용
        angle = (i % 360) * (math.pi / 180)  # [0, 2π] 범위로 정규화
        result += math.sin(angle) * math.cos(angle) * (1 / (math.sqrt(i % 100 + 1)))
    return result

@app.post("/process")
async def process_from_d(request: Request):
    received_data = await request.body()
    await heavy_trig_computation(E_ITER)
    return {"e_result": "done"}
