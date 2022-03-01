"""
Generate query workload with given number of queries (number), maximal query length (size).    
"""
from tree import *
import random as rd
import sys
import pickle


with open('network',  'rb') as  nw_file:
        nw = pickle.load(nw_file)
    
PrimitiveEvents = list(string.ascii_uppercase[:len(nw[0])])
 
Prim  = {}
for i in range(len(PrimitiveEvents)):
        Prim[i] = PrimitiveEvents[i]
        
        
def getPrim():
    x = rd.uniform(0, len(PrimitiveEvents))
    x = int(x)
    return PrimEvent(Prim[x])

def generate_workload(size, maxlength): #count, lenthh
    qwl = []
    
    while len(qwl) !=  size:
        mylength = int(rd.uniform(2, maxlength+1)) 
        while mylength == 2:
            mylength = int(rd.uniform(2, maxlength+1))         
        nesting_depth = rd.uniform(1,mylength-1)        
        x = rd.uniform(0,1)
        if x <=0.5:
            query = SEQ()
        else:
            query = AND()
        query.children = generateQ(query, int(nesting_depth), mylength)
        query = number_children(query)
        if not hasdoubles(query): # changed
            qwl.append(query) 
        

    return qwl

def hasdoubles(query):
    prims = map(lambda x: str(x), query.leafs())
    prims = list(map(lambda x: filter_numbers(x), prims))
    if len(prims) > len(list(set(prims))):
        return True
    else: 
        return False
    
def number_children(query):
    mychildren = query.leafs()
    children = query.getleafs()
    types = list(set(mychildren))
    for i in types:
        mycount = mychildren.count(i)
        if mycount > 1:
           c = 0
           for k in children:
               if str(k) == i:
                   newName = str(i) + str(c + 1)
                   c += 1
                   k.rename(newName)
                
    return query
    
def generateQ(query, nestingdepth, maxlength):
    count = 0
    children = []    
    remainingPrims = (maxlength - 1  - nestingdepth)    
    if nestingdepth == 1:
        for i in range(maxlength):   
            newchild = getPrim()

            children.append(newchild)    
        return children
    
    else:
        x = rd.uniform(0,remainingPrims)
        
        for i in range(int(x) +1):                
                newchild = getPrim()                  
                   
                children.append(newchild)
                count +=1               
              
        if isinstance(query,AND):
                    myquery = SEQ()
        elif isinstance(query,SEQ):
                    myquery = AND()
        myquery.children = generateQ(myquery, nestingdepth-1, maxlength - count)
        children.append(myquery)

        return children        

def makeLong(count, length):
    wl = generate_workload(count, length)     
    while True: 
        for i in wl:           
            if len(i.leafs()) == length:
                return wl         
        wl = generate_workload(count, length)     
    

def main():
    count = 10
    length = 6
    if len(sys.argv) > 1: 
        length  = int(sys.argv[1])
    if len(sys.argv) > 2:
        count = int(sys.argv[2])    
        
    wl =  makeLong(count, length)     
        


    with open('current_wl', 'wb') as wl_file:
        pickle.dump(wl, wl_file)

    print("QUERY WORKLOAD")
    print("---------------") 
    for i in (list(map(lambda x: str(x), wl))):
        print(i) 
    print("\n") 

if __name__ == "__main__":
    main()
