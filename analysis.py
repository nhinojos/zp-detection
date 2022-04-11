# Does the physics calulations
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Reads the .csv for the example 750V case from document
with open("data\\csv\\ee_mll650_electrons.csv") as file:
    df_650=pd.read_csv(file,index_col=0)

## Inital given variables:
    # Mass electron in GeV
mass_e = .510998950 * (10**-3)

pT1 = df_650.loc[:,"Momenta 1"]
phi1 = df_650.loc[:,"Phi 1"]
eta1 = df_650.loc[:,"Eta 1"]

pT2 = df_650.loc[:,"Momenta 2"]
phi2 = df_650.loc[:,"Phi 2"]
eta2 = df_650.loc[:,"Eta 2"]


## Momentum, Energy, and Four-Vector Calculations.
# Momentum.
p1 = [ pT1*np.cos(phi1), pT1*np.sin(phi1), pT1*np.sinh(eta1) ]
p2 = [ pT2*np.cos(phi2), pT2*np.sin(phi2), pT2*np.sinh(eta2) ]
psum = p1 + p2
pdot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]

# Energy.
E1 = np.sqrt( (mass_e**2) + (p1[0]**2) + (p1[1]**2) + (p1[2]**2) )
E2 = np.sqrt( (mass_e**2) + (p2[0]**2) + (p2[1]**2) + (p2[2]**2) )
Esum = E1 + E2

# Four-Vector.
fv1 = [E1,p1[0],p1[1],p1[2]]
fv2 = [E2,p2[0],p2[1],p2[2]]
fvsum = fv1 + fv2


## Invariant Mass Calulation.

inv_mass = np.sqrt( 2*(mass_e**2 + E1*E2 - pdot) )




print(inv_mass)

display_historgram = True
if display_historgram:
    signal = 1
    rng=(710,830)
    df = signal * inv_mass
    ax = df.plot.hist(bins=39, range=rng)
    plt.show()


