"""
Generate for each query the set of beneficial projections.
Generate for each beneficial projection all non-redundant combination.
Generates for each (projection,combination) the set of local placements.
"""
import pickle
import time
import subsets as sbs 
import random as rd
import numpy as np
from tree import * 


start_time = time.time()

mode = "no" 
 
with open('current_wl',  'rb') as  wl_file:
    wl = pickle.load(wl_file)
    
with open('selectivities', 'rb') as selectivity_file:
    selectivities = pickle.load(selectivity_file)  
    
    
ninf = - np.inf
used  = {}
matches = map(lambda i: i.leafs(), wl)
match_query_dict = dict(zip(wl, matches))
placement_options = {}


def settoproj(evlist,query):
    """ take query and list of prim events and return projection"""
    leaflist = []
    evlist = sepnumbers(evlist)    
    for i in evlist:   
        leaflist.append(PrimEvent(i))        
    newproj = query.getsubop(leaflist)  
    return newproj 
    
def may_be_placed(proj, outrate):
    po = []
    myrates = []
    proj = filter_numbers(proj)
    maximalrate = max(map(lambda x: rates[x], proj))
    sumrates = sum(map(lambda x: rates[x], proj))
    
    if sumrates > outrate : 
        for i in proj:      
            if mode == "ex": 
                po.append(i)                
            else:
                if rates[i]< maximalrate and rates[i] > outrate * instances_func(proj) and not i in po:
                     po.append(i)             
                elif rates[i] == maximalrate and rates[i]  > outrate * (instances_func(proj) / instances[i]) and not i in po:
                      po.append(i)
    return po

def rec_placements(proj, placement_options_dic, x):
       """ recursively generate local placement options for projection """
       
       ind = list(placement_options_dic.keys()).index(proj)
       key = list(placement_options_dic.keys())[ind]
       
    
       
       for e in placement_options_dic[key]:
           e = filter_numbers(e)
           if len(e) == 1: 
               if not e in x:
                   x.append(e)
           else:
             
              rec_placements(e, placement_options_dic,x)
       return x   
    
def unredundantcombo(combolist, projkey):   
    """ check if a combination is redundant """
    notredundant = True
    doubles = getdoubles_key(projkey)
    for i in combolist:
      
        if i in doubles:
            continue
        else:
            newcombolist = list(combolist)
            newcombolist.remove(i)   
            i = sepnumbers(i)
            temp_combo = "".join(list(set(newcombolist)))      
            if set(i) == set(i).intersection(set(sepnumbers(temp_combo))):
                return False
    return notredundant  



def return_selectivity(proj, selectivities):
    """ return selectivity for arbitrary projection """
    proj = list(map(lambda x: filter_numbers(x), proj))
    two_temp = sbs.printcombination(proj,2)    
    selectivity = 1
    for two_s in two_temp:       
        if two_s in selectivities.keys():           
           if selectivities[two_s]!= 1:
               selectivity *= selectivities[two_s]
    return selectivity

def min_max_doubles(query,projevents):
    doubles = getdoubles_k(projevents)
    leafs = map(lambda x: filter_numbers(x), query.leafs())
    for event in doubles.keys():
        if not doubles[event] == leafs.count(event):
            return False
    return True
   

