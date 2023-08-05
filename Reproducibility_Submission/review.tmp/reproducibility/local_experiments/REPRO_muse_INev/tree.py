"""
Implementation of Query-Tree

"""
from helper import * 
import copy
from itertools import *
from parse_network import * 

class Tree():
    
    def __eq__(self, other): 
        if  isinstance(other, PrimEvent) and isinstance(self, PrimEvent):
            return self.evtype == other.evtype 
        elif (isinstance(self, AND) and isinstance(other, AND)) or (isinstance(self, SEQ) and isinstance(other, SEQ)):
            if len(self.children) != len(other.children):
                return False
            for i in self.children:
                mycount = self.children.count(i)
                if not i in other.children or other.children.count(i) != mycount :
                    return False
            for i in other.children:
                mycount = other.children.count(i)
                if not i in self.children or self.children.count(i) != mycount :
                    return False
            if isinstance(self, SEQ) and isinstance(other, SEQ):
                truelist = [1 for x in range(len(self.children)) if str(self.children[x]) == str(other.children[x])]
                if sum(truelist) == len(self.children):                    
                        return True
            else:
                return True      
        else:
             return False
         
    def __hash__(self):
        return hash(str(self))
    def __len__(self):
        return len(self.leafs()) #orleafs?
    
    def isleaf(self, node):
        if not hasattr(node,'children'): 
                return True
        else:
            return False        
        
    def getleafs(self):
        leafs = []    
        if isinstance(self, PrimEvent):
            return [self]
        for i in self.children:            
           if hasattr(i,'children'): 
                leafs = leafs +  i.getleafs()
           else:
                leafs.append(i)              
        return leafs 
    
    def getnodes(self):
        nodes = [self]       
        for i in self.children:           
           if hasattr(i,'children'):   
               nodes = nodes + i.getnodes()                      
        return nodes        
        
    def leafs(self):
        s = []
        leafs = self.getleafs()
        for i in leafs:
            s.append(str(i)) 
        return s
        
    def getparent(self, node): 
        for i in self.getnodes():
            if node in i.children:
                return i

    def getancestors(self, node): 
        
        ancestors = []       
        if self.is_root(node):
           return ancestors
        else:
            mypar = self.getparent(node)     
            ancestors.append(mypar)
            ancestors += self.getancestors(mypar)       
        return ancestors
    
    def getrev_ancestors(self, node):         
        rev_ancestors = []       
        if self.isleaf(node):
           return rev_ancestors
        else:
            mychildren = node.children     
            rev_ancestors += mychildren
            for child in mychildren:
                rev_ancestors += self.getrev_ancestors(child)                  
            return rev_ancestors
                      
        
    def is_root(self,node):
        if self.getparent(node) == None:
            return True
        else:
            return False
        
    def level(self,node):        
        if self.is_root(node):
            return 0
        else:
            return self.level(self.getparent(node))+1
    
                    
    def getsiblings(self,node):
        parent = self.getparent(node)
        siblings = list(parent.children)
        siblings.remove(node)
        return siblings
        
    def getsubop(self, *nodes):
            """
            Return projection for given query and set of leafs (primitive event types of query).
            """
     
            subop = copy.deepcopy(self)   
            if len(nodes) == 1:
                nodes = nodes[0]
                if self.getleafs().count(nodes) > 1:
                    nodes = [nodes for i in range(self.getleafs().count(nodes))];
            for  i in sorted(subop.getleafs(), key = lambda x: self.level(x), reverse = True):  
                 if i not in nodes:                      
                     parent = subop.getparent(i)  
                     l = list(parent.children)    
                     l.remove(i)                 
                     parent.children = l
                 
            for i in sorted(subop.getnodes(), key = lambda x: subop.level(x), reverse = True):                   
                if not list(i.children):
                    parent = subop.getparent(i)
                    l = list(parent.children)
                    l.remove(i)
                    parent.children = l
                if len(i.children) == 1:
                    if subop.is_root(i):
                        
                        subop = i.children[0]
                        
                    else: 
                        parent = subop.getparent(i)
                        l = list(parent.children)
                        ind = l.index(i)
                        l[ind]=i.children[0]                        
                        parent.children = l
                
                         
            return subop
        
    def rename_leafs(self, newleaflist):
        doubles = getdoubles_k(newleaflist)
        counts = {}
        for i in self.getleafs():
               my_i = filter_numbers(str(i))
               if not my_i in counts.keys():
                   counts[my_i] = 0
               if filter_numbers(str(i)) in newleaflist:
                   i.rename(filter_numbers(str(i)))
               if filter_numbers(str(i)) in doubles.keys():   
                  counts[my_i] =  counts[my_i] +1
                  i.rename(filter_numbers(str(i))+str(counts[my_i])) 
        return self
    
    def renamed(self):
       doubles = []
       mychildren =  list(map(lambda x: str(x) , self.children))
       mychildren = list(map(lambda x: filter_numbers(x), mychildren))
       for i in mychildren:
           if mychildren.count(i)>1 and not i in doubles:
               doubles.append(i)
       mychildren = filter(lambda x: x not in doubles, mychildren)
       return self.rename_leafs(mychildren)

    def getsequences(self):
        mysequence = {}
        for i in sorted(self.getnodes(), key = lambda x: self.level(x), reverse = True):  
                if isinstance(i, SEQ):
                   for childindex in range(len(i.children)): 
                       mysequence[str(i.children[childindex])] = []
                       if isinstance(i.children[childindex], PrimEvent):
                           if i.children[childindex+1:]:
                               mysequence[str(i.children[childindex])].append(list(map(lambda x: x.leafs(), i.children[childindex+1:])))
                       else:
                           for l in i.children[childindex].leafs():
                               if not str(l) in mysequence.keys():
                                   mysequence[str(l)] = []
                            
                               mysequence[str(l)].append(list(map(lambda x: x.leafs(), i.children[childindex+1:])))
        mysequencelist = list(mysequence.keys())                       
        for i in  mysequencelist :
            if  not mysequence[i]:
                del mysequence[i]
            else:               
               mysequence[i] = sum(mysequence[i], [])
               mysequence[i] = sum(mysequence[i], [])
        return mysequence
               
    def ispartof(self, other):
        if set(list(map(lambda x: filter_numbers(x),self.leafs()))) != set(list(map(lambda x: filter_numbers(x),other.leafs()))):            
            return False
        elif isinstance(self,PrimEvent) and isinstance(other, PrimEvent):
            if self == other:
                return True
        else:
            mysequence = self.getsequences()
            othersequence = other.getsequences()
            for i in othersequence.keys():               
                if not i in mysequence.keys() :          
                   return False
                
                elif not set(othersequence[(i)]).issubset(set(mysequence[i])):             
                    return False
        return True
    
    def can_be_used(self, other):
        """
        True if projection (other) can be used in combination of another projection (self).
        """
        mychildren = list(map(lambda x: filter_numbers(x),self.leafs()))
       
        otherchildren = list(map(lambda x: filter_numbers(x),other.leafs()))
        
        
        
        if not set(otherchildren).issubset(set(mychildren)):
            return False
         
        mysequence = self.getsequences()
        othersequence = other.getsequences()
        newothersequence = {}
    
        if len(self.leafs()) == len(list(map(lambda x: filter_numbers(x),self.leafs()))):
            for k in othersequence.keys(): 
                if k not in mysequence.keys():
                    return False
                for v in othersequence[k]:
                    if not v in mysequence[k]:
                        return False
        return True
            
            
        

class AND(Tree):
    def __init__ (self, *children):
        self.children = children
        self.mytype = 'AND'
        
    def __str__(self):
        s = "AND("
        for i in self.children:
            s = s + str(i) + ", "
        s = s[:-2]
        s = s + ")"
        return s
    
    def evaluate(self): 
        rate = 1         
        for i in self.children:
            rate *= i.evaluate()
        rate *= len(self.children)
        return rate
    

class SEQ(Tree):
    def __init__ (self, *children):        
        self.children = children
        self.mytype = 'SEQ'
        
    def __str__(self):
        s = "SEQ("
        for i in self.children:            
            s = s + str(i) + ", "
        s = s[:-2]
        s = s + ")"            
        return s
    
    def evaluate(self): 
        rate = 1
        for i in self.children:
            rate *= i.evaluate()
        return rate

class PrimEvent(Tree):
    def __init__ (self, evtype):
        self.evtype = evtype
        
    def __str__(self):
        return self.evtype
    
    
    def rename (self, value):
        self.evtype = value
        return self
    
    def evaluate(self):
        return rates[filter_numbers(self.evtype)]



