#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 31 13:22:58 2021

@author: samira
"""
class EvaluationPlan():
    def __init__ (self, projections, instances):
        self.projections = projections
        self.instances = instances
        
    def addProjection(self, projectionName):
        p = Projection(projectionName, {}, [], [], [])
        self.projections.append(p)
        # init spawned projections 
        
    def getProjection(self, projectionName):
        for i in self.projections:
            if i.name == projectionName:
                return i
            
    def addInstances(self, proj, name):
        self.instances.append(Instance(proj, name, [], {}))   # we could actually add one source here already... 
        
    def getByName(self, newname):
        for i in self.instances:
            if i.name == newname:
                return i
    
    def updateInstances(self, newInstances):
        for i in newInstances:
            myInstance = self.getByName(i.name)
            if myInstance: #TODO remove later when instances for peojwctions also there
                myInstance.update(i)
            
    def initInstances(self, InstanceDict):
        for name in InstanceDict.keys():
            if len(name) > 1:
                newInstance = Instance(name[0], name, [InstanceDict[name]], {})
                self.instances.append(newInstance)
        
class Projection():
# projections have names and combinations which are also lists of projections, sink nodes (depending on placement style), and sources which encapsulate routing inforation for each etb of etype in combination
    def __init__ (self, name, combination, sinks, spawnedInstances, Filters):
        self.name = name
        self.sinks = sinks
        self.combination = combination #dict: key is projection name, value is list of instances
        self.spawnedInstances = spawnedInstances
        self.Filters = Filters
        
    def addSinks(self, sink):
        self.sinks.append(sink)
    
    def addProjection(self, combination):
        self.combination[combination] = ''
    
    def addInstances(self, projection, instances):
        self.combination[projection] = instances
    
    def addSpawned(self, spawned):
        self.spawnedInstances += spawned
     
    
      
    
    #spawned Instances

    def __str__(self):
        mystring = "Projection: " + str(self.name) + "\n============================= \n- Combination: ["
        for proj in self.combination.keys():
            mystring += str(proj) + " "
        mystring += "] \n- Sink: " + str(self.sinks) + "\n"
        mystring +=  "Instances: "  + "\n"
        for key in self.combination.keys():
             mystring +=  str(key) + " :  \n"
             for instance in self.combination[key]:
                 mystring += str(instance) + " \n"
        mystring += "Filters: \n"
        for filterTuple in self.Filters:
            mystring += str(filterTuple[0]) + " : " + str(filterTuple[1]) + "\n"
        mystring += " \n"
    
        return mystring
        
    
class Instance(): # single etbs, where they are from and how they are routed to the source of the projection, there will be multiple instances of the same etb having a 
      def __init__ (self, projname, name, sources, routingDict):
        self.projname = projname
        self.name = name
        self.sources = sources
        self.routingDict = routingDict #[SEQ(AB): treeObject which describes how a1 from node 1 is routed]
        
      def __str__(self):
         mystring = str(self.projname) + "\n" 
         mystring +=  "Instance: " + str(self.name) + "; Source: " + str(self.sources)  + " \n" 
         for key in self.routingDict.keys():
             mystring += str(key) + " : " + str(self.routingDict[key]) + " \n"
         return mystring
     
      def update(self, newinstance):
          for newsource in newinstance.sources:
              if not newsource in self.sources:
                  self.sources.append(newsource)
          for newkey in newinstance.routingDict.keys():
              self.routingDict[newkey] = newinstance.routingDict[newkey]
          
        


