#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 16:32:53 2021

@author: samira
"""
from placement import *
import time
import csv
import sys


maxDist = max([max(x) for x in allPairs])

def main():
    
    
    experimentParam = 0
    experimentName = "None"
    if len(sys.argv) > 1:
        experimentParam =int(sys.argv[1])
    if len(sys.argv) > 2:
        experimentName = str(sys.argv[2])
        
    ccosts = NEWcomputeCentralCosts(wl) #TODO
    print("central costs : " + str(ccosts))
    
    curcosts = 1 
    start_time = time.time()
    
    hopLatency = {}
    
       
    EventNodes = initEventNodes()[0]
    IndexEventNodes = initEventNodes()[1]    
    
    myPlan = EvaluationPlan([], [])
    
    myPlan.initInstances(IndexEventNodes) # init with instances for primitive event types
    
    
    unfolded = mycombi
       
    sharedDict = getSharedMSinput(unfolded)    
    dependencies = compute_dependencies(unfolded)
    
    processingOrder = sorted(compute_dependencies(unfolded).keys(), key = lambda x : dependencies[x] ) # unfolded enthält kombi   
        
    costs = 0
    for projection in processingOrder:
                    
            if unfolded[projection] == projection.leafs(): #initialize hop latency with maximum of children
               hopLatency[projection] = 0 
            else:
                hopLatency[projection] = max([hopLatency[x] for x in unfolded[projection] if x in hopLatency.keys()])
          
            partType = returnPartitioning(projection, unfolded[projection])
            if partType : 
                result = computeMSplacementCosts(projection, unfolded[projection], partType, sharedDict)
                additional = result[0]
                costs += additional
                hopLatency[projection] += result[1]
                
                myPlan.addProjection(result[2]) #!
                for newin in result[2].spawnedInstances: # add new spawned instances
                    myPlan.addInstances(newin) 
                    
                myPlan.updateInstances(result[3]) #! update instances
                
                print("MS " + str(projection) + " At: " + str(partType) + " PC: " + str(additional))
            else:
                
                result = ComputeSingleSinkPlacement(projection, unfolded[projection])
                additional = result[0]
                costs += additional
                hopLatency[projection] += result[2]
                
                myPlan.addProjection(result[3]) #!
                for newin in result[3].spawnedInstances: # add new spawned instances
                    myPlan.addInstances(newin)
                
                myPlan.updateInstances(result[4]) #! update instances
                
                print("SiS " + str(projection) + "PC: " + str(additional))
                
    print("COSTS " + str(costs))        
    mycosts = costs/ccosts[0]
    print("Transmission Ratio: " + str(mycosts))
    print("Levels : " + str((float(max(list(dependencies.values())))/2) * maxDist))
    #print("Hop Latency: " + str(hopLatency[wl[0]]) )
    totaltime = str(round(time.time() - start_time, 2))
    print(totaltime)
    
    with open("EvalPlan", "a") as evalPlan:
        writer = csv.writer(evalPlan)        
        for i in myPlan.instances:
            writer.writerow([i])
    
    with open("combigen_comparison.csv", "a") as result:
          writer = csv.writer(result)
          writer.writerow(['NoOpt', mycosts])

if __name__ == "__main__":
    main()                    