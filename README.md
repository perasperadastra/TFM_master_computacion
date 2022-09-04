# TFM_master_computacion
Different scripts to run and work with VASP and Zacros software.

## Zacros enviroment:

### pyZacros modifications:
  In the pyZacros library go to *core/Species.py*, if you dont know how to find these files, open your python3 enviroment, and do:
  ``` 
  import pyzacros
  pyzacros 
  ```
  In core **Species.py**, in the *__init__* function search for 
  ```
  self.__composition = chemparse.parse_formula( symbol.replace("*","") )
  ```
  remove this line and change for:
  ```
  chem_name = self.symbol.replace("*","")
  chem_name = chem_name.replace("cis","")
  chem_name = chem_name.replace("tra","")
  self.__composition = chemparse.parse_formula(chem_name)
  ```
  Now you can add cis and tra species, this methodology can be used for add other molecules names. The problem that is solved with this lines is that pyzacros use the specie name to calculate it mass and/or other paremeters, so if you add strings that do no represent atoms it break the building.

### Simulation builder:
   In the *simulation_builder* directory you can find an a simulation builder for (0001) Mo2C MXene to build a kMC simulation for Zacros software. If ou are going to change parameters to build your own simulation remebeber to read in detail the pyZacros and Zacros manual, and follow my methodology to add new molecules or parameters.
   The main script **simulation_builder.py** accepts three parameters: Temperature, partial pressure of CO2 and partial pressure of H2. If you want to give more or less parameter the input transference of infomation is done with the python library sys, and using sys.argv .
  
### Obtaining general results
In the *data_obtainer* directory there are two sub-directorys. In bothe there are one python script that obtain information from Zacros simulations and save them in a xlsx file.
The main difference between them , is that the **data_obtainer_serie.py** file (on *data_obtainer/byhand_serie*) should be used with a super-script builder that is contained in the *tools_box/multi_builder* directory.

In the *data_obtainer/complete_justforone* directory there is a script with similar behaviour. This script have a interface that ask the user if he wnats to obtain all the information ( that is authomatic for any kMC simulation) or if he wants a specific information ( that shoul de modified by hand for each Zacros simulation)

### Tools box

In the Tools box there are:
- state_builder.py:
  This python script is count all the snapshot saved in the **history_output.txt** file and then gives the user the possibility to obtain the state of a specific snap. The lattice state is returned in the **state_input.dat** file, that have the name and format needed by Zacros to use this state as the initial state of another simulation ( so you can use this file to re-start a simulation from a specific point).
- multi_builder/creator.sh:
  As commented before this is a super-script to build several simulation in different thermodynamic conditions. Also, it build a **runner.sh** file (that gives the possibility of send to the queque all this simulation at once) and the **results.sh** ( that obtain information from all this simulations, and the save them in a results.xlsx file). To use this script you need to adapt your **simulation_builder.py** and **data_obtainer_serie.py** file for your desired data and simulations.
  

