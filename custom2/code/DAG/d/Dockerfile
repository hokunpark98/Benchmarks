FROM python:3.9-slim

WORKDIR /app
COPY d.py /app
RUN pip install --no-cache-dir fastapi uvicorn httpx

ENV HOST=0.0.0.0
ENV PORT=11003

EXPOSE 11003

