
"""
Generate network with given size (nwsize), node-event ratio (node_event_ratio), 
number of event types (num_eventtypes), event rate skew (eventskew)-
"""
import sys
import pickle
import numpy as np
import string
import random

""" Experiment network rates 

average event rates for google cluster data set first 12h, timewindow 30 min, 20 nodes
#ev = [[0,855, 212, 24, 400, 129, 0, 0.005,0.05]]
    
event rates experiment set 1
#ev = [[1, 6, 1, 1, 1, 7, 8777, 1, 542, 72, 39, 1, 1, 318, 3, 1, 17, 2, 12, 2]]
    
event rates experiment set 2 (scalability)
#ev = [[2, 71, 1, 168, 1717781, 24, 1, 2574, 4, 4, 39, 1, 6, 59, 9, 154, 2370, 7, 2, 4]]
"""    


with open('rates',  'rb') as  rates_file:
        res = pickle.load(rates_file)
        event_rates_file = res[0]
        event_node_assignment = res[1]
        
        
        
ev =  [[1, 6, 1, 1, 1, 7, 8777, 1, 542, 72, 39, 1, 1, 318, 3, 1, 17, 2, 12, 2]]
ev_PP = [[0.2994830154521548 , 0.14354286459134916 , 0.009297964702092328 , 0.2568894819120937 , 0.0771288310049754 ,  0.009297964702092328, 0.2994830154521548 , 0.26592179047984055 ]]    
ev_Test = [[0.018, 0, 0, 0.002, 0, 0.002, 0, 0, 0.044, 0, 0.027, 0.001]]
participants = [[17500, 350, 20, 10, 10, 20, 5, 4, 2]]


def generate_eventrates(eventskew,numb_eventtypes):
    eventrates = np.random.zipf(eventskew,numb_eventtypes)
    #while max(eventrates) > 1000:
    eventrates = np.random.zipf(eventskew,numb_eventtypes)
    return eventrates
   # print(eventrates)
    #return list(map(lambda x: x/1000, eventrates))

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
    print(eventtype)
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

    
    #default values for simulation 
    nwsize = 20
    node_event_ratio = 1.0
    num_eventtypes = 25
    eventskew = 1.3
    toFile = False
    swaps = 0
    #ev =  [[1485,1000, 161, 300, 480, 229, 1, 1,20]] # google? 
    ev =  [[0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60]] #citibike !
    #ev = [[6, 1, 2, 1082, 126, 322, 4, 1, 13] ] # citibike Steven
    #generate network of size nwsize, with node_event_ratio for given event rates (ev)
   # ev = list(map(lambda x: x/1000, ev_Test[0]))
    
    
    
    

    
    # NEW: read event rates from pickle, write to pickle

    if len(sys.argv) > 1:
        nwsize =int(sys.argv[1])
    if len(sys.argv) > 2:
        node_event_ratio = float(sys.argv[2])
    if len(sys.argv) > 3:
        eventskew = float(sys.argv[3])
    if len(sys.argv) > 4:
        num_eventtypes = int(sys.argv[4])
    if len(sys.argv) > 4 and len(sys.argv) < 7 :    
        #eventrates = generate_eventrates(eventskew,num_eventtypes)   
        toFile = True
    if len(sys.argv) > 6:     
        eventrates = event_rates_file
        nodeassignment = event_node_assignment 
        swaps = int(sys.argv[6])
        toFile = False
        
    if len(sys.argv) > 6:        
        eventtype = str(sys.argv[6])
    
    if len(sys.argv) > 7:
        param = str(sys.argv[7])
        eventrates = swapRatesMax(eventtype, eventrates, param)  # NEW:  for setting negated event to max and to min 
    
    
    
        
        
    if toFile:
        eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
        nw= []
        for node in range(nwsize):
            nw.append(generate_events(eventrates, node_event_ratio))
        print(nw)
        nodeassignment = generate_assignment(nw, num_eventtypes)
        with open('rates', 'wb') as rates_file:
              pickle.dump((eventrates, nodeassignment), rates_file) 
    #eventrates = event_rates_file
    
    print("old", list(eventrates))    
    eventrates = swapRates(swaps, eventrates)
    print("new", eventrates)

    
    # TODO!!! do not change assignement from nodes to event types when swapping rates
    
    if not toFile:
       nw= generateFromAssignment(nodeassignment, eventrates,  nwsize)

    #random.shuffle(eventrates)
    #for node in range(nwsize):
    #    nw.append(generate_events(eventrates, node_event_ratio))
    
    
    
    #while not allEvents(nw):
    #    nw = []
    #   for node in range(nwsize):
     #       nw.append(generate_events(eventrates, node_event_ratio))
   # print(nw)
    #nw = [[6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604], [6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604],[6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604], [6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604], [0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604],[6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604], [6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604],[6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604], [6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604], [0, 0, 0, 0,3604],[0, 0, 0, 12,0 ],[0, 0, 0, 0,3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12, 3604],[0, 0, 0, 12,0 ],[6, 0, 20, 0,3604],[0, 0, 20, 12, 3604],[0, 0, 0, 12, 3604]]           
    #nw = [[6, 0, 20, 0, 0],[0, 50, 0, 0, 0],[0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604], [0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604],  [0, 50, 20, 0, 3604],[6, 0, 20, 12, 3604],[6, 0, 0, 0,3604]]
    
    # CASA REAL WORLD DATA SET
    # nw = [[17500, 350, 20, 10, 10, 20, 5, 4, 2], [17500, 350, 20, 10, 10, 20, 5, 4, 2],  [17500, 350, 0, 0, 10, 0, 5, 4, 2],  [17500, 350, 0, 0, 10, 0, 5, 4, 2],  [17500, 350, 0, 10, 10, 0, 5, 4, 2],  [17500, 350, 0, 10, 10, 20, 5, 4, 2],  [17500, 350, 20, 10, 10, 0, 5, 4, 2],  [17500, 350, 20, 0, 10, 0, 5, 4, 2],  [17500, 350, 20, 0, 10, 20, 5, 4, 2],  [17500, 350, 0, 10, 10, 0, 5, 4, 2],  [17500, 350, 0, 0, 10, 0, 5, 4, 2],  [17500, 350, 0, 10, 10, 20, 5, 4, 2],  [17500, 350, 20, 10, 10, 20, 5, 4, 2],  [17500, 350, 20, 0, 10, 20, 5, 4, 2],  [17500, 350, 20, 10, 10, 20, 5, 4, 2],  [17500, 350, 0, 0, 10, 20, 5, 4, 2],  [17500, 350, 0, 0, 0, 10, 5, 4, 2], [17500, 350, 20, 10, 10, 0, 5, 4, 2],  [17500, 350, 20, 10, 10, 20, 5, 4, 2],  [17500, 350, 0, 0, 10, 20, 5, 4, 2],  [17500, 350, 0, 10, 10, 0, 5, 4, 2],  [17500, 350, 0, 10, 10, 0, 5, 4, 2], [17500, 350, 0, 10, 10, 0, 5, 4, 2],  [17500, 350, 20, 10, 10, 0, 5, 4, 2],  [17500, 350, 0, 10, 10, 20, 5, 4, 2]]
    
    
    #export eventskew, node_eventratio, networksize, maximal difference in rates
    networkExperimentData = [eventskew, num_eventtypes, node_event_ratio, nwsize, min(eventrates)/max(eventrates)]
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


        



