#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 16:32:53 2021

@author: samira
"""
from placement_aug import *
import time
import csv
import sys


maxDist = max([max(x) for x in allPairs])

def getLowerBound(query):
    MS = []
    for e in query.leafs():        
        myprojs= [p for p in list(set(projsPerQuery[query]).difference(set([query]))) if totalRate(p)<rates[e] and not e in p.leafs()] #TODO define over paths
        if myprojs:
            MS.append(e)
        for p in [x for x in projsPerQuery[query] if e in x.leafs()]:
            part = returnPartitioning(p,p.leafs())            
            if e in part:
                MS.append(e)
    nonMS = [e for e in query.leafs() if not e in MS]  
    if nonMS:          
        minimalRate = sum(sorted([totalRate(e) for e in query.leafs() if not e in MS])) * longestPath
    else:
        minimalRate = min([totalRate(e) for e in query.leafs()]) * longestPath
    minimalProjs = sorted([totalRate(p) for p in projsPerQuery[query] if not p==query])[:len(list(set(MS)))-1]
    if not len(nonMS) == len(query.leafs()):
        minimalRate +=  sum(minimalProjs) * longestPath
    return minimalRate



def main():
    
    
  
    Filters = []
    
    filename = "None"
    noFilter = 0
    
    
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    if len(sys.argv) > 2:
        noFilter = int(sys.argv[2])
        
    ccosts = NEWcomputeCentralCosts(wl)
    centralHopLatency = max(allPairs[ccosts[1]])
    print("centralCosts: " + str(ccosts[0]))
    print("central Hop Latency: " + str(centralHopLatency))
    MSPlacements = {}
    curcosts = 1 
    start_time = time.time()
    
    hopLatency = {}
    
       
    EventNodes = initEventNodes()[0]
    IndexEventNodes = initEventNodes()[1]    
    
    myPlan = EvaluationPlan([], [])
    
    myPlan.initInstances(IndexEventNodes) # init with instances for primitive event types
    
    unfolded = mycombi
    sharedDict = getSharedMSinput(unfolded, projFilterDict)    
    dependencies = compute_dependencies(unfolded)
    processingOrder = sorted(compute_dependencies(unfolded).keys(), key = lambda x : dependencies[x] ) # unfolded enthält kombi   
    costs = 0
    for projection in processingOrder:  
            if set(unfolded[projection]) == set(projection.leafs()): #initialize hop latency with maximum of children
               hopLatency[projection] = 0 
            else:
                hopLatency[projection] = max([hopLatency[x] for x in unfolded[projection] if x in hopLatency.keys()])

          
            partType = returnPartitioning(projection, unfolded[projection], criticalMSTypes)
            if partType : 
                MSPlacements[projection] = partType
                result = computeMSplacementCosts(projection, unfolded[projection], partType, sharedDict, noFilter)
                additional = result[0]
                costs += additional
                hopLatency[projection] += result[1]
                
                myPlan.addProjection(result[2])
                
                for newin in result[2].spawnedInstances: # add new spawned instances
                    myPlan.addInstances(projection, newin) 
                    
                myPlan.updateInstances(result[3]) #! update instances
                
                Filters += result[4]

                print("MS " + str(projection) + " At: " + str(partType) + " PC: " + str(additional) + " Hops:" + str(result[1]))
            else:
                
                result = ComputeSingleSinkPlacement(projection, unfolded[projection], noFilter)
                additional = result[0]
                costs += additional
                hopLatency[projection] += result[2]
                
                myPlan.addProjection(result[3]) #!
                for newin in result[3].spawnedInstances: # add new spawned instances
                    myPlan.addInstances(projection, newin)
                
                myPlan.updateInstances(result[4]) #! update instances
                Filters += result[5]
               
                print("SiS " + str(projection) + "PC: " + str(additional)  + " Hops: " + str(result[2]))
                
    mycosts = costs/ccosts[0]
    print("Muse Transmission " + str(costs) )
    lowerBound = 0
    for query in wl:
        lowerBound += getLowerBound(query)
    print("Lower Bound: " + str(lowerBound / ccosts[0]))

    print("Transmission Ratio: " + str(mycosts))
    print("MuSE Depth: " + str(float(max(list(dependencies.values()))+1)/2))
    
    hoplatency = max([hopLatency[x] for x in wl if x in hopLatency.keys()]) 
    
    print("Hop Latency: " + str(hoplatency))
    
    
    
    totaltime = str(round(time.time() - start_time, 2))

        
    with open('networkExperimentData', 'rb') as networkExperimentData_file: 
          networkParams = pickle.load(networkExperimentData_file)   
    with open('selectivitiesExperimentData', 'rb') as selectivities_file: 
          selectivityParams  = pickle.load(selectivities_file)   
    with open('combiExperimentData', 'rb') as combiExperimentData_file: 
          combigenParams = pickle.load(combiExperimentData_file) 
    with open('processingLatency', 'rb') as processingLatency_file: 
          processingLatencyParams = pickle.load(processingLatency_file)            
                      
    ID = int(np.random.uniform(0,10000000))
    hopfactor = processingLatencyParams[2]
    museLatency = processingLatencyParams[0]  + hoplatency * hopfactor
    centralLatency = processingLatencyParams[1] + centralHopLatency * hopfactor - hopfactor * longestPath * 1.5
  
    totalLatencyRatio = museLatency/centralLatency
    
    print("total LatencyRatio: " + str(totalLatencyRatio))
    
    f = open("out.txt","w")
    if Filters:        
        f.write("VAR=true")       
    else:
        f.write("VAR=false") 
    f.close
    
    filterTrue = 0
    if Filters:
         filterTrue  = 1
    
    myResult = [ID, mycosts,  filterTrue, networkParams[3], networkParams[0], networkParams[2], len(wl), combigenParams[3], selectivityParams[0], selectivityParams[1], combigenParams[1], longestPath, totaltime, hoplatency, float(max(list(dependencies.values()))/2), totalLatencyRatio, ccosts[0], lowerBound / ccosts[0], networkParams[1]]
    schema = ["ID", "TransmissionRatio", "FilterUsed", "Nodes", "EventSkew", "EventNodeRatio", "WorkloadSize", "NumberProjections", "MinimalSelectivity", "MedianSelectivity","CombigenComputationTime", "Efficiency", "PlacementComputationTime", "HopCount", "Depth", "ProcessingLatencyRatio", "CentralTransmission", "LowerBound", "EventTypes"] 
    
 
    new = False
    try:
        f = open("../res/"+str(filename)+".csv")   
    except FileNotFoundError:
        new = True           
        
    with open("../res/"+str(filename)+".csv", "a") as result:
      writer = csv.writer(result)  
      if new:
          writer.writerow(schema)              
      writer.writerow(myResult)
      
    with open('EvaluationPlan',  'wb') as EvaluationPlan_file:
        pickle.dump([myPlan, ID, MSPlacements], EvaluationPlan_file)
    
    with open('CentralEvaluationPlan',  'wb') as CentralEvaluationPlan_file:
        pickle.dump([ccosts[1],ccosts[3], wl], CentralEvaluationPlan_file)
    
    with open('ExperimentID',  'wb') as ExperimentID_file:
        pickle.dump([ID,ccosts[0]], ExperimentID_file)
    
    print(list(map(lambda x: totalRate(x), wl)))

if __name__ == "__main__":
    main()                    