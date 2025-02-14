from flask import Flask, request, jsonify
import aiohttp
import asyncio
import logging

# 상위 컴포넌트 정의
upper_app = Flask(__name__)

# 디버그 모드 활성화 (개발 시 사용, 운영 시 비활성화)
upper_app.config["DEBUG"] = True

# 로깅 설정
logging.basicConfig(level=logging.DEBUG)

# 비동기 GET 요청을 보내는 함수
async def send_async_request(dest_url):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(dest_url, timeout=5) as response:
                response_text = await response.text()
                return response.status, response_text
    except Exception as e:
        logging.error(f"Error in send_async_request: {e}")
        raise

# GET /send?dest="{url:port}" 요청 처리
@upper_app.route('/send', methods=['GET'])
async def send():
    dest_url = request.args.get('dest')
    
    if not dest_url:
        return jsonify({'error': 'dest parameter is missing'}), 400

    try:
        # 비동기 요청 보내기
        response_code, response_text = await send_async_request(dest_url)
        return jsonify({'status': 'success', 'response_code': response_code, 'response_text': response_text}), response_code
    except Exception as e:
        logging.error(f"Error in /send route: {e}")
        return jsonify({'status': 'failure', 'error': str(e)}), 500

if __name__ == "__main__":
    upper_app.run(port=12000, host='0.0.0.0')
