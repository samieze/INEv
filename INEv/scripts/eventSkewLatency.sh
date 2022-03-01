#!/bin/sh



cd ../code

python3.8 generate_network.py 30 0.5 1.1 20
python3.8 generate_qwls.py 7 10
python3.8 generate_selectivity.py 0.01
python3.8 generate_graph.py
python3.8 allPairs.py


for j in  1.3 1.5 1.7 1.9 
do
		a=0
		while [ $a -lt 50 ]
		do
		python3.8 generate_network.py 30 0.5 $j 20
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py 1

		python3.8 centralProcessingLatency.py 
                for l in 10 100 1000 10000 100000
		        do			
			python3.8 estimateLatency.py $l
			python3.8 combigen_latency.py
			python3.8 computePlanCosts_aug.py latency+"$l"
			done
		a=`expr $a + 1`
		done
done
