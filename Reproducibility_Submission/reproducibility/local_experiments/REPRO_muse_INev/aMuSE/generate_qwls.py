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

def generate_workload(maxlength, size):
    qwl = []
    
    for i in range(size):
        mylength = int(rd.uniform(2, maxlength+1))         
        nesting_depth = rd.uniform(1,mylength-1)        
        x = rd.uniform(0,1)
        if x <=0.5:
            query = SEQ()
        else:
            query = AND()
        query.children = generateQ(query, int(nesting_depth), mylength)
        query = number_children(query)
        qwl.append(query) 
    qwl_matches = map(lambda x: "".join(sorted(x.leafs())), qwl)
    if len(set(qwl_matches)) < len(qwl):
        qwl = generate_workload(mylength, size)
    return qwl

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

def main():
    size = 6
    number = 10
    

    ### test for reproducibility 
    q1 = SEQ(PrimEvent("K"), AND(PrimEvent("I1"), PrimEvent("L"), PrimEvent("I2"), PrimEvent("I3")))
    q2 = SEQ(PrimEvent("O"), AND(PrimEvent("L"), PrimEvent("G"), SEQ(PrimEvent("J"), PrimEvent("E2"), PrimEvent("B"))))
    q3 = SEQ(PrimEvent("M1"), AND(PrimEvent("M2"), PrimEvent("L1"), PrimEvent("M3"), PrimEvent("L2"), PrimEvent("L3"), PrimEvent("N")))
    q4 = AND(PrimEvent("D"), PrimEvent("K"), PrimEvent("A"), PrimEvent("C"))
    q5 = AND(PrimEvent("H"),PrimEvent("N1"), PrimEvent("D"), PrimEvent("N2"), PrimEvent("N3"))	
    wl = [q1, q2, q3, q4, q5]
    ###
    wl = generate_workload(size, number) 
    if len(sys.argv) > 1: 
        number = int(sys.argv[1])
    if len(sys.argv) > 2:
        size = int(sys.argv[2])    
        wl = generate_workload(size, number) 
    

    with open('current_wl', 'wb') as wl_file:
        pickle.dump(wl, wl_file)

    print("QUERY WORKLOAD")
    print("---------------") 
    for i in (list(map(lambda x: str(x), wl))):
        print(i) 
    print("\n") 

if __name__ == "__main__":
    main()
