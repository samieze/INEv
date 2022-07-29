"""
Initialize selectivities for given tuple of primitive event types (projlist) within interval [x,y].
"""
import random as rd
import numpy as np
import sys
from generate_qwls import *



""" Experiment Selectivities:   
    

selectivities Google Cluster Data: [selectivity for each tuple of primitive event types x,y such that x.job_ID == y.job_ID]
selectivities = {'HF':0.05, 'FH':0.05,'IF':0.05,'FI':0.05,'IE':0.05,'EI':0.05,'HC':0.05, 'CH':0.05,'HD':0.05, 'DH':0.05,'IB':0.05,'BI':0.05,'HI':0.05, 'IH':0.05, 'IC':0.05,'CI':0.05,'DI':0.05,'ID':0.05,  'IB':0.05,'BF': 0.05, 'FB': 0.05,'AB': 0.05,'AF': 0.05,'FA': 0.05,'BA':0.05,'AC':0.05,'CA':0.05, 'BC':0.05, 'CB':0.05,'BG':0.05, 'GB':0.05, 'AD': 0.05, 'DA':0.05, 'CD':0.05, 'DC':0.05, 'BD':0.05, 'DB': 0.05,  'AE':0.05, 'EA':0.05, 'CF':0.05, 'FC':0.05, 'CG': 0.05,  'GC':0.05, 'GF':0.05, 'FG':0.05,  'DF':0.05, 'DG':0.05 }
#selectivities = {'EF': 0.05, 'FE': 0.05,'HB':0.05, 'BH':0.05, 'HF':0.05, 'FH':0.05,'IF':0.05,'FI':0.05,'IE':0.05,'EI':0.05,'HC':0.05, 'CH':0.05,'HD':0.05, 'DH':0.05,'IB':0.05,'BI':0.05,'HI':0.05, 'IH':0.05, 'IC':0.05,'CI':0.05,'DI':0.05,'ID':0.05,  'IB':0.05,'BF': 0.05, 'FB': 0.05,'AB': 0.05,'AF': 0.05,'FA': 0.05,'BA':0.05,'AC':0.05,'CA':0.05, 'BC':0.05, 'CB':0.05,'BG':0.05, 'GB':0.05, 'AD': 0.05, 'DA':0.05, 'CD':0.05, 'DC':0.05, 'BD':0.05, 'DB': 0.05,  'AE':0.05, 'EA':0.05, 'CF':0.05, 'FC':0.05, 'CG': 0.05,  'GC':0.05, 'GF':0.05, 'FG':0.05,  'DF':0.05, 'DG':0.05 }

"""
with open('network',  'rb') as  nw_file:
        nw = pickle.load(nw_file)
    
PrimitiveEvents = list(string.ascii_uppercase[:len(nw[0])])

def initialize_selectivities(primEvents,x,y): 

   
    projlist = generate_twosets(primEvents)       
    projlist = list(set(projlist))
    selectivities = {}
    selectivity = 0
    for i in projlist: 
        #if len(filter_numbers(i)) >1 :                  
            selectivity = rd.uniform(0.0,0.3)             
            if selectivity > 0.2:
                selectivity = 1
                selectivities[str(i)] =  selectivity
                selectivities[str(changeorder(i))] =  selectivity
            if selectivity < 0.2: 
                selectivity = rd.uniform(x,y)                
                selectivities[str(i)] =  selectivity
                selectivities[str(changeorder(i))] =  selectivity
    return selectivities


def main():
  """default selectivity interval"""
  x = 0.0001
  y = 0.00001
  

  primEvents = PrimitiveEvents
  
  if len(sys.argv) > 1: 
      x = float(sys.argv[1])
      
  if len(sys.argv) >2 :
      x = float(sys.argv[1])
      y = float(sys.argv[2])
 
  selectivities = initialize_selectivities(primEvents,x,y)
  
  print(len(selectivities.keys()))
  print("SELECTIVITIES")
  print("--------------")
  
  
  print(selectivities)
  
  
  
  
  #export minimal selectivity, average/median selectivity
  selectivitiesExperimentData = [x, np.median(list(selectivities.values()))]
  with open('selectivitiesExperimentData', 'wb') as selectivitiesExperimentDataFile:
      pickle.dump(selectivitiesExperimentData, selectivitiesExperimentDataFile)

  with open('selectivities', 'wb') as selectivity_file:
    pickle.dump(selectivities,  selectivity_file)   
    
 
  
if __name__ == "__main__":
    main()



    
