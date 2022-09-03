#!/usr/bin/python3
###############################################################
#
#   This is a builder script for the simulation done in the
#     TFM done in the UB, Spain. Only 3 argument should be 
#     given to this script: 
#           -> Temperature of the simulation.
#           -> Partial pressure of CO2
#           -> Partial pressure of H2
#   Following the argument passed strategy is ease to adapt
#     to accept more argument (method sys.argv[]). On the 
#     other hand, the defaults values included here can be 
#     used to obtain a simulation of the RWGS reaction on 
#     (0001) Mo2C MXene, in a simplified lattice model.
#   Its imporatn to add the energies in the formation_E.ods
#     file, as in the frequecies.ods file; remeber that you
#     should use the same name (Case and space sensitive) as
#     in this script.
#     For last, this script was build with Pyzacros 1.0.0 down-
#        loaded from the github repository on the 03/06/2022, some
#        modification where done in the library to be cappable of
#        add the cis trans species. Those modification will be des-
#        cribed on my github repository.
#
#     Tamaragua                                     Anon 
##############################################################
#
#
#
#
#
#
#
#
#
##############################################################
import numpy as np
import scm.plams
import pyzacros as pz
import pandas as pd
import os 
import sys

# Complementary libraries.
import prefactor as pf
import dataframe as inf

    # Colors for output in terminal
class colors():
    Black= "\u001b[30;1m"
    Red= "\u001b[31;1m"
    Green= "\u001b[32;1m"
    Yellow= "\u001b[33;1m"
    Blue= "\u001b[34;1m"
    Magenta= "\u001b[35;1m"
    Cyan= "\u001b[36;1m"
    White= "\u001b[37;1m"
    END="\u001b[0m"


# Obtaining actual directory
dir_path = os.path.dirname(os.path.realpath(__file__))

print("#######################################################")
print(colors.Yellow+"         Starting simulation building.             "+ colors.END)
print("         Files will be saved on :  "+colors.Red+dir_path+colors.END )
print("#######################################################")

########################################################################
#############       Thermodynamic values        ########################
########################################################################

# Temperature
Temp = float(sys.argv[1])      # K
# Pressures
Pressure = 1.0    # bar
P_CO2 = float(sys.argv[2])
P_H2 = float(sys.argv[3])
P_CO = 0.0
P_H2O = 0.0

# Cell vectors
v1 = np.array([3.097132,0.0000]) # A
v2 = np.array([-1.548566,2.682195]) # A
# Area = 8,3055 A²

########################################################################
#############       Simulation Parameters       ########################
########################################################################
# number of sites per unit cell
num_sites=1
# repeat
repeat_factor = 12

# Momentos de inercia gases Ia*Ib*Ic en A²
# https://cccbdb.nist.gov/exp2x.asp?casno=124389&charge=0

I_CO2= 43.20143
I_CO= 8.768466
I_H2 = 0.2770222
I_H2O = 1.275365

# symmetry number
#https://webbook.nist.gov/cgi/cbook.cgi?ID=C14940637&Mask=800
Sym_CO2= 2
Sym_CO = 1
Sym_H2 = 2
Sym_H2O= 2

# ESCALADO 
CO2_ads_escal = 1.0
CO_ads_escal = 1.0
H2_ads_escal = 1.0
H2O_ads_escal = 1.0
CO2_COyO_escal = 1.0
CO2yH_HCOO_escal = 1.0
CO2yH_tCOOH_escal = 1.0
tCOOH_cCOOH_escal = 1.0 # Conformational necesita reescalado
cCOOH_COHyO_escal = 1.0
COyH_COH_escal = 1.0
HCOO_HCOyO_escal = 1.0
OyH_OH_escal = 1.0
OHyH_H2O_escal = 1.0
HCO_HyCO_escal = 1.0
OHyOH_H2OyO_escal = 1.0
H2_HyH_escal = 1.0
cCOOH_COyOH_escal = 1.0
H_diff_escal = 1.0
O_diff_escal = 1.0
CO_diff_escal = 1.0
OH_diff_escal = 1.0


########################################################################
#############           Reading ods             ########################
########################################################################

Freq_Frame = pd.read_excel((dir_path+"/frequencies.ods"))
Ef_Frame = pd.read_excel((dir_path+"/formation_E.ods"))
#print(Ef_Frame)


########################################################################
#                         /|\
#                        //|\\
#                       ///|\\\
#                      /|//|\\|\
#                     ///|||||\\\
#                    ///|/|||\|\\\
#                   ///|//|||\\|\\\
#                  ///|///|||\\\|\\\
#                  #################
#                  ##### ZACROS ####
#                  #################
#                  \\\|\\\|||///|///
#                   \\|\\\|||///|//
#                    \|\\\|||///|/
#                     |\\\|||///|
#                      \\|\|/|//
#                       \\\|///
#                        \\|//
#                         \|/
########################################################################
#############        Species declaration        ########################
########################################################################
# 1. Gas species

