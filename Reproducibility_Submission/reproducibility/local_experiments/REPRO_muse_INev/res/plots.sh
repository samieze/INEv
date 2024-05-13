#!/bin/sh


#MuSE INEv Comp
python3.8 plot.py -i  nw_Muse.csv nw_Inev.csv -x Nodes -y TransmissionRatio -l  Muse INEv -o Fig_4d_nwSize.pdf
python3.8 plot.py -i  skew_Muse.csv skew_Inev.csv -x EventSkew -y TransmissionRatio -l Muse INEv -o Fig_4c_skew.pdf
