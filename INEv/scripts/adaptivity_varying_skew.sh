cd ..

for skew in 1.3 1.5 1.7 # one run with different skews
do
	a=0
	while [ $a -lt 50 ] # number of networks 
		do 
		python3.8 generate_network.py 20 0.5 $skew 24 1 #lock rates
		python3.8 generate_projections.py  
		python3.8 combigen.py
		python3.8 computePlanCosts_aug_adaptivity.py $a 0 $skew # best INEv for new rates, and initial combination
		for swaps in 0 1 2 3 4 5 6 7 8 9 10 11 12 # swaps 
			do
			python3.8 generate_network.py 20 0.5 1.3 25 1 $swaps #swap rates
			python3.8 adaptivity.py $a $swaps $skew  # costs of swapped plan, only take into account for processing when swaps >  0
			python3.8 generate_projections.py    # to make process combination work
			python3.8 combigen.py 
			python3.8 computePlanCosts_aug_adaptivity_noEval.py $a $swaps $skew # best INEv, centralized costs for new rates, NO NEW EVALPLAN WRITTEN
			done
		a=`expr $a + 1`	
		done
done
