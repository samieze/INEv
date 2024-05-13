#!/bin/sh
./multi-query5.sh 
./multi-query10.sh 
./multi-query20.sh 
cd ../res
./plots.sh
cd figs
cp * ../../../Figures
