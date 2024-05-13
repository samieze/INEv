#!/bin/sh

cd ../code_topology_change
b=0				# iterations

while [ $b -lt 1 ]
do
	#wrap with different networks
	#python3.8 generate_network.py 50 0.5 1.3 15
	#python3.8 generate_qwls.py 6 5
	#python3.8 generate_graph.py
	#python3.8 allPairs.py
	#python3.6 generate_selectivity.py 
	#python3.8 write_config_single.py
	#python3.8 determine_all_single_selectivities.py
	python3.8 generate_projections.py
	python3.8 combigen.py
	python3.8 computePlanCosts_aug.py 

	for k in 10 30 50 60 80 90 # percentage change
	do 
		for j in 0 1 2  # 0 = remove; 1 = add; 2 = permute
		do
				a=0				# iterations
				while [ $a -lt 50 ]
				do
				python3.8 generate_graph.py $k $j
				python3.8 allPairs.py
				python3.8 newGraphCosts.py $k $j
				a=`expr $a + 1`
				done
		done
	done

	b=`expr $b + 1`
done
