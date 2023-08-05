"""
Generate query workload incrementally (only used in experiments to evaluate benefit of sharing).
Generates single query while number of so far generated queries less than desired size of workload, appends to current workload. 
Load workload from file if desired size.
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
    
    #for i in range(size):          # changed
    while len(qwl) !=  size:
        mylength = int(rd.uniform(maxlength/2 , maxlength+1)) 
        while mylength == 2:
            mylength = int(rd.uniform(2, maxlength+1))         
        nesting_depth = rd.uniform(1,mylength-1)        
        x = rd.uniform(0,1)
        if x <=0.5:
            query = SEQ()
        else:
            query = AND()
        query.children = generateQ(query, int(nesting_depth), mylength)
        
        #query.children = generateQKL(query, int(nesting_depth), mylength, False, False) # WORKLOAD WITH KLEENE 
        
        #query.children = getNSEQQuery(query, int(nesting_depth), mylength, False)  # WORKLOAD WITH NSEQ 
        
        query = number_children(query)
        if not hasdoubles(query): # changed
            qwl.append(query) 
    #qwl_matches = map(lambda x: "".join(sorted(x.leafs())), qwl)

    return qwl



def generate_BalancedWorkload(size, maxlength): #count, lenthh
    qwl = []
    kleene  = [] 
    negation = []
    none  = []
    #for i in range(size):          # changed
    while len(qwl) !=  size:
        mylength = int(rd.uniform(maxlength/2 , maxlength+1)) 
        while mylength == 2:
            mylength = int(rd.uniform(2, maxlength+1))         
        nesting_depth = rd.uniform(1,mylength-1)        
        x = rd.uniform(0,1)
        if x <=0.5:
            query = SEQ()
        else:
            query = AND()
        #query.children = generateQ(query, int(nesting_depth), mylength)
        
        query.children = generateQKL(query, int(nesting_depth), mylength, False, False)
        query = number_children(query)
        if not hasdoubles(query): # changed
            qwl.append(query)
    for i in qwl:
            print(i)
            if i.hasKleene():
                kleene.append(i)
            if i.hasNegation():
                negation.append(i)
            if not i in negation and not i in kleene:
                none.append(i)
    # print("kleene", list(map(lambda x: str(x), kleene)))    
    # print("negation", list(map(lambda x: str(x), negation))) 
    # print("None", list(map(lambda x: str(x), none)))  
          
    if len(kleene) < int(size/3):            
            while len(kleene)  <int(size/3):
                mylength = int(rd.uniform(maxlength/2 , maxlength+1)) 
                while mylength == 2:
                    mylength = int(rd.uniform(2, maxlength+1))         
                nesting_depth = rd.uniform(1,mylength-1)        
                x = rd.uniform(0,1)
                if x <=0.5:
                    query = SEQ()
                else:
                    query = AND()
                query.children = getKleeneQuery(query, int(nesting_depth), maxlength, False)
                if  not hasdoubles(query):
                    kleene.append(query)
                    if none:
                        none.pop(0)
                               
    if len(negation) < int(size/3):    
            while len(negation) < int(size/3):
                mylength = int(rd.uniform(maxlength/2 , maxlength+1)) 
                while mylength == 2:
                    mylength = int(rd.uniform(2, maxlength+1))         
                nesting_depth = rd.uniform(1,mylength-1)        
                x = rd.uniform(0,1)
                if x <=0.5:
                    query = SEQ()
                else:
                    query = AND()
                query.children = getNSEQQuery(query, int(nesting_depth), maxlength, False)
                if  not hasdoubles(query): # changed            
                    negation.append(query)
                    if none:
                        none.pop(0)
                #query.children = getNSEQQuery(query, int(nesting_depth), mylength, False)
            print("negation", list(map(lambda x: str(x), negation)))      
         
    #qwl_matches = map(lambda x: "".join(sorted(x.leafs())), qwl)
    qwl = none + kleene + negation
    return list(set(qwl))


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


def generateQKL(query, nestingdepth, maxlength, negation, kleene):
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
        negKL = rd.uniform(0,1)  
        for i in range(int(x) +1):                
                newchild = getPrim()        
                   
                children.append(newchild)
                count +=1               
        
        if not kleene:
            if negKL < 1 and maxlength-count-1 >= remainingPrims:      # Kleene           
                    newchild = getPrim()             
                    children.append(KL(newchild))
                    count +=1            
                    kleene = True
                    # nestingdepth = min(maxlength - count -1, nestingdepth)
        if not negation:
           if negKL < 1 and maxlength-count-3 >= remainingPrims:      # negation           
                    myq = NSEQ()
                    myq.children = [getPrim(), getPrim(), getPrim()]
                    children.append(myq)
                    count +=3            
                    negation = True
                    #nestingdepth = min(maxlength - count -1, nestingdepth)
        if isinstance(query,AND):
                    myquery = SEQ()
        elif isinstance(query,SEQ):
                    myquery = AND()
        nestingdepth = min(nestingdepth, maxlength - count -1)    
        if nestingdepth < 2:
            nestingdepth = 2
        myquery.children = generateQKL(myquery, nestingdepth-1, maxlength - count, negation, kleene)
        children.append(myquery)

        return children 
        

def getKleeneQuery(query, nestingdepth, maxlength, kleene):
    count = 0
    children = []    
    remainingPrims = (maxlength - 1  - nestingdepth)   
    if nestingdepth == 1:
        if not kleene:
           newchild = getPrim()             
           children.append(KL(newchild))
           count +=1            
           kleene = True
        for i in range(maxlength - count):   
            newchild = getPrim()

            children.append(newchild)    
        return children
    else:
       if not kleene:
           newchild = getPrim()             
           children.append(KL(newchild))
           count +=1            
           kleene = True
       if isinstance(query,AND):
                    myquery = SEQ()
       elif isinstance(query,SEQ):
                    myquery = AND() 
       nestingdepth = min(nestingdepth, maxlength - count -1)    
       if nestingdepth < 2:
            nestingdepth = 2 
       myquery.children = getKleeneQuery(myquery, nestingdepth-1, maxlength - count,  kleene)
       children.append(myquery)

       return children      
   
def getNSEQQuery(query, nestingdepth, maxlength, negation):
    count = 0
    children = []    
    if nestingdepth == 1:
        if not negation:
           myq = NSEQ()
           myq.children = [getPrim(), getPrim(), getPrim()]
           children.append(myq)
           negation = True
           count += 3
           
        for i in range(maxlength - count):   
            newchild = getPrim()

            children.append(newchild)    
        return children
    else:
       if not negation:
           myq = NSEQ()
           myq.children = [getPrim(), getPrim(), getPrim()]
           children.append(myq)
           count +=3            
           negation = True
       
       if isinstance(query,AND):
                    myquery = SEQ()
       elif isinstance(query,SEQ):
                    myquery = AND() 
                    
       nestingdepth = min(nestingdepth, maxlength - count - 1)
    
       if nestingdepth < 2:
            nestingdepth = 2 
       myquery.children = getNSEQQuery(myquery, nestingdepth-1, maxlength - count,  negation)
       children.append(myquery)

       return children     
   
def makeLong(count, length):
    wl = generate_workload(count, length)     
    while True: 
        for i in wl:           
            if len(i.leafs()) == length:
                return wl         
        wl = generate_workload(count, length)     
        
def assign_windows(wl):
    my_wl = []
    for q in wl:
        my_wl.append((q, int(rd.uniform(1,10)))) #change timewindow span
    return my_wl
   
def makeLongBalanced(count, length):
   
    wl = generate_BalancedWorkload(count, length)      
    return wl
    # while True: 
    #     for i in wl:           
    #         if len(i.leafs()) == length:
    #             return wl         
    #     wl = generate_BalancedWorkload(count, length)      

def main():
    count = 2
    length = 5
    iteration = count
    
    if len(sys.argv) > 1: 
        length  = int(sys.argv[1])
    if len(sys.argv) > 2:
        count = int(sys.argv[2])    
    if len(sys.argv) > 3:
        # negated = int(sys.argv[3])
        iteration = int(sys.argv[3])     
    
    wl = generate_workload(count, length)
    wl_windows = assign_windows(wl)
    
    #with open('original_wl', 'rb') as wl_file:
    #    wl = pickle.load(wl_file)
    #with open('wl_windows', 'rb') as wl_windows_file:
     #   wl_windows = pickle.load(wl_windows_file) 
    
    window = max(wl_windows[x][1] for x in range(len(wl_windows)))
    #        notFirst = False
    #else:            
    #        notFirst = True
    #wl_from_file = []    
    #if notFirst:         
    #  with open('incremental_wl',  'rb') as  incremental_wl_file:
    #        wl_from_file = pickle.load(incremental_wl_file)   
    

    #if iteration < count: # if not desired qwl size
    #    wl = generate_workload(1, length) # generate single query
    #    incremental_wl = wl_from_file +  wl # append query to other queries for pickle
    #else: 
    #    wl = wl_from_file
    #    incremental_wl = []
        

    
    with open('current_wl', 'wb') as wl_file:
        pickle.dump(wl, wl_file)
        
    with open('original_wl', 'wb') as wl_file:
        pickle.dump(wl, wl_file)    
     
    with open('wl_windows', 'wb') as wl_windows_file:
        pickle.dump(wl_windows, wl_windows_file)   
        
    #with open('incremental_wl', 'wb') as incremental_wl_file:
    #    pickle.dump(incremental_wl, incremental_wl_file)    
        
    
    # overwrite rates!
    # SCALE RATES with current windows
    
    with open('original_network', 'wb') as original_network_file:
        pickle.dump(nw, original_network_file)  
        
    for i in range(len(nw)):  
        for rate in range(len(nw[i])):
            nw[i][rate] = window * nw[i][rate]
    with open('network', 'wb') as network_file:
        pickle.dump(nw, network_file)    

    print("QUERY WORKLOAD")
    print("---------------") 
    for i in (list(map(lambda x: str(x), wl))):
        print(i) 
    print("\n") 

if __name__ == "__main__":
    main()
