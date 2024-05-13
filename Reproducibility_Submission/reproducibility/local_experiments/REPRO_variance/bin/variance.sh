#!/bin/bash -x
DIRECTORY=/vol/home-vol2/svt/akilsami/reproducibility_sigmod_23/INEv/DCEP_Ambrosia/inputexamples/variance
for file in "$DIRECTORY"/*; do
for k in 0 10 20 30 50 70; do
     ./DCEP.Simulation $file -w 1 -d 10 -t Minute -v $k --name bla > $file+_+$k.txt & 	
    echo "starting $file..."	
    sleep 660
done
done
