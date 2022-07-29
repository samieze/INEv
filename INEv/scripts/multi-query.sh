#!/bin/sh
cd ..
# a identifies workload
for skew in  1.3 1.5 1.7 #skew for x-axis
do 
b=0
while [ $b -lt 20 ] # number networks per skew
do
python3.8 generate_network.py 20 0.6 $skew 10
a=0
while [ $a -lt 20 ] # number of different workloads
	do
	for k in 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15  #wl_length	(+1) runs necessary
				do	
				python3.8 generate_qwls_incremental.py 6 15 $k 
				python3.8 write_config_single.py
				python3.8 determine_all_single_selectivities.py
				python3.8 generate_projections.py
				python3.8 combigen.py
				python3.8 computePlanCosts_aug_incremental.py $a $k 15 $b $skew
				python3.8 mergedcosts.py $a $k 15 $b $skew
				
				done
	a=`expr $a + 1`
done
b=`expr $b + 1`
done
done
