#!/bin/bash

cd /home/dnc/hokun/Benchmarks/custom2/code/pair2/a
docker build -t hokunpark/pair2:serviceA .
docker push hokunpark/pair2:serviceA

cd /home/dnc/hokun/Benchmarks/custom2/code/pair2/b
docker build -t hokunpark/pair2:serviceB .
docker push hokunpark/pair2:serviceB
