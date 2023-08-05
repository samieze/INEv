cd ../code_selectivity_change



b=0				# iterations
while [ $b -lt 20 ]
	do
	python3.8 generate_network.py 50 0.5 1.3 15
	python3.8 generate_qwls.py 6 5
	python3.8 generate_graph.py
	python3.8 allPairs.py
	python3.6 generate_selectivity.py 0.01 0.001
	python3.8 write_config_single.py
	python3.8 determine_all_single_selectivities.py 
	python3.8 generate_projections.py
	python3.8 combigen.py
	python3.8 computePlanCosts_aug.py 
	for k in 10 30 50 70 90 # percentage 
		do
		a=0
		while [ $a -lt 20 ] # number of different selectivity constellations
			do 
			python3.6 generate_selectivity.py 0.01 0.001 $k
			python3.8 adaptivity.py $k
			a=`expr $a + 1`	
			done
	done
b=`expr $b + 1`
done
