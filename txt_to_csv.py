### Converts the .txt data to .csv. 
## Importing libraries.
import pandas as pd
import os

for filename in os.listdir('data\\txt'):
    file_txt=open(os.path.join("data\\txt",filename),'r')
    df=pd.DataFrame(columns=['Momenta','Eta','Phi'])

    ## Extracts data in .txt file line-by-line.
    investigate_collision=0
    for line in file_txt:
        # Scans for instances where the number of electrons is two.
        if "NumElectrons: 2" in line:    
            # Initial variables for data extraction. 
            investigate_collision=2
            momenta=[]
            eta=[]
            phi=[]
            charge=0
        
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
            
            # Investigates collision twice. 
            investigate_collision-=1

            #Appends extrated data to dataframe. 
            if investigate_collision==0:
                df.loc[len(df.index)]=[momenta,eta,phi]
    
    # Writes the panda dataframe as a .csv file to the csv folder within the data folder. 
    df.to_csv("data\\csv\\"+filename[:-4]+".csv")