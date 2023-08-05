#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 23 12:08:24 2022

@author: samira
"""
# plot wl orders

import matplotlib.pyplot as plt
import pandas as pd 
import numpy as np
import csv
import sys
import argparse
import os

# for each file, compute variance, i.e. max diff in values, relative 
# for each filename, extract first nunmber as wl size
# assign values of variance dicte
# for path in myargs.inputs: # schemas are  equal or overlap



path = '.'
folder = os.fsencode(path)
filenames = []

for file in os.listdir(folder):
    filename = os.fsdecode(file)
    if filename.endswith( ('.csv') ): 
        filenames.append(filename)


mydata = {}

for path in filenames:     
        df = pd.read_csv(path)
        network = int(path.split('+')[0])  
        run = int(path.split('+')[1])
        size = int(path.split('+')[2].split('.')[0])      
        if network in mydata.keys():
            if run in mydata[network]:
                mydata[network][run][size] = df
            else:
                mydata[network][run] = {}
                mydata[network][run][size] = df
        else:
            mydata[network]  = {}
            mydata[network][run] = {}
            mydata[network][run][size] = df

ofInterest  = 2
#mydata = mydata[ofInterest]
toPlot = {}

# for key in mydata:
#     toPlot[key] = []
toPlot = {}
for network in mydata.keys():
    for run in mydata[network].keys():
        for size in mydata[network][run].keys():
                  if not size in toPlot.keys():
                      toPlot[size] = [np.std(mydata[network][run][size]["TransmissionRatio"].tolist())]
                  else:
                      toPlot[size].append(np.std(mydata[network][run][size]["TransmissionRatio"].tolist()))
                  print(size, np.std(mydata[network][run][size]["TransmissionRatio"].tolist()))
              
          #print(max(dataframe["TransmissionRatio"]), min(dataframe["TransmissionRatio"]))       
#         dif = max(dataframe["TransmissionRatio"]) - min(dataframe["TransmissionRatio"])
#         dev = dif / (min(dataframe["TransmissionRatio"])/100)
#         if dev > 0:
#             toPlot[key].append(dev)
        
print(toPlot)
plt.rcParams.update({'font.size':20})
plt.xlabel('Workload Size')
plt.ylabel('Stdev. Transmission Ratio')
labels, data = sorted(list(toPlot.keys())), toPlot.values()
plt.yscale("log")
plt.boxplot(data)
plt.xticks(range(1, len(labels) + 1), labels)
plt.savefig("figs/Fig_7c_wl_order.pdf", format = 'pdf',  bbox_inches='tight')

#plt.show()