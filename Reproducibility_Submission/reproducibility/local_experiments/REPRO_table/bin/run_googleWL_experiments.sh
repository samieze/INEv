#!/bin/sh
nohup ./DCEP.Simulation ../inputdata/ClusterData_MS/AND_MS.txt -d 10 -w 30 -t Minute --doBenchmarkTo CSV -n AND_MS > AND_MS.csv &
nohup ./DCEP.Simulation ../inputdata/ClusterData_MS/SEQ_MS.txt -d 10 -w 30 -t Minute  --doBenchmarkTo CSV -n SEQ_MS > SEQ_MS.csv &
nohup ./DCEP.Simulation ../inputdata/ClusterData_MS/QWL_MS.txt -d 10 -w 30 -t Minute  --doBenchmarkTo CSV -n QWL_MS > QWL_MS.csv & 
nohup ./DCEP.Simulation ../inputdata/ClusterData_OP/AND_OP.txt -d 10 -w 30 -t Minute  --doBenchmarkTo CSV -n AND_OP > AND_OP.csv &
nohup ./DCEP.Simulation ../inputdata/ClusterData_OP/SEQ_OP.txt -d 10 -w 30 -t Minute  --doBenchmarkTo CSV -n SEQ_OP > SEQ_OP.csv &
nohup ./bin/DCEP.Simulation ../inputdata/ClusterData_OP/QWL_OP.txt -d 10 -w 30 -t Minute  --doBenchmarkTo CSV -n QWL_OP > QWL_OP.csv & 
wait
cd ../../scripts
python3.8 plot_latency.py
python3.8 plot_throughput.py

