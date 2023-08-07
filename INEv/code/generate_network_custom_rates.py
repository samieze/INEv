
"""
Generate network with given size (nwsize), node-event ratio (node_event_ratio), 
number of event types (num_eventtypes), event rate skew (eventskew)-
"""
import sys
import pickle
import numpy as np
import string
import random
import argparse
""" Experiment network rates 


#ev =  [[0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60]] # average rates citibike experiment

"""    


with open('rates',  'rb') as  rates_file:
        res = pickle.load(rates_file)
        event_rates_file = res[0]
        event_node_assignment = res[1]
        

def generate_eventrates(eventskew,numb_eventtypes):
    eventrates = np.random.zipf(eventskew,numb_eventtypes)
    return eventrates


def generate_events(eventrates, n_e_r):
    myevents = []
    for i in range(len(eventrates)):
        x = np.random.uniform(0,1)
        if x < n_e_r:
            myevents.append(eventrates[i])
        else:
            myevents.append(0)
    
    return myevents

def regain_eventrates(nw):
    eventrates = [0 for i in range(len(nw[0]))]
    interdict = {}
    for i in nw:
        for j in range(len(i)):
            if i[j] > 0 and not j in interdict.keys():
                interdict[j] = i[j]
    for j in sorted(interdict.keys()):
        eventrates[j] = interdict[j]
    return eventrates 

def allEvents(nw):
    for i in range(len(nw[0])) :
        column = [row[i] for row in nw]
        if sum(column) == 0:
            return False
    return True

def swapRatesMax(eventtype, rates, maxmin):
    rates = list(rates)
    if maxmin == 'max':
        maxRate = max(rates)
    else: 
        maxRate = min(rates)
    maxIndex = rates.index(maxRate)
    eventTypeIndex = string.ascii_uppercase.index(eventtype)
    newRates = [x for x in rates]
    newRates[maxIndex], newRates[eventTypeIndex] =   newRates[eventTypeIndex], newRates[maxIndex]
    return newRates

def swapRates(numberofswaps,rates):
    newRates = [x for x in rates]
    for i in range(numberofswaps):        
        newRates = [x for x in newRates]
        index = int(len(newRates)/2)
        left = index - (i+1) 
        right = index + i
        newRates[left], newRates[right] = newRates[right], newRates[left]
    return newRates

def generate_assignment(nw, eventtypes):
    assignment = {k: [] for k in range(eventtypes)}
    for node in range(len(nw)):
        for eventtype in range(len(nw[node])):
            if nw[node][eventtype] > 0:
                assignment[eventtype].append(node)        
    return assignment

def generateFromAssignment(assignment, rates, nwsize):
    return [[rates[eventtype]  if x in assignment[eventtype] else 0 for eventtype in assignment.keys()] for x in range(nwsize)]

def main():

        

    ev = [[0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60]] # average rates citibike experiment

    
    #default values for simulation 
    nwsize = 10
    node_event_ratio = 1.0
    num_eventtypes = len(ev[0])
 
    parser = argparse.ArgumentParser(description='Process some integers and a second parameter.')
    parser.add_argument('-event_rates', nargs='+', type=int, help='List of event rates',default = ev)
    parser.add_argument('-network_size', type=int, help='Size of network', default = nwsize)
    parser.add_argument('-node_event_ratio', type=float, help='Percentage of events of event universe generate per node', default = node_event_ratio)
    args = parser.parse_args()
    
    ev = args.event_rates
    nwsize = args.network_size
    node_event_ratio = args.node_event_ratio 
    
    eventrates = ev
    
    nw = []    
    for node in range(nwsize):
        nw.append(generate_events(eventrates, node_event_ratio))
        
    print(nw)     
    while not allEvents(nw):
        nw = []    

        for node in range(nwsize):
            nw.append(generate_events(eventrates, node_event_ratio))


    ## INSERT NETWORK HERE
    #nw = [[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40],[2970, 2000, 322, 600, 960, 458, 2, 2, 40]]

    networkExperimentData = [1.0, num_eventtypes, node_event_ratio, nwsize, min(eventrates)/max(eventrates)]
    with open('networkExperimentData', 'wb') as networkExperimentDataFile:
        pickle.dump(networkExperimentData, networkExperimentDataFile)
    
    with open('network', 'wb') as network_file:
          pickle.dump(nw, network_file)      
          
         
    
   
    print("NETWORK")  
    print("--------") 
    for i in range(len(nw)):
      print("Node " + str(i) + " " + str(nw[i])) 
    print("\n")
    
    
        
if __name__ == "__main__":
    main()


        