# 1.1 Reactives
#     Define  the gas reactive species
H2_g = pz.Species("H2")
CO2_g = pz.Species("CO2")

# 1.2 Products
#   Define the gas product specie
H2O_g = pz.Species("H2O")
CO_g = pz.Species("CO",gas_energy=float(inf.dimelo("CO_g","FE",Ef_Frame).out))


#  2. SURFACE SPECIES
#    2.1   Empty space
s0 = pz.Species("*",1)


#    2.2   Adsorbed species
cCOOH_s = pz.Species("cisCOOH*",1)
tCOOH_s = pz.Species("traCOOH*",1)
CO2_s  = pz.Species("CO2*",1)
COH_s = pz.Species("COH*",1)
H_s = pz.Species("H*",1)
H2_s  = pz.Species("H2*",1)
H2O_s  = pz.Species("H2O*",1)
HCO_s = pz.Species("HCO*",1)
HCOO_s = pz.Species("HCOO*",1) # Imporant, taken always one of the hol1s
O_s = pz.Species("O*",1)
CO_s = pz.Species("CO*",1)
OH_s = pz.Species("OH*",1)
my_list = pz.SpeciesList([CO2_g, CO_g, H2_g, H2O_g])


########################################################################
#############        Simulation conditions      ########################
########################################################################
sett = pz.Settings()
sett.random_seed = 953111
sett.temperature = Temp
sett.pressure = Pressure
sett.snapshots = ('event', 10000000)
sett.process_statistics = ('event', 1000000)
sett.species_numbers = ('event', 1000000)
sett.event_report = 'off'
sett.max_steps = 100000000
sett.max_time = "infinity"

sett.molar_fraction.CO2 = P_CO2
sett.molar_fraction.H2 = P_H2 
sett.molar_fraction.CO = P_CO 
sett.molar_fraction.H2O = P_H2O

########################################################################
#############    Lattice and sites definitions  ########################
########################################################################

lattice = pz.Lattice(cell_vectors=[v1, v2],   #[3.097132,0.0000],[-1.548566,2.682195]],
                      repeat_cell=[repeat_factor,repeat_factor],
                      site_types=["MoTop"],
                      site_coordinates=[[0.5, 0.5]],
                   neighboring_structure=[ [(0,0), pz.Lattice.NORTH],
                                           [(0,0), pz.Lattice.EAST],
                                           [(0,0), pz.Lattice.NORTHEAST]]
                    )

Area_site = np.cross(v1,v2)/num_sites


                                               ####@@...@@####
                                               ####@@...@@####
###############################################               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################    Clusters   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                                               ####@@...@@####
                                               ####@@...@@####      

# Definitions for cluster, its needed to use the "inf.dimelo" function
#    which obtains the formation energy. for more information about this functions
#    go to the pyzacros manual.  After building each cluster object it shoul de added
#    to a python list; i this script the name of this list is the cluster_list.



