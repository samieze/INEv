#!/bin/sh
cd ..


#python3.8 generate_network.py 20 0.5 1.3 25
#python3.8 generate_graph.py
#python3.8 allPairs.py

#python3.8 generate_qwls.py 10 6
#python3.8 generate_selectivity.py 
for j in  1.1 1.3 1.5 1.7 1.9 
	do
			a=0
			while [ $a -lt 50 ]
			do
			python3.8 generate_network.py 20 0.5 $j 25
			python3.8 generate_graph.py
			python3.8 allPairs.py
			python3.8 write_config_single.py
			python3.8 determine_all_single_selectivities.py
			python3.8 generate_projections.py
			python3.8 combigen.py
			python3.8 computePlanCosts_aug.py "skew"
			cp current_wl aMuSE
			cp network aMuSE
			cd aMuSE
			echo "computing MUSEGRAPH"
			timeout 2m python3.8 aMuse.py
			echo "computed MUSEGRAPH"
			cd ..
			cp aMuSE/musegraph .
			python3.8 MuSECosts.py "skew"
			a=`expr $a + 1`
			done
	done





