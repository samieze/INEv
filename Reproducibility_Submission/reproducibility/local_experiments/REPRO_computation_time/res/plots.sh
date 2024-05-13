#!/bin/sh

#computation Time
#merge all csv files for computation time projection

python plot_generic_scatter.py -i computationTime.csv  -x Projections -y CombigenComputationTime -o Fig_10_computationTime_Projections
python plot_generic_scatter.py -i computationTime.csv -x QueryLength -y CombigenComputationTime -o Fig_10_computationTime_QueryLen



