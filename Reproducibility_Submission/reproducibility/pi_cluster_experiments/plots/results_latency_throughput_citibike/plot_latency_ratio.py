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
import re
     
query={1:"E,F,G,H",2:"C,D,E,I",3:"A,SEQ(D,I),F",4:"A,AND(B,I),E",  5:"E,F,C,H"}          
def extractLatencies_Flink(line): 
    pt = datetime.strptime(line[-16:][:-4],'%H:%M:%S.%f')
    total_msseconds = pt.second*1000 + pt.minute*60000 + pt.hour*3600000 + pt.microsecond/1000
    return total_msseconds  

def extractThroughput_Flink(line): 
    pt = datetime.strptime(line[-16:][:-4],'%H:%M:%S.%f')
    total_msseconds = pt.second*1000 + pt.minute*60000 + pt.hour*3600000 + pt.microsecond/1000
    return total_msseconds  
               
def extractLatency_INEv(line): 
    pt = datetime.strptime(line[:-4],'%H:%M:%S.%f')
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
    
    
def getLatencies_flink(file_name):
    latencies = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:        
            
             if row and "detection latency" in row[0]:
                # print(row[0])
                 latencies.append(int(row[0].split(":")[len(row[0].split(":"))-1]))
    return latencies            

def getLatencies_inev(file_name,ID):
    latencies = []
    with open(file_name) as csvfile:
        reader = csv.reader(csvfile,delimiter=';')
        for row in reader:      
             
             if row and "Complex" in row[0] and query[ID] in row[1]:       
                 latency = row[len(row)-1]                
                 latencies.append(extractLatency_INEv(latency))
             if ID == 4:
                 if row and "Complex" in row[0] and query[5] in row[1]:       
                     latency = row[len(row)-1]                
                     latencies.append(extractLatency_INEv(latency))
    return latencies  
    

def latency_per_folder_inev(folder_path,ID):
    latencies = []
    for root, dirs, files in os.walk(folder_path):
        for file_name in files:             
             if "out" in str(file_name):
                 latencies+=getLatencies_inev(folder_path+"/"+file_name,ID)                 
    return latencies


def iterate_folders_inev(directory_path_inev):
    experimentData = {}
    for entry in os.scandir(directory_path_inev):
        if entry.is_dir():
            ID = int(entry.name.split("_")[2][1])
            experimentData[ID] =latency_per_folder_inev(entry.path,ID)
    return experimentData

def iterate_folders_flink(directory_path):
    experimentData = {}
    for root, dirs, files in os.walk(directory_path):
        for file_name in files: 
            ID = int(file_name.split("_")[2][0])            
            if ID in experimentData.keys():
                experimentData[ID]+=getLatencies_flink(directory_path+"/"+file_name)
            else:
                experimentData[ID] = getLatencies_flink(directory_path+"/"+file_name)
    return experimentData                
                    
directory_path_flink  = "results_flink"
directory_path_inev  = "results_inev"

experimentData_flink = iterate_folders_flink(directory_path_flink)
experimentData_inev = iterate_folders_inev(directory_path_inev)


Q1 = [experimentData_flink[1],experimentData_inev[1]]
Q2 = [experimentData_flink[2],experimentData_inev[2]]
#Q3 = [experimentData_flink[3],experimentData_inev[3]]
#Q4 = [experimentData_flink[4],experimentData_inev[4]]

df_list = [Q1, Q2]#, Q3, Q4]
titles = ['Q1', 'Q2']#, 'Q3', 'Q4']
fig, axes = plt.subplots(1, 2, sharey = True)
plt.yscale("log")

plt.rcParams.update({'font.size':22})
fig.add_subplot(111, frameon=False)
plt.tick_params(labelcolor='none', top=False, bottom=False, left=False, right=False)
plt.ylabel("Latency (ms)")
 
for r in range(len(df_list)):
         axes[r].set_title(titles[r])        
         axes[r].set_xticklabels(['F','I'])
         axes[r].boxplot(df_list[r], whis=np.inf )


axes[0].set_xticklabels(['F','I'])
axes[1].set_xticklabels(['F','I'])
#axes[2].set_xticklabels(['26','74'])
#axes[3].set_xticklabels(['26','74'])

# plt.show()


# latencyResults = {}
# for ID in experimentData.keys():
#     latencyResults[ID] = getLR(experimentData[ID]["CC"],experimentData[ID]["MS"])

# myValues = [(latencyResults[id], TR_dict[id]) for id in IDs if id in latencyResults.keys()]
# x = [t[1] for t in myValues]
# y = [t[0] for t in myValues]

# plt.yscale("log")

# plt.scatter(x, y,alpha=0.6, s = 300,  zorder = 10)
# plt.rcParams.update({'font.size':20})
# plt.xlabel("Transmission Ratio")
# plt.ylabel('Latency Ratio')
plt.savefig("../figs/Fig_5a_latency_citibike.pdf", format = 'pdf',  bbox_inches='tight')