def generate_proj_combs_placements(query, selectivities, projection_dict, placement_options_dic, projrates, subop_mapping, global_subop_mapping):      
    match = query.leafs()
    projlist = match
    subop_mapping[str(query)]["".join(sorted(query.leafs()))] = [query]
    querykey = "".join(sorted(query.leafs()))
    if not querykey in global_subop_mapping.keys():
        global_subop_mapping[querykey] = [query]
    else:
         global_subop_mapping[querykey].append(query)
    for i in range(2, len(match)):
           iset =  sbs.boah(match, i) 
           for k in range(len(iset)):                   
                    curcom = list(iset[k].split(","))          
                    projevents = rename_without_numbers("".join(sorted(list(set(curcom))))) #A1BC becomes ABC and A1B1CA2 becomes A1BCA2                    
                    mysubop = settoproj(curcom, query) 
                    mysubop = mysubop.rename_leafs(sepnumbers(projevents))      #renaming on tree > A1BC becomes ABC and A1B1CA2 becomes A1BCA2                                                                  
                    outrate = mysubop.evaluate()                          
                    selectivity =  return_selectivity(curcom, selectivities)
                    rate = outrate * selectivity                            
                    placement_options = may_be_placed(projevents,rate)                 
                    if placement_options and min_max_doubles(query, projevents):                           
                                if not projevents in global_subop_mapping.keys():
                                    global_subop_mapping[projevents] = [mysubop]
                                elif global_subop_mapping[projevents].count(mysubop) == 0:
                                    global_subop_mapping[projevents].append(mysubop)   
                                if list(projection_dict.keys()).count(mysubop) == 0:        
                                    projection_dict[mysubop] = [sorted(list(set(map(lambda x: filter_numbers(x),curcom))))]
                                projrates[mysubop] = (selectivity, rate)
                                placement_options_dic[mysubop] = placement_options 
                                    
    projlist +=  subop_mapping[str(query)].keys() 
    projection_dict[query] = sorted([list(set(map(lambda x: filter_numbers(x), list(query.leafs()))))]) 
    placement_options_dic[query] = list(set(map(lambda x: filter_numbers(x),query.leafs())))
    
    for i in projection_dict.keys():
        if not i in wl:
            used[str(i)] = False
    outrate = query.evaluate()                          
    selectivity =  return_selectivity(list(set(query.leafs())), selectivities)
    rate = outrate * selectivity                            
    projrates[query] = (selectivity, rate)    
    
    return projrates, projection_dict, placement_options_dic, subop_mapping, global_subop_mapping



def onlyforsubops(mysubop, mysubopkey, projlist, global_subop_mapping):
    """ return list of projection keys that can be used in a combination of a given projection"""
    
    combination_translation = {} 
    curprojlist = copy.deepcopy(projlist)
   
    for i in projlist:       
         cur_i = filter_numbers(i)
         cur_my_i = filter_numbers(mysubopkey)
         if len(cur_i)>len(cur_my_i):             
             curprojlist.remove(i)            
         else:
             for l in cur_i:                 
                  if not l in cur_my_i:                
                      if i in curprojlist:                          
                          curprojlist.remove(i)                          
    for i in curprojlist:
            for myops in global_subop_mapping[i]:    
                if not myops == mysubop:
                 if myops.can_be_used(mysubop):    
                    if not i in combination_translation.keys():
                        combination_translation[i] = [myops]
                    else:
                        combination_translation[i].append(myops)
                     
    curprojlist = list(combination_translation.keys()) + list(set(list(filter_numbers(mysubopkey))))
    if wl.count(mysubop)>0: 
        projections_of_matches["".join(sorted(mysubop.leafs()))] = sum(combination_translation.values(),[])
        projections_of_matches["".join(sorted(mysubop.leafs()))].append(mysubop)    


    return curprojlist, combination_translation

def getdoubles(subop):
    """ return list of primitive event types that appear multiple times in a query and the number of occurrences """
    doubles =  {}
    mylist = map(lambda x: str(x), subop.leafs())
    mylist = map(lambda y: filter_numbers(y), mylist)
    myevents = list(set(mylist))
    for i in myevents:
        if myevents.count(i)>1:
            doubles[i] = mylist.count(i)           
    return doubles

def getdoubles_key(subopkey):
    doubles = []
    mylist = map(lambda y: filter_numbers(y), subopkey)
    myevents = list(set(mylist))
    for i in myevents:
        if  myevents.count(i)>1:
            doubles.append(i)          
    return doubles

