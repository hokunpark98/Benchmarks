#!/bin/bash

cd /home/dnc/master/customBench/service/a
docker build -t hokunpark/paper2:serviceA1 .
docker push hokunpark/paper2:serviceA1

cd /home/dnc/master/customBench/service/b
docker build -t hokunpark/paper2:serviceB1 .
docker push hokunpark/paper2:serviceB1


cd /home/dnc/master/customBench/service/c
docker build -t hokunpark/paper2:serviceC1 .
docker push hokunpark/paper2:serviceC1


cd /home/dnc/master/customBench/service/d
docker build -t hokunpark/paper2:serviceD1 .
docker push hokunpark/paper2:serviceD1

cd /home/dnc/master/customBench/service/e
docker build -t hokunpark/paper2:serviceE1 .
docker push hokunpark/paper2:serviceE1