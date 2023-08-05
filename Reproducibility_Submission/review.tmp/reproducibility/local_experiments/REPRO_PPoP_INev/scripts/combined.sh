#!/bin/sh
cd ../code


python3.8 generate_network.py 20 0.5 1.1 6
python3.8 generate_qwls.py 7 1
python3.8 generate_graph.py
python3.8 allPairs.py

python3.8 generate_selectivity.py  0.01
for small in 0 1 
do
for j in  1.1 1.2 1.3 1.4 1.5 1.6 1.7 1.8 1.9 
do
		a=0
		while [ $a -lt 50 ]
		do
		python3.8 generate_network.py 20 0.5 $j 6 $small
		python3.8 write_config_single.py
		python3.8 determine_all_single_selectivities.py
		python3.8 generate_projections.py
		python3.8 combigen.py
		python3.8 computePlanCosts_aug.py INEv_small_+"$small"
	        python3.8 write_PP_config.py
		a=`expr $a + 1`
		done

done
done

cp -r PP_config_big ../bin
cp -r PP_config_small ../bin

cd ../bin
./start.sh
cd result
mv result_PPoP_big.csv ../../res
mv result_PPoP_small.csv ../../res

cd ../../res
python3.8 plot_generic.py -i result_PPoP_big.csv INEv_small_+0.csv -x EventSkew -y TransmissionRatio -l PPoP INEv -o PPoP_INEv_big 
python3.8 plot_generic.py -i result_PPoP_small.csv INEv_small_+1.csv -x EventSkew -y TransmissionRatio -l PPoP INEv -o PPoP_INEv_small
cd figs
cp * ../../../Figures
