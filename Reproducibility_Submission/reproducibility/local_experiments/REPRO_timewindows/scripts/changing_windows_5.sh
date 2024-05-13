cd ../code_5
# for each workload size, 1 value for shared computation and 1 for merged inevs for individual queries, having different rates
for d in 1 2 3 4
do
python3.8 generate_network.py 20 0.5 1.4 15
python3.8 generate_graph.py
python3.8 allPairs.py

for k in 5 10 15 20 # for different wl sizes    
	do
	b=0
	while [ $b -lt 20 ]	
		do
		python3.8 generate_qwls_incremental_different_windows.py 6 $k  #generate query workload with windows, use maximal rates to scale network -> overwrite network
		python3.8 network.py #call network.py to overwrite nodes, rates, etc
		#compute inev
		python3.8 generate_selectivity.py 0.01 0.001
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py 
		python3.8 generate_projections.py
		python3.8 combigen.py
		python3.8 computePlanCosts_aug.py 1 #TODO -> check what to pass for writing results

		# for each query in the workload -> $k
		a=0
			while [ $a -lt $k ]
				do
				python3.8 exchange_queries.py $a #call extra python file which generates timewindow for each query, overwrites network -> keep state? -> hand over index -> iterate over size of query workload
				python3.8 network.py #call network.py to overwrite nodes, rates, etc
				#construct inev -> save partial inev
				python3.8 write_config_single.py
				python3.8 determine_all_single_selectivities.py 
				python3.8 generate_projections.py
				python3.8 combigen.py
				python3.8 computePlanCosts_aug.py 0 #TODO -> check what to pass for writing results
				# merged costs, at least for routing of prim events edit merges costs -> write
				python3.8 mergedcosts.py $a $k # a is iteration, k is wl size
				a=`expr $a + 1`	
				done
		b=`expr $b + 1`	
		rm partialInev	
		done
	done	
done
