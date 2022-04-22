# Calulates invariant mass
# Plots invariant mass on histograms
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
sig_df = pd.DataFrame(columns=["Mass","Statistical Significance","Zp Invariant Mass","Delta"])
hist_wght = pd.read_csv("hist_weights.csv",index_col=0)
bkgd_to_sgnl = {"175":"200","275":"300","375":"400","450":"500","650":"750","900":"1000"}
i = 0

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



    ## Initial variables for histogram construction.
    # Histogram Weights.
    wght_bkgd = hist_wght.loc[i,"Background Weight"]*np.ones(len(imass_bkgd.index))
    wght_sgnl = hist_wght.loc[i,"Signal Weight"]*np.ones(len(imass_sgnl.index))
    wght_comb = np.concatenate((wght_bkgd,wght_sgnl))
    # Graph range and bin size, chosen almost arbitrarily.
    mass = hist_wght.loc[i,"Mass"]
    range_delta = 20 + .02*mass
    bin=40
    # Boolean for both iterations.
    include_signal = False
    
    ## Constructing histograms.
    # One iteration for background, another for both background+signal.
    for chart in range(2):

        # Background+Signal histogram construction. 
        if include_signal:
            imass_comb = pd.concat([imass_bkgd,imass_sgnl])
            hist_comb = plt.hist(imass_comb,
                                 bins = bin, 
                                 range = (mass - range_delta,mass + range_delta),
                                 weights = wght_comb,
                                 label = "Signal",
                                 color = 'mediumturquoise')

        # Background-Only histogram construction.
        hist_bkgd = plt.hist(imass_bkgd,
                             bins = bin, 
                             range = (mass - range_delta,mass + range_delta),
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


    ### Statistical Significance
    ## M_Z` values are recorded as peaks of n signal values.
    # n signal variables generated.
    # imass_opt is a list of 'optimal' invariant masses.
    n_sgnl_list = hist_comb[0] - hist_bkgd[0]
    n_sgnl_avg = np.average(n_sgnl_list)
    n_sgnl_prior = 0
    imass_opt = []
    for j,n_sgnl in enumerate(n_sgnl_list):

        # If n signal decreased and the prior n signal is above average,
        # record the corresponing invariant mass.
        if (n_sgnl <= n_sgnl_prior) and (n_sgnl_prior >= n_sgnl_avg):
            imass_opt.append(hist_comb[1][j-1])

        # Assigns curreny n signal as prior n signal for the next iteration.
        n_sgnl_prior = n_sgnl


    ## Finding optimal statistical significance
    sig_vals=(0,0,0)
    # Numerical analysis by testing larger deltas. 
    for imass in  imass_opt:
        for delta in range(1,100):
            # Histogram index of {mass +- delta} window.
            window_index = (min(np.where(hist_comb[1] >= imass - .1*delta)[0]), 
                            max(np.where(hist_comb[1] <= imass + .1*delta)[0]))

            # Summing histogram n's using window indeces.
            ntot_bkgd = np.sum(hist_bkgd[0][window_index[0]: window_index[1] + 1])
            ntot_sgnl = np.sum(n_sgnl_list[window_index[0]: window_index[1] + 1])
            
            # Calculating statistical significance by
            # Keeping maximum value and recording corresponding delta.
            ss = ntot_sgnl / np.sqrt(ntot_bkgd)
            if ss > sig_vals[0]:
                sig_vals = (ss,imass,.1*delta)
    
    sig_df.loc[len(sig_df.index)] = [bkgd_to_sgnl[filename[6:9]], sig_vals[0], sig_vals[1], sig_vals[2]]

    i+=1

print("")
print(sig_df)
