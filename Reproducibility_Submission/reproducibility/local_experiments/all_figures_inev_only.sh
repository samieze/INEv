#!/bin/bash
# only simulation / INEv algorithms
cd REPRO_muse_INev/scripts
./combined.sh &
cd ../../REPRO_PPoP_INev/scripts
./combined.sh &
cd ../../REPRO_multiquery/scripts
./combined.sh &
cd ../../REPRO_timewindows/scripts
./combined.sh &
cd ../../REPRO_basic/scripts 
./combined.sh &
cd ../../REPRO_wlorder/scripts
./combined.sh &
cd ../../REPRO_adaptivity/scripts
./combined.sh &


