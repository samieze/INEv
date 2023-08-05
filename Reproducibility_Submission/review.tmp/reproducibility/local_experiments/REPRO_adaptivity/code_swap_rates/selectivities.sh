#!/bin/sh

for j in  0.01 0.001 0.0001 0.00001 0.000001 
do
		a=0
		k=$(echo "scale=10;0.1 * $j" | bc)
		echo $k
		while [ $a -lt 20 ]
		do
		
		python3.8 generate_selectivity.py $j $k
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py
		python3.8 computePlanCosts.py 
		a=`expr $a + 1`
		done
done