cluster_list = []
#\\\\\\\\\\\\\\\ cCOOH*
cCOOH_top = pz.Cluster( species=[cCOOH_s],
                     cluster_energy= (inf.dimelo("cCOOH*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="cCOOH*")
cluster_list.append(cCOOH_top)
#\\\\\\\\\\\\\\\ tCOOH*
tCOOH_top = pz.Cluster( species=[tCOOH_s],
                     cluster_energy= (inf.dimelo("tCOOH*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="tCOOH*")
cluster_list.append(tCOOH_top)
#\\\\\\\\\\\\\\\ CO2*
CO2_top = pz.Cluster( species=[CO2_s],
                     cluster_energy= (inf.dimelo("CO2*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="CO2*")
cluster_list.append(CO2_top)
#\\\\\\\\\\\\\\\ COH*
COH_top = pz.Cluster( species=[COH_s],
                     cluster_energy= (inf.dimelo("COH*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="COH*")
cluster_list.append(COH_top)
#\\\\\\\\\\\\\\\ H*
H_top = pz.Cluster( species=[H_s],
                     cluster_energy= (inf.dimelo("H*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="H*")
cluster_list.append(H_top)
#\\\\\\\\\\\\\\\ H2*
H2_top = pz.Cluster( species=[H2_s],
                     cluster_energy= (inf.dimelo("H2*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="H2*")
cluster_list.append(H2_top)
#\\\\\\\\\\\\\\\ H2O*
H2O_top = pz.Cluster( species=[H2O_s],
                     cluster_energy= (inf.dimelo("H2O*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="H2O*")
cluster_list.append(H2O_top)
#\\\\\\\\\\\\\\\ HCO*
HCO_top = pz.Cluster( species=[HCO_s],
                     cluster_energy= (inf.dimelo("HCO*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="HCO*")
cluster_list.append(HCO_top)
#\\\\\\\\\\\\\\\ HCOO*
HCOO_top = pz.Cluster( species=[HCOO_s],
                     cluster_energy= (inf.dimelo("HCOO*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="HCOO*")
cluster_list.append(HCOO_top)
#\\\\\\\\\\\\\\\ O*
O_top = pz.Cluster( species=[O_s],
                     cluster_energy= (inf.dimelo("O*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="O*")
cluster_list.append(O_top)
#\\\\\\\\\\\\\\\ CO*
CO_top = pz.Cluster( species=[CO_s],
                     cluster_energy= (inf.dimelo("CO*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="CO*")
cluster_list.append(CO_top)
#\\\\\\\\\\\\\\\ OH*
OH_top = pz.Cluster( species=[OH_s],
                     cluster_energy= (inf.dimelo("OH*","FE",Ef_Frame).out),
                     site_types=["MoTop"],
                     label="OH*")
#\\\\\\\\\\\\\\\ empy hC*
none_pointhMo = pz.Cluster( species=[pz.Species.UNSPECIFIED],
                          cluster_energy=0.0,
                          site_types=["MoTop"],
                          label="None-hMo")
cluster_list.append(none_pointhMo)





                                               ####@@...@@####
                                               ####@@...@@####
###############################################               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
############################################### Interacciones @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################   Laterales   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                                               ####@@...@@####
                                               ####@@...@@####      

# Lateral interactions shoul now be defined, remember that this definitions should be in accord with the lattice
#    definition. Also, it's used the "info.dimelo" function, the information about this function is on the dataframe.py
#    file in this same directory.
# Is recommended to use as name of each interacion object the species that are defined in this interaction, therefore,
#       later will be more easy to check all the information.

O_H = pz.Cluster(species=[O_s,H_s],
                     cluster_energy= (inf.dimelo("O+H","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     entity_number=[0,1],
                     neighboring=[(0,1)],
                     label="O_H")
cluster_list.append(O_H)

CO2_H = pz.Cluster(species=[CO2_s,H_s],
                     cluster_energy= (inf.dimelo("CO2+H","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="CO2_H")
cluster_list.append(CO2_H)

CO_H= pz.Cluster(species=[CO_s,H_s],
                     cluster_energy= (inf.dimelo("CO+H","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="CO_H")
cluster_list.append(CO_H)

COH_O= pz.Cluster(species=[COH_s,O_s],
                     cluster_energy= (inf.dimelo("COH+O","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="COH_O")
cluster_list.append(COH_O)

CO_O= pz.Cluster(species=[CO_s,O_s],
                     cluster_energy= (inf.dimelo("CO+O","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="CO_O")
cluster_list.append(CO_O)

CO_OH = pz.Cluster(species=[CO_s,OH_s],
                     cluster_energy= (inf.dimelo("CO+OH","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="CO+OH")
cluster_list.append(CO_OH)

H2O_O= pz.Cluster(species=[H2O_s,O_s],
                     cluster_energy= (inf.dimelo("H2O+O","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="H2O+O")
cluster_list.append(H2O_O)

HCO_O= pz.Cluster(species=[HCO_s,O_s],
                     cluster_energy= (inf.dimelo("HCO+O","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="HCO+O")
cluster_list.append(HCO_O)

HCOO_H= pz.Cluster(species=[HCOO_s,H_s],
                     cluster_energy= (inf.dimelo("HCOO+H","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="HCOO+H")
cluster_list.append(HCOO_H)

O_H= pz.Cluster(species=[O_s,H_s],
                     cluster_energy= (inf.dimelo("O+H","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="O+H")
cluster_list.append(O_H)

OH_H = pz.Cluster(species=[OH_s,H_s],
                     cluster_energy= (inf.dimelo("OH+H","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="OH+H")
cluster_list.append(OH_H)

OH_OH= pz.Cluster(species=[OH_s,OH_s],
                     cluster_energy= (inf.dimelo("OH+OH","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="OH+OH")
cluster_list.append(OH_OH)

H_H= pz.Cluster(species=[H_s,H_s],
                     cluster_energy= (inf.dimelo("H+H","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="H+H")
cluster_list.append(H_H)


CO_CO = pz.Cluster(species=[CO_s,CO_s],
                     cluster_energy= (inf.dimelo("CO+CO","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="CO_CO")
cluster_list.append(CO_CO)

CO2_CO2 = pz.Cluster(species=[CO2_s,CO2_s],
                     cluster_energy= (inf.dimelo("CO2+CO2","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="CO2_CO2")
cluster_list.append(CO2_CO2)

O_O = pz.Cluster(species=[O_s,O_s],
                     cluster_energy= (inf.dimelo("O+O","FE",Ef_Frame).out),
                     site_types=["MoTop","MoTop"],
                     neighboring=[(0,1)],
                     label="O_O")
cluster_list.append(O_O)

cluster_list = pz.ClusterExpansion(cluster_list)





                                               ####@@...@@####
                                               ####@@...@@####
###############################################               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################   Mechanism   @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################               @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                                               ####@@...@@####
                                               ####@@...@@####      


# Mechanism/process in the kMC simlation should be defined now. The calculation of the preexponential factor is separated
#     in other file and can be called as a package. There are just 4 types of reaction/process that can be used in this script
#     , to see more information about this go to thefile "prefactor.py", wher you can find more information. To see more informtion
#     about the ElementaryReaction object go to the pyZacros manual.


#### ADSORPTION
mecha_list = []

pe_fwd = CO2_ads_escal*(pf.typeads_fwd(CO2_g, P_CO2, Temp, Area_site).preratio)
pe_rev = CO2_ads_escal*(pf.typeads_rev(CO2_g,Temp, \
                        inf.dimelo("CO2_g","FREQ",Freq_Frame).out,\
                        inf.dimelo("CO2*","FREQ",Freq_Frame).out, \
                        I_CO2, Sym_CO2, Area_site,True).preratio)
if (P_CO2==0):
    CO2_ads = pz.ElementaryReaction( initial=[CO2_s], final=[s0,CO2_g],
                                    site_types=[ "MoTop"],
                                    final_entity_number=[0,1],
                                    reversible=True,
                                    pre_expon = pe_rev,
                                    pe_ratio= 1,
                                    label="CO2_de-adsorption" )
else:
    CO2_ads = pz.ElementaryReaction( initial=[s0,CO2_g], final=[CO2_s],
                                    site_types=[ "MoTop"],
                                    final_entity_number=[0],
                                    reversible=True,
                                    pre_expon = pe_fwd,
                                    pe_ratio=(pe_fwd/pe_rev),
                                    label="CO2_adsorption" )
mecha_list.append(CO2_ads)

pe_fwd = CO_ads_escal*(pf.typeads_fwd(CO_g, P_CO, Temp, Area_site).preratio)
pe_rev = CO_ads_escal*(pf.typeads_rev(CO_g,Temp, \
                        inf.dimelo("CO_g","FREQ",Freq_Frame).out,\
                        inf.dimelo("CO*","FREQ",Freq_Frame).out,\
                         I_CO, Sym_CO,Area_site,True).preratio)
if (P_CO==0):
    CO_ads = pz.ElementaryReaction( initial=[CO_s], final=[s0, CO_g],
                                    site_types=["MoTop"],
                                    final_entity_number=[0,1],
                                    reversible = True,
                                    pre_expon = pe_rev,
                                    pe_ratio=1,
                                    label="CO_de-adsorption" )
    mecha_list.append(CO_ads)
else:
    CO_ads = pz.ElementaryReaction( initial=[s0, CO_g], final=[CO_s],
                                    site_types=["MoTop"],
                                    final_entity_number=[0],
                                        reversible=True,
                                    pre_expon = pe_fwd,
                                    pe_ratio=(pe_fwd/pe_rev),
                                    label="CO_adsorption" )
    mecha_list.append(CO_ads)



pe_fwd = H2_ads_escal*(pf.typeads_fwd(H2_g, P_H2, Temp, Area_site).preratio)
pe_rev = H2_ads_escal*(pf.typeads_rev(H2_g,Temp,\
                        inf.dimelo("H2_g","FREQ",Freq_Frame).out,\
                        inf.dimelo("H2*","FREQ",Freq_Frame).out,\
                        I_H2, Sym_H2,Area_site,True).preratio)
if(P_H2==0):
    H2_ads = pz.ElementaryReaction( initial=[H2_s], final=[s0, H2_g],
                                    site_types=["MoTop"],
                                    final_entity_number=[0,1],
                                    reversible=True,
                                    pre_expon = pe_rev,
                                    pe_ratio=1,
                                    label="H2_adsorption" )
else:
    H2_ads = pz.ElementaryReaction( initial=[s0, H2_g], final=[H2_s],
                                    site_types=["MoTop"],
                                    final_entity_number=[0],
                                        reversible=True,
                                    pre_expon = pe_fwd,
                                    pe_ratio=(pe_fwd/pe_rev),
                                    label="H2_adsorption" )
mecha_list.append(H2_ads)

pe_fwd = H2O_ads_escal*(pf.typeads_fwd(H2O_g, P_H2O, Temp, Area_site).preratio)
pe_rev = H2O_ads_escal*(pf.typeads_rev(H2O_g,Temp,\
                        inf.dimelo("H2O_g","FREQ",Freq_Frame).out,\
                        inf.dimelo("H2O*","FREQ",Freq_Frame).out,\
                        I_H2O, Sym_H2O,Area_site,False).preratio)
if (P_H2O==0):
    H2O_ads = pz.ElementaryReaction( initial=[H2O_s], final=[s0, H2O_g],
                                    site_types=["MoTop"],
                                    final_entity_number=[0],
                                    reversible=True,
                                    pre_expon = pe_rev,
                                    pe_ratio=1,
                                    label="H2O_de-adsorption" )
    mecha_list.append(H2O_ads)
else:
    H2O_ads = pz.ElementaryReaction( initial=[s0, H2O_g], final=[H2O_s],
                                    site_types=["MoTop"],
                                    final_entity_number=[0],
                                        reversible=True,
                                    pre_expon = pe_fwd,
                                    pe_ratio=(pe_fwd/pe_rev),
                                    label="H2O_adsorption" )
    mecha_list.append(H2O_ads)


## RWGS
######################################
#    REACTIONS    
######################################
#   CO2 -> CO + O 
#   
      
pe_fwd = CO2_COyO_escal*(pf.type2(Temp, \
                  inf.dimelo("CO2*","FREQ",Freq_Frame).out, \
                  inf.dimelo("CO2 → CO+O","FREQ",Freq_Frame).out).preratio)
pe_rev = CO2_COyO_escal*(pf.type1(Temp, \
                  inf.dimelo("CO*","FREQ",Freq_Frame).out,\
                  inf.dimelo("O*","FREQ",Freq_Frame).out,\
                  inf.dimelo("CO2 → CO+O","FREQ",Freq_Frame).out,\
                  ).preratio)
react1 = pz.ElementaryReaction( initial=[CO2_s, s0],
                                final=[ O_s,CO_s],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("CO2 → CO+O","FE",Ef_Frame).out,
                                label="CO2_dissociation" )
mecha_list.append(react1)

######################################
#   CO2 + H-> HCOO 
#   
#   
#      

pe_fwd = CO2yH_HCOO_escal*(pf.type1(Temp, \
                  inf.dimelo("CO2*","FREQ",Freq_Frame).out,\
                  inf.dimelo("H*","FREQ",Freq_Frame).out,\
                  inf.dimelo("CO2+H → HCOO","FREQ",Freq_Frame).out,\
                  ).preratio)

pe_rev = CO2yH_HCOO_escal*(pf.type2(Temp, \
                  inf.dimelo("HCOO*","FREQ",Freq_Frame).out, \
                  inf.dimelo("CO2+H → HCOO","FREQ",Freq_Frame).out).preratio)
react2 = pz.ElementaryReaction( initial=[CO2_s,H_s],
                                final=[ HCOO_s, s0 ],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("CO2+H → HCOO","FE",Ef_Frame).out,
                                label="HCOO_formation" )
mecha_list.append(react2)

######################################
#   CO2 + H-> tCOOH 
#   
#   
#      

pe_fwd = CO2yH_tCOOH_escal*(pf.type1(Temp, \
                  inf.dimelo("CO2*","FREQ",Freq_Frame).out,\
                  inf.dimelo("H*","FREQ",Freq_Frame).out,\
                  inf.dimelo("CO2+H → tCOOH","FREQ",Freq_Frame).out,\
                  ).preratio)

pe_rev = CO2yH_tCOOH_escal*(pf.type2(Temp, \
                  inf.dimelo("tCOOH*","FREQ",Freq_Frame).out, \
                  inf.dimelo("CO2+H → tCOOH","FREQ",Freq_Frame).out).preratio)
react3 = pz.ElementaryReaction( initial=[CO2_s, H_s],
                                final=[tCOOH_s, s0],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("CO2+H → tCOOH","FE",Ef_Frame).out,
                                label="tCOOH_formation" )
mecha_list.append(react3)

######################################
#   tCOOH -> cCOOH 
#   
#   
#      
pe_fwd = tCOOH_cCOOH_escal*(pf.type2(Temp, \
                  inf.dimelo("tCOOH*","FREQ",Freq_Frame).out,\
                  inf.dimelo("tCOOH → cCOOH","FREQ",Freq_Frame).out,\
                  ).preratio)

pe_rev = tCOOH_cCOOH_escal*(pf.type2(Temp, \
                  inf.dimelo("cCOOH*","FREQ",Freq_Frame).out, \
                  inf.dimelo("tCOOH → cCOOH","FREQ",Freq_Frame).out).preratio)
react4 = pz.ElementaryReaction( initial=[tCOOH_s],
                                final=[cCOOH_s],
                                site_types=["MoTop"],
                                final_entity_number=[0],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("tCOOH → cCOOH","FE",Ef_Frame).out,
                                label="COOH_conformational" )
mecha_list.append(react4)

######################################
#   cCOOH -> COH + O 
#   
#   
#      
pe_fwd = cCOOH_COHyO_escal*(pf.type2(Temp, \
                  inf.dimelo("cCOOH*","FREQ",Freq_Frame).out,\
                  inf.dimelo("cCOOH → COH+O","FREQ",Freq_Frame).out,\
                  ).preratio)

pe_rev = cCOOH_COHyO_escal*(pf.type1(Temp, \
                  inf.dimelo("O*","FREQ",Freq_Frame).out, \
                  inf.dimelo("COH*","FREQ",Freq_Frame).out, \
                  inf.dimelo("cCOOH → COH+O","FREQ",Freq_Frame).out).preratio)
react5 = pz.ElementaryReaction( initial=[cCOOH_s,s0],
                                final=[COH_s, O_s],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("cCOOH → COH+O","FE",Ef_Frame).out,
                                label="cCOOH_dissociation_1" )
mecha_list.append(react5)



######################################
#   CO + h ->  COH 
#   
#   
#      
pe_fwd = COyH_COH_escal*(pf.type1(Temp, \
                  inf.dimelo("CO*","FREQ",Freq_Frame).out, \
                  inf.dimelo("H*","FREQ",Freq_Frame).out, \
                  inf.dimelo("CO+H→COH","FREQ",Freq_Frame).out).preratio)
pe_rev = COyH_COH_escal*(pf.type2(Temp, \
                  inf.dimelo("cCOOH*","FREQ",Freq_Frame).out,\
                  inf.dimelo("CO+H→COH","FREQ",Freq_Frame).out,\
                  ).preratio)

react5 = pz.ElementaryReaction( initial=[CO_s, H_s],
                                final=[COH_s, s0 ],
                                site_types=["MoTop", "MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("CO+H→COH","FE",Ef_Frame).out,
                                label="COH_formation" )
mecha_list.append(react5)
######################################
#   HCOO->HCO+O  
#   
#   
#      
pe_fwd = HCOO_HCOyO_escal*(pf.type2(Temp, \
                  inf.dimelo("HCOO*","FREQ",Freq_Frame).out, \
                  inf.dimelo("HCOO → HCO+O","FREQ",Freq_Frame).out).preratio)
pe_rev = HCOO_HCOyO_escal*(pf.type1(Temp, \
                  inf.dimelo("O*","FREQ",Freq_Frame).out,\
                  inf.dimelo("HCO*","FREQ",Freq_Frame).out,\
                  inf.dimelo("HCOO → HCO+O","FREQ",Freq_Frame).out,\
                  ).preratio)

react6 = pz.ElementaryReaction( initial=[HCOO_s, s0],
                                final=[HCO_s, O_s],
                                site_types=["MoTop", "MoTop",],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("HCOO → HCO+O","FE",Ef_Frame).out,
                                label="HCOO_disociation" )
mecha_list.append(react6)
 

 
######################################
#   O+H ->OH   
#   
#   
#      
pe_fwd = OyH_OH_escal*(pf.type1(Temp, \
                  inf.dimelo("O*","FREQ",Freq_Frame).out, \
                  inf.dimelo("H*","FREQ",Freq_Frame).out,\
                  inf.dimelo("O+H → OH","FREQ",Freq_Frame).out).preratio)
pe_rev = OyH_OH_escal*(pf.type2(Temp, \
                  inf.dimelo("OH*","FREQ",Freq_Frame).out,\
                  inf.dimelo("O+H → OH","FREQ",Freq_Frame).out).preratio)

react7 = pz.ElementaryReaction( initial=[O_s,H_s],
                                final=[OH_s,s0],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("O+H → OH","FE",Ef_Frame).out,
                                label="OH_formation" )
mecha_list.append(react7)


######################################
#   OH+H→ H2O  
#   
#   
#      
pe_fwd = OHyH_H2O_escal*(pf.type1(Temp, \
                  inf.dimelo("O*","FREQ",Freq_Frame).out, \
                  inf.dimelo("OH*","FREQ",Freq_Frame).out,\
                  inf.dimelo("OH+H→ H2O","FREQ",Freq_Frame).out).preratio)
pe_rev = OHyH_H2O_escal*(pf.type2(Temp, \
                  inf.dimelo("H2O*","FREQ",Freq_Frame).out,\
                  inf.dimelo("OH+H→ H2O","FREQ",Freq_Frame).out).preratio)

react8 = pz.ElementaryReaction( initial=[OH_s,H_s],
                                final=[H2O_s,s0],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("OH+H→ H2O","FE",Ef_Frame).out,
                                label="H2O_formation_1" )
mecha_list.append(react8)

######################################
#   HCO -> H + CO 
#   
#   
      
pe_fwd = HCO_HyCO_escal*(pf.type2(Temp, \
                  inf.dimelo("HCO*","FREQ",Freq_Frame).out, \
                  inf.dimelo("HCO → H+CO","FREQ",Freq_Frame).out).preratio)
pe_rev = HCO_HyCO_escal*(pf.type1(Temp, \
                  inf.dimelo("H*","FREQ",Freq_Frame).out,\
                  inf.dimelo("CO*","FREQ",Freq_Frame).out,\
                  inf.dimelo("HCO → H+CO","FREQ",Freq_Frame).out).preratio)

react9 = pz.ElementaryReaction( initial=[HCO_s, s0],
                                final=[CO_s,H_s],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("HCO → H+CO","FE",Ef_Frame).out,
                                label="HCO_formation" )
mecha_list.append(react9)

######################################
#   OH+OH → H2O+O  
#   
#   
#      
pe_fwd = OHyOH_H2OyO_escal*(pf.type1(Temp, \
                  inf.dimelo("OH*","FREQ",Freq_Frame).out, \
                  inf.dimelo("OH*","FREQ",Freq_Frame).out,\
                  inf.dimelo("OH+OH → H2O+O","FREQ",Freq_Frame).out).preratio)
pe_rev = OHyOH_H2OyO_escal*(pf.type1(Temp, \
                  inf.dimelo("H2O*","FREQ",Freq_Frame).out,\
                  inf.dimelo("O*","FREQ",Freq_Frame).out,\
                  inf.dimelo("OH+OH → H2O+O","FREQ",Freq_Frame).out).preratio)

react10 = pz.ElementaryReaction( initial=[OH_s,OH_s],
                                final=[O_s,H2O_s],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("OH+OH → H2O+O","FE",Ef_Frame).out,
                                label="H2O_formation_2" )
mecha_list.append(react10)

######################################
#   H2→ H + H  
#   
#   
#      
pe_fwd = H2_HyH_escal*(pf.type2(Temp, \
                  inf.dimelo("H2*","FREQ",Freq_Frame).out, \
                  inf.dimelo("H2→ 2H","FREQ",Freq_Frame).out).preratio)
pe_rev = H2_HyH_escal*(pf.type1(Temp, \
                  inf.dimelo("H*","FREQ",Freq_Frame).out,\
                  inf.dimelo("H*","FREQ",Freq_Frame).out,\
                  inf.dimelo("H2→ 2H","FREQ",Freq_Frame).out).preratio)

react11 = pz.ElementaryReaction( initial=[H2_s,s0],
                                final=[H_s,H_s],
                                site_types=["MoTop", "MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("H2→ 2H","FE",Ef_Frame).out,
                                label="H2_dissociation" )
mecha_list.append(react11)

######################################
#   cCOOH → CO + OH  
#   
#   
#      
pe_fwd = cCOOH_COyOH_escal*(pf.type2(Temp, \
                  inf.dimelo("cCOOH*","FREQ",Freq_Frame).out, \
                  inf.dimelo("cCOOH → CO + OH","FREQ",Freq_Frame).out).preratio)
pe_rev = cCOOH_COyOH_escal*(pf.type1(Temp, \
                  inf.dimelo("CO*","FREQ",Freq_Frame).out,\
                  inf.dimelo("OH*","FREQ",Freq_Frame).out,\
                  inf.dimelo("cCOOH → CO + OH","FREQ",Freq_Frame).out).preratio)

react12 = pz.ElementaryReaction( initial=[cCOOH_s,s0],
                                final=[ CO_s, OH_s],
                                site_types=["MoTop","MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("cCOOH → CO + OH","FE",Ef_Frame).out,
                                label="cCOOH_dissociation_2" )
mecha_list.append(react12)

                                               ###@@..@@###
                                               ###@@..@@###
###############################################            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
############################################### DIFFUSIONS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@                 
                                               ###@@..@@###   
                                               ###@@..@@###                    


#################################
###       cCOOH Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("cCOOH*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("cCOOH*","FREQ",Freq_Frame).out).preratio
#react13 = pz.ElementaryReaction( initial=[cCOOH_s,s0],
#                                final=[s0,cCOOH_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                reversible=False,
#                                pre_expon = pe_fwd,
#                                activation_energy=inf.dimelo("cCOOH* diff","FE",Ef_Frame).out,
#                                label="cCOOH_diffussion" )
#mecha_list.append(react13)

#################################
###       tCOOH Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("tCOOH*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("tCOOH*","FREQ",Freq_Frame).out).preratio
#react14 = pz.ElementaryReaction( initial=[tCOOH_s,s0],
#                                final=[s0,tCOOH_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                reversible=False,
#                                pre_expon = pe_fwd,
#                                activation_energy=inf.dimelo("tCOOH* diff","FE",Ef_Frame).out,
#                                label="tCOOH_diffussion" )
#mecha_list.append(react14)

#################################
###       CO2 Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("CO2*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("CO2*","FREQ",Freq_Frame).out).preratio
#react15 = pz.ElementaryReaction( initial=[CO2_s,s0],
#                                final=[s0,CO2_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                reversible=False,
#                                pre_expon = pe_fwd,
#                                activation_energy=inf.dimelo("CO2* diff","FE",Ef_Frame).out,
#                                label="CO2_diffussion" )
#mecha_list.append(react15)

#################################
###       COH Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("COH*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("COH*","FREQ",Freq_Frame).out).preratio
#react16 = pz.ElementaryReaction( initial=[COH_s,s0],
#                                final=[s0,COH_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                reversible=False,
#                                pre_expon = pe_fwd,
#                                activation_energy=inf.dimelo("COH* diff","FE",Ef_Frame).out,
#                                label="COH_diffussion" )
#mecha_list.append(react16)

#################################
###       H Diff

pe_fwd = H_diff_escal*(pf.type2(Temp, \
                  inf.dimelo("H*","FREQ",Freq_Frame).out, \
                  inf.dimelo("H* diff","FREQ",Freq_Frame).out).preratio)
pe_fwd=pe_fwd/2.0
pe_rev = pe_fwd
react17 = pz.ElementaryReaction( initial=[H_s,s0],
                                final=[s0,H_s],
                                site_types=["MoTop", "MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("H* diff","FE",Ef_Frame).out,
                                label="H_diffussion" )
mecha_list.append(react17)

#################################
###       H2 Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("H2*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("H2*","FREQ",Freq_Frame).out).preratio
#react18 = pz.ElementaryReaction( initial=[H2_s,s0],
#                                final=[s0,H2_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                pre_expon = pe_fwd,
#                                reversible=False,
#                                activation_energy=inf.dimelo("H2* diff","FE",Ef_Frame).out,
#                                label="H2_diffussion" )
#mecha_list.append(react18)

#################################
###       H2O Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("H2O*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("H2O*","FREQ",Freq_Frame).out).preratio
#react19 = pz.ElementaryReaction( initial=[H2O_s,s0],
#                                final=[s0,H2O_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                reversible=False,
#                                pre_expon = pe_fwd,
#                                activation_energy=inf.dimelo("H2O* diff","FE",Ef_Frame).out,
#                                label="H2O_diffussion" )
#mecha_list.append(react19)

#################################
###       HCO Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("HCO*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("HCO*","FREQ",Freq_Frame).out).preratio
#react20 = pz.ElementaryReaction( initial=[HCO_s,s0],
#                                final=[s0,HCO_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                reversible=False,
#                                pre_expon = pe_fwd,
#                                activation_energy=inf.dimelo("HCO* diff","FE",Ef_Frame).out,
#                                label="HCO_diffussion" )
#mecha_list.append(react20)


#################################
###       HCOO Diff

#pe_fwd = pf.type2(Temp, \
#                  inf.dimelo("HCOO*","FREQ",Freq_Frame).out, \
#                  inf.dimelo("HCOO*","FREQ",Freq_Frame).out).preratio
#react22 = pz.ElementaryReaction( initial=[HCOO_s,s0],
#                                final=[s0,HCOO_s],
#                                site_types=["MoTop", "MoTop"],
#                                neighboring=[(0,1)],
#                                final_entity_number=[0,1],
#                                reversible=False,
#                                pre_expon = pe_fwd,
#                                activation_energy=inf.dimelo("HCOO* diff","FE",Ef_Frame).out,
#                                label="HCOO_diffussion" )
#mecha_list.append(react22)


#################################
###       O Diff

pe_fwd = O_diff_escal*(pf.type2(Temp, \
                  inf.dimelo("O*","FREQ",Freq_Frame).out, \
                  inf.dimelo("O* diff","FREQ",Freq_Frame).out).preratio)
pe_fwd=pe_fwd/2.0
pe_rev = pe_fwd
react24 = pz.ElementaryReaction( initial=[O_s,s0],
                                final=[s0,O_s],
                                site_types=["MoTop", "MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("O* diff","FE",Ef_Frame).out,
                                label="O_diffussion" )
mecha_list.append(react24)

#################################
###       CO* Diff

pe_fwd = CO_diff_escal*(pf.type2(Temp, \
                  inf.dimelo("CO*","FREQ",Freq_Frame).out, \
                  inf.dimelo("CO* diff","FREQ",Freq_Frame).out).preratio)
pe_fwd=pe_fwd/2.0
pe_rev = pe_fwd
react25 = pz.ElementaryReaction( initial=[CO_s,s0],
                                final=[s0,CO_s],
                                site_types=["MoTop", "MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("CO* diff","FE",Ef_Frame).out,
                                label="CO_diffussion" )
mecha_list.append(react25)

#################################
###       OH Diff

pe_fwd = OH_diff_escal*(pf.type2(Temp, \
                  inf.dimelo("OH*","FREQ",Freq_Frame).out, \
                  inf.dimelo("OH* diff","FREQ",Freq_Frame).out).preratio)
pe_fwd=pe_fwd/2.0
pe_rev = pe_fwd
react26 = pz.ElementaryReaction( initial=[OH_s,s0],
                                final=[s0,OH_s],
                                site_types=["MoTop", "MoTop"],
                                neighboring=[(0,1)],
                                final_entity_number=[0,1],
                                reversible=True,
                                pre_expon = pe_fwd,
                                pe_ratio=(pe_fwd/pe_rev),
                                activation_energy=inf.dimelo("OH* diff","FE",Ef_Frame).out,
                                label="OH_diffussion" )
mecha_list.append(react26)



mecha_list=pz.Mechanism(mecha_list)

job = pz.ZacrosJob(settings=sett, lattice=lattice,
                    mechanism=mecha_list,
                    cluster_expansion=cluster_list)

print("#######################################################")
print(colors.Green+"         Perfect! all data has been build.             "+ colors.END)
print("#######################################################")


# writing input files for Zacros software
file = open("simulation_input.dat","w")
file.write(job.get_simulation_input())

file = open("mechanism_input.dat","w")
file.write(job.get_mechanism_input())

file = open("lattice_input.dat","w")
file.write(job.get_lattice_input())

file = open("energetics_input.dat","w")
file.write(job.get_energetics_input())

