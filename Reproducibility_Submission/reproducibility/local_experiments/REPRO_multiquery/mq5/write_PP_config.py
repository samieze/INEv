#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 09:55:12 2022

@author: samira
"""
from generate_projections import *

with open('ExperimentID', 'rb') as ExperimentID_file: 
      myexperimentID =pickle.load(ExperimentID_file)  
 
with open('networkExperimentData', 'rb') as networkExperimentData_file: 
          networkParams = pickle.load(networkExperimentData_file)   
          
def getString(eventlist):
    mystr = ""
    for i in sorted(rates.keys()):
        if i in eventlist:
            mystr +=  "1,"
        else:
            mystr += "0,"
    mystr = mystr[:-1]   
    return mystr     



mystr = "intXaxis = \ndoubleXaxis = memoryFactor: 0.1 ; 1.0 ; 0.05\nnetworkType = 3 \nmaxRep = 1 \nrawEvents = 6 \nrawEventGlobalFrequency = 0.1 \nrawEventFrequencySkew = 3 \n"
mystr += "shared = false \ncomplexEvents = 2	\nedtHeight = 2 \nsharedEvents = 2 \nsharingDegree = 3 \nfanoutMean = 3	\nfanoutStd = 0.001 \nselectivityScale=1 \n"
mystr += "andOrSeqSelectivitySkew = 2 	\noperatorTypes=3 	\nwindow = 1 \ntotalNodes = 20\nmaxTreeChildren = 2 \nmaxLatency = 1 \nminLatency = 1 \nleafDiameter = 	5 \n"
mystr += "step = 2  \nvorRadius = 0	\nnodesPerEvent = 5 \ndistributionSkew = 0.00001	\nrandomWalkReps = 10 \nminimizeCost = true \nmemoryLimit = false \nbandwidthLimit = false \n"
mystr += "worstCaseBandwidth = true \ncountOnlySuccesses = false \ninsideLoop = true \nconstrainedPercentage = 1 \ncostFactor = 100000 \nlatencyFactor=  10 \nmemoryFactor = 100000\n"
mystr += "bandwidthFactor = 100000 \nDP= false \nBF= true \nakdere = false \ngreedy =  false \ngreedyp = false \ngreedyinNet = false \nSBON = false \nSBON_HEUR = false \n"
mystr += "heuristic = false \nhealse uristicp = false \ncheckBandwidthAndMemoryOnRootPlanOnlyForHeur = false \ntopK = false \nheurExploreSites = -1 \noperatorScalingFactor = 1 \n"
mystr += "addOrsPerScalingFactor = true \nrealNetworkTopology = false \nminimumSpanningTree = false \nconnectedNeighbours = 3 \nrealNetworkFile = CELL_IDs_Masked_100.csv \nrealData = true\n"	
mystr += "realf = "
for etype in rates.keys():
    mystr+= str(rates[etype]) + ";"
mystr = mystr[:-1]
mystr += "\n"
mystr += "ceFrequencies = "
for k in PP_Projs:
   mystr+= str(k) + ";"
mystr = mystr[:-1]
mystr += "\n"    
mystr += "eventNodes="     
for i in network.keys():
    mystr += getString(network[i]) + ";"
mystr += "\ntransmissionFactor = true \ncandidateSet = 3 \nrootOrSiteDistanceFromDataCenter = -1 \nincludeRootOrSiteToCandidateSet = true \nkeepStableRootSite = true\n"
mystr += "akdereAtStableRootOrSite= true \ndefaultPlan = true \nprintAllExperimentalResults = true"
mystr += "\neventskew = " + str(networkParams[0])+ "\ncentralTransmission=" + str(myexperimentID[1])

print(mystr)
f = open("PP_config/configFile_" + str(myexperimentID[0]),"w")    
f.write(mystr)  
f.close()
#ADD _ExperimentID_or Skew