#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 15:10:35 2023

@author: samira
"""
import os
import re
import matplotlib.pyplot as plt
import numpy as np
folder_path = "../inputexamples"  # Replace with the actual path to your folder
data = {}

# Iterate over files in the folder
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt") and "MS" in file_name:
        file_path = os.path.join(folder_path, file_name)
        
        # Extract the number after the last "+" in the file name
        match = re.search(r"\+(\d+)\.txt", file_name)
        if match:
            x_value = int(match.group(1))
            # Extract the prefix before the first underscore in the file name
            prefix = file_name.split("_")[0]
            with open(file_path, "r") as file:
                # Read the lines and search for the line with the event count
                for line in file:
                    match = re.search(r"Total number of events sent over network:  (\d+)", line)
                    if match:
                        num_events = int(match.group(1))
                        # Update the data dictionary with the prefix and numEvents values
                        if x_value in data:
                            if prefix in data[x_value]:
                                    data[x_value][prefix] = num_events
                            else:
                                data[x_value][prefix] = num_events
                        else:
                            data[x_value] = {prefix: num_events}
                            

                     
for file_name in os.listdir(folder_path):
    if file_name.endswith(".txt") and "CC" in file_name:
        file_path = os.path.join(folder_path, file_name)
        
        # Extract the number after the last "+" in the file name
        match = re.search(r"\+(\d+)\.txt", file_name)
        if match:
            x_value = int(match.group(1))
            # Extract the prefix before the first underscore in the file name
            prefix = file_name.split("_")[0]
            with open(file_path, "r") as file:
                # Read the lines and search for the line with the event count
                for line in file:
                    match = re.search(r"Total number of events sent over network:  (\d+)", line)
                    if match:
                        num_events = int(match.group(1))
                        # Update the data dictionary with the prefix and numEvents values
                        if x_value in data.keys():
                            if prefix in data[x_value].keys():
                                data[x_value][prefix] = data[x_value][prefix]/ num_events

toRemove = []
for variancevalue in data.keys():
    for experiment in data[variancevalue]:
        if data[variancevalue][experiment] > 1:
            toRemove.append(experiment)

for k in toRemove:     
    for var in [0,10,20,30,50,70]:
        del data[var][k]


# Sort the averaged data by x-value
points = sorted([(key, np.average(list(data[key].values()))) for key in data.keys()])
x_values = [point[0] for point in points]
y_values = [point[1] for point in points]
# Generate the plot
plt.rcParams.update({'font.size':17})
plt.yscale("log")
plt.plot(x_values, y_values, marker = "o")
plt.xlabel("Variance in %")
plt.ylabel("Transmission Ratio")
plt.savefig("figs/Fig_8e_variance", format = 'pdf',  bbox_inches='tight')