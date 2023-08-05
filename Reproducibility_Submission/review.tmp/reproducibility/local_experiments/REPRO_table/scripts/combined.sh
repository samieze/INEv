cd ..
echo "Starting Experiments for Citibike Dataset"
./generate_res_DCEP_citibike
echo "Starting Experiments for Google Cluster Dataset"
./generate_res_DCEP_google
python3.8 get_res_inev_muse.py
echo "Starting Computation of PPoP results"
cd bin_PPoP
./start.sh
cd ..
python3.8 get_res_inev_muse.py
cd res
cp * ../../Figures
