#!/bin/sh
# lowerbound -> to parametrize
python3.8 switchRows.py
python3.8 plot_generic.py -i lower+0.01.csv lower+0.01_real.csv lower+0.001.csv lower+0.001_real.csv -x EventSkew -y TransmissionRatio -l INEv0.1 lower0.1 INEv0.01 lower0.01 -o Fig_5_lowerbound
python3.8 plot_generic.py -i QWL+5.csv QWL+10.csv QWL+20.csv -x EventTypes -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_7a_overlap.pdf # OVERLAP
python3.8 plot_generic.py -i eventSkew_qwl+5.csv eventSkew_qwl+10.csv eventSkew_qwl+20.csv -x EventSkew -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_7b_eventSkew.pdf # eventSkew
python3.8 plot_generic.py -i eventNode_qwl+5.csv eventNode_qwl+10.csv eventNode_qwl+20.csv -x EventNodeRatio -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_7d_eventNodeRatio.pdf #eventNodeRatio
python3.8 plot_generic.py -i nwSize_qwl+5.csv nwSize_qwl+10.csv nwSize_qwl+20.csv -x Nodes -y TransmissionRatio -l QWL5 QWL10 QWL20 -o Fig_7c_Nodes.pdf #NWSize
### KLEENE & NSEQ 

python3.8 plot_generic.py -i KL+min+1.csv KL+min+0.csv KL+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_KL min_nKL max_KL max_nKL -o Fig_8a_Kleene.pdf # KLEENE, no KLeene

python3.8 plot_generic.py -i NSEQ+min+1.csv KL+min+0.csv NSEQ+max+1.csv KL+max+0.csv -x EventSkew -y TransmissionRatio -l min_NSEQ min_SEQ max_NSEQ max_SEQ -o Fig_8b_NSEQ.pdf # NSEQ, no NSEQ

#computation Time
#merge all csv files for computation time projection

python3.8 plot_generic_scatter.py -i eventSkew_qwl+20.csv  -x NumberProjections -y CombigenComputationTime -o Fig_12_computationTime_Projections
python3.8 plot_generic_scatter.py -i computationTime.csv -x EventTypes -y CombigenComputationTime -o Fig_12_computationTime_QueryLen



