#!/bin/sh
a=0		

                while [ $a -lt 200 ]
		do

		python3.8 generate_network.py 20 0.4 1.3
		python3.8 generate_graph.py
		python3.8 allPairs.py
		python3.8 generate_qwls.py 6 3
		python3.8 generate_selectivity.py
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py 
		python3.8 computePlanCosts.py getFilter
		#python3.8 combigen_latency.py 
		#python3.8 computePlanCosts.py 
		a=`expr $a + 1`
		. /home/samira/Diss/code/topologies/out.txt
		Ex=$VAR
		echo "$Ex"   
		if $Ex; then
			#break
			python3.8 generateEvaluationPlan.py
		fi
		a=`expr $a + 1`
		done
