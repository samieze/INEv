#!/bin/sh

for j in  1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9
do
		a=0
		while [ $a -lt 50 ]
		do
		python3.8 generate_network.py 20 0.6 $j	6
		python3.8 generate_selectivity.py
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py
		python3.8 computePlanCosts.py PP_Plans_big #unconstrainedFilter
		python3.8 generateEvaluationPlansteven.py "$j"_"$a"
		python3.8 write_PP_config.py
		a=`expr $a + 1`
		done
done
