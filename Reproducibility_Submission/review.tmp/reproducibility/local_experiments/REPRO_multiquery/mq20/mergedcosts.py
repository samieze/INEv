#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul  8 19:20:58 2022

@author: samira
"""

import sys
import csv
from EvaluationPlan import *
from generate_projections import *
import pickle
import math 



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

          
def getNewProjrates():
    myProjrates = {}
    for proj in myplan.projections:
        thisproj = proj.name.name          
        rate = thisproj.evaluate() * return_selectivity(thisproj.leafs())
        myProjrates[thisproj] = rate
    for eventtype in  rates.keys():
        myProjrates[eventtype] = rates[eventtype]
    return myProjrates    

def getTuples_single(mylist):
     
    newlist = []
    if len(mylist) > 0:
        if isinstance(mylist[0], tuple):
            return mylist
        else: 
            for i in range(len(mylist) - 1):
                newlist.append((mylist[i],mylist[i+1] ))
                
    return newlist

def getSingleSinkRouting(etbsource, destination):
    myshortest = nx.shortest_path(G, etbsource, destination, method='dijkstra')
    return getTuples(myshortest)

def getSingleNodeRoute(routingDict):
    finalroute = []
    for proj in routingDict.keys():
        if routingDict[proj]:
            if isinstance(routingDict[proj][0], int):
                finalroute.append(routingDict[proj])
    return finalroute

def getCosts(routing, rate, etbs):
    costs = 0 
    for i in routing.keys(): # new                                           
        costs += len(routing[i]) * rate[etbs[i][0]] * etbs[i][1]
    return costs

def getRoutingInfo(routingDict):
    finalroute = []
    for proj in routingDict.keys():
        finalroute.append(getTuples(routingDict[proj]))
    return list(set(sum(finalroute, [])))

def merge_projrates(projRates1, projRates2):
    projRates1.update(projRates2)
    return  projRates1

def merge_myRouting(newRouting, oldRouting):
    for k in newRouting.keys():
        if not k in oldRouting.keys():
            oldRouting[k] = newRouting[k]
        else:
            oldRouting[k] = list(set(oldRouting[k]).union(set(newRouting[k])))
    return oldRouting       


with open('EvaluationPlan', 'rb') as EvaluationPlan_file: 
              myplan = pickle.load(EvaluationPlan_file)[0]
def main():

    
    
    
    cur_routingDict = {}
    cur_projRates = {}    
    cur_NumETbs = {}
    
    
    myID = 0
    iteration = 0 
    qwlLength = 15
    notFirst = True 
    run = 0
    skew = 0
    if len(sys.argv) > 1:
        myID = int(sys.argv[1])
    if len(sys.argv) > 2:
        iteration = int(sys.argv[2])
    if len(sys.argv) > 3:
        qwlLength = int(sys.argv[3])  
    if len(sys.argv) > 4:
        run = int(sys.argv[4])     
    if len(sys.argv) > 5:
        skew = float(sys.argv[5])     
   
    if iteration == 0:
        notFirst = False
        Last = False
    elif iteration < qwlLength :
        notFirst = True
        Last = False
    elif qwlLength  == iteration :
         Last = True
         notFirst = True
    
    
    if notFirst:
        with open('partialInev', 'rb') as partialInev_file: 
              partialInev = pickle.load(partialInev_file)
              cur_routingDict = partialInev[0]
              cur_projRates = partialInev[1]
              cur_NumETbs = partialInev[2]
              
    
    print("Old_Costs", getCosts(cur_routingDict,  cur_projRates, cur_NumETbs))
    
    
    singleNodeRoutes =  {}
    
    myprojrates = getNewProjrates()
    sources = {}
    myRouting = {}
    myNumEtbs = {}
    for i in myplan.instances:     
                 myNumEtbs[i.name] = (i.projname, NumETBsByKey(i.name, i.projname))
                 # 0. construct dict with sources per etb, update for m-n placements that become single sink placements
                # if not i.projname in wl:
                 if ''.join([n for n in i.name if n.isdigit()]) != '':
                         sources[i.name] = int(''.join([n for n in i.name if n.isdigit()]))# get original source by extracting node name from etb name
                 elif i.sources:
                         sources[i.name]  = i.sources[0] #TODO!!!
                 myRouting[i.name] = getRoutingInfo(i.routingDict)
                 singleNodeRoutes[i.name] = getSingleNodeRoute(i.routingDict)
                 
    # Compute Costs for current config 
    print("Costs", getCosts(myRouting,  myprojrates, myNumEtbs))
    
    myprojrates = merge_projrates(myprojrates, cur_projRates)
    myRouting = merge_myRouting(myRouting, cur_routingDict)
    cur_NumETbs.update(myNumEtbs)
    
    if not Last:
        with open('partialInev', 'wb') as partialInev_file: 
              pickle.dump((myRouting, myprojrates, cur_NumETbs),partialInev_file)
    
    print("Merged Costs", getCosts(myRouting,  myprojrates, cur_NumETbs)) 
    
    myResult  = [myID, getCosts(myRouting,  myprojrates, cur_NumETbs), run, skew]
    schema = ["ID", "UnsharedRatio", "Run", "Skew"]       
       
    if Last:
            new = False
            try:
                f = open("../res/unsharedCosts_20.csv")   
            except FileNotFoundError:
                new = True           
            
            with open("../res/unsharedCosts_20.csv", "a") as result:
              writer = csv.writer(result)  
              if new:
                  writer.writerow(schema)              
              writer.writerow(myResult)
              

if __name__ == "__main__":
    main()    