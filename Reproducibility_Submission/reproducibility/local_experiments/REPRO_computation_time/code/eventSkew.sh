#!/bin/sh

for j in  1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 2.0
do
		a=0
		while [ $a -lt 10 ]
		do
		python3.8 generate_network.py 20 0.5 $j
		#python3.8 generate_graph.py
		#python3.8 allPairs.py
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
                python3.8 centralProcessingLatency.py
		python3.8 combigen.py
		python3.8 estimateLatency.py
		python3.8 computePlanCosts.py basicFilter #unconstrainedFilter
		python3.8 generateEvaluationPlan.py
		python3.8 combigen.py 1
		python3.8 estimateLatency.py
		python3.8 computePlanCosts.py basicNoFilter 1 #unconstrainedNoFilter	
		python3.8 generateEvaluationPlan.py
		a=`expr $a + 1`
		done
done
