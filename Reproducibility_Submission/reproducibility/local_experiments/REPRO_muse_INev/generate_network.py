
"""
Generate network with given size (nwsize), node-event ratio (node_event_ratio), 
number of event types (num_eventtypes), event rate skew (eventskew)-
"""
import sys
import pickle
import numpy as np



""" Experiment network rates 

average event rates for google cluster data set first 12h, timewindow 30 min, 20 nodes
#ev = [[0,855, 212, 24, 400, 129, 0, 0.005,0.05]]
    
event rates experiment set 1
#ev = [[1, 6, 1, 1, 1, 7, 8777, 1, 542, 72, 39, 1, 1, 318, 3, 1, 17, 2, 12, 2]]
    
event rates experiment set 2 (scalability)
#ev = [[2, 71, 1, 168, 1717781, 24, 1, 2574, 4, 4, 39, 1, 6, 59, 9, 154, 2370, 7, 2, 4]]
"""    


ev = [[1154, 125, 1, 2, 74, 1, 1, 19, 1, 1, 3, 1, 2, 1, 20]]  
ev = [[2, 71, 1, 168, 1717781, 24, 1, 2574, 4, 4, 39, 1, 6, 59, 9, 154, 2370, 7, 2, 4,5000,1,90,4333,1,3]]  
def generate_eventrates(eventskew,numb_eventtypes):
    return np.random.zipf(eventskew,numb_eventtypes)

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

def main():
    
    
    #default values for simulation 
    nwsize = 20
    node_event_ratio =0.6
    num_eventtypes = 15
    eventskew = 1.5
    
    eventrates = regain_eventrates(ev) #generate network of size nwsize, with node_event_ratio for given event rates (ev)

    #
    eventrates = regain_eventrates(ev)
    
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
        
    nw= []
    
    for node in range(nwsize):
        nw.append(generate_events(eventrates, node_event_ratio))
        
               
        
    with open('network', 'wb') as network_file:
          pickle.dump(nw, network_file)       
    networkExperimentData = [eventskew, num_eventtypes, node_event_ratio, nwsize, min(eventrates)/max(eventrates)]      
    with open('networkExperimentData', 'wb') as networkExperimentDataFile:
        pickle.dump(networkExperimentData, networkExperimentDataFile)
    
    print("NETWORK")  
    print("--------") 
    for i in range(len(nw)):
      print("Node " + str(i) + " " + str(nw[i])) 
    print("\n")
    
    
if __name__ == "__main__":
    main()


        



