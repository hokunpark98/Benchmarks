#!/bin/bash

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/a-lb-with-single/lb
docker build -t hokunpark/custom-metrix-lb-with-single:lb .
docker push hokunpark/custom-metrix-lb-with-single:lb

cd /home/dnc/hokun/Benchmarks/1-custom-metrix/a-lb-with-single/a
docker build -t hokunpark/custom-metrix-lb-with-single:servicea .
docker push hokunpark/custom-metrix-lb-with-single:servicea
