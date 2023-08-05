cp -r results-lt-final plots/results_latency_throughput_synthetic
cd plots/results_latency_throughput_synthetic
python3.8 plot_latency_ratio.py
python3.8 plot_throughput_ratio.py
