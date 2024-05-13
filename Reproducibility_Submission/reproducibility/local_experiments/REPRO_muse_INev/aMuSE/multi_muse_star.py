"""
Compute MuSE graph for network and query workload.
"""
import sys
import time
import combigen_star as cn
import numpy as np
from wl_order_star import *



ninf = -np.inf
start_time = time.time()

rates = cn.rates
instances = cn.instances
combigen_time = cn.combigen_time 
combinationcosts = cn.combinationcosts
projections = combinationcosts.keys()
placement_options = cn.placement_dict
projection_of_matches = cn.projections_of_matches
global_subop_mapping = cn.global_subop_mapping

combis = {}     
received_events_sender = {}
received_events = {}
for projection in combinationcosts.keys():
    received_events_sender[projection] = {}
    for i in network.keys():
        received_events[i] = []
        received_events_sender[projection][i] = []
  
        
        
def centralcosts():
    """ compute central costs for evaluation of query workload """
    costs = 0
    eventtypes = "".join(list(projections_of_matches.keys()))
    for i in instances.keys():
        if len(i) == 1 and i in list(eventtypes):
            costs += rates[i] * instances[i]
    return costs
        


def muse_needed(rest, placement_proj, placement, query): 
    """ decide if Multi Sink or Single Sink placement for a given projection, combination"""
    costs = 0 
    for ev in rest:            
            costs += rates[ev]*instances[ev]  
    if ((costs <= rates[placement_proj]  * (instances[placement_proj] / len(nodes[placement[0]]))) and (len(finalplacement_dict[placement_proj][placement[0]]) == len(nodes[placement[0]]))) or (query in wl and costs <= rates[placement_proj] ):
        return True
    else: 
        return False
    
def already_gathered(placement): 
    """ update received events after computation for a query of wl """
    gathered_eventtypes = sum(received_events.values(),[])
    if placement[0] in gathered_eventtypes:
        return True
    else:
        return False
    
def getlocalrate(node): 
    localrate = sum(map(lambda x: rates[x],network[node]))
    for evtype in received_events[node]:
        localrate += rates[evtype] * instances[evtype]
        if evtype in network[node]:
            localrate -= rates[evtype]
    return localrate

def muse_costs(proj, combi, rest, ingredient, placement): 
    """ compute costs """    
    new_placementcost = 0       
    startcost = finalcost[ingredient][placement[0]]    
    if not placement[0] in combis2[proj].keys():
        combis2[proj][placement[0]] = {}
    combis2[proj][placement[0]][combi] = {}
    if len(ingredient)>1:
        combis2[proj][placement[0]][combi][ingredient] = placement[0]
    mycost = 0 
   
    for child_proj in rest:
        mycost = np.inf 
        if len(child_proj)>1:           
           for child_placement in finalcost[child_proj]:
                 outrate = rates[child_proj] * instances[child_proj] * len(nodes[placement[0]])                  
                 if finalcost[child_proj][child_placement] != ninf: 
                                       if len(finalplacement_dict[child_proj][child_placement]) == len(nodes[child_placement]): 
                                           local_savings =  len(set((finalplacement_dict[child_proj][child_placement])).intersection(set(nodes[placement[0]]))) * (instances[child_proj]/len(finalplacement_dict[child_proj][child_placement])) * rates[child_proj]          
                                       else: 
                                           local_savings = len(set((finalplacement_dict[child_proj][child_placement])).intersection(set(nodes[placement[0]]))) * instances[child_proj] * rates[child_proj]
                                       outrate -= local_savings
                                       cur_costs = outrate + finalcost[child_proj][child_placement]
                                       mycost  = min(cur_costs, mycost)
                                       if mycost == cur_costs:
                                          combis2[proj][placement[0]][combi][child_proj] = child_placement
                                       
        else:
             mycost = finalcost[placement[0]][child_proj]    
             if mycost != 0: 
                 for node in nodes[placement[0]]:
                     if node in received_events.keys() and child_proj in received_events[node]:
                         mycost -= (rates[child_proj] * instances[child_proj]) - (network[node].count(child_proj) * rates[child_proj])
                         
        new_placementcost = mycost + new_placementcost 
    new_placementcost = new_placementcost + startcost

    return new_placementcost   

