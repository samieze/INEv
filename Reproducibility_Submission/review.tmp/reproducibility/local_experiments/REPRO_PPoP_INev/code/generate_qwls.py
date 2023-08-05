"""
Generate query workload with given number of queries (number), maximal query length (size).    

Queries for Case Studies:
    #wl = [AND(PrimEvent('E'), PrimEvent('F'), PrimEvent('G'),PrimEvent('H'))] # final 1 bikecity
    #wl =  [SEQ(PrimEvent('C'), PrimEvent('D'), PrimEvent('E'),PrimEvent('I'))]  # final 2 bikecity
    #wl = [AND(PrimEvent('A'), SEQ(PrimEvent('D'), PrimEvent('I')),PrimEvent('F'))] #final 3 bikecity
    #wl = [SEQ(PrimEvent('A'), AND(PrimEvent('B'), PrimEvent('I')),PrimEvent('E')), AND(PrimEvent('E'), PrimEvent('F'), PrimEvent('C'),PrimEvent('H'))] #final 4 bikecity

    #wl = [SEQ(PrimEvent('A'), PrimEvent('C'), PrimEvent('I'), PrimEvent('E')), AND(PrimEvent('F'), SEQ(PrimEvent('C'), PrimEvent('I')), PrimEvent('G'))]
    
    #wl = [SEQ(PrimEvent('A'), PrimEvent('B'), PrimEvent('G'), PrimEvent('F'), PrimEvent('I'))] # Google: jobLost
    #wl= [SEQ(PrimEvent('B'), PrimEvent('C'), PrimEvent('F'), PrimEvent('H'))] # Google: unlucky user
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
        
        
        query = number_children(query)
        if not hasdoubles(query): # changed
            qwl.append(query) 

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
            if i.hasKleene():
                kleene.append(i)
            if i.hasNegation():
                negation.append(i)
            if not i in negation and not i in kleene:
                none.append(i)
          
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
        if not negation:
           if negKL < 1 and maxlength-count-3 >= remainingPrims:      # negation           
                    myq = NSEQ()
                    myq.children = [getPrim(), getPrim(), getPrim()]
                    children.append(myq)
                    count +=3            
                    negation = True
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
        
def makeLongBalanced(count, length):
    wl = generate_BalancedWorkload(count, length)      
    return wl

def main():
    count = 1
    length = 3
    if len(sys.argv) > 1: 
        length  = int(sys.argv[1])
    if len(sys.argv) > 2:
        count = int(sys.argv[2])    
    if len(sys.argv) > 3:
        negated = int(sys.argv[3])
    

    # generate workload with 1/3 queries containing kleene and 1/3 queries containing nseq
    #wl =  makeLongBalanced(count, length)      
    
    # generate workload without kleene and nseq
    wl = generate_workload(count, length)
    
    
    # if negated:
    #      wl = [AND(PrimEvent('D'),SEQ(PrimEvent('B'), KL(PrimEvent('A')), PrimEvent('C')),PrimEvent('E'))]
    # else:
    #      wl = [AND(PrimEvent('D'),SEQ(PrimEvent('B'),  PrimEvent('A'), PrimEvent('C')),PrimEvent('E'))]
        
    
    #wl = [AND(PrimEvent('E'), PrimEvent('F'), PrimEvent('G'),PrimEvent('H'))] # final 1 bikecity
    #wl =  [SEQ(PrimEvent('C'), PrimEvent('D'), PrimEvent('E'),PrimEvent('I'))]  # final 2 bikecity
    #wl = [AND(PrimEvent('A'), SEQ(PrimEvent('D'), PrimEvent('I')),PrimEvent('F'))] #final 3 bikecity
    #wl = [SEQ(PrimEvent('A'), AND(PrimEvent('B'), PrimEvent('I')),PrimEvent('E')), AND(PrimEvent('E'), PrimEvent('F'), PrimEvent('C'),PrimEvent('H'))] #final 4 bikecity

    #wl = [SEQ(PrimEvent('A'), SEQ(PrimEvent('H'), PrimEvent('B')),PrimEvent('I'))] # Google double update
    #wl = [SEQ(PrimEvent('I'), SEQ(PrimEvent('B'), PrimEvent('D')),PrimEvent('H'), PrimEvent('G'))] # Google failed update
    #wl = [SEQ(PrimEvent('A'), PrimEvent('B'), PrimEvent('G'),PrimEvent('F'), PrimEvent('I'))] # Google Lost Job 
    #wl = [SEQ(PrimEvent('B'), SEQ(PrimEvent('C'), PrimEvent('F')),PrimEvent('H'))] # Google unlucky
    
    wl = [AND(SEQ(PrimEvent('A'), PrimEvent('B'), PrimEvent('C')),SEQ(PrimEvent('D'), PrimEvent('E'), PrimEvent('F')))] # PP Comp

    
    with open('current_wl', 'wb') as wl_file:
        pickle.dump(wl, wl_file)

    print("QUERY WORKLOAD")
    print("---------------") 
    for i in (list(map(lambda x: str(x), wl))):
        print(i) 
    print("\n") 

if __name__ == "__main__":
    main()
