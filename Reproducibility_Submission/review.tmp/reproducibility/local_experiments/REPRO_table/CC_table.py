#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 31 21:24:11 2023

@author: samira
"""
import os 
import networkx as nx 
import pickle
import multiprocessing

CC_table = {"citibike":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}, "google":{1:{5:0,10:0,20:0,30:0,50:0},2:{5:0,10:0,20:0,30:0,50:0},3:{5:0,10:0,20:0,30:0,50:0},4:{5:0,10:0,20:0,30:0,50:0}}}

queries_cb = {1:"E,F,G,H",2:"C,D,E,I",3:"A,D,I,F",4:"A,B,I,F,E,C,H"}
queries_google = {1:"A,H,B,I",2:"A,B,G,F,I",3:"I,B,H,G,D",4:"B,C,F,H"}
with open('graph_5',  'rb') as graph_file:
     G5 = pickle.load(graph_file)
with open('graph_10',  'rb') as graph_file:
     G10 = pickle.load(graph_file)    
with open('graph_20',  'rb') as graph_file:
     G20 = pickle.load(graph_file)       
with open('graph_30',  'rb') as graph_file:
     G30 = pickle.load(graph_file)       
with open('graph_50',  'rb') as graph_file:
     G50 = pickle.load(graph_file)        


def getAllPairs(G):
    myNodes = list(G.nodes)
    allPairs = [[] for x in myNodes]
    for i in range(len(allPairs)):
        allPairs[i] = fillMyMatrice(G,i)
    return allPairs

    
def fillMyMatrice(G,me):  
    myDistances = []
    for j in range(len(G.nodes)):            
           myDistances.append(len(nx.shortest_path(G, me, j, method='dijkstra')) - 1)   
    return myDistances


allPairs5 = getAllPairs(G5)
allPairs10 = getAllPairs(G10)
allPairs20 = getAllPairs(G20)
allPairs30 = getAllPairs(G30)
allPairs50 = getAllPairs(G50)

centralized = {5:[],10:[],20:[],30:[],50:[]}
centralized[5] = [x for x in allPairs5 if sum(x) == min([sum(y) for y in allPairs5])][0]
centralized[10] = [x for x in allPairs10 if sum(x) == min([sum(y) for y in allPairs10])][0]
centralized[20] = [x for x in allPairs20 if sum(x) == min([sum(y) for y in allPairs20])][0]
centralized[30] = [x for x in allPairs30 if sum(x) == min([sum(y) for y in allPairs30])][0]
centralized[50] = [x for x in allPairs50 if sum(x) == min([sum(y) for y in allPairs50])][0]

def count_lines_in_text_file_citi(file_path,query): #CITIBIKE
    line_count=0
    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.split(",")[1] and line.split(",")[1][0] in queries_cb[query]:
                        line_count +=1
    except FileNotFoundError:
        print("File not found at the given path.")
        return None
    return line_count


def count_lines_in_text_file_google(file_path,query): #google
    line_count=0

    try:
        with open(file_path, 'r') as file:
            for line in file:
                if line.split(",")[1] and line.split(",")[1][0] in queries_google[query]:
                        line_count +=1
    except FileNotFoundError:
        print("File not found at the given path.")
        return None    

    return line_count

for dataset in ["citibike", "google"]:
    for partitioning in [5,10,20,30,50]:
        for query in [1,2,3,4]:        
            if dataset == "citibike":
                    path = "citibike/"+str(partitioning)+"/inev"
                    files_and_subdirs = os.listdir(path)
                    for filename in files_and_subdirs:
                           if "hm" in filename:
                               nodeID = int(filename.split("_")[2].split(".")[0])
                               CC_table["citibike"][query][partitioning] += centralized[partitioning][nodeID] * count_lines_in_text_file_citi(os.path.join(path, filename),query)
            else:
                path = "google/"+str(query)+"/"+str(partitioning)    
                files_and_subdirs = os.listdir(path)
                for filename in files_and_subdirs:
                                        if "hm" in filename:
                                            nodeID = int(filename.split("_")[2].split(".")[0])
                                            CC_table["google"][query][partitioning] += centralized[partitioning][nodeID] * count_lines_in_text_file_google(os.path.join(path, filename),query)
                                            
#print(CC_table)                                            
           