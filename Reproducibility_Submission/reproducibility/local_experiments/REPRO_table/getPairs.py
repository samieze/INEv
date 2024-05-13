#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 21 18:08:06 2023

@author: samira
"""
import csv
import os
from CC_table import *

for dataset in CC_table.keys():
    for q in CC_table[dataset].keys():
        for part in CC_table[dataset][q].keys():
            if CC_table[dataset][q][part] == 0:
                CC_table[dataset][q][part] = 1

allPairs = allPairs10
allPairsDict = {}
for k in range(len(allPairs)):
    allPairsDict[k]={}
    for dest in range(len(allPairs[k])):
        allPairsDict[k][dest]=allPairs[k][dest]

queries = {'cb10':{1:"E,F,G,H",2:"C,D,E,I",3:"A,D,I,F",4:"A,B,I,F,E,C,H"}, 'cluster10':{1:"A,H,B,I",2:"A,B,G,F,I",3:"I,B,H,G,D",4:"B,C,F,H"}}

def read_file_row_by_row(filename, ID, query, dataset):
    
    # want dict {nodeID: {nodeIDRecipient:occurrences*hops}}
    costs = 0
    try:
        with open(filename, 'r') as file:
            if dataset == "cb10":
                for line in file:
                   if int(line.split(",")[3]) in list(allPairsDict.keys()) and line.split(",")[1] in queries[dataset][query]: 
                       costs += allPairsDict[ID][int(line.split(",")[3])]
            else:
                 for line in file:
                   if int(line.split(",")[4]) in list(allPairsDict.keys()) and line.split(",")[1] in queries[dataset][query]: 
                       costs += allPairsDict[ID][int(line.split(",")[4])]
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
    except IOError:
        print(f"Error reading file '{filename}'.")
    return costs

def read_files_in_directory(directory_path, query):
    costs = 0
    try:
        files = os.listdir(directory_path)
        for file_name in files:
            file_path = os.path.join(directory_path, file_name)
            if os.path.isfile(file_path):
                #print(f"Reading file: {file_name}")
                node_ID= file_path.split("_")[2][0]
                costs += read_file_row_by_row(file_path,int(node_ID),query, directory_path)

    except FileNotFoundError:
        print(f"Directory '{directory_path}' not found.")
    except PermissionError:
        print(f"Permission denied for directory '{directory_path}'.")
    return costs   

for query in [1,2,3,4]:
    for dataset in ['cb10', 'cluster10']:
                    costs =  read_files_in_directory(dataset, query)
                    print(dataset,query,costs)
                    if dataset == 'cb10':
                        mydataset = 'citibike'
                    elif dataset == 'cluster10':
                        mydataset = 'google'
                    myResult = [mydataset, query, 10, costs/CC_table[mydataset][query][10], "True", "Flink"]                  
                    #myResult = [mydataset, query, 10, costs/centralizedCosts["cluster10"][query], "Flink"]         
                            
                    with open("res/table.csv", "a") as result:
                          writer = csv.writer(result)  
                          writer.writerow(myResult)