def return_placements_old(rest, placement_proj, placement):
    # return nodes for op: find best sink/s (latter for hybrid placement)

    d = 0
    placements = []
    cur_local_d = 0
    best_placement = nodes[placement][0]    
    for event in rest: 
            d += rates[event]*instances[event] 
  
    if len(placement_proj) == 1:        
        for i in nodes[placement]:           
          
            local_d = 0 
            for ingredient in rest: 
                if ingredient != placement_proj:
                    
                    if i in received_events.keys() and ingredient in received_events[i]: #len(ingredient) == 1  and                 
                                                
                            local_d += rates[ingredient] * instances[ingredient]    
                    elif len(ingredient) == 1 and ingredient in network[i]:                        
                        local_d +=rates[ingredient]                    
                    elif i in finalplacement_dict[ingredient].keys():
                        local_d +=rates[ingredient]
         
            if rates[placement_proj] > d - local_d:   
                placements.append(i)
            if i in received_events.keys() and placement_proj in received_events[i]:  
                local_d += rates[placement_proj]*instances[placement_proj]
            else:
                local_d += rates[placement_proj]
            if local_d > cur_local_d:
               best_placement = i 
               cur_local_d = local_d
        if not placements:
            return [best_placement]
        else:
            return placements
    else: 
        for i in finalplacement_dict[placement_proj][placement]:            
            local_d = rates[placement_proj]
            for ingredient in rest: 
                if len(ingredient) == 1 and (ingredient in events(i)):
                    local_d +=rates[ingredient]
                elif len(ingredient) == 1  and i in received_events.keys():
                    if ingredient in received_events[i]:
                        local_d += rates[ingredient] * instances[ingredient]            
                elif i in finalplacement_dict[ingredient].keys():
                    local_d +=rates[ingredient] 
            if rates[placement_proj] > (d - (local_d-rates[placement_proj])):    
                placements.append(i)
            if local_d > cur_local_d:
               best_placement = i 
               cur_local_d = local_d
        if not placements:
            return [best_placement]
        else:
            return placements


        
def return_placements(projection, rest, placement_proj, placement):  
    return return_placements_old(rest, placement_proj, placement)
                

def singlesink_costs(projection, combination, ingredient, placement, placementnodes):   
        
     if not placement[0] in combis2[projection].keys():
         combis2[projection][placement[0]] = {}       
     combis2[projection][placement[0]][combination] = {}        
     if len(ingredient)>1:
        combis2[projection][placement[0]][combination][ingredient] = placement[0]

     startcost = finalcost[ingredient][placement[0]]
     costs = 0
     if len(placementnodes)==1: #SINGLE SINK 
       
         for child_proj in combination:
                mycost  = 0          
                if not  child_proj in received_events[placementnodes[0]]:             
                    mycost = np.inf 
                    outrate = instances[child_proj] * rates[child_proj]
                    local_savings = 0               
                    if len(child_proj)>1: 
                       for child_placement in finalcost[child_proj]:                       
                            new_outrate = outrate                          
                            if finalcost[child_proj][child_placement] != ninf:                                
                                if placementnodes[0] in finalplacement_dict[child_proj][child_placement]: 
                                    local_savings = rates[child_proj]*instances[child_proj]/len(finalplacement_dict[child_proj][child_placement])
                                    new_outrate -= local_savings
                                if not child_proj == ingredient:
                                    new_outrate += finalcost[child_proj][child_placement]    
                                  
                                mycost = min(new_outrate, mycost)
                                if mycost == new_outrate:
                                   combis2[projection][placement[0]][combination][child_proj] = child_placement
                                   
                    else:
                        if child_proj in events(placementnodes[0]):
                            local_savings = rates[child_proj] 
                        mycost = outrate - local_savings
                   
                elif len(child_proj)>1:
                              
                        combis2[projection][placement[0]][combination][child_proj] = received_events_sender[child_proj][placementnodes[0]][0]  
                if set(combination).issubset(set(received_events[placementnodes[0]])):       
                    combis2[projection][placement[0]][combination][projection] = [placement[0]]
                costs +=mycost
        
       
     else: # HYBRID SINK
   
        completecosts = 0            
        for node in placementnodes:           
            costs = 0            
            for child_proj in combination:
                mycosts = 0                              
                if child_proj != ingredient:     
               
                    if len(child_proj) == 1 and child_proj in received_events[node]:
                        mycosts = 0
                    elif len(ingredient) > 1 and finalcost[child_proj][ingredient] == 0 and node in finalplacement_dict[child_proj][ingredient]:
                        mycosts = 0
                        combis2[projection][placement[0]][combination][projection] = [placement[0]]
                       
                    else:
                        
                         outrate = instances[child_proj] * rates[child_proj]
                         if len(child_proj)>1:
                             mycosts = np.inf
                             cur_cost = np.inf
                             for child_placement in finalcost[child_proj]:   
                               
                                 if finalcost[child_proj][child_placement] != ninf:
                                     cur_cost = finalcost[child_proj][child_placement] + outrate
                                     if node in finalplacement_dict[child_proj][child_placement]: 
                                         cur_cost -= rates[child_proj]*instances[child_proj]/len(finalplacement_dict[child_proj][child_placement])
                                     mycosts = min(cur_cost,mycosts)
                                     if mycosts == cur_cost:
                                         combis2[projection][placement[0]][combination][child_proj] = child_placement
                         else:
                             mycosts = outrate - nodes[child_proj].count(node)
                costs += mycosts 
            completecosts += costs
          
        if len(ingredient) == 1:   
            completecosts += (instances[ingredient]  - len(placementnodes)) * rates[ingredient] 
        costs = completecosts
        
     return costs+startcost
 
 
