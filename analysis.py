# Does the physics calulations
import pandas as pd
import numpy as np

# Reads the .csv
with open("data\\csv\\ee_mll650_electrons.csv") as file:
    df_650=pd.read_csv(file,index_col=0)

## Inital given variables:
mass_e = .5109906 * (10**6)

pT1 = df_650.loc[:,"Momenta 1"]
phi1 = df_650.loc[:,"Phi 1"]
eta1 = df_650.loc[:,"Eta 1"]

pT2 = df_650.loc[:,"Momenta 2"]
phi2 = df_650.loc[:,"Phi 2"]
eta2 = df_650.loc[:,"Eta 2"]


## Momentum & Energy Calculations.
pvector1 = [pT1*np.cos(phi1),pT1*np.sin(phi1),pT1*np.sinh(eta1)]
energy1 = np.sqrt( (mass_e**2) + (pvector1[0]**2) + (pvector1[1]**2) + (pvector1[2]**2) )
fvector_1 = [energy1, pvector1[0], pvector1[1], pvector1[2] ]

pvector2 = [pT2*np.cos(phi2),pT2*np.sin(phi2),pT2*np.sinh(eta2)]
energy2 = np.sqrt( (mass_e**2) + (pvector2[0]**2) + (pvector2[1]**2) + (pvector2[2]**2) )
fvector_2 = [energy2, pvector2[0], pvector2[1], pvector2[2] ]

_4vector_sum = fvector_1+fvector_2
_4vector_sum_norm =np.sqrt( _4vector_sum[0]**2 + _4vector_sum[1]**2 + _4vector_sum[2]**2 + _4vector_sum[3]**2 )
inv_mass = np.sqrt( (energy1 + energy2)**2 - _4vector_sum_norm**2 )

print("")

print("inv_mass")
print(inv_mass)
for i in range(3):
    print("")

print("E_1 + E_2")
print(energy1 + energy2)
for i in range(3):
    print("")

print("_4vector_sum_norm")
print(_4vector_sum_norm)
for i in range(3):
    print("")




