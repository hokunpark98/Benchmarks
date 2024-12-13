FROM python:3.9-slim

WORKDIR /app
COPY c.py /app
RUN pip install --no-cache-dir fastapi uvicorn httpx

ENV HOST=0.0.0.0
ENV PORT=11002

EXPOSE 11002