def  update_placementcosts(projection, combination, placement, new_placementcost):
      placementl = list(placement)
      placementl[1] = new_placementcost
      tempplacement = tuple(placementl)
      pind = combinationcosts[projection][combination].index(placement)
      combinationcosts[projection][combination].pop(pind)
      combinationcosts[projection][combination].append(tempplacement)
      sorted(combinationcosts[projection][combination])     
      combis[projection][placement[0]] = [combination]
      
############## Update finalcosts for multiple queries ########
      
def update_costs(res):
    changes  = []
    x = np.inf
    for i in finalcost[res].keys():      
        if finalcost[res][i] < x and finalcost[res][i] != ninf :
               bestplacement = i
               x = finalcost[res][i]
    bestplacements[res] = bestplacement
    bestplacementcosts[res] = finalcost[res][bestplacement]
    
    finalcost[res][bestplacement] = 0
    newtup = ([res],bestplacement)
    changes.append(newtup)
    rec_updatecosts(finalcombi[res][bestplacement], bestplacement,res, changes)    
    return changes       
    
bestplacementcosts  =  {}

def rec_updatecosts(combi, bestplacement, res, changes):    
    """ QWL"""
    if len(combi) == 1:
        return []
    newprojs = genproj_combi(res,combi, bestplacement)  
    for newproj in newprojs.keys():
        finalcost[newproj][bestplacement] = 0
        if not bestplacement in finalcost[newproj].keys(): 
             addplacement_option(bestplacement, newproj, res) 
                    
        finalplacement_dict[newproj][bestplacement]= finalplacement_dict[res][bestplacement] 
        finalcombi[newproj][bestplacement] = newprojs[newproj]
        
        newtup = ([newproj],bestplacement)
        changes.append(newtup)
        
        combis2[newproj][bestplacement] = {}
        combis2[newproj][bestplacement][newprojs[newproj]] = {}
        for element in newprojs[newproj]:
            if len(element)>1:
                if combi in combis2[res][bestplacement].keys():
                    combis2[newproj][bestplacement][newprojs[newproj]][element] = combis2[res][bestplacement][combi][element]
                else:
                    combis2[newproj][bestplacement][newprojs[newproj]][element] = bestplacement
            
        
    for projection in sorted(combi, key = len) :
        if len(projection) == 1 :
               if  (len(finalplacement_dict[res][bestplacement]) == 1) or (not bestplacement == projection):
                   for node in finalplacement_dict[res][bestplacement]: 
                        if not projection in received_events[node]:
                                        received_events[node].append(projection)
               if  (len(finalplacement_dict[res][bestplacement]) == len(nodes[bestplacement])) and (not bestplacement == projection):
                    finalcost[bestplacement][projection] = 0
               elif finalcost[bestplacement][projection] >  0 : 
                    finalcost[bestplacement][projection] -= rates[projection] * len(finalplacement_dict[res][bestplacement])
               
        else:   

                if (not bestplacement ==  combis2[res][bestplacement][combi][projection]) or (len(finalplacement_dict[res][bestplacement]) != len(nodes[bestplacement])):
                    for node in finalplacement_dict[res][bestplacement]: 
                                if not projection in received_events[node]:
                                        received_events[node].append(projection)
                                        received_events_sender[projection][node].append(combis2[res][bestplacement][combi][projection])                                        
                if not bestplacement in finalcost[projection].keys(): 
                   addplacement_option(bestplacement, projection, res)
                finalcost[projection][bestplacement] = 0 
                newtup = ([projection],bestplacement)
                changes.append(newtup)
                
                if bestplacement in finalplacement_dict[projection]: 
                    finalplacement_dict[projection][bestplacement] = list(set(finalplacement_dict[projection][bestplacement] + finalplacement_dict[res][bestplacement]))               
                else:
                    finalplacement_dict[projection][bestplacement] = finalplacement_dict[res][bestplacement]  
                 
                if not bestplacement == combis2[res][bestplacement][combi][projection]:  
                    finalcombi[projection][bestplacement] = tuple([projection])                  
                    if not bestplacement in combis2[projection].keys():
                        combis2[projection][bestplacement]= {}                    
                    if not [tuple([projection])] in list(combis2[projection][bestplacement].keys()):
                        combis2[projection][bestplacement][tuple([projection])] = {}
                    combis2[projection][bestplacement][tuple([projection])][tuple([projection])] = combis2[res][bestplacement][combi][projection] 
                
                
                                
                newtup = ([projection], [combis2[res][bestplacement][combi][projection]])
                changes.append(newtup)
                finalcost[projection][combis2[res][bestplacement][combi][projection]] = 0    

                rec_updatecosts(finalcombi[projection][combis2[res][bestplacement][combi][projection]], combis2[res][bestplacement][combi][projection], projection, changes)
                          

    return changes

