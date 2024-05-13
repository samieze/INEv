#!/bin/sh
cd ../code


python3.8 generate_network.py 20 0.5 1.3 25
python3.8 generate_graph.py
python3.8 allPairs.py

for k in 5 10 20  
do 

	python3.8 generate_qwls.py 6 $k
	python3.8 generate_selectivity.py 
	for j in  5 20 50 100 150 200 
	do
			a=0
			while [ $a -lt 60 ]
			do
			python3.8 generate_network.py $j 0.5 1.3 25
			python3.8 generate_graph.py
			python3.8 allPairs.py
			python3.8 write_config_single.py
			python3.8 determine_all_single_selectivities.py
			python3.8 generate_projections.py
			python3.8 combigen.py
			python3.8 computePlanCosts_aug.py nwSize_qwl+$k
			a=`expr $a + 1`
			done
	done
done

