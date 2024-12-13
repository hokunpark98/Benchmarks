#!/bin/bash

cd /home/dnc/hokun/Benchmarks/custom2/code/DAG/a
docker build -t hokunpark/custom2:serviceA .
docker push hokunpark/custom2:serviceA

cd /home/dnc/hokun/Benchmarks/custom2/code/DAG/b
docker build -t hokunpark/custom2:serviceB .
docker push hokunpark/custom2:serviceB


cd /home/dnc/hokun/Benchmarks/custom2/code/DAG/c
docker build -t hokunpark/custom2:serviceC .
docker push hokunpark/custom2:serviceC


cd /home/dnc/hokun/Benchmarks/custom2/code/DAG/d
docker build -t hokunpark/custom2:serviceD .
docker push hokunpark/custom2:serviceD

cd /home/dnc/hokun/Benchmarks/custom2/code/DAG/e
docker build -t hokunpark/custom2:serviceE .
docker push hokunpark/custom2:serviceE