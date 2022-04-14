# Does the physics calulations
from cProfile import label
from operator import index
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


## Calculates invariant mass for two electron collision
def invariant_mass(pT1,phi1,eta1,pT2,phi2,eta2):
    
    # Electron mass in GeV
    mass_e = .510998950 * (10**-3)
    
    # Momentum Vectors.
    p1 = [ pT1*np.cos(phi1), pT1*np.sin(phi1), pT1*np.sinh(eta1) ]
    p2 = [ pT2*np.cos(phi2), pT2*np.sin(phi2), pT2*np.sinh(eta2) ]
    pdot = p1[0]*p2[0] + p1[1]*p2[1] + p1[2]*p2[2]
    
    # Energies.
    E1 = np.sqrt( (mass_e**2) + (p1[0]**2) + (p1[1]**2) + (p1[2]**2) )
    E2 = np.sqrt( (mass_e**2) + (p2[0]**2) + (p2[1]**2) + (p2[2]**2) )
    
    # Invariant Mass Calulation.
    return np.sqrt( 2*(mass_e**2 + E1*E2 - pdot) )


## Calculating and plotting histograms.
# Initial variables.
hist_wght = pd.read_csv("hist_weights.csv",index_col=0)
bkgd_to_sgnl = {"175":"200","275":"300","375":"400","450":"500","650":"750","900":"1000"}
i = 0

## Parsing through .csv data
for filename in os.listdir("data\\csv\\background"):

    ## Reads each .csv as Pandas dataframe. 
    # Reads background and signal data.
    with open(os.path.join("data\\csv\\background",
              filename), 
              'r') as file:
        data_bkgd = pd.read_csv(file,index_col=0)
    with open(os.path.join("data\\csv\\signal", 
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

    ## Initial variables for histogram construction.
    # Histogram Weights.
    wght_bkgd = hist_wght.loc[i,"Background Weight"]*np.ones(len(imass_bkgd.index))
    wght_sgnl = hist_wght.loc[i,"Signal Weight"]*np.ones(len(imass_sgnl.index))
    wght_comb = np.concatenate((wght_bkgd,wght_sgnl))

    # Graph range and bin size
    mass = hist_wght.loc[i,"Mass"]
    delta = 20+.03*mass
    b=40
    # Boolean for both iterations.
    include_signal = False
    
    ## Constructing histograms.
    # One iteration for background, another for both background+signal.
    for chart in range(2):

        # Background+Signal histogram construction. 
        if include_signal:
            imass_comb = pd.concat([imass_bkgd,imass_sgnl])
            hist_sgnl = plt.hist(imass_comb,
                                 bins = b, 
                                 range = (mass-delta,mass+delta),
                                 weights = wght_comb,
                                 label = "Signal",
                                 color = 'mediumturquoise')

        # Background-Only histogram construction.
        
        bkgd_hist = imass_bkgd.plot.hist(bins = b, 
                                        range = (mass-delta,mass+delta),
                                        weights = wght_bkgd,
                                        label= "Bkgd",
                                        color= "darkslategray")
        
        # Labels for both histograms
        plt.ylabel("Entities / bin")
        plt.xlabel("Mass [GeV]")

        # Label and save background-only histogram.
        if not include_signal:
            plt.title(str(mass)+"GeV Background")
            plt.savefig("histograms\\"+str(mass)+"GeV_background.png")
            include_signal = True


        # Label and save background+signal histogram.
        else:
            plt.title(str(mass)+"GeV Background+Signal")
            plt.legend()
            plt.savefig("histograms\\"+str(mass)+"GeV_signal-background.png")
        plt.clf()
    i+=1