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
   In the *simulation builder* directory you can find an a simulation builder for (0001) Mo2C MXene to build a kMC simulation for Zacros software. If ou are going to change parameters to build your own simulation remebeber to read in detail the pyZacros and Zacros manual, and follow my methodology to add new molecules or parameters.
   The main script **simulation_builder.py** accepts three parameters: Temperature, partial pressure of CO2 and partial pressure of H2. If you want to give more or less parameter the input transference of infomation is done with the python library sys, and using sys.argv .
  
### Obtaining general results
