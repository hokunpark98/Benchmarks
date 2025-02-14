#!/bin/bash

cd Benchmarks/1-custom-metrix/c-lb-with-dag-python/lb
docker build -t hokunpark/custom-metrix-lb-with-dag-python:lb .
docker push hokunpark/custom-metrix-lb-with-dag-python:lb

cd Benchmarks/1-custom-metrix/c-lb-with-dag-python/a
docker build -t hokunpark/custom-metrix-lb-with-dag-python:servicea .
docker push hokunpark/custom-metrix-lb-with-dag-python:servicea


cd Benchmarks/1-custom-metrix/c-lb-with-dag-python/b
docker build -t hokunpark/custom-metrix-lb-with-dag-python:serviceb .
docker push hokunpark/custom-metrix-lb-with-dag-python:serviceb


cd Benchmarks/1-custom-metrix/c-lb-with-dag-python/c
docker build -t hokunpark/custom-metrix-lb-with-dag-python:servicec .
docker push hokunpark/custom-metrix-lb-with-dag-python:servicec

cd Benchmarks/1-custom-metrix/c-lb-with-dag-python/d
docker build -t hokunpark/custom-metrix-lb-with-dag-python:serviced .
docker push hokunpark/custom-metrix-lb-with-dag-python:serviced