#!/bin/bash
set -x

cp config ../deploy/.ssh/config
cp IPs.txt ../IPs.txt
cp IPs.txt ../deploy/publish/IPs.txt
cp IPs.txt ../flink-experiment/IPs.txt
