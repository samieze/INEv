#!/bin/sh
a=0		

                while [ $a -lt 200 ]
		do 		
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py 0 0 
		python3.8 computePlanCosts.py 
		a=`expr $a + 1`
		. /home/samira/Diss/code/topologies/msFilter.txt
		Ex=$VAR
		echo "$Ex"   
		if $Ex; then
			break
		fi
		a=`expr $a + 1`
		done
