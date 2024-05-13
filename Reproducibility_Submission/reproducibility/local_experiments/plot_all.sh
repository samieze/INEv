# MuSE vs INEv Plots
cd REPRO_muse_INev/res
./plots.sh &

# PPoP vs INEv Plots
cd ../../REPRO_PPoP_INev/res
python3.8 plot_generic.py -i result_PPoP_big.csv INEv_small_+0.csv -x EventSkew -y TransmissionRatio -l PPoP INEv -o PPoP_INEv_big &
python3.8 plot_generic.py -i result_PPoP_small.csv INEv_small_+1.csv -x EventSkew -y TransmissionRatio -l PPoP INEv -o PPoP_INEv_small &

# Varying Network Parameters Plots
cd ../../REPRO_basic/res
./plots.sh &

# Multiquery Plots
cd ../../REPRO_multiquery/res
./plots.sh &

# Workload Order Plots
cd ../../REPRO_wlorder/res
./plots.sh &

# Timewindow Plots
cd ../../REPRO_timewindows/res
./plots.sh & 

# Adaptivity Plots
cd ../../REPRO_adaptivity/adaptivity_selectivity_change
python3.8 plot_adaptivity_brokenprojections.py &
cd ../adaptivity_swap_rates
./plots.sh & 
cd ../adaptivity_topology_change
python3.8 plot_topology_correct.py


