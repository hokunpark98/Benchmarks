from flask import Flask, jsonify, request
import time
import numpy as np
import threading
import queue

# Flask 애플리케이션 정의
lower_app = Flask(__name__)

# 처리 시간과 결과를 저장할 리스트
process_times = []
lock = threading.Lock()

# 작업 대기 큐 생성
task_queue = queue.Queue()

def matrix_multiplication():
    size = 500  # 행렬의 크기 설정
    # 2부터 10 사이의 랜덤 실수 값으로 채워진 행렬 생성
    A = np.random.uniform(2, 10, (size, size))
    B = np.random.uniform(2, 10, (size, size))
    # 행렬 곱셈 수행
    result = np.dot(A, B)
    return result

def worker():
    while True:
        # 큐에서 작업 가져오기
        item = task_queue.get()
        if item is None:
            break  # 종료 신호
        event, result_container, enqueue_time = item
        # CPU 집약적인 작업 수행
        matrix_multiplication()
        end_time = time.time()
        process_time = (end_time - enqueue_time) * 1000  # 처리 시간(ms) 계산
        # 처리 시간 저장
        with lock:
            process_times.append(process_time)
        # 결과 저장
        result_container['process_time'] = process_time
        # 이벤트 설정하여 작업 완료 알림
        event.set()
        task_queue.task_done()

# 워커 스레드 생성
NUM_WORKERS = 1
threads = []
for i in range(NUM_WORKERS):
    t = threading.Thread(target=worker)
    t.daemon = True
    t.start()
    threads.append(t)

@lower_app.route('/process', methods=['POST'])
def process_request():
    enqueue_time = time.time()
    event = threading.Event()
    result_container = {}
    # 작업 큐에 작업 추가
    task_queue.put((event, result_container, enqueue_time))
    # 작업 완료 대기
    event.wait()
    process_time = result_container['process_time']
    return jsonify({
        "process_time_ms": f"{process_time:.2f}ms"
    }), 200

@lower_app.route('/stats', methods=['GET'])
def get_stats():
    with lock:
        if process_times:
            # 각 요청의 처리 시간 로그 생성 (딕셔너리 형태)
            logs = [{'request_number': i + 1, 'process_time_ms': f"{time_ms:.2f}ms"} for i, time_ms in enumerate(process_times)]
            avg_process_time = sum(process_times) / len(process_times)  # 평균 처리 시간 계산
            response = {
                "average_process_time_ms": f"{avg_process_time:.2f}ms",
                "total_received_requests": len(process_times),
                "logs": logs  # 딕셔너리 리스트로 변경된 로그
            }
            return jsonify(response), 200
        else:
            return jsonify({"message": "아직 처리된 요청이 없습니다."}), 200

if __name__ == "__main__":
    lower_app.run(port=12001, host='0.0.0.0')
