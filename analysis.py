# Does the physics calulations
import pandas as pd
import numpy as np

# Reads the .csv
with open("data\\csv\\ee_mll175_electrons.csv") as file:
    df_175=pd.read_csv(file,index_col=0)
print(df_175)
pt_1=df_175.loc[:,"Momenta 1"]
phi_1=df_175.loc[:,"Phi 1"]
px_1=pt_1*np.cos(phi_1)
print(px_1)
