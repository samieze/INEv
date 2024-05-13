#!/bin/bash -x

cd ../inputexamples
for file in *; do
    for k in 0 10 20 30 50 70; do  # Added 'done' here
        echo "$file"
        ./../bin/DCEP.Simulation ../inputexamples/"$file" -w 1 -d 10 -t Minute -v $k --name bla > "$file+$k.txt" &

        sleep 605
    done  
done

cd ../res
python3.8 plot_variance.py
cd figs
cp * ../../../Figures
