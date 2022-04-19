# Determines the statistical significance within each invariant mass window
# WORK IN PROGRESS: Only done for 200GeV Case. 
import os
import math
import pandas as pd

def statistical_significance(df_bkgd,df_sgnl,m):
    stat_sgnf = 0
    md_range = [0,0]
    for m0 in range(-40,41):
        mass = m + (.5*m0)
        for d in range(1,100):
            # Determines number of entities within mass and delta range
            n_bkgd = df_bkgd[(df_bkgd["Invariant Mass"] >= mass - .1*d)
                            & (df_bkgd["Invariant Mass"] <= mass + .1*d)].size

            n_sgnl = df_sgnl[(df_sgnl["Invariant Mass"] >= mass - .1*d)
                            & (df_sgnl["Invariant Mass"] <= mass + .1*d)].size
            
                
            # Determines statistical significance. 
            # Records signficiance if greater than prior significance range
            s = n_sgnl / math.sqrt(n_bkgd)
            if s > stat_sgnf:
                stat_sgnf = s
                md_range[0] = mass
                md_range[1] = .1*d
    
    return stat_sgnf,md_range[0],md_range[1]

print("Opening files!")
## Testing Statistical Significance calulator on 200GeV data. 
# Opening invariant mass datagframes
with open(os.path.join("inv mass data\\background",
                       "175_inv_mass.csv"),
          'r') as file:
    im_bkgd = pd.read_csv(file,index_col=0)

with open(os.path.join("inv mass data\\signal",
          "200_inv_mass.csv"),
         'r') as file:
    im_signal = pd.read_csv(file,index_col=0)

print("Calculating Significance!")
## Calculating optime statistical significance
x=statistical_significance(im_bkgd,im_signal,200)
print("")
print("Optimal Significance:",str(x[0])+"%")
print("At mass range ("+ str(x[1] - x[2]) +  "," + str(x[1] + x[2]) + ")")
print("")
