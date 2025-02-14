# upper_component/Dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY metrix.py /app

RUN pip install Flask requests
RUN pip install numpy

EXPOSE 12001
