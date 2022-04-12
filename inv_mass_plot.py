# Does the physics calulations
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
hist_weights = pd.read_csv("hist_weights.csv",index_col=0)
bkgd_to_sgnl = {"175":"200","275":"375","450":"500","650":"750","900":"1000"}
i = 0
# Parsing through .csv data
for filename in os.listdir("data\\csv\\background"):
    #*** For now, I will only be testing on the example case from the assignment. 
    #*** Delete before finalization.
    if "650" not in filename:
        i+=1
        continue


    ## Reads each .csv as Pandas dataframe. 
    # Reads background and signal data.
    with open(os.path.join("data\\csv\\background",
              filename), 
              'r') as file:
        bkgd_df = pd.read_csv(file,index_col=0)

    with open(os.path.join("data\\csv\\signal", 
                            "zp_mzp"+bkgd_to_sgnl[filename[6:9]]+"_electrons.csv"),
                            'r') as file:
        sgnl_df = pd.read_csv(file,index_col=0)
    # Calculates invariant mass for bacgkround and signal.  
    bkgd_inv_mass = invariant_mass(pT1 = bkgd_df.loc[:,"Momenta 1"],
                              phi1 = bkgd_df.loc[:,"Phi 1"],
                              eta1 = bkgd_df.loc[:,"Eta 1"],
                              pT2 = bkgd_df.loc[:,"Momenta 2"],
                              phi2 = bkgd_df.loc[:,"Phi 2"],
                              eta2 = bkgd_df.loc[:,"Eta 2"])

    sgnl_inv_mass = invariant_mass(pT1 = sgnl_df.loc[:,"Momenta 1"],
                              phi1 = sgnl_df.loc[:,"Phi 1"],
                              eta1 = sgnl_df.loc[:,"Eta 1"],
                              pT2 = sgnl_df.loc[:,"Momenta 2"],
                              phi2 = sgnl_df.loc[:,"Phi 2"],
                              eta2 = sgnl_df.loc[:,"Eta 2"])


    ## Constructing both histograms.
    # Intiial Variables
    include_signal = False
    weight = 1
    delta = 50
    b=40
    # One iteration for background, another for both background+signal
    for chart in range(2):
        # Determine weight for signal+background histogram.
        if include_signal:
            weight = hist_weights.loc[i,"Background Weight"]
        # Create background histogram.
        mass = hist_weights.loc[i,"Mass"]
        bkgd_hgram = bkgd_inv_mass.plot.hist(bins = b, 
                        range = (mass-delta,mass+delta),
                        weights = weight*np.ones(len(bkgd_inv_mass.index)))
        # Save only-background histogram. Next iteration include signal.
        if not include_signal:
            plt.savefig("histograms\\"+str(mass)+"GeV_background.png")
            include_signal = True
        # Include signal to histogram, then save. 
        # ISSUE TO RAISE IN CLASS
            # Should I add the signal dataset to the background dataset when forming the combined histogram?
            # Right now, they are separate. 

            # If I do, should the weight THEN be assign the weight accordingly.
            # Or, do I somehow change the weight of each of the two individual datasets?
            # ^^^^ No, they have to be separate since singals are mere for the joint case
            # Perhaps I just have to stack both histograms on top of each other somehow? Hmmmm.
            
        else:
            print("Including signal!")
            weight = hist_weights.loc[i,"Signal Weight"]
            print("Signal Weight",weight)
            print("Signal inv_mass df", sgnl_inv_mass)
            sgnl_hgram = sgnl_inv_mass.plot.hist(bins = b, 
                        range = (mass-delta,mass+delta),
                        weights = weight*np.ones(len(sgnl_inv_mass.index)))
            plt.savefig("histograms\\"+str(mass)+"GeV_signal.png")
    plt.show()
    quit()
    i+=1