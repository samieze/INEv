cp -r results-cb plots/results_latency_throughput_citibike
cp -r flink-experiment/results_flink plots/results_latency_throughput_citibike
cd  plots/results_latency_throughput_citibike
mv results-cb results_inev
python3 plot_latency_ratio.py
python3 plot_throughput_ratio.py
