#!/bin/bash

cd /home/dnc/hokun/Benchmarks/custom2/code/pair/a
docker build -t hokunpark/pair:serviceA .
docker push hokunpark/pair:serviceA

cd /home/dnc/hokun/Benchmarks/custom2/code/pair/b
docker build -t hokunpark/pair:serviceB .
docker push hokunpark/pair:serviceB


cd /home/dnc/hokun/Benchmarks/custom2/code/pair/c
docker build -t hokunpark/pair:serviceC .
docker push hokunpark/pair:serviceC