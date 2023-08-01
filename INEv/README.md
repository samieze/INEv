# INEv Algorithms

This folder contains the algorithms used to construct INEv graphs for a given network, query workload, network topology and set of selectivities. To this end, it also contains generators for networks and workloads for given characteristics.

## Scripts
The scripts contained can reproduce the following subset of the experiments presented in the paper, e.g.:
- *\_qwl execute set a of experiments for query workloads of varying sizes for networks with different event rate distributions (./eventSkew_qwl), event node distributions (./eventNode) and number of nodes (./nwSize)
- conflicting_qwl to reproduce performance of multi-query scenario with varying overlap in event types between queries

Using the `eventSkew_qwl_plan.sh`, saves for each experiment the resulting INEv graphs as well as their counter part for a centralized evaluation in the `plans/` folder. 

Please note, that only only one script can be executed at a time.


## Schema of Results
Results of an experiment can be found in `res/` folder. Each result file contains among others the following  experiment parameters and metrics of the INEv graphs constructed during the respective experiment:
- ID
- TransmissionRatio
- Filters (used output selectors)
- Network Parameters (EventSkew, EventNodeRatio, Number of Eventtypes, NetworkSize, Outdegree)
- Query Parameters (Size of Queryworkload, Length of Query, Median Selectivity, Minimal Selectivity)
- Computation Time for Placement and Combination Construction

## Plotting Results

The results in the `res/` folder can be plotted using `plot.py`, e.g., the following command generates a plot for the resulting files of the eventSkew_single experiment:

`python3.8 plot.py -i eventSkew_5.csv eventSkew_10.csv eventSkew_20.csv -x EventSkew -y TransmissionRatio -l 5 10 20 -o eventSkew_qwl`

Resulting plots are saved in `figs/`.

### Parameters for plot script
Parameter | Meaning
------------ | -------------
-i| Required. Input File(s)
-x| Required. Column in input file(s) to use as x-axis
-y |  Required. Column in input file(s) to use as y-axis
-l |  Required. Labels for line types
-o |  Optional. Name for output file (saved in `figs/` folder) 
-box |  Optional. Adds boxplot for each value

## Evaluation Plans

Using the `_plan.sh`-version of a script, saves for each experiment the resulting INEv graphs in the `plans/` folder. 
The name of an INEv graph plan corresponds to the IDs in the result file for the experiment.
For each INEv graph `_INEv.txt`, a corresponding plan for a centralized placement `_Centralized.txt` is also saved in the  `plans/` folder.
The prefix `_os` denotes that output selectors were used in the INEv graph.
A plan can be used as input to our DCEP engine by passing its path as input parameter.
