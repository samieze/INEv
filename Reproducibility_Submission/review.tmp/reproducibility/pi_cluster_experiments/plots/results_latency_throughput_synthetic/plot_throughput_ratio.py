#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 29 11:50:53 2021

@author: samira
"""
import csv
import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import os



IDs = [1539294, 159823, 1760538, 2044060, 2283428, 2333799, 2993699, 3048756, 3487303, 4169565, 4216043, 4253129, 4335269, 4458057, 4534045, 4983802, 5186997, 5398168, 5536775, 5561997, 6016817, 6270657, 6638974, 7019636, 8043516, 8246193, 9025015, 9303418, 9581457, 9709975]
TR_dict = {}
with open("None.csv") as csvfile:
            myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in myreader:
                TR_dict[int(row[0])] = float(row[1])



def generateArray(foldername):
    troughputs = []
    for j in range(1000):
        troughputs.append(0)
    for i in [0,1,2,3,4,5,6,7,8,9]:
        with open(foldername+"/"+str(i)+".csv") as csvfile:
            myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in myreader:
                if (len(row[0]) < 6):
                     troughputs[myreader.line_num] += int(row[0])
    troughputs = [x for x in troughputs if x != 0]
 
    return [x for x in troughputs if x != 0]
  
def generateArray_OP(filename):    
     troughputs = []
          
     with open(filename+".csv") as csvfile:
            myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in myreader:
                if (len(row[0]) < 6):
                     troughputs.append(int(row[0]))
     troughputs = [x for x in troughputs if x != 0]    
     return troughputs#[:1800]

def new_ThroughputArray(file):
    throughputs = []
    with open(file) as csvfile:
            myreader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in myreader:
                if (len(row[0]) < 6):
                     throughputs.append(int(row[0]))
    #throughputs = [x for x in throughputs if x < np.average(throughputs)/10]    
    return  throughputs


def add(array1, array2):    
    for i in range(len(array1)):
        if len(array2) > i:
            array1[i] += array2[i]
    return array1

def cleanArray(myarray):    
    myarray = [x for x in myarray if x > np.average(myarray) / 10]
    return  myarray

def iterate_folders(directory_path):
    experimentData = {}
    for entry in os.scandir(directory_path):
        if entry.is_dir():
            experimentData[int(entry.name)]={}
            for subdir in os.scandir(entry.path):
                if "CC" in str(subdir):
                    experimentData[int(entry.name)]["CC"] =generateArray(subdir.path)
                elif "MS" in str(subdir):
                    experimentData[int(entry.name)]["MS"] = generateArray(subdir.path)
    return experimentData    
    
mydict = {}
directory_path = "results-lt-final"
mydict = iterate_folders(directory_path)
throughputResults = {}
for filename in mydict.keys():
     throughputResults[filename]= np.average(mydict[filename]['MS'])/ np.average(mydict[filename]['CC'])

#compressedDict = mydict
#for k in mydict.keys():
 #   compressedDict[k] = mydict[k]['div']

myValues = [(throughputResults[id], TR_dict[id]) for id in IDs if id in throughputResults.keys()]

x = [t[1] for t in myValues]
y = [t[0] for t in myValues]

plt.yscale("log")

plt.scatter(x, y,alpha=0.6, s = 300,  zorder = 10)
plt.rcParams.update({'font.size':20})
plt.xlabel("Transmission Ratio")
plt.ylabel('Throughput Ratio')
plt.savefig("../figs/Fig_5d_throughput_synthetic.pdf", format = 'pdf',  bbox_inches='tight')
#plt.show()