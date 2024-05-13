#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Sep 28 11:20:18 2021

@author: samira
"""

import pickle
import sys
from processCombination import *



#myquery = sorted(mycombi.keys(), key = lambda x: len(x.leafs()), reverse= True)[0]

def getQuery(projection):
    for query in wl:
        if projection in projsPerQuery[query]:
            return query

def getLatency(proj, newcombi):
        query = getQuery(proj)
        myPart = returnPartitioning(proj, newcombi[proj])
        myRates = {x: totalRate(x) for x in newcombi[proj]}
     
        if myPart:
            myRates[myPart[0]] = myRates[myPart[0]] / len(nodes[myPart[0]])
            
        # choose minimum, add to latency
        myMin = [x for x in newcombi[proj] if myRates[x] == min(myRates.values())][0]
        myState = myMin        
        myLatency = myRates[myState]        
        myRest = [x for x in newcombi[proj] if not x == myMin]
        if myState in myPart:
                div = len(nodes[myPart[0]])
        else:
            div = 1
        for x in sorted(myRest, key = lambda x: myRates[x]):            
            if x in myPart:
                div = len(nodes[myPart[0]])          
            myLatency += (myRates[myState] / div) * myRates[x]   +  myRates[x]        # div because rate of state is total rate of projection          
            nextStateInfo = getNewState(myState, x, query) # query to which current projections belongs
            myRates[nextStateInfo[0]] = nextStateInfo[1]  
            myState =  nextStateInfo[0]          
            #myLatency += myRates[myState] / div
            
        #myLatency +=  getFilterLatency(proj)    
        return myLatency    

def getDiv(i, partType):
    if len(i)==1:
        if i == partType:
            return instances[partType]
        return 1
    elif partType in i.leafs():
        return instances[partType]
    return 1
    
def getLatency_Diamond(proj, *args):
        sampleSize = 1
        if args:
            thisCombi = args[0]
        else:
            thisCombi = copy.deepcopy(mycombi)
        if len(args)>1:
            sampleSize = args[1]
            
        mycombis = []
        myLatency = 0
        myPart = returnPartitioning(proj, thisCombi[proj]) 
        if myPart:
                myPart = myPart[0]     
        if len(thisCombi[proj]) <= 2: 
            return getLatency(proj, thisCombi) + getFilterLatency_Diamonds(proj, thisCombi)       
        
        mycombis = getMiniDiamonds(proj,myPart, thisCombi[proj], "", sampleSize)  
        for combi in mycombis:                
            div0 = getDiv(combi[0], myPart)
            div1 = getDiv(combi[1], myPart)
        

            myLatency += (totalRate(combi[0]) / div0) * (totalRate(combi[1]) / div1)   +  (totalRate(combi[0]) / div0) + (totalRate(combi[1]) / div1)     # div because rate of state is total rate of projection          
        myLatency +=  getFilterLatency_Diamonds(proj, thisCombi)   
        
        return myLatency    

def getFilterLatency(proj): # this is for the upstream projection proj and computes for each filter of each subprojections additional latencies
    totalLatency = 0
    
    for i in [x for x in mycombi[proj] if x in projFilterDict.keys() and len(list(projFilterDict[x].keys()))>1]: #input x of combi of proj has filter
        myfilters = list(getMaximalFilter(projFilterDict, i))  
        print(myfilters) 
        myRates = {x: totalRate(x) for x in myfilters} # Problem: not Totalrates anymore for determining costs -> add cost Dict for Diamonds
        myRates.update({x: totalRate(x) * singleSelectivities[getKeySingleSelect(x, i)] for x in [x for x in i.leafs() if not str(x) in myfilters]})      
        localcombi = i.leafs()
        print(localcombi)
        # choose minimum, add to latency
        myMin = [x for x in localcombi if myRates[x] == min(myRates.values())][0]
        myState = myMin        
        myLatency = myRates[myState]        
        myRest = [x for x in localcombi if not x == myMin]
        for x in sorted(myRest, key = lambda x: myRates[x]):
            myLatency += myRates[myState]  * myRates[x]   +  myRates[x]        
            nextStateInfo = getNewState_Filter(myState, x, i) # query to which current projections belongs
            myRates[nextStateInfo[0]] = nextStateInfo[1]  
#            myState =         # if len(thisCombi[proj]) <= 2:
        #     return getLatency(proj) + getFilterLatency_Diamonds(proj)   nextStateInfo[0] 
        totalLatency += myLatency
    return totalLatency




def getFilterLatency_Diamonds(proj, *combi): # this is for the upstream projection proj and computes for each filter of each subprojections additional latencies
    if combi:
        thisCombi = combi[0]
    else:
        thisCombi = copy.deepcopy(mycombi)
    totalLatency = 0

    for i in [x for x in thisCombi[proj] if x in projFilterDict.keys() and len(list(projFilterDict[x].keys()))>1]: #input x of combi of proj has filter
        myfilters = list(getMaximalFilter(projFilterDict, i))  
        localcombi = i.leafs() # compute Costs (also used in getMiniDiamonds, such that it reflects rates & selectivities of filtered)
        myDiamonds = getMiniDiamonds(i,"", localcombi, [x for x in localcombi if not x in myfilters])      
        totalLatency += Diamond_costsFiltered(i, myDiamonds,  [x for x in localcombi if not x in myfilters])
    return totalLatency





def getNewState_Filter(current, transition, query): #maybe the same for both
    if len(current) == 1:
        current = PrimEvent(current)
    if len(transition) == 1:
        transition = PrimEvent(transition)    
    eventList = list(set(current.leafs()).union(set(transition.leafs())))
    myproj = settoproj(eventList, query)
    if myproj in projrates.keys():
        myrate = totalRate(myproj)          
    else:
        outrate = myproj.evaluate() +  getNumETBs(myproj)  
        selectivity =  return_selectivity(eventList)
        myrate = outrate * selectivity  
    return(myproj,myrate)

def getNewState(current, transition, query):
    if len(current) == 1:
        current = PrimEvent(current)
    if len(transition) == 1:
        transition = PrimEvent(transition)    
    eventList = list(set(current.leafs()).union(set(transition.leafs())))
    myproj = settoproj(eventList, query)
    if myproj in projrates.keys():
        myrate = totalRate(myproj)          
    else:
        outrate = myproj.evaluate() *  getNumETBs(myproj)  
        selectivity =  return_selectivity(eventList)
        myrate = outrate * selectivity  

    return(myproj,myrate)    



# def getCentralProcessingLatency_Diamond(myquery):    
#         myLatency = 0                 
#         mycombis = getMiniDiamonds(myquery,"", myquery.leafs())              
#         for combi in mycombis:   
#             myLatency += totalRate(combi[0]) * totalRate(combi[1]) +  totalRate(combi[0])  + totalRate(combi[1])   
#         return myLatency
                           

# def getCentralProcessingLatency(myquery):
#     myRates = {x: totalRate(x) for x in myquery.leafs()}
#     myMinRate = min(myRates[x] for x in myquery.leafs())
#     myMin = [x for x in myquery.leafs() if myRates[x] == myMinRate][0]
#     myRest = [x for x in myquery.leafs() if not x == myMin]
    
#     myState = myMin
#     myLatency = myMinRate
#     for x in sorted(myRest, key = lambda x: myRates[x]):
#             myLatency += myRates[myState] * myRates[x] + myRates[x]        
#             nextStateInfo = getNewState(myState, x, myquery)
#             myRates[nextStateInfo[0]] = nextStateInfo[1]  
#             myState =  nextStateInfo[0]
#             #myLatency += myRates[myState]
            
#     return myLatency



# def centralLatency():
#     latencies = []
#     for query in wl:
#         latencies.append(getCentralProcessingLatency_Diamond(query))
#         #latencies.append(getCentralProcessingLatency(query))
#     return max(latencies)

def getProcessingLatency(*newcombi):
    sampleSize = 0
    if newcombi and not newcombi[0] == "":
        thisCombi = newcombi[0]
    else:
        thisCombi = copy.deepcopy(mycombi)
    if len(newcombi) > 1:
        sampleSize = newcombi[1]
    levels = compute_dependencies(thisCombi)
    LatencyDict = {x:0 for x in list(thisCombi.keys()) + sum([x.leafs() for x in wl],[])}    
    
    for proj in sorted(thisCombi.keys(), key = lambda x: levels[x]):
        myLatency = getLatency_Diamond(proj, thisCombi)
        if sampleSize > 0:
            myLatency = getLatency_Diamond(proj, thisCombi, sampleSize)
        #myLatency = getLatency(proj)
        myMax = max(LatencyDict[x] for x in thisCombi[proj])
        LatencyDict[proj] += myLatency + myMax      

    return LatencyDict

                     
         
 
def LatencyInducedByFilter(proj):
    for myfilter in projFilterDict[proj]:
        # compute costs for automaton
        return myfilter
    
def main() :   
    hopfactor = 20000
    if len(sys.argv) > 1: 
        hopfactor = int(sys.argv[1])


    latencies = getProcessingLatency("",1000)
    latency = max([latencies[query] for query in wl])

    print("MuSE Latency: " + str(latency))
                   
    with open('centralLatency', 'rb') as centralLatency_file: 
        centralLatency = pickle.load(centralLatency_file)  
      
    #hopfactor = centralLatency[1]      
    centralLatency = centralLatency[0] + hopfactor * longestPath * 1.5
    print("central Latency: " + str(centralLatency))

 
    with open('processingLatency',  'wb') as processingLatency_file:
            pickle.dump([latency, centralLatency, hopfactor], processingLatency_file)

        
if __name__ == "__main__":
    main()