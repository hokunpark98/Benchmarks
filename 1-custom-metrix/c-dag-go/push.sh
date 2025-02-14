#!/bin/bash
cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go/loadbalancer
docker build -t hokunpark/dag-go:loadbalancer-v1 .
docker push hokunpark/dag-go:loadbalancer-v1

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go/service-a
docker build -t hokunpark/dag-go:servicea-v1 .
docker push hokunpark/dag-go:servicea-v1


cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go/service-b
docker build -t hokunpark/dag-go:serviceb-v1 .
docker push hokunpark/dag-go:serviceb-v1


cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go/service-c
docker build -t hokunpark/dag-go:servicec-v1 .
docker push hokunpark/dag-go:servicec-v1

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go/service-d
docker build -t hokunpark/dag-go:serviced-v1 .
docker push hokunpark/dag-go:serviced-v1