### Converts the .txt data to .csv. 
## Importing libraries.
import pandas as pd
import os

# Opening objects from txt folder to read line-by-line.
for filename in os.listdir('data\\txt'):
    file_txt=open(os.path.join("data\\txt",filename),'r')
    df=pd.DataFrame(columns=["Momenta 1","Momenta 2","Eta 1","Eta 2","Phi 1","Phi 2"])



    ## Extracts data in .txt file line-by-line.
    investigate_collision=0
    for n,line in enumerate(file_txt):
        if n%10000==0:
            print("Line: ",n)
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
                df.loc[len(df.index)]=[momenta[0],momenta[1],eta[0],eta[1],phi[0],phi[1]]
    
    ## Writes the panda dataframe as a .csv file to the csv folder within the data folder. 
    # Specifies which folder based on the name of the file. 
    if "ee" in filename:
        folder="background"
    else:
        folder="signal"
    df.to_csv("data\\csv\\"+folder+"\\"+filename[:-3]+"csv")