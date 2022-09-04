#!/usr/bin/python3
#################################################################################################################
#      This script obtain informationd desired (for more/less information this script shol be modified by hand) 
#       from a Zacros simulation. The aim of this script is to be used with other super-scripts that use this 
#       script to obtain data from several simulations in different folders.
#      
#      This script just accept one input, that is the column number, of the ods file with "results.xsx" name,
#       where you want to be printed all the information obtained in this script.
#
#################################################################################################################

import numpy as np
import scm.plams
import pyzacros as pz
import pandas as pd
import os
import re
import sys
import xlsxwriter
import openpyxl

# Decuelve el valor en porcentaje de ocupacion
# Retur the fractional ocupation on the lattice of the specie given
#   Input:
#       -spec:
#           specnum object (see pyZacros manual for more information)
#       -name:
#           String with the name of the specie desired
#       -surf_specs_names:
#           List with all the species that can be in the surface
#   Output:
#       - return the ocupation from the total (empty site are not taken into account)
def ocupacion(spec,name,surf_specs_names):
    total = 0
    for spc in surf_specs_names:
        total += spec.get(spc)[-1]
    name_val = spec.get(name)[-1]
    if (total==0):
        return 0
    return name_val/total

# Retur the total number of events 
#   Input:
#       -name:
#           String with the name of the specie desired
#       -num_events_proc:
#           Object with al the numer of events at one time. This object is obtained from the pyZacros function 
#               "pstat=result.get_process_statistics()" and the if you select for example last step "dats=pstat[-1]"
#               and now you can obtain the num_events_proc object as "num_events_proc=(dats["number_of_events"])".
#       -rev:
#           If you want to reverse the reaction, take fwd as rev and rev as fwd.
#   Output:
#       - return the number of procces (it rest fwd and rev giving the real total number of process with direction.)
def proc_dime( name, num_events_proc, rev=False):
    name_fwd = name + "_fwd"
    name_rev = name + "_rev"
    if (rev==False):
        av_t_1 = num_events_proc[name_fwd]
        av_t_2 = num_events_proc[name_rev]
        av_t_1 = av_t_1 - av_t_2
        return av_t_1 # devuelve el numero de procesos hacia delante de esta reacción
    elif (rev==True):
        av_t_1 = num_events_proc[name_fwd]
        av_t_2 = num_events_proc[name_rev]
        av_t_1 = av_t_2 - av_t_1
        return av_t_1 # devuelve el numero de procesos hacia delante de esta reacción

# Obtaining path of actual directory
CWD_path = os.getcwd()
# Creating the path to the .xlsx file
xlx_path = CWD_path+"/results.xlsx"
# Building he pyZacros object ZacrosJob
work = pz.ZacrosJob.load_external(path=CWD_path,finalize=True)

# Definning as succesful, if not anything will run
work.status="successful"
# Getting results
result = work.results

# Obtaining main data object from pyZacros
spec = result.provided_quantities()
pstat = result.get_process_statistics()
number_of_lattice_sites= result.number_of_lattice_sites()

# Obtaing the name of all surface species, the gas molar fractions and the gas species nammes from the simulation_input file
with open(CWD_path+"/simulation_input.dat") as data_file:
    for line in data_file:
        if line.startswith("surf_specs_names"):
            surf_specs_names = (line.split()[1:])
        if line.startswith("gas_molar_fracs"):
            gas_molar_fracs= line.split()[1:]
        if line.startswith("gas_specs_names"):
            gas_specs_names= line.split()[1:]

# Opening the xlsx file
wb = openpyxl.load_workbook(xlx_path)
ws = wb['Sheet1']

# Select the letter of the column
number_col = int(sys.argv[1])
# Converting the number given to a letter (ex: column 4 -> column D)
letter = xlsxwriter.utility.xl_col_to_name(number_col)

# Geting information from last frame
dats=pstat[-1]

# Obtaining the num_event_proc object from las step of the simulation
num_events_proc=(dats["number_of_events"])

# Now a dataframe with all the information to print to the xlsx file will be builded.
column = pd.DataFrame({'Nueva':[
str(spec.get("Temperature")[-1]),
"time_simulation",
dats["time"],
"P_parc",
float(gas_molar_fracs[0]), # PCO2
float(gas_molar_fracs[2]), # PH2
float(gas_molar_fracs[1]), # P
float(gas_molar_fracs[3]), # P
"GAS_prod",
spec.get("CO2")[-1],
spec.get("H2")[-1],
spec.get("CO")[-1],
spec.get("H2O")[-1],
"ADS",
spec.get("CO2*")[-1],
spec.get("H2*")[-1],
spec.get("CO*")[-1],
spec.get("H2O*")[-1],
"OCUPACION",
ocupacion(spec,"CO2*", surf_specs_names),
ocupacion(spec,"CO*", surf_specs_names),
ocupacion(spec,"H2*", surf_specs_names),
ocupacion(spec,"H2O*", surf_specs_names),
ocupacion(spec,"O*", surf_specs_names),
ocupacion(spec,"H*", surf_specs_names),
ocupacion(spec,"HCOO*", surf_specs_names),
ocupacion(spec,"traCOOH*", surf_specs_names),
ocupacion(spec,"cisCOOH*", surf_specs_names),
ocupacion(spec,"COH*", surf_specs_names),
ocupacion(spec,"HCO*", surf_specs_names),
ocupacion(spec,"OH*", surf_specs_names),
"OC_FREQ",
"freq ads",
proc_dime("CO2_adsorption", num_events_proc),
proc_dime("CO_de-adsorption", num_events_proc),
proc_dime("H2_adsorption", num_events_proc),
proc_dime("H2O_de-adsorption", num_events_proc),
"others",
proc_dime("CO2_dissociation", num_events_proc),
proc_dime("HCOO_formation", num_events_proc),
proc_dime("tCOOH_formation", num_events_proc),
proc_dime("COOH_conformational", num_events_proc),
proc_dime("cCOOH_dissociation_1", num_events_proc),
proc_dime("COH_formation", num_events_proc),
proc_dime("HCOO_disociation", num_events_proc),
proc_dime("OH_formation", num_events_proc),
proc_dime("H2O_formation_1", num_events_proc),
proc_dime("HCO_formation", num_events_proc),
proc_dime("H2O_formation_2", num_events_proc),
proc_dime("H2_dissociation", num_events_proc),
proc_dime("cCOOH_dissociation_2", num_events_proc)
]})

# Printing to file
for index, row in column.iterrows():
    cell = '{letter}{val}'.format(letter=letter, val=(index + 2 ))
    ws[cell] = row[0]
    
wb.save('results.xlsx')