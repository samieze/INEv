
"""
Generate network with given size (nwsize), node-event ratio (node_event_ratio), 
number of event types (num_eventtypes), event rate skew (eventskew)-
"""
import sys
import pickle
import numpy as np



""" Experiment network rates 

(rates for single query experiments (length 7) varying event node ratio, network size, outdegree)
ev = [[78607, 9, 1, 1, 104, 27, 4505]]

(rates for multi query experiments varying event node ratio, network size)
ev = [[507, 13, 1, 60, 4, 4, 6, 1144112, 2, 313, 13, 45, 45, 931, 27, 1, 39, 1, 628, 2, 214, 1, 30, 3, 6226]]

"""    



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

def main():

    
   # evQWL = [[507, 13, 1, 60, 4, 4, 6, 1144112, 2, 313, 13, 45, 45, 931, 27, 1, 39, 1, 628, 2, 214, 1, 30, 3, 6226]]
    #eventrates = regain_eventrates(evQWL) #-> for real world data set
    #default values for simulation 
    nwsize = 20
    node_event_ratio = 0.5
    num_eventtypes = 7
    eventskew = 1.7
    eventrates = [[]]
    #generate network of size nwsize, with node_event_ratio for given event rates (ev)   
    #eventrates = regain_eventrates(ev) #-> use rates given above to reproduce results from plots
    
    if len(sys.argv) > 1:
        nwsize =int(sys.argv[1])
    if len(sys.argv) > 2:   
        	node_event_ratio = float(sys.argv[2])
    if len(sys.argv) > 3:
        eventskew = float(sys.argv[3])
    if len(sys.argv) > 4:
        num_eventtypes = int(sys.argv[4])
        
    if len(sys.argv) > 3:    
        eventrates = generate_eventrates(eventskew,num_eventtypes)   
    print("HALLO" + str(eventrates))
    if not eventrates[0]:
   	  eventrates = generate_eventrates(eventskew,num_eventtypes)
    
    nw= []
    
    
    
    for node in range(nwsize):
        nw.append(generate_events(eventrates, node_event_ratio))
    
    while not allEvents(nw):
        nw = []
        for node in range(nwsize):
           nw.append(generate_events(eventrates, node_event_ratio))
    print(nw)

    
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


        



