# Calculates invariant mass and saves to csv.
from email import header
import os
import pandas as pd
from plot_hist import invariant_mass

# Initial variables
bkgd_to_sgnl = {"175":"200","275":"300","375":"400","450":"500","650":"750","900":"1000"}

## Parsing through .csv data
for filename in os.listdir("collision data\\csv\\background"):

    ## Reads each .csv as Pandas dataframe. 
    # Reads background and signal data.
    with open(os.path.join("collision data\\csv\\background",
                           filename),
              'r') as file:
        data_bkgd = pd.read_csv(file,index_col=0)

    with open(os.path.join("collision data\\csv\\signal", 
                            "zp_mzp"+bkgd_to_sgnl[filename[6:9]]+"_electrons.csv"),
              'r') as file:
        data_sgnl = pd.read_csv(file,index_col=0)
   
    # Calculates invariant mass for bacgkround and signal.  
    imass_bkgd = invariant_mass(pT1 = data_bkgd.loc[:,"Momenta 1"],
                              phi1 = data_bkgd.loc[:,"Phi 1"],
                              eta1 = data_bkgd.loc[:,"Eta 1"],
                              pT2 = data_bkgd.loc[:,"Momenta 2"],
                              phi2 = data_bkgd.loc[:,"Phi 2"],
                              eta2 = data_bkgd.loc[:,"Eta 2"])
    
    imass_sgnl = invariant_mass(pT1 = data_sgnl.loc[:,"Momenta 1"],
                              phi1 = data_sgnl.loc[:,"Phi 1"],
                              eta1 = data_sgnl.loc[:,"Eta 1"],
                              pT2 = data_sgnl.loc[:,"Momenta 2"],
                              phi2 = data_sgnl.loc[:,"Phi 2"],
                              eta2 = data_sgnl.loc[:,"Eta 2"])

    imass_bkgd.to_csv("inv mass data\\background\\"+filename[6:9]+"_inv_mass.csv", header=["Invariant Mass"])
    imass_sgnl.to_csv("inv mass data\\signal\\"+bkgd_to_sgnl[filename[6:9]]+"_inv_mass.csv", header=["Invariant Mass"])