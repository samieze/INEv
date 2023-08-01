#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 10:20:16 2022

@author: samira

Compute processing latency of centralized evaluation using mini-diamonds to reduce number of partial matches during processing.
Centralized processing latency is used as bound for latency bounded INEv graph computation.

"""
import sys
import pickle
from processCombination import *


def getCentralProcessingLatency_Diamond(myquery):    
        myLatency = 0                 
        mycombis = getMiniDiamonds(myquery,"", myquery.leafs(), "", 2000)              
        for combi in mycombis:   
            myLatency += totalRate(combi[0]) * totalRate(combi[1]) +  totalRate(combi[0])  + totalRate(combi[1])   
        return myLatency


def centralLatencyF():
    latencies = []
    for query in wl:
        latencies.append(getCentralProcessingLatency_Diamond(query))
        #latencies.append(getCentralProcessingLatency(query))
    return max(latencies)


def main():
    
    hopfactor = 20000
    if len(sys.argv) > 1: 
        hopfactor = int(sys.argv[1])

    centralLatency = centralLatencyF() #+ hopfactor * longestPath * 1.5
    print(centralLatency)
    
    with open('centralLatency',  'wb') as centralLatency_file:
            pickle.dump([centralLatency, hopfactor], centralLatency_file)
            
        
if __name__ == "__main__":
    main()