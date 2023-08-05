#!/bin/sh

for j in  10 20 50 75 10 150
do
		a=0
		while [ $a -lt 20 ]
		do
		python3.8 generate_network.py $j
		python3.8 generate_graph.py
		python3.8 allPairs.py
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py
		python3.8 computePlanCosts.py 
		a=`expr $a + 1`
		done
done