def addplacement_option(placement, subprojection, res):    
    for projection in combinationcosts.keys():
      
        if subprojection.can_be_used(projection):
            for combi in combinationcosts[projection]:
                if subprojection in list(combi):
                    combinationcosts[projection][combi].append((placement, ninf))
                    if not placement in finalcost[projection].keys():
                       finalcost[projection][placement] =  ninf
                      
    

                            
def genproj_combi(res, combination, bestplacement):
    """ get implicit costs from sharing -> if ABC is generated with @C with [A,B,C], then also AB@C is available for costs = 0 """
    newprojs = {}   
    for i in range(2,len(combination)):
        twosets = sbs.printcombination2(list(combination), i)
        for possproj in twosets:              
            for proj in combinationcosts.keys():
                    if not proj in [res]:                         
                        if tuple(sorted(possproj, key = len)) in combinationcosts[proj].keys():
                            newcombi = tuple(sorted(list(possproj), key = len))
                            newprojs[proj] = newcombi
    return newprojs


   
finalcost = {}
placement_dict = {}
combis2 = {} 
finalcombi = {}
bestplacements = {} 
finalplacement_dict = {}    

for proj in primEvents:
    finalcost[proj] = {}
    placement_dict[proj] = {}
    finalplacement_dict[proj] = {}
    placement_dict[proj][proj] =  {}
    placement_dict[proj][proj][proj] = nodes[proj]
    finalplacement_dict[proj][proj] = nodes[proj]
    for e in primEvents:
        if e != proj:
            finalcost[proj][e] = rates[e]*len(nodes[proj])*len(nodes[e]) - len(set(nodes[proj]).intersection(set(nodes[e])))*rates[e]
        else:
            finalcost[proj][e] = 0

for projection in combinationcosts.keys():
    finalcost[projection] = {} 
    combis2[projection] ={}
    placement_dict[projection] = {}
    combis[projection] = {}
    placement_dict[projection]  = {}             
    finalcombi[projection] = {}
    finalplacement_dict[projection] = {} 
    
    for placement in list(set(map(lambda x: filter_numbers(x), projection.leafs()))):
        finalcost[projection][placement] = ninf


