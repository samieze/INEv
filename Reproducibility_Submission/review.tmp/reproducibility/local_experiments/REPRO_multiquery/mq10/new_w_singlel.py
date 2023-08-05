#!/bin/sh
a=0
#for j in 25 50 75 100 124 150 175 200
#do             

		while [ $a -lt 200 ]
		do

		python3.8 generate_network.py
		python3.8 generate_graph.py
		python3.8 allPairs.py
		python3.8 generate_qwls.py
		python3.8 generate_selectivity.py
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
        python3.8 combigen_short_per_query_old_but_gold_excessive.py
		python3.8 computePlanCosts.py
		done

