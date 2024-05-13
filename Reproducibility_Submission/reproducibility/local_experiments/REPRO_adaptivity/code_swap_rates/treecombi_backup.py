def getBestTreeCombiRec(projection, mylist, mycombi, mycosts): # atm combinations are generated redundantly and also performance could be improved with a hashtable [ -> the projections with which ABC could be combined in a combination for ABCDE are a subset of the projections AB can be combined...]
    if mylist:
        for proj in sorted(mylist): # for the combination use only those projections which have a multi-sink placement
            combiBefore = [x for x in  mycombi]
            mycombi.append(proj)
            mycosts += combiDict[proj][2]  
            
            #exclude redundant combinations
            mycombiEvents = ''.join(map(lambda x: ''.join(x.leafs()), mycombi))
            subProjections = [x for x in mylist if not set(x.leafs()).issubset(set(list(mycombiEvents))) and not set(list(mycombiEvents)).issubset(set(x.leafs()))]
            
            #exclude the projections of the list in which the partitioning input type of proj is element of the leafs
            partProj = combiDict[proj][1][0]
            subProjections = [x for x in subProjections if not partProj in x.leafs()]
            
            # exclude case in which part proj of other projection in the list is part of projs leafs
            subProjections = [x for x in subProjections if not (x in combiDict.keys() and combiDict[x][1][0] in proj.leafs())]
            
            # exclude subprojections in which the events covered by multi-sink placement are a subset of those events covered by the projections in the combination so far
            allAncestors = []
            allSiSEvents= []
            for ingredient in mycombi:
                allAncestors += [ingredient] + sharedAncestors(ingredient, combiDict[ingredient][0])
                allSiSEvents += getSiSevents(ingredient)
            allMSAncestors = list(set([x for x in allAncestors if combiDict[x][1]]))
            allPartProjs = list(set([combiDict[x][1][0] for x in allMSAncestors]))
            subProjections  = [x for x in subProjections if not set(AncestorPartProjs(x)).issubset(set(allPartProjs))]                    
            
            # exclude the projection in which one of the partProjs of the combination so far is used as input of a single sink placement of an ancestor
            allSiSEvents = list(set(allSiSEvents))  
            subProjections = [x for x in subProjections if not set(allPartProjs).intersection(set(getSiSevents(x))) and not list(set(AncestorPartProjs(x)).intersection(set(allSiSEvents)))]

            
            getBestTreeCombiRec(projection, subProjections, mycombi, mycosts)
            mycombi =  combiBefore
            mycosts -= combiDict[proj][2]
    else:            
       if not mycombi:  #not even one ms placeable subprojection exists
           return 
       
