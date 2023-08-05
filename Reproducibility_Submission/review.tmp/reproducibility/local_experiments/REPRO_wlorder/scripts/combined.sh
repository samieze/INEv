#!/bin/sh
cd ..

for i in  1 2 3 4 5
	do
        python3.8 generate_network.py 20 0.5 1.3 26
	python3.8 generate_selectivity.py
	a=0
	while [ $a -lt 20 ] # number of different workloads
	do
		for j in  5 10 20 30 # j is workload size
			do 		
				python3.8 generate_qwls.py 5 $j 
				python3.8 write_config_single.py
				python3.8 determine_all_single_selectivities.py
				python3.8 generate_projections.py
				b=0
				while [ $b -lt 30 ] # number of permutations per size
						do
						python3.8 combigen.py
						python3.8 computePlanCosts_aug.py $i+$a+$j #unconstrainedFilter
						b=`expr $b + 1`
						done
				a=`expr $a + 1`
				done
			done
done

cd ../res
./plots.sh
cd figs
cp * ../../../Figures
