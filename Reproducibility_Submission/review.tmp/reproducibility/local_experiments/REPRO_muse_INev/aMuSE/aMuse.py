"""
Print MuSE graph (formatted to be input for DCEP-Ambrosia), transmission ratio and computation time.
Write result to musecosts_*.csv
"""
import pickle
import csv
import sys
from multi_muse import *

final_dict = {}


def format_output(res, placementnode):
    interdict = {res : (finalcombi[res][placementnode], finalplacement_dict[res][placementnode], get_source(res, placementnode))}
    string =  "SELECT " + str(res) + " FROM " +  format_input_combi(finalcombi[res][placementnode]) + " ON " + format_input_nodes(finalplacement_dict[res][placementnode]) + "/n(" + get_source(res, placementnode) +")"
    if not res in wl:
        string += " WITH selectionRate = " + str(projrates[res][0])
    print(string)
    for element in finalcombi[res][placementnode]:        
        if len(element) > 1 and not len(finalcombi[res][placementnode]) == 1: 
            interdict.update(format_output(element, combis2[res][placementnode][finalcombi[res][placementnode]][element]))
            
    return interdict
        
    
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
        final_dict.update(format_output(i, bestplacements[i]))
    print("\n")   
    
    print("central costs " + str(centralcosts()))
    print("final costs muse: " + str(musecosts))    
    print("transmission ratio " + str(transmissionratio))
    print("total computation time: " + totaltime )   
    
    if len(sys.argv)>1:
        experiment_id = sys.argv[1]
    else:
        experiment_id = 1
    if len(sys.argv)>2:
        filename = sys.argv[2]
    else:
        filename = "none"
    
    with open('musegraph', 'wb') as muse_file:
        pickle.dump(final_dict, muse_file)    
    with open("aMuSE_"+str(filename)+".csv", "a") as result:
      writer = csv.writer(result)
      writer.writerow([experiment_id, transmissionratio, len(list(combinationcosts.keys()))-len(wl), round(time.time() - start_time,2) + combigen_time])

        
if __name__ == "__main__":
    main()