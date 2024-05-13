#!/bin/sh


#cp qwl, sel from folder to folder...
./eventSkew_qwl.sh
cp ../nw_workload/current_wl ..
cp ../nw_workload/selectivities ..
./nw_size.sh
cd ../res
./plots.sh
cd figs
cp * ../../../Figures
