#!/usr/bin/python3
####################################################################################################################
#   This script get the information of a Zacros simulation and returns a input file to re-run the simulation
#       from a specific step (that the user must give to the script). So, it build the "state_input.dat" file that
#       Zacros use as initial condition for the lattice.
#
####################################################################################################################
import os
import re

# Colors, for fancy user's
class bcolors:
    Black= "\u001b[30;1m"
    Red= "\u001b[31;1m"
    Green= "\u001b[32;1m"
    Yellow= "\u001b[33;1m"
    Blue= "\u001b[34;1m"
    Magenta= "\u001b[35;1m"
    Cyan= "\u001b[36;1m"
    White= "\u001b[37;1m"
    END="\u001b[0m"
# Obtaining path
file_Path = str(os.getcwd())+"/history_output.txt"

# Try to open the "history_output.txt" file, if it does not exist the script stops
try :
    with open(file_Path, "r") as file:
        lines = file.readlines()
except: 
    print(bcolors.Red+"Error: no history_output.txt"+bcolors.END)
    quit()

# Count the number of configurations that are saved in the "history_output.txt"
count = 0
for line in lines:
    if re.search(r"\bconfiguration\b", line, flags=re.IGNORECASE):
        count += 1
# Obtainig surface species
species = lines[1].split()

# Gives the user the number of snapshots avalible and then ask the user to select one.
print(" Number of snapshots")
print(bcolors.Yellow +"     "+ str(count) +bcolors.END)
txt = " Please choose the number of the desired snap"+bcolors.Green+ "\n     "
while (True):
    snap = input(txt)
    try:
        snap = int(snap)
    except:
        print(bcolors.Red+"That is not a valid number"+bcolors.END)
        continue
    if ((snap<=count) and (snap>=1)):
        break
    else:
        pass
print(bcolors.END)

# Now the configuration select will be saved
count2 = 0 
new_lines = []
record = False
first=True
for line in lines:
    # if condition to control when the " if record" condition is active or not
    #   when we are in the correct interval record saves the information.
    if re.search(r"\bconfiguration\b", line, flags=re.IGNORECASE):
        count2 += 1 
        # When the configuration desired is founded, the boolean variable record is changed, and now we record the confg  
        if ((count2==snap) and (first)):
            record = True
            first=False
        elif (count2>=snap):
            record  = False        
    if record:
        new_lines.append(line)
new_lines = new_lines[1:-1]

# Build the full path to the result file.
file_Path =  str(os.getcwd())+"/state_input.dat"

# writing the file
with open(file_Path, "w") as file:
    file.write("initial_state\n")
    for line in new_lines:
        values = line.split()
        if (int(values[2])!= 0 ):
            spec = species[int(values[2])]
            values[0] # site id
            txt = "seed_on_sites"+ " " + spec +" "+ values[0] + "\n"
            file.write(txt)

    file.write("end_initial_state\n")


    

#for i in range(len(species))