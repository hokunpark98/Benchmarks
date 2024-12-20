#!/bin/bash

cd /home/dnc/hokun/Benchmarks/1-src/A-custom-metrix/b-lb-with-pair/lb
docker build -t hokunpark/custom-metrix-lb-with-pair:lb .
docker push hokunpark/custom-metrix-lb-with-pair:lb

cd /home/dnc/hokun/Benchmarks/1-src/A-custom-metrix/b-lb-with-pair/a
docker build -t hokunpark/custom-metrix-lb-with-pair:servicea .
docker push hokunpark/custom-metrix-lb-with-pair:servicea


cd /home/dnc/hokun/Benchmarks/1-src/A-custom-metrix/b-lb-with-pair/b
docker build -t hokunpark/custom-metrix-lb-with-pair:serviceb .
docker push hokunpark/custom-metrix-lb-with-pair:serviceb