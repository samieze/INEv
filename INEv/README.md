#INEv Algorithms



## Scripts

## Schema of Results
Results of an experiment can be found in `res/`. Each result file contains among others the following metric of the experiment parameters and INEv graphs constructed during the respective experiment:
- ID
- TransmissionRatio
- Filters (used output selectors)
- Network Parameters (EventSkew, EventNodeRatio, Number of Eventtypes, NetworkSize, Outdegree)
- Query Parameters (Size of Queryworkload, Length of Query, Median Selectivity, Minimal Selectivity)
- Computation Time for Placement and Combination Construction

## Plotting Results

The results in the `res/` folder can be plotted using `plot.py`, e.g., the following command generates a plot for the resulting files of the eventSkew_single experiment:

`python3.8 plot.py -i eventSkew7+0.1.csv eventSkew7+0.01.csv eventSkew7+0.001.csv -x EventSkew -y TransmissionRatio -l 0.1 0.01 0.001 -o eventSkew_single`

Resulting plots are saved in `figs/`.

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
For each INEv graph `_INEv.txt`, a corresponding plan for a centralized placement `_Centralized.txt` saved in the folder.
The prefix `_os` denotes that output selectors were used in the INEv graph.
A plan can be used as input to our DCEP engine by passing its path as input parameter.
