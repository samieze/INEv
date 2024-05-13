#!/bin/sh
echo "Computation Time"
./computation_time.sh
cd ../res
./plots.sh
cd figs
cp * ../../../Figures
