"""
Print MuSE graph (formatted to be input for DCEP-Ambrosia), transmission ratio and computation time.
Write result to musecosts_*.csv
"""
import pickle
import csv
import sys
from multi_muse_star import *


def format_output(res, placementnode):

    string =  "SELECT " + str(res) + " FROM " +  format_input_combi(finalcombi[res][placementnode]) + " ON " + format_input_nodes(finalplacement_dict[res][placementnode]) + "/n(" + get_source(res, placementnode) +")"
    if not res in wl:
        string += " WITH selectionRate = " + str(projrates[res][0])
    print(string)
    for element in finalcombi[res][placementnode]:
        if len(element) > 1 and not len(finalcombi[res][placementnode]) == 1: 
            format_output(element, combis2[res][placementnode][finalcombi[res][placementnode]][element])
   
    
def format_input_combi(combi):
    mystring = " "
    for i in combi:
        mystring += str(i) + ", "
    mystring = mystring[:-2]
    return mystring

def format_input_nodes(nodes):
    mystring = "{"
    for i in nodes:
        mystring += str(i) + ", "
    mystring = mystring[:-2]
    mystring += "}"
    return mystring



def main():
    
    print("MuSE Graph")
    print("-----------")    
    for i in bestplacements.keys():
        format_output(i, bestplacements[i])
    print("\n")   
    
    print("central costs " + str(centralcosts()))
    print("final costs muse: " + str(musecosts))    
    print("transmission ratio " + str(transmissionratio))
    print("total computation time: " + totaltime )   
    
    # anpassen für experimentnamen nur filename
    if len(sys.argv)>1:
        filename  = sys.argv[1]
    else: 
        filename = "none"
          
    
    with open('selectivities_params', 'rb') as selectivities_params_file:
        selectivities_params  = pickle.load(selectivities_params_file)  
    
    with open('network_params', 'rb') as network_params_file:
        network_params = pickle.load(network_params_file)  
     
    computationTime = round(time.time() - start_time,2) + combigen_time
    
    myResult = [transmissionratio, len(nw), network_params[0], network_params[1], len(wl), len(list(combinationcosts.keys()))-len(wl), selectivities_params, computationTime]
    schema = ["TransmissionRatio", "Nodes", "EventSkew", "EventNodeRatio", "WorkloadSize", "NumberProjections", "MinimalSelectivity", "ComputationTime"] 
    
    new = False
    try:
        f = open("res/aMuSE_star_"+str(filename)+".csv")
   
    except FileNotFoundError:
        new = True
        
    with open("res/aMuSE_star_"+str(filename)+".csv", "a") as result:
      writer = csv.writer(result)  
      if new:
          writer.writerow(schema)              
      writer.writerow(myResult)
        
if __name__ == "__main__":
    main()