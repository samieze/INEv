#!/bin/sh


#MuSE INEv Comp
python3.8 plot.py -i nw_Inev.csv nw_Muse.csv -x Nodes -y TransmissionRatio -l INEv Muse -o Fig_4d_nwSize.pdf
python3.8 plot.py -i skew_Inev.csv skew_Muse.csv -x EventSkew -y TransmissionRatio -l INEv Muse -o Fig_4c_skew.pdf
