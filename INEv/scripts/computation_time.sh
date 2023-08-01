#!/bin/sh
cd ../code
for j in 4 5 6 7 8
do
		a=0
		while [ $a -lt 60 ]
		do		
		python3.8 generate_network.py 20 0.5 1.4 $j
		python3.8 generate_qwls.py $j 1
		python3.8 generate_selectivity.py 		
		python3.8 generate_graph.py
		python3.8 allPairs.py
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py
		python3.8 computePlanCosts_aug.py computationTime
		a=`expr $a + 1`
		done
done
