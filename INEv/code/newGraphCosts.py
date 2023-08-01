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

  
with open("allPairs", "rb") as allPairs_file:
    allPairs = pickle.load(allPairs_file)

with open('graph',  'rb') as graph_file:
    G = pickle.load(graph_file)    
   
with open('ExperimentResults',  'rb') as result_file:
    results = pickle.load(result_file)
    
with open('EvaluationPlan', 'rb') as EvaluationPlan_file: 
          myplan = pickle.load(EvaluationPlan_file)[0]
  
myprojs = []
multinode = []
sources = {}
mycombi = {}
myrate = {}
myRouting = {}
placement_dict = nodes
routing_dict = {}
MSTypes = []



    #sinks = set(projection.name.sinks)
    #print(sinks)
    #for instance in projection.getInputInstances():
    #    sources = set(instance.sources)
    #    if sinks == sources:
    #        return instance.projname

        

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


def main():
    percentage = 0
    experiment = 'None'
         
    if len(sys.argv) > 1: 
      percentage = float(sys.argv[1])
      
    if len(sys.argv) >2 :
         if int(sys.argv[2]) == 0:          
              experiment = 'remove'
         elif int(sys.argv[2]) == 1:
              experiment = 'add'
         elif int(sys.argv[2]) == 2:
              experiment = 'permute'
    # 1. iterate through projections, get placements, combination, multi-node placed projections
    
    for k in myplan.projections:    
        myprojs.append(k.name.name) # list of projections
        mycombi[k.name.name] = k.name.combination.keys() # combination dict
        placement_dict[k.name.name] = k.name.sinks
        if len(k.name.sinks)>1:
            #print(myplan.getProjection(k.name.name))
            multinode.append(k.name.name) # multi-node placed projections      
            MSTypes.append(returnPartitioning(k.name.name, list(mycombi[k.name.name]))[0])
            
            
    # 2. for each source of ingredient, get shortest path, check that pathes have edges, tuples,  maintain dict with first key on type and second on etb whereas latter only for ms and single event type applies,  unifiy paths
    for projection in mycombi.keys():
         for sink in placement_dict[projection]:
             for ingredient in mycombi[projection]:
                 if not ingredient in MSTypes:
                    if not ingredient in routing_dict.keys():
                         routing_dict[ingredient] = {}
                    for source in placement_dict[ingredient]:
                         shortest = nx.shortest_path(G, source, sink, method='dijkstra') 
                         shortest = traverseList(source, shortest)
                         #if not source in placement_dict[projection]: # fix that a source that is a sink in one context does not have to be a MN placement, maybe just remove dicts of mn types after this loop
                         if not source in routing_dict[ingredient].keys():
                                     routing_dict[ingredient][source] = shortest
                         else:
                                     routing_dict[ingredient][source] = list(set(routing_dict[ingredient][source] + shortest))
    
    for x in routing_dict.keys():
        print(x)
        for k in routing_dict[x]:
            print(k, routing_dict[x][k])
    
    costs = 0                
    for projection in routing_dict.keys():   
         for source in routing_dict[projection].keys():
             if len(routing_dict[projection].keys()) > 0:
                 etbsPerSource = len(routing_dict[projection])
                 costs += (totalRate(projection)/etbsPerSource) * len(routing_dict[projection][source])
    
    print("Costs", costs)
    

    schema = ["ID", "TransmissionRatioINEV", "Change", "TransmissionRatioChange", "Nodes"] 
    
    myResult = [results[0], results[1], percentage,  costs/results[2], len(allPairs)] 
      
    new = False
    try:
         f = open("../res/" + experiment +".csv")   
    except FileNotFoundError:
            new = True           
    
            
    with open("../res/" + experiment +".csv", "a") as result:
           writer = csv.writer(result)  
           if new:
               writer.writerow(schema)              
           writer.writerow(myResult)
          
    
    # # get correct eval plans for engine...
if __name__ == "__main__":
    main()   