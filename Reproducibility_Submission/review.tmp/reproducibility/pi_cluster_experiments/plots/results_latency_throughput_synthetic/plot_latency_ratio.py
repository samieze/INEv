#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 20 22:23:44 2022

@author: samira
"""

from datetime import datetime
import csv
from datetime import datetime
import os
import numpy as np
import matplotlib.pyplot as plt


IDs = [1539294, 159823, 1760538, 2044060, 2283428, 2333799, 2993699, 3048756, 3487303, 4169565, 4216043, 4253129, 4335269, 4458057, 4534045, 4983802, 5186997, 5398168, 5536775, 5561997, 6016817, 6270657, 6638974, 7019636, 8043516, 8246193, 9025015, 9303418, 9581457, 9709975]
TR_dict = {}
with open("None.csv") as csvfile:
            myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in myreader:
                TR_dict[int(row[0])] = float(row[1])
                
                
def extractLatency(line):
    pt = datetime.strptime(line[-16:][:-4],'%H:%M:%S.%f')
    total_msseconds = pt.second*1000 + pt.minute*60000 + pt.hour*3600000 + pt.microsecond/1000
    return total_msseconds

def usable(latencies):
    if sorted(latencies) == latencies:
        return False
    else:
        return True

def getLR(ccValues, msValues):
    if not ccValues or not usable(ccValues):
        return np.inf
    if not msValues or not usable(msValues):
        return -np.inf
    else:
        return np.median(msValues)/np.median(ccValues)
    
    
def getLatencies(file_name):
    latencies = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:             
             if row and "Complex" in row[0]:
                 latencies.append(extractLatency(row[len(row)-1]))
    return latencies            

    

def latency_per_folder(folder_path):
    latencies = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:             
             if "out" in str(file_name):
                 latencies += getLatencies(folder_path+"/"+file_name)
    return latencies


def iterate_folders(directory_path):
    experimentData = {}
    for entry in os.scandir(directory_path):
        if entry.is_dir():
            experimentData[int(entry.name)]={}
            for subdir in os.scandir(entry.path):
                if "CC" in str(subdir):
                    experimentData[int(entry.name)]["CC"] =latency_per_folder(subdir.path)
                elif "MS" in str(subdir):
                    experimentData[int(entry.name)]["MS"] = latency_per_folder(subdir.path)
    return experimentData                
                    
directory_path  = "results-lt-final"
experimentData = iterate_folders(directory_path)
print(experimentData)

latencyResults = {}
for ID in experimentData.keys():
    latencyResults[ID] = getLR(experimentData[ID]["CC"],experimentData[ID]["MS"])

myValues = [(latencyResults[id], TR_dict[id]) for id in IDs if id in latencyResults.keys()]
x = [t[1] for t in myValues]
y = [t[0] for t in myValues]

plt.yscale("log")

plt.scatter(x, y,alpha=0.6, s = 300,  zorder = 10)
plt.rcParams.update({'font.size':20})
plt.xlabel("Transmission Ratio")
plt.ylabel('Latency Ratio')
plt.savefig("../figs/Fig_5c_latency_synthetic.pdf", format = 'pdf',  bbox_inches='tight')
#plt.show()
