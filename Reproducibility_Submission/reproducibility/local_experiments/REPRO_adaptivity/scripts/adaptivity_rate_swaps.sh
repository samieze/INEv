cd ../code_swap_rates
#generate qwl with 15 queries

#lock config
python3.8 generate_network.py 20 0.5 1.3 25
#python3.8 generate_qwls.py 6 15
#python3.8 generate_selectivity.py
#python3.8 write_config_single.py
#python3.8 determine_all_single_selectivities.py
# one run with different sel ranges
# always same query -> no need to compute single selectivities new
for selectivity in 0.01 0.0001 # one run with different skews
do
	python3.8 generate_selectivity.py $selectivity
	a=0
	while [ $a -lt 20 ] # number of networks 
		do 
		python3.8 generate_network.py 20 0.5 1.3 25 1 #lock rates
		python3.8 generate_projections.py  
		python3.8 combigen.py
		python3.8 computePlanCosts_aug_adaptivity.py $a 0 $selectivity # best INEv for new rates, and initial combination
		for swaps in 0 1 2 3 4 5 6 7 8 9 10 11 12 # swaps ofc. 
			do
			python3.8 generate_network.py 20 0.5 1.3 25 1 $swaps #swap rates
			python3.8 adaptivity_swap_rates.py $a $swaps $selectivity  # costs of swapped plan, only take into account for processing when swaps >  0
			python3.8 generate_projections.py    # to make process combination work
			python3.8 combigen.py 
			python3.8 computePlanCosts_aug_adaptivity_noEval.py $a $swaps $selectivity # best INEv, centralized costs for new rates, NO NEW EVALPLAN WRITTEN
			done
		a=`expr $a + 1`	
		done
done
