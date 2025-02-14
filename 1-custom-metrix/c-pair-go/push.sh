#!/bin/bash
cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-pair-go/loadbalancer
docker build -t hokunpark/pair-go:loadbalancer-v1 .
docker push hokunpark/pair-go:loadbalancer-v1

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-pair-go/service-a
docker build -t hokunpark/pair-go:servicea-v1 .
docker push hokunpark/pair-go:servicea-v1

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/c-pair-go/service-b
docker build -t hokunpark/pair-go:serviceb-v1 .
docker push hokunpark/pair-go:serviceb-v1