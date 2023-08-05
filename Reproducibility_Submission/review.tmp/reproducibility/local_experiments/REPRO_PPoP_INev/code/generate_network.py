
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
    
event rates push-pull comparison:
small:
ev_PP = [[0.2994830154521548 , 0.14354286459134916 , 0.009297964702092328 , 0.2568894819120937 , 0.0771288310049754 ,  0.009297964702092328, 0.2994830154521548 , 0.26592179047984055 ]]    
big: 
ev =  [[1, 6, 1, 1, 1, 7, 8777, 1, 542, 72, 39, 1, 1, 318, 3, 1, 17, 2, 12, 2]]


#ev =  [[1485,1000, 161, 300, 480, 229, 1, 1,20]] # average rates google cluster experiment
#ev =  [[0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60]] # average rates citibike experiment

"""    


with open('rates',  'rb') as  rates_file:
        res = pickle.load(rates_file)
        event_rates_file = res[0]
        event_node_assignment = res[1]
        

def generate_eventrates(eventskew,numb_eventtypes, small):
    eventrates = np.random.zipf(eventskew,numb_eventtypes)
    if small:
        eventrates = [x/max(eventrates) for x in eventrates]
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

    
    #default values for simulation 
    nwsize = 5
    node_event_ratio = 1.0
    num_eventtypes = 10 
    eventskew = 1.3
    toFile = False
    swaps = 0   
    small = 0
      
    if len(sys.argv) > 1: #network size
        nwsize =int(sys.argv[1])
    if len(sys.argv) > 2:
        node_event_ratio = float(sys.argv[2]) # event node ratio
    if len(sys.argv) > 3: # event skew
        eventskew = float(sys.argv[3]) 
    if len(sys.argv) > 4: # size event universe
        num_eventtypes = int(sys.argv[4])
    if len(sys.argv) > 5: # all rates <=1
        small = int(sys.argv[5])	   

    
    eventrates = sorted(generate_eventrates(eventskew,num_eventtypes,small))
        
        
  
    
    #if not toFile:
    #   nw= generateFromAssignment(nodeassignment, eventrates,  nwsize)

    #random.shuffle(eventrates)
    
    #eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))



    #eventrates = [2970 * 2, 2000 * 2, 322 * 2, 600 * 2, 960 * 2, 458 * 2,2 *2, 2 * 2, 40*2] # google 5
    #eventrates = [2970, 2000, 322, 600, 960, 458,2, 2, 40] # google 10	
    #eventrates  =  [1485,1000, 161, 300, 480, 229, 1, 1,20] #google 20
    #eventrates =  [990,666,107,200,320,152, 0.6, 0.6,13.3] #google 30
    #eventrates = [2970/5, 2000/5, 322/5, 600/5, 960/5, 458/5,2/5, 2/5, 40/5] # google 50    
    
    #eventrates = [1*2,12*2,2*2,272*2, 2000*2, 500*2, 1*2, 60*2, 120*2] # citibike 5
    #eventrates = [1,12,2,272, 2000, 500, 1, 60, 120] # citibike 10
    #eventrates =  [0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60] # citibike 20
    #eventrates = [0.3, 4, 0.6, 91, 666, 166, 0.3, 20, 40] # citibike 30
    #eventrates = [1/5,12/5,2/5,272/5, 2000/5, 500/5, 1/5, 60/5, 120/5] # citibike 50



    
    nw = []    
    for node in range(nwsize):
        nw.append(generate_events(eventrates, node_event_ratio))
        
    while not allEvents(nw):
        
        for node in range(nwsize):
            nw.append(generate_events(eventrates, node_event_ratio))

    
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


        



