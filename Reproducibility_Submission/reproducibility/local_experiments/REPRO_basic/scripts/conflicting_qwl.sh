#!/bin/sh

cd ../code
	
   for k in 5 10 20 # qwl size
	do 
	for h in 6 10 15 20 25 #num event types
		do
		python3.8 generate_network.py 20 0.5 1.3 $h
		python3.8 generate_graph.py
		python3.8 allPairs.py
			a=0
			while [ $a -lt 50 ]
				do	
				python3.8 generate_qwls.py 6  $k	
	                        python3.8 generate_selectivity.py 
				python3.8 write_config_single.py
				python3.8 determine_all_single_selectivities.py
				python3.8 generate_projections.py
				python3.8 combigen.py
				python3.8 computePlanCosts_aug.py "QWL"+"$k"
				a=`expr $a + 1`
				done
	
			done
		done
	

