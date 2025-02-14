#!/bin/bash

cd Benchmarks/1-custom-metrix/c-lb-with-dag/lb
docker build -t hokunpark/custom-metrix-lb-with-dag:lb .
docker push hokunpark/custom-metrix-lb-with-dag:lb

cd Benchmarks/1-custom-metrix/c-lb-with-dag/a
docker build -t hokunpark/custom-metrix-lb-with-dag:servicea .
docker push hokunpark/custom-metrix-lb-with-dag:servicea


cd Benchmarks/1-custom-metrix/c-lb-with-dag/b
docker build -t hokunpark/custom-metrix-lb-with-dag:serviceb .
docker push hokunpark/custom-metrix-lb-with-dag:serviceb


cd Benchmarks/1-custom-metrix/c-lb-with-dag/c
docker build -t hokunpark/custom-metrix-lb-with-dag:servicec .
docker push hokunpark/custom-metrix-lb-with-dag:servicec

cd Benchmarks/1-custom-metrix/c-lb-with-dag/d
docker build -t hokunpark/custom-metrix-lb-with-dag:serviced .
docker push hokunpark/custom-metrix-lb-with-dag:serviced