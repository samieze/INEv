#!/bin/bash
a=0
         

		while [ $a -lt 500 ]
		do

		python3.8 generate_network.py
		python3.8 generate_graph.py
		python3.8 allPairs.py
		python3.8 generate_qwls.py
		python3.8 generate_selectivity.py
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
        	python3.8 combigen.py
		python3.8 computePlanCosts.py > outEx.txt
		source outEx.txt
		Ex=$VAR1
		python3.8 combigen_short_per_query_old_but_gold.py 
       		python3.8 computePlanCosts.py 2    > outGold.txt 
		source outGold.txt
		Gold=$VAR2  
                echo "$Gold > $Ex"   
		#if (( $(echo "$Gold < $Ex" |bc -l) )); then
		#	break
		#fi
		a=`expr $a + 1`
		done

