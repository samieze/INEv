#!/bin/sh
cd ../code


python3.8 generate_network.py 20 0.5 1.3 7
python3.8 generate_qwls.py 7 1
python3.8 generate_graph.py
python3.8 allPairs.py

for k in 0.1 0.01 0.001 
do 

	python3.8 generate_selectivity.py $k 
	for j in  5 10 20 50 100 150 200 
	do
			a=0
			while [ $a -lt 2 ]
			do
			python3.8 generate_network.py $j
			python3.8 generate_graph.py
			python3.8 allPairs.py
			python3.8 write_config_single.py
			python3.8 determine_all_single_selectivities.py
			python3.8 generate_projections.py
			python3.8 combigen.py
			python3.8 computePlanCosts_aug.py nwSize+"$k"
			a=`expr $a + 1`
			done
	done
done
