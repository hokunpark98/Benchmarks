FROM python:3.9-slim

WORKDIR /app

COPY loadGenerator.py /app

# 필요한 패키지 설치 (Flask, requests, aiohttp)
RUN pip install flask[async] requests aiohttp hypercorn

EXPOSE 12000
