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

def getLatencies_flink(file_name):
    latencies = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:                    
             if row and "Throughput" in row[0]:
                 latencies.append(int(row[0].split(":")[len(row[0].split(":"))-1]))
    return latencies   




def throughput_per_folder_inev(foldername):
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


def getThroughputs_flink(filepath):
    myDict = {}
    with open(filepath) as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        for row in reader:                    
             if len(row) > 1 and "Throughput" in row[1]:
                 myID = row[0].split("seconds")[0]
                 if int(myID)<1000:
                     myDict[int(myID)] = int(row[1].split(":")[1])
    return myDict       
      
def iterate_folders_inev(directory_path_inev):
    experimentData = {}
    for entry in os.scandir(directory_path_inev):
        if entry.is_dir():
            ID = int(entry.name.split("_")[2][1])
            experimentData[ID] = throughput_per_folder_inev(entry.path)
    return experimentData

def initializeExperimentData():
    throughputs = []
    experimentData = {}
    for j in range(10000):
        throughputs.append(0)
    for ID in [1,2,3,4]:
        experimentData[ID] = {k:0 for k in throughputs}
    return  experimentData


def iterate_folders_flink(directory_path):
    experimentData = {}
    for root, dirs, files in os.walk(directory_path):
        for file_name in files: 
            ID = int(file_name.split("_")[2][0])            
            if ID in experimentData.keys():
                addDict = getThroughputs_flink(directory_path+"/"+file_name)
                for k in  addDict.keys():
                        experimentData[ID][k] += addDict[k]
                       # print(ID,k, experimentData[ID][k])
            else:
                experimentData[ID] = getThroughputs_flink(directory_path+"/"+file_name)
    for k in experimentData.keys():
        experimentData[k] = list(experimentData[k].values())
        experimentData[k] = [x for x in experimentData[k] if not x == 0]           
    return experimentData   
    
directory_path_flink  = "results_flink"
directory_path_inev  = "results_inev"

experimentData_flink = iterate_folders_flink(directory_path_flink)
experimentData_inev = iterate_folders_inev(directory_path_inev)
print(experimentData_flink)

Q1 = [experimentData_flink[1],experimentData_inev[1]]
Q2 = [experimentData_flink[2],experimentData_inev[2]]
# #Q3 = [experimentData_flink[3],experimentData_inev[3]]
# #Q4 = [experimentData_flink[4],experimentData_inev[4]]

df_list = [Q1, Q2]#, Q3, Q4]
titles = ['Q1', 'Q2']#, 'Q3', 'Q4']
fig, axes = plt.subplots(1, 2, sharey = True)
plt.yscale("log")

plt.rcParams.update({'font.size':22})
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.ylabel("Throughput per Second")
 
for r in range(len(df_list)):
          axes[r].set_title(titles[r])        
          axes[r].set_xticklabels(['F','I'])
          axes[r].boxplot(df_list[r], whis=np.inf )


axes[0].set_xticklabels(['F','I'])
axes[1].set_xticklabels(['F','I'])
plt.savefig("../figs/Fig_5b_throughput_citibike.pdf", format = 'pdf',  bbox_inches='tight')
