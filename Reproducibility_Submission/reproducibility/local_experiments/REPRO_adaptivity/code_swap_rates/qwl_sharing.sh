#!/bin/bash

         
for j in 1.2 1.3 1.4 1.5 1.6 1.7 1.8 
do
		a=0
		while [ $a -lt 10 ]
		do

		python3.8 generate_network.py 20 0.5 1.5
		python3.8 generate_graph.py
		python3.8 allPairs.py
		python3.8 generate_qwls.py 6 3
		python3.8 generate_selectivity.py 
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
        	python3.8 combigen.py 0 0 
		python3.8 estimateLatency.py
		python3.8 computePlanCosts.py 
		python3.8 generateEvaluationPlan.py
		a=`expr $a + 1`
		done
done
