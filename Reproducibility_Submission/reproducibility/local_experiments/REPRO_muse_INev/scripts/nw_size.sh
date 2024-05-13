#!/bin/sh
cd ..


#python3.8 generate_network.py 20 0.5 1.2 25
#python3.8 generate_graph.py
#python3.8 allPairs.py

#python3.8 generate_qwls.py 10 6
python3.8 write_config_single.py
python3.8 determine_all_single_selectivities.py
python3.8 generate_projections.py
for j in  10 20 50 100 150
	do
			a=0
			while [ $a -lt 50 ]
			do
			python3.8 generate_network.py $j # 0.5 1.3 25
			python3.8 generate_graph.py
			python3.8 allPairs.py
			#python3.8 write_config_single.py
			#python3.8 determine_all_single_selectivities.py
			python3.8 generate_projections.py
			python3.8 combigen.py
			python3.8 computePlanCosts_aug.py "nw"
			cp current_wl aMuSE
			cp network aMuSE
			cp selectivities aMuSE
			cd aMuSE
			python3.8 aMuse.py
			cd ..
			cp aMuSE/musegraph .
			python3.8 MuSECosts.py "nw"
			a=`expr $a + 1`
			done
	done





