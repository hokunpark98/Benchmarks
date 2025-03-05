#!/bin/bash
cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go-v2/loadbalancer
docker build -t hokunpark/dag-go:loadbalancer-v2 .
docker push hokunpark/dag-go:loadbalancer-v2

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go-v2/service-a
docker build -t hokunpark/dag-go:servicea-v2 .
docker push hokunpark/dag-go:servicea-v2


cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go-v2/service-b
docker build -t hokunpark/dag-go:serviceb-v2 .
docker push hokunpark/dag-go:serviceb-v2


cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go-v2/service-c
docker build -t hokunpark/dag-go:servicec-v2 .
docker push hokunpark/dag-go:servicec-v2

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go-v2/service-d
docker build -t hokunpark/dag-go:serviced-v2 .
docker push hokunpark/dag-go:serviced-v2

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-dag-go-v2/service-e
docker build -t hokunpark/dag-go:servicee-v2 .
docker push hokunpark/dag-go:servicee-v2