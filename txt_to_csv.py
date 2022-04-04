### Converts the .txt data to .csv. 
## Importing libraries.
import numpy as np
import pandas as pd
from pathlib import Path


## Generating data variables.
    # _txt is the original .txt file
    # _df is a panda dataframe
with Path(r"C:\Users\noaha\Documents\GitHub\Searching-For-Z'-Boson-P121W-Lab\data\.txt\ee_mll175_electrons.txt") as path:
    b175_txt=open(path,'r')
b175_df=pd.DataFrame(columns=['Momenta','Eta','Phi'])


## Extracts data in .txt file line-by-line.
investigate_collision=0
l=0
for line in b175_txt:
    print('Line:',l)
    l+=1
    # Scans for instances where the number of electrons is two.
    if "NumElectrons: 2" in line:    
        # Initial variables for data extraction. 
        investigate_collision=2
        momenta=[]
        eta=[]
        phi=[]
        charge=0
        continue
    
    # Will extract collision data for two iterations.
    elif investigate_collision>0:
        # Noting charges
        if line[7+line.find("Charge ")]=='1':
            charge+=1
        else:
            charge-=1
        if investigate_collision==1 and charge!=0:
            investigate_collision=0
            continue

        # Extracting Momenta.
        index_l=14
        index_r=line.find(" Eta")
        momenta.append(float(line[index_l:index_r]))

        # Extracting Eta.
        index_l=5+index_r
        index_r=line.find(" Phi")
        eta.append(float(line[index_l:index_r]))

        # Extracting Phi.
        index_l=5+index_r
        index_r=line.find(" Charge")
        phi.append(float(line[index_l:index_r]))
        
        investigate_collision-=1
        if investigate_collision==0:
            print('momenta:',momenta)
            print('eta',eta)
            print('phi',phi)
            b175_df.loc[len(b175_df.index)]=[momenta,eta,phi]

with Path(r"C:\Users\noaha\Documents\GitHub\Searching-For-Z'-Boson-P121W-Lab\data\.csv\ee_mll175_electrons.csv") as path:
    b175_df.to_csv(path)