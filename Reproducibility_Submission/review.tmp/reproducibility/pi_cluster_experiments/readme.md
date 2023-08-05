# How to reproduce experiments run on raspberry pi cluster

## Prepare your local machine
 - This assumes Ubuntu 22.10 with bash
 - Install dependencies:
`sudo apt install python3 python3-venv rsync ansible-core`

## Preparing the cluster
### Option 1: Obtain and set up hardware using mythic beasts
We used 10 Raspberry Pis rented from the cloud service provider mythic beasts (https://mythic-beasts.com) for the experiments. 

Refer to the file README.md in the `provisonMythicBeasts` folder for a script for instructions on how to reproduce this setup using a mythic beasts account.
 
### Option 2: Set up your own pi cluster
- Set up 10x Raspberry Pi 4 1.5GHz 4GB RAM running Raspbian Buster 10 32 bit, in a 1 GBit Ethernet LAN
- Configure SSH to allow passwordless access to each of the the Pis under the (host) names `pi0` to `pi9` from this machine.

- Subsitute IP-Adresses in IPs.txt with the external IP addresses of all pis.

### Configure IPs
- Overwrite deploy/publish/IPs.txt and flink-experiment/IPs.txt with the IPs.txt file you created in the last step. 
- If not using mythic beasts, set the IPs in deploy/.ssh/config according to your IPs.txt (otherwise this is already done)

### Install software on Pis and setup ssh connectivity between PIs
- In the folder ./ansible, run the `setup-pis.yaml` playbook to cofigure the system:

`ansible-playbook ./setup-pis.yaml`

This will install required packages on the pis, ensure the pis have appropriate local hostnames (pi0...pi9), and ensure that all pis are reachable with passwordless ssh from pi0 under the names pi0 to pi9.  Finally it will copy the folders ./deploy to /root folder of the pis.

Ansible may take up to half an hour to run. If there are errors it may help to run the playbook again. The playbook is idempotent so it is not a problem to run them multiple times, and should run faster on the second run.

## Run Latency-Throughput Experiment for Synthetic Data

### Run experiments
- Log into pi0 (`ssh pi0`)
- Start tmux shell (`byobu`). This ensures the process will not stop if you disconnect from the cluster.
- Change into the "./publish" folder (`cd publish`)
- Run the experiment with

`./run-latency-throughput inputdata/latency_throughput_revision/*.txt`

The experiments run for about 48 hours.

### Collect results
After it has finished, run the following scripts locally (not on the pi) to collect the results:

`./latency-throughput--collect`

This should generate an output folder "./results-lt".

`./latency-throughput--create-final-folder`

This should generate an output folder "./results-lt-final".



## Run Latency-Throughput Experiment for Citibike Dataset
### Run experiment
- Log into pi0 (`ssh pi0`)
- Start tmux shell (`byobu`). This ensures the process will not stop if you disconnect from the cluster.
- Change into the "./publish" folder (`cd publish`)
- Run the experiment with
`./run-citibike.sh inputdata/citibike/citibike*.txt`

This should run for less than 6 hours.

### Collect results
After it has finished, run the following scripts locally (not on the pi) to collect the results:

./citibike--collect

This should generate an output folder "./results-cb".


## Run flink experiment

In the "./flink-experiment" folder, run the script "./run".
The experiment takes about 24h.
The respective results should appear in the folder "./flink-experiment/results_flink"


## Generate Plots

Run the script

`./generate_all_plots.sh`

to generate the plots for the latency and throughput experiments on synthetic data and the Citibike data set.
The resulting plots should appear in the folder "plots/figs"
