def critical_doubles(subop, query, combitranslation):
    critical_doubles_list = []
    doubles = getdoubles(subop)
    
    for sub in subop.getnodes():       
        if isinstance(sub,SEQ):
            mychildren = map(lambda x: str(x), sub.children)
            mychildren = map(lambda x: filter_numbers(x), mychildren)
            for i in doubles.keys():
                if i in mychildren  and not mychildren.count(i) == doubles[i]: 
                     critical_doubles_list.append((sub,i))
    critical_doubles_list_ancestors = []
    for critical_tuple in  critical_doubles_list: 
        subop = critical_tuple[0]
        subop_renamed = copy.deepcopy(subop)
        subop_renamed = subop_renamed.renamed()
        mydouble = critical_tuple[1] 
        for anc in combitranslation: 
            if subop in query.getrev_ancestors(anc) or subop_renamed in query.getrev_ancestors(anc):
                ancleafs = map(lambda x: filter_numbers(x), anc.leafs())
                if ancleafs.count(mydouble) < doubles[mydouble]:
                     critical_doubles_list_ancestors.append((anc, mydouble))
    critical_doubles_list += critical_doubles_list_ancestors
    return critical_doubles_list, doubles


def combination_fix_doubles(mysubop,newcurcoms, query, combitranslation):
    v =  combitranslation.values()
    v = sum(v,[])
    criticalout = critical_doubles(mysubop, query, v)
    criticalops = criticalout[0]
    for curcom in newcurcoms:
            complete = False
            for critops in criticalops:
                if critops[0] in curcom:
                    for element in range(len(curcom)):
                        myelement = curcom[element]
                        if myelement == critops[1]:
                            complete = True
                        elif isinstance(myelement,Tree) and (myelement not in [a[0] for a in criticalops if a[1] == critops[1]]) and (critops[1] in map(lambda x: str(x), myelement.children)):
                            complete = True
                        elif element == len(curcom)-1 and not complete:
                
                            curcom.append(critops[1])
                else:
                    myprojkey = "".join(sorted(list(set(map(lambda x: filter_numbers(x), mysubop.leafs() )))))
                    curcomkeys = ["".join(sorted(x.leafs()))  if isinstance(x,Tree) else x for x in curcom]
                    if not unredundantcombo(curcomkeys, myprojkey):
                        curcom == list(set(curcom))
                        for i in curcom:
                            if len(i) == 1:
                                for j in curcom:
                                    if len(j)>1:
                                        if i in j.leafs() and i in curcom:
                                            curcom.remove(i)        
    return newcurcoms


    
def combitranslate(curcom, combitranslation):
    curcoms = [[]]

    for element in curcom:        
        if len(filter_numbers(element)) == 1: 
            for variant in curcoms:
                variant.append(element)      
        elif len(combitranslation[element]) ==1 :
             for variant in curcoms:
                 variant.append(combitranslation[element][0])  
        else:
            for variant in curcoms:
                myvariants = []
                todelete = []
                for translation in combitranslation[element]:                    
                    myvariant = variant + [translation]
                    myvariants.append(myvariant)
                    todelete.append(variant)
            for i in todelete:
                if i in curcoms:
                    curcoms.remove(i)
            for i in myvariants:
                curcoms.append(i)
            
    return curcoms

def generatecombinations(projection_dict, global_subop_mapping):   
  """ generate combination for each projection of queries in query workload """   
  projlist = list(global_subop_mapping.keys())  
  
  for mysubopkey in sorted(global_subop_mapping.keys(), key = len):         
      for mysubop in global_subop_mapping[mysubopkey]:                     
                   
                   
                   onlyforsubopsout  = onlyforsubops(mysubop, mysubopkey, projlist, global_subop_mapping)                   
                   my_list= onlyforsubopsout[0]                   
                   combitranslation = onlyforsubopsout[1]
                   
                   for i in range(1, len(filter_numbers(mysubopkey))):
                       iset =  sbs.boah(my_list, i)                
                       for k in range(len(iset)):                       
                                curcom = list(iset[k].split(","))      
                                projkey = []            
                                for c in curcom:                                    
                                    if len(c) > 1:
                                        c = sepnumbers(c)
                                    else:
                                        c = [c]
                                    projkey += c                                                    
                                projkey = sorted(list(set(map(lambda x: filter_numbers(x), projkey))))
                                projkey = "".join(projkey)                               
                                if (projkey == mysubopkey or projkey=="".join(sorted(list(set(filter_numbers(mysubopkey)))))) and unredundantcombo(curcom, mysubopkey):        
                                   
                                    ind = sorted(list((projection_dict.keys())), key = len).index(mysubop)
                                    mykey = sorted(list(list(projection_dict.keys())), key= len)[ind]  
                        
                                    
                                    if not curcom in projection_dict[mykey]:                                               
                                            newcurcoms = combitranslate(curcom, combitranslation)
                                           
                                            if len(set(mysubopkey)) != len(mysubopkey): # here mysubopkey = ABD is accepted to generate AB1B2D                                                
                                                newcurcoms = combination_fix_doubles(mysubop, newcurcoms, query,combitranslation)                                            
                                            for newcurcom in newcurcoms:
                                                newcurcom = list(set(newcurcom))                                          
                                                if not newcurcom in projection_dict[mykey]:                                                
                                                   projection_dict[mykey].append(newcurcom)    
                                    
  return projection_dict
       
