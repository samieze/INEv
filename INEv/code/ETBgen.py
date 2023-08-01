#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 11:45:52 2020

@author: samira
"""



class Tuple:    
       def __init__(self, node, evtype):
        self.node = node
        self.evtype = evtype
     

class ETB: 
      def __init__(self, tuples):
          self.tuples = tuples

      def generateFromNW(self,network):
          for i in network.keys():
              for j in network[i]:
                      tuple = Tuple(i, j)
                      self.tuples.append(tuple)
                    
l = ETB([])


def printtuple(tuple):
    st = "(" +str(tuple.node) + ","+ tuple.evtype +")"
    return st



def generateETBS(query, tuples):
    start = [[]]
    query = list(map (lambda x: str(x), query.getleafs()))
    for i in query:
        c = True
        for tp in tuples:
            if tp.evtype == i:
               if not c:
                     length = len(start)
                     for et in range(len(start)):
                            x = list(start[et])
                            x.pop()
                            start.append(x)
                     for j in range(length, len(start)):
                            start[j].append(tp)
               else:                
                     for et in range(len(start)):
                            start[et].append(tp)
                            c = False  
    start = [list(tupl) for tupl in {tuple(item) for item in start }]
    return start 

       
       
def transformETBs(listETBs):
    myETBs = []
    for etb in listETBs:
        myETB = ""
        for element in etb:
            myETB+= element.evtype
            myETB+=str(element.node)
        myETBs.append(myETB)
    return  myETBs

def returnETBs(eventlist, network):
    l = ETB([])
    l.generateFromNW(network) 
    ETBs = generateETBS(eventlist, l.tuples)
    return transformETBs(ETBs)


def getETBofMS(etblist, parttype, node):
    outlist = []
    for etb in etblist:
        if parttype + str(node) in etb:
            outlist.append(etb)
    return outlist 