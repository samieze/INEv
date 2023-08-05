"""
Change order of queries in workload.    
"""
import pickle
from combigen_star import *
from parse_network import * 

def sort_wl_1(wl):
    """ sort based on central cost of queries """
    wl = sorted(wl, key = lambda x:costs(x), reverse = True)
    return wl      
     


def sort_wl_2(wl):
     """ sort based on number of combinations """
     wl = sorted(wl, key=lambda x: len(combinationcosts[x].keys()))
     return wl

def costs(query):
    leaflist = map(lambda x: filter_numbers(x), query.leafs())
    leaflist = list((leaflist))
    leaflist = map(lambda x: rates[x] *instances[x], leaflist)
    return  sum(leaflist)

with open('current_wl',  'rb') as  wl_file:
    wl = pickle.load(wl_file) 
    
wl = wl 
  
queries ={}
matches = ["".join(sorted(x.leafs())) for x in wl]
for i in wl:
    queries["".join(sorted(i.leafs()))] = i



