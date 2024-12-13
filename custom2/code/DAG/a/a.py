from fastapi import FastAPI
import httpx

app = FastAPI()

@app.get("/start")
async def start():
    # a는 단순히 b에 요청만 보내고 결과 반환
    async with httpx.AsyncClient() as client:
        response = await client.post("http://serviceb:11001/process", data=b"")  # 빈 데이터 전송
        return {"a_forwarded_to_b": True, "b_response": response.json()}
