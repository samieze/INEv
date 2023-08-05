#!/bin/sh

./adaptivity_rate_swaps.sh  
./adaptivity_selectivity_change.sh  
./changing_topology.sh
cd ../adaptivity_selectivity_change
python3.8 plot_adaptivity_brokenprojections.py
cd ../adaptivity_swap_rates
./plots.sh
cd ../adaptivity_topology_change
python3.8 plot_topology_correct.py
cd ../res/figs
cp * ../../../Figures
