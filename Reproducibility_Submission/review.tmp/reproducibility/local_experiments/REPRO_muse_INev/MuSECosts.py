#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Sep  1 15:09:38 2022

@author: samira
"""
import sys
import csv
from EvaluationPlan import *
from generate_projections import *
import pickle
import math 



filename = "None"


#with open('EvaluationPlan', 'rb') as EvaluationPlan_file: 
#         myplan = pickle.load(EvaluationPlan_file)[0]
  
with open("allPairs", "rb") as allPairs_file:
    allPairs = pickle.load(allPairs_file)

with open('graph',  'rb') as graph_file:
    G = pickle.load(graph_file)    

    
with open('ExperimentResults',  'rb') as result_file:
    results = pickle.load(result_file)    
    
with open('musegraph',  'rb') as muse_file:
    musegraph = pickle.load(muse_file)    
    
filename = results[5]
  
def getTuples(mylist):
    if mylist:
        if isinstance(mylist[0], list):
            myTuples = []
            for i in mylist:
                myTuples += getTuples_single(i)
            return list(set(myTuples))
        else:
            return  getTuples_single(mylist)
    else:
        return []

def getTuples_single(mylist):
     
    newlist = []
    if len(mylist) > 0:
        if isinstance(mylist[0], tuple):
            return mylist
        else: 
            for i in range(len(mylist) - 1):
                newlist.append((mylist[i],mylist[i+1] ))
                
    return newlist


placement_dict = nodes
combi_dict = {}
mnprojs = []
MSTypes = []
# compute projection rates (additionally to proj rates)
# for k in myplan.projections:   
#   #  print(k.name.name, list(map(lambda x: str(x), k.name.combination.keys())), list(set(k.name.sinks)))
#     placement_dict[k.name.name] = list(set(k.name.sinks))
#     combi_dict[k.name.name]  = k.name.combination.keys()
#     if len(list(set(k.name.sinks))) > 1:
#         mnprojs.append(k.name.name)
        
        
for k in musegraph.keys():
    placement_dict[k] =  musegraph[k][1]
    combi_dict[k]     =  musegraph[k][0]
    if len(placement_dict[k])>1:
        mnprojs.append(k)
        MSTypes.append(musegraph[k][2])



def getCom(mylist):
    return [(mylist[i],mylist[i+1]) for i in range(len(mylist)) if i < len(mylist) -1 ]    

def traverseList(source, mylist): 

    for i in range(len(mylist)):

        if mylist[i]==source:
            myindex = i
    firstpart = mylist[:myindex+1]
    firstpart.reverse()
    secondpart = mylist[myindex:]    
    mytuples = getCom(firstpart)
    mytuples += getCom(secondpart)
    return mytuples



routing_dict = {}
for projection in combi_dict.keys():
    for sink in placement_dict[projection]:
        for ingredient in combi_dict[projection]:
            if not ingredient in MSTypes:
                if not ingredient in routing_dict.keys():
                    routing_dict[ingredient] = {}
                for source in placement_dict[ingredient]:
                    shortest = nx.shortest_path(G, source, sink, method='dijkstra') 
                    shortest = traverseList(source, shortest)
                    if not source in placement_dict[projection]: # fix that a source that is a sink in one context does not have to be a MN placement, maybe just remove dicts of mn types after this loop
                        if not source in routing_dict[ingredient].keys():
                            routing_dict[ingredient][source] = shortest
                        else:
                            routing_dict[ingredient][source] = list(set(routing_dict[ingredient][source] + shortest))
                        

print(routing_dict)
costs = 0                
for projection in routing_dict.keys():   
    for source in routing_dict[projection].keys():
        if len(routing_dict[projection].keys()) > 0:
            etbsPerSource = len(routing_dict[projection])
            costs += (totalRate(projection)/etbsPerSource) * len(routing_dict[projection][source])
        # for each source of ingredient, get shortest path, check that pathes have edges, tuples
        # maintain dict with first key on type and second on etb whereas latter only for ms and single event type applies
        # unifiy paths
        # write function that gets costs from forwarding dict

#print(routing_dict)

#for i in routing_dict.keys():
  #  print(i, len(sum(list(routing_dict[i].values()),[])) * (totalRate(i)/len(list(routing_dict[i].keys()))))
print("MUSECOSTS", costs, results[2])     


#schema = ["ID", "TransmissionRatioINEV", "TransmissionRatioMuSE", "EventSkew"] 
schema = ["ID", "TransmissionRatio", "EventSkew", "Nodes"] 

myResult = [results[0], costs/results[2], results[3],  results[4]] 
  
new = False
try:
        f = open("res/"+filename+"_Muse.csv")   
except FileNotFoundError:
        new = True           

        
with open("res/"+filename+"_Muse.csv", "a") as result:
      writer = csv.writer(result)  
      if new:
          writer.writerow(schema)              
      writer.writerow(myResult)
      
