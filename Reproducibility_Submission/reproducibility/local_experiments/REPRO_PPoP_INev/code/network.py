import string
import pickle

with open('network',  'rb') as  nw_file:
    nw = pickle.load(nw_file)

network = {}
rates = {}
primEvents = []

ind = 0
for node in nw:
    network[ind] = []
    for eventtype in range(len(node)):
        if node[eventtype] > 0:
            network[ind].append(string.ascii_uppercase[eventtype])
            if not string.ascii_uppercase[eventtype] in primEvents:
                primEvents.append(string.ascii_uppercase[eventtype])
            if not string.ascii_uppercase[eventtype] in rates.keys():
                rates[string.ascii_uppercase[eventtype]] = float(node[eventtype])
    ind+=1        
            

def events(node):
    return network[node]

nodes = {}
for i in network.keys():
    for event in network[i]:
        if not event in nodes.keys():
            nodes[event] = [i]
        else:
            nodes[event].append(i)

def instances_func(proj):    
    num = 1
    for i in proj:
        if len(i) == 1:
             num = len(nodes[i])*num
        else:
            for j in i:
                num = len(nodes[j])*num     
    return num

instances = {}
for i in primEvents:
    instances[i] = len(nodes[i])


    
