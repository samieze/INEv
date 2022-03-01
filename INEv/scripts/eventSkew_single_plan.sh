#!/bin/sh
cd ../code


python3.8 generate_network.py 20 0.5 1.1 7
python3.8 generate_qwls.py 7 1
python3.8 generate_graph.py
python3.8 allPairs.py

for s in 0.1 0.01 0.001
do
python3.8 generate_selectivity.py $s
for j in  1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 
do
		a=0
		while [ $a -lt 100 ]
		do
		python3.8 generate_network.py 20 0.5 $j 7
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py
		python3.8 computePlanCosts_aug.py eventSkew7+"$s"
		python3.8 generateEvaluationPlan.py
		a=`expr $a + 1`
		done
done
done