def generate_combination_costs(projection_dict, placement_options_dict, wl):
    combinationcosts= {}
    for proj in projection_dict.keys():
        combinationcosts[proj] = {} 
        for combi in projection_dict[proj]: 
            key = []
            for element in combi :
                if not isinstance(element, Tree):
                    key.append(element)
                else:
                    index = list(projection_dict.keys()).index(element)
                    key.append(list(projection_dict.keys())[index])
            key = tuple(key) 
            combinationcosts[proj][key] = []         
            for i in combi:                            
                if not isinstance(i, Tree):
                    i = filter_numbers(i)
                    if (i in placement_options_dict[proj] or proj in wl) and not (i,ninf) in combinationcosts[proj][key]:
                        combinationcosts[proj][key].append((i,ninf))
                else:                
                        index = list(projection_dict.keys()).index(i) 
                        new_i = list(projection_dict.keys())[index]                        

                        pl = rec_placements(new_i,placement_options_dict,[])       
                        for po  in pl:
                             if not (po,ninf) in combinationcosts[proj][key]:
                                combinationcosts[proj][key].append((po,ninf)) 

            if not combinationcosts[proj][key]:               
               del combinationcosts[proj][key] 
    return combinationcosts

def initialize_rates(projrates, rates):
    for i in projrates.keys():
        rates[i] = projrates[i][1]
    return rates

def initialize_instances(projection_dict, instances):
    for i in projection_dict.keys():
        myleafs = i.leafs()
        myinstances = 1
        for leaf in myleafs:
                myinstances *=instances[filter_numbers(leaf)]
        instances[i] = myinstances
    return instances 



projection_dict = {}
subop_mapping = {}
placement_options_dic = {} 
projrates = {}
subop_mapping = {}
global_subop_mapping = {}
projections_of_matches = {}

for i in range(len(wl)):    
    query = wl[i]
    subop_mapping[str(query)] = {}
    x = generate_proj_combs_placements(query, selectivities,projection_dict, placement_options_dic, projrates, subop_mapping,   global_subop_mapping)
    if i == 0:
        projection_dict = x[1]
        placement_dict = x[2]
        projrates = x[0]
        suop_mapping = x[3]
        global_subop_mapping = x[4]
    else: 
       
        projection_dict.update(x[1])
        placement_dict.update(x[2])
        projrates.update(x[0])
        suop_mapping.update(x[3])
        global_subop_mapping.update(x[4])




projection_dict.update(generatecombinations(projection_dict, global_subop_mapping))

         

for query in projections_of_matches.keys():    
    newprojections = []
    for projection in projections_of_matches[query]:
        index = list(projection_dict.keys()).index(projection)
        newprojection =  list(projection_dict.keys())[index]

        newprojections.append(newprojection)
    del projections_of_matches[query]
    projections_of_matches[query] = newprojections

for query in wl:
    x = "".join(sorted(query.leafs()))
    if not x in projections_of_matches.keys():
        projections_of_matches[x] = [query]
        for proj in projection_dict.keys():
            if not proj in wl:
                del projection_dict[proj]

          
          
rates = initialize_rates(projrates, rates)
instances = initialize_instances(projection_dict, instances)
combinationcosts =  generate_combination_costs(projection_dict, placement_dict,  wl)

combigen_time = round(time.time() - start_time, 2)





