#!/bin/sh
echo "conflicting"
./conflicting_qwl.sh
echo "EventSkew"
./eventSkew_qwl.sh
echo "NWSize"
./nwSize_qwl.sh
echo "EventNode"
./eventNode_qwl.sh
echo "Lower Bound"
./lower_bound.sh
echo "NSEQ, KLEENE"
./negated_unnegated.sh
echo "Computation Time"
./computation_time.sh
cd ../res
./plots.sh
cd figs
cp * ../../../Figures