for res in matches:    
    for projection in sorted(projection_of_matches[res], key = lambda x: len(x.leafs())):        
     
        for combi in combinationcosts[projection]:         
            placement_dict[projection][combi]  = {}              
            if sorted(list(combi), key = len) == sorted(list(set(map(lambda x:filter_numbers(x), projection.leafs()))), key = len):
                  
               for placement in sorted(combinationcosts[projection][combi]):
                    
                    rest = list(combi) 
                    if not list(map(lambda x: filter_numbers(x), projection.leafs())).count(placement[0])>1: 
                        rest.remove(placement[0])
                    if muse_needed(rest,placement[0], placement[0], projection) and list(map(lambda x: filter_numbers(x), projection.leafs())).count(placement[0])<2:
                            
                          
                            placement_dict[projection][combi][placement[0]] = nodes[placement[0]]
                            finalplacement_dict[projection][placement[0]]  = nodes[placement[0]]
                            new_placementcost = muse_costs(projection, combi, rest, placement[0], placement)
                            placementl = list(placement)
                            placementl[1] = new_placementcost
                            tempplacement = tuple(placementl)                                   
                            pind = combinationcosts[projection][combi].index(placement)
                            combinationcosts[projection][combi].pop(pind)
                            combinationcosts[projection][combi].append(tempplacement)
                            sorted(combinationcosts[projection][combi])
                            finalcost[projection][placement[0]] = new_placementcost
                       
                    else:  
                        my_placements = return_placements(projection, rest, placement[0] , placement[0])
                        placement_dict[projection][combi][placement[0]] =  my_placements 
                        new_placementcost = singlesink_costs(projection, combi, placement[0], placement[0], my_placements)
                        finalcost[projection][placement[0]] = new_placementcost        
                        placementl = list(placement)
                        placementl[1] = new_placementcost
                        tempplacement = tuple(placementl)                                   
                        pind = combinationcosts[projection][combi].index(placement)
                        combinationcosts[projection][combi].pop(pind)
                        combinationcosts[projection][combi].append(tempplacement)
                        sorted(combinationcosts[projection][combi])
                        finalplacement_dict[projection][placement[0]] = my_placements
                    primitivecombi =  sorted(list(set(map(lambda x:filter_numbers(x), projection.leafs()))))
                    

                    finalcombi[projection][placement[0]]  = tuple(primitivecombi) 

for res in matches: 
    for projection in sorted(projection_of_matches[res], key = lambda x: len(x.leafs())):         
             for combi in combinationcosts[projection]:     
               hasmulti = False
               placement_dict[projection][combi] = {}
               for ingredient in combi:              
                  if (not hasmulti) or projection == res:  
                                          
                    rest = list(combi)
                    if len(ingredient) == 1 and not list(map(lambda x: filter_numbers(x), projection.leafs())).count(ingredient)>1: 
                        rest.remove(ingredient)
                    
                    for placement in sorted(combinationcosts[projection][combi]):
                   
                      if placement[0] in finalplacement_dict[ingredient].keys():                      
                            # CASE 1: Muse Placement                         
                         
                            if muse_needed(rest, ingredient, placement[0], projection) and not already_gathered(placement):                         
                               hasmulti= True
                               placement_dict[projection][combi][placement[0]] = nodes[placement[0]] 
                               new_placementcost = muse_costs(projection, combi, rest, ingredient, placement)

                               if  placement[1]==ninf or (placement[1]!=ninf and new_placementcost<placement[1]):                                   
                                       update_placementcosts(projection, combi, placement, new_placementcost)       
                                      
                               
                            # CASE 2: Single Sink/Hybrid Placement  
                            else:  
                                   
                                   my_placements = return_placements(projection, rest,ingredient,placement[0])  
                                   placement_dict[projection][combi][placement[0]] = my_placements 
                                   
                                   new_placementcost = singlesink_costs(projection, combi, ingredient, placement, my_placements)

                                   if  placement[1]==ninf or (placement[1]!=ninf and new_placementcost<placement[1]):
                                       update_placementcosts(projection, combi, placement, new_placementcost)
                                       
                                    
          
             for combi in combinationcosts[projection]:    
                                   
                    for place in combinationcosts[projection][combi]: 
                        if place[1] != ninf:
                          curfinalcosts = finalcost[projection][place[0]]
                          if not curfinalcosts == 0: 
                            if ((curfinalcosts== ninf ) or curfinalcosts > place[1]): 
                                finalcost[projection][place[0]] =  place[1]
                                finalcombi[projection][place[0]] = combi 
                                finalplacement_dict[projection][place[0]] = placement_dict[projection][combi][place[0]]
                       
                          
    changes = update_costs(queries[res])   
    
musecosts = 0
for res in bestplacements.keys():
    musecosts +=  bestplacementcosts[res]

transmissionratio = musecosts/centralcosts()

def get_source(res, placementnode):
    if len(placementnode) == 1:
        return placementnode
    else:
        for proj in finalcombi[res][placementnode]:
            if placementnode in list(map(lambda x: str(x), proj.leafs())):
                return str(proj)


           
totaltime = str(round(time.time() - start_time + combigen_time , 2))
 

