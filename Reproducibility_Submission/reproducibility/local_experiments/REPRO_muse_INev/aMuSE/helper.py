import string

def generate_twosets(match):
    match = list(set(match))
    return printcombination(match)

def filter_numbers(in_string):
    x = list(filter(lambda c: not c.isdigit(), in_string))    
    return "".join(x)


def changeorder(duo):
    temp = []
    duolist = list(duo)
    temp.append(duolist[1])
    temp.append(duolist[0])
    temp  = "".join(temp)
    return temp  

def getdoubles_k(subopkey):
    doubles ={}
    mylist = sepnumbers(subopkey)
    mylist = map(lambda y: filter_numbers(y), mylist)
    myevents = list(set(mylist))
    for i in myevents:
        if myevents.count(i)>1:
            doubles[i] = mylist.count(i)         
    return doubles

def rename_without_numbers(projkey):
    """ take care of query projections: input string "A1B2C3A2" -> "A1BCA2", but also "A1A3C" -> "A1A2C" """
    doubles = getdoubles_k(projkey)
    newlist = []
    for i in projkey:
        if not filter_numbers(i) in doubles.keys(): 
            newlist.append(filter_numbers(i)) 
    for i in doubles.keys():
        for num in range(doubles[i]):
            newlist.append(i+str(num+1))
             
 
    return "".join(sorted(list(newlist))) 


        
def add_numbering(projkey):
    """ take care of query projections: input string "AAB" -> "A1A2B" """
    types = list(set(projkey))
    projkey = list(projkey)
    for i in types:
        mycount = projkey.count(i)
        if mycount > 1:
           c = 0
           for k in projkey:
               if k == i:
                   m = i + str(c + 1)
                   projkey[projkey.index(k)] = m
                   c += 1
                            
    return ''.join(projkey)


def sepnumbers(evlist):
    """ "A1B" -> [A1,B] """   
    newevlist = []
    if (len(evlist) > len(filter_numbers(evlist))):            
        for i in range(len(evlist)):   
            if  evlist[i] in list(string.ascii_uppercase):
                newevlist.append(evlist[i])
            else:                 
                newevlist[len(newevlist)-1] = newevlist[len(newevlist)-1] + str(evlist[i])               
    else:
        newevlist = evlist
    return newevlist


def combinationUtil(arr, n, r, index, data, i, b1): 

    if(index == r): 
        b2 = ""
        for j in range(r): 
           b2 = b2 + data[j]
        b1.append(b2) 
        return  
 
    if(i >= n): 
        return   

    data[index] = arr[i] 
    combinationUtil(arr, n, r, index + 1, data, i + 1, b1)     

    combinationUtil(arr, n, r, index, data, i + 1, b1) 
  
  

def printcombination(arr): 
    r = 2
    n = len(arr)
    data = list(range(r)) 
    b1 = []

    combinationUtil(arr, n, r, 0, data, 0, b1) 
    return b1


def combinationUtil2(arr, n, r,  
                    index, data, i, b1): 

    if(index == r): 
        b2 = ""
        for j in range(r): 
           b2 = b2 + data[j]
        b1.append(b2) 
        return
  
 
    if(i >= n): 
        return 
  

    data[index] = arr[i] 
    combinationUtil(arr, n, r, index + 1, data, i + 1, b1) 
      

    combinationUtil(arr, n, r, index, data, i + 1, b1) 
  
  

def printcombination2(arr): 
    r = 2
    n = len(arr)
    data = list(range(r)) 
    twosets = []

    combinationUtil(arr, n, r, 0, data, 0, b1) 
    return twosets

