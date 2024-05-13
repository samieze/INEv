#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 17:12:21 2021

@author: samira
"""
import networkx as nx 
import pickle
#from networkx.algorithms.components import is_connected
import matplotlib.pyplot as plt
import sys

def main():
   with open('network', 'rb') as network_file:
            nw = pickle.load(network_file) 

   outdegree = 2
   if len(sys.argv) > 1:
        outdegree =int(sys.argv[1])
         

   G = nx.Graph()
   G = nx.connected_watts_strogatz_graph(len(nw),outdegree,0.2)

   #nx.draw(G, with_labels=True, font_weight='bold')
   #plt.show()
   
   with open('graph', 'wb') as graph_file:
              pickle.dump(G,graph_file)         
              
          
          
          
if __name__ == "__main__":
    main()          
