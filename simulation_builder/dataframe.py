#!/usr/bin/python3
#########################################################################################################################
#	This script is part of complete repository on github (https://github.com/perasperadastra/TFM_master_computacion)
#		The dimelo functio obtain information from two .ods files, its addapted to recibe the "FE" or "FREQ" string, 
#       where the first one refers to the formation energy, and the second one for frequencies. The .ods file were read
#       in the main script, this function just recive the frame obtained from this read.	
#########################################################################################################################


import pandas as pd
import math

class dimelo():
	def __init__(self ,symbol, value, frame):
		# symbol: name of the species
		# value: its FE or FREQ ?
		# frame: data frame
		self.symbol = symbol
		self.value = value
		self.frame = frame
		self.out = self.calculate()

	def calculate(self):
		if (self.value=="FE" or self.value=="Fe" or self.value=="fE"):
			list_Names = self.frame.loc[self.frame["Name"] == self.symbol, "FE"].iloc[0]  #.loc["CO2_g"]
			return(list_Names)
		if (self.value=="Freq" or self.value=="freq" or self.value=="FREQ"):
			freqs = self.frame.loc[ \
					self.frame["Name"] == self.symbol] \
					.iloc[0].tolist()[1:]
			# Removing nan data
			freqs = [item for item in freqs if not(math.isnan(item)) == True]
			return(freqs)

