#!/bin/sh


#MuSE INEv Comp
python plot.py -i nw_Inev.csv nw_Muse.csv -x Nodes -y TransmissionRatio -l INEv Muse -o Fig_4d_nwSize.pdf
python plot.py -i skew_Inev.csv skew_Muse.csv -x EventSkew -y TransmissionRatio -l INEv Muse -o Fig_4c_skew.pdf
