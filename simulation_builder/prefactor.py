#!/usr/bin/python3
#########################################################################################################################
#   The prefactor is a parameter that should be included in the kMC framework (in this case runned with Zacros). Here we
#      have four type of preafactor calculation for 4 types of reactions:
#                           X* + Y* ->  &&&&&&
#                           X* -> &&&&&&
#                           X(g) + * -> X*
#                           X* -> X(g) + *
#
#########################################################################################################################

import scipy.constants as cte
import math as m
Kb= cte.k # Boltzman constants in J/K
# Convert to eV/K
Kb = 0.0001 * (1.380649/1.60217663)

#######################################################################
#                            X* + Y* ->  &&&&&&
# Input:
#   T: temperature in kelvin
#   freq1: list with all the energyes frequencies in eV for X*
#   freq2: list with all the energyes frequencies in eV for Y*
#   freq3: list with all the energies freq in eV for the transition state
class type1():
    def __init__(self,T,freq1,freq2, freq3):
        self.T = T
        self.freq1 = freq1
        self.freq2 = freq2
        self.freq3 = freq3

        q_vib_x = 1
        for i in range(len(freq1)):
            q_vib_x = q_vib_x * ( 1 / (1 - m.exp(-((freq1[i]*10**(-3))/(Kb*T))) ))
        
        q_vib_y= 1
        for i in range(len(freq2)):
            q_vib_y = q_vib_y * ( 1 / (1 - m.exp(-((freq2[i]*10**(-3))/(Kb*T))) ) )
        
        q_vib_trans = 1
        for i in range(len(freq3)):
            q_vib_trans = q_vib_trans * (1 / (1 - m.exp(-((freq3[i]*10**(-3))/(Kb*T))) ) )
        
        self.preratio = (q_vib_trans/(q_vib_x*q_vib_y)) * (cte.k * T/cte.h)

#######################################################################
#                            X* -> &&&&&&
# Input:
#   T: temperature in kelvin
#   freq1: list with all the energyes frequencies in eV for X*
#   freq2: list with all the energies freq in eV for the transition state
class type2():
    def __init__(self,T,freq1,freq2):
        self.T = T
        self.freq1 = freq1
        self.freq2 = freq2

        q_vib_x = 1
        for i in range(len(freq1)):
            q_vib_x = q_vib_x * ( 1 / (1 - m.exp(-((freq1[i]*10**(-3))/(Kb*T))) ))
        
        q_vib_trans = 1
        for i in range(len(freq2)):
            q_vib_trans = q_vib_trans * ( 1 / (1 - m.exp(-((freq2[i]*10**(-3))/(Kb*T))) ) )

        self.preratio = (q_vib_trans/(q_vib_x)) * (cte.k * T/cte.h)

#######################################################################
#                            X(g) + * -> X*
# Input:
#   gas: pyzacros class of the gas specie
#   T: temperature in kelvin
#   freq1: list with all the energyes frequencies in eV for X gas
#   freq2: list with all the energyes frequencies in eV for X*
class typeads_fwd():
    def __init__(self,gas,partial_P, T,Area):
        self.gas = gas
        self.partial_P=partial_P
        self.T = T
        self.Area = Area
        # forward non-actived
        self.preratio= (partial_P*101325 * Area /m.sqrt(2.0* m.pi\
            * (self.gas.mass()*(1.380649)*(1.66054) * self.T )) *(10.0**(5)))


#######################################################################
#                            X* -> X(g) + *
# Input:
#   gas: pyzacros class of the gas specie
#   T: temperature in kelvin
#   freq_g: list with all the energyes frequencies in eV for X gas
#   freq1: list with all the energyes frequencies in eV for X*
#   inertial: inertial  moment of gas molecule
#   sym_num:  symmetric number of gas molecule
#   linear: true/false si la simetria de la molecula es lineal
class typeads_rev():
    def __init__(self, gas, T, freq_g, freq1, inertial, sym_num,Area ,linear):
        self.gas = gas
        self.T = T
        self.freq_g = freq_g
        self.freq1 = freq1
        self.inert = inertial
        self.sym_num = sym_num
        self.linear = linear
        self.Area = Area

        q_vib_gas = 1
        for i in range(len(freq_g)):
            q_vib_gas = q_vib_gas * ( 1 / (1 - m.exp(-((freq1[i]*10**(-3))/(Kb*T))) ))

        q_vib_x = 1
        for i in range(len(freq1)):
            q_vib_x = q_vib_x * ( 1 / (1 - m.exp(-((freq1[i]*10.0**(-3))/(Kb*T))) ))

        if (linear==True):
            q_rot = ((8.0*(m.pi**2)*self.inert * self.T)/(self.sym_num))*(0.00052218)
        elif (linear==False):
            q_rot = ((((m.pi*self.inert))**(1.0/2.0))/self.sym_num) \
                        * ((8.0*(m.pi**2)*self.T)**(3.0/2.0)) * (0.000011932)

        q_trans_2D = (2.0 * m.pi * self.T *  (self.gas.mass()) * (Area * 0.00052218))
        self.preratio = (q_vib_gas * q_rot * q_trans_2D /q_vib_x) * (20836619595.023898027* T)


