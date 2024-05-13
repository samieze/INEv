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
import random

def main():
    
   with open('network', 'rb') as network_file:
            nw = pickle.load(network_file) 
            
   percentage = 0
   outdegree = 4
   experiment = 'None'
   G = nx.Graph()
   G = nx.connected_watts_strogatz_graph(len(nw),outdegree,0.2)
     
   if len(sys.argv) > 1: 
      percentage = float(sys.argv[1])      
   if len(sys.argv) >2 :
     if int(sys.argv[2]) == 0:
          G = remove_edges(G, percentage)
          experiment = 'remove'
     elif int(sys.argv[2]) == 1:
          G = add_edges(G, percentage)
          experiment = 'add'
     elif int(sys.argv[2]) == 2:
          G = permute_edges(G, percentage)  
          experiment = 'permute'
          
   print(G.edges)
  # G = permute_edges(G, percentage)  
   print(G.edges)

 
   with open('graph', 'wb') as graph_file:
         pickle.dump(G,graph_file)     


def permute_edges(G,percentage): # new graph has less nodes as nodes are inferred from edges
    
    number =int( (len(G.edges) / 100) * percentage)
    list_edges = list(G.edges)
    random.shuffle(list_edges)
    new_edges = []
    for i in range(number):
        a = int(random.uniform(0, len(G.nodes)))
        b = int(random.uniform(0, len(G.nodes)))
        new_edges.append((a,b))
    my_edges=  list_edges[- (len(list_edges) - number):] + new_edges
    my_G = nx.Graph()
    my_G.add_edges_from(my_edges)
    while set(my_G) == set(G.edges) or G.nodes != my_G.nodes:
        list_edges = list(G.edges)
        random.shuffle(list_edges)
        new_edges = []
        for i in range(number):
            a = int(random.uniform(0, len(G.nodes)))
            b = int(random.uniform(0, len(G.nodes)))
            new_edges.append((a,b))
        my_edges=  list_edges[- (len(list_edges) - number):] + new_edges
        my_G = nx.Graph()
        my_G.add_edges_from(my_edges)
    return my_G


def remove_edges(G,percentage): 
    
    number =int( (len(G.edges) / 100) * percentage)
    list_edges = list(G.edges)
    random.shuffle(list_edges)
    
   
    my_edges = list_edges[0:len(list_edges ) - number]
    my_G = nx.Graph()
    if percentage > 50:
        return my_G
    my_G.add_edges_from(my_edges)
    while not nx.is_connected(my_G) or G.nodes != my_G.nodes:
        list_edges = list(G.edges)
        random.shuffle(list_edges)
        my_edges = list_edges[0:len(list_edges ) - number]
        my_G = nx.Graph()
        my_G.add_edges_from(my_edges)
    return my_G    

def add_edges(G,percentage):
    number =int( (len(G.edges) / 100) * percentage)
    list_edges = list(G.edges)
    random.shuffle(list_edges)
    new_edges = []
    for i in range(number):
        a = int(random.uniform(0, len(G.nodes)))
        b = int(random.uniform(0, len(G.nodes)))
        new_edges.append((a,b))
    my_edges = list_edges + new_edges 
    my_G = nx.Graph()
    my_G.add_edges_from(my_edges)
    while not nx.is_connected(my_G) or G.nodes != my_G.nodes:
        list_edges = list(G.edges)
        random.shuffle(list_edges)
        new_edges = []
        for i in range(number):
            a = int(random.uniform(0, len(G.nodes)))
            b = int(random.uniform(0, len(G.nodes)))
            new_edges.append((a,b))
        my_edges = list_edges + new_edges 
        my_G = nx.Graph()
        my_G.add_edges_from(my_edges)
    return my_G
    
              
          
          
          
if __name__ == "__main__":
    main()          