
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
        

def generate_eventrates(eventskew,numb_eventtypes):
    eventrates = np.random.zipf(eventskew,numb_eventtypes)
    while max(eventrates) > 100000:
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


def getmin(assignmentdict, distribution, ratesdict,nwsize):
    nodecosts = {x: 0 for x in range(nwsize)}
    for x in assignmentdict.keys():
        for y in assignmentdict[x]:
            if not y in nodecosts.keys():
                nodecosts[y] = [ratesdict[x]]
            else:
                nodecosts[y] += ratesdict[x]
    return sorted(nodecosts.keys(), key = lambda x: nodecosts[x])[:distribution]
                
def getPartitioning(rates, nwsize):
    ratesdict = {i:rates[i] for i in range(len(rates))}
    assignmentdict = {x : [] for x in range(len(rates))}
    for i in ratesdict.keys():
        distribution = int(np.random.uniform(1,nwsize))
        ratesdict[i] = ratesdict[i]/distribution
        for k in getmin(assignmentdict, distribution, ratesdict,nwsize):
            assignmentdict[i].append(k)        
    return generateFromAssignment(assignmentdict, ratesdict, nwsize)
        

def main():

    
    #default values for simulation 
    nwsize = 5
    node_event_ratio = 0.6
    num_eventtypes = 10
    eventskew = 1.6
    toFile = False
    swaps = 0
    #ev = [[6, 1, 2, 1082, 126, 322, 4, 1, 13] ] # citibike Steven
    #generate network of size nwsize, with node_event_ratio for given event rates (ev)
   # ev = list(map(lambda x: x/1000, ev_Test[0]))
    
    
    
    

    
    # NEW: read event rates from pickle, write to pickle

    if len(sys.argv) > 1: #network size
        nwsize =int(sys.argv[1])
    if len(sys.argv) > 2:
        node_event_ratio = float(sys.argv[2]) # event node ratio
    if len(sys.argv) > 3: # event skew
        eventskew = float(sys.argv[3]) 
    if len(sys.argv) > 4: # size event universe
        num_eventtypes = int(sys.argv[4])
    if len(sys.argv) > 4 and len(sys.argv) < 7 :   #write event types to file  
        #eventrates = generate_eventrates(eventskew,num_eventtypes)   
        toFile = True
    if len(sys.argv) > 6:     # generate event types from file and apply given number of swaps
        eventrates = event_rates_file # get event rates for event types
        nodeassignment = event_node_assignment  # get node assignment, which node generates which event types
        swaps = int(sys.argv[6]) # number of swaps
        toFile = False # do not save generated rates to file
        
    if len(sys.argv) > 6:        # for setting event types to min/max rates (kleene, nseq experiments)
        eventtype = str(sys.argv[6]) 
    
    if len(sys.argv) > 7: # set eventtype to param=max/min rate (kleene, nseq experiments)
        param = str(sys.argv[7])
        eventrates = swapRatesMax(eventtype, eventrates, param)   
    
    
    eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
        
        
    if toFile:
        eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
        nw= []
        for node in range(nwsize): 
            nw.append(generate_events(eventrates, node_event_ratio))
        print(nw)
        nodeassignment = generate_assignment(nw, num_eventtypes)
        with open('rates', 'wb') as rates_file:
              pickle.dump((eventrates, nodeassignment), rates_file) 
                
    
    #if not toFile:
    #   nw= generateFromAssignment(nodeassignment, eventrates,  nwsize)

    #random.shuffle(eventrates)
    
    eventrates = sorted(generate_eventrates(eventskew,num_eventtypes))
    
    #eventrates = regain_eventrates([[0.5, 6, 1, 136, 1000, 250, 0.5, 30, 60]])
    
    nw = []    
    for node in range(nwsize):
        nw.append(generate_events(eventrates, node_event_ratio))
        
    while not allEvents(nw):
        
        for node in range(nwsize):
            nw.append(generate_events(eventrates, node_event_ratio))

    print(eventrates)
    #FOR PARALLEL
    #eventrates = [12, 16, 48, 260, 764]
    #nw = getPartitioning(eventrates, nwsize)

    #nw = [[0, 30, 0, 0, 0], [250, 0, 0, 0, 0], [0, 0, 0, 0, 0], [250, 0, 100, 0, 0], [0, 0, 100, 0, 0], [250, 0, 0, 0, 0], [0, 0, 0, 0, 0], [250, 0, 0, 0, 0], [0, 0, 0, 30, 0], [0, 0, 0, 0, 50]]
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


        



