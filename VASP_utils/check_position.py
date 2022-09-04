#!/usr/bin/python3
# This python script trys to reorder the POSCAR file to make easier the visualization. What its done is to read
#   the POSCAR file and the using periodic boundary conditions and a toleranc value, atoms are reordered.
import ase, ase.neb
from ase.io import read, write
from ase.io.trajectory import Trajectory
from ase.optimize import FIRE
from copy import deepcopy
from ase.visualize import view
from ase.constraints import FixAtoms
import numpy as np
import os
import sys

# The tolerance value, for example using 0.9 will mean that if any atom is in a position that 
#   is higher than 0.9 of the periodic unit cell, it will be moved to the opposite place
tolerance = 0.9

initial = read('POSCAR',format='vasp')

cell=initial.get_cell()
v1=cell[0]
v2=cell[1]

L1=np.sqrt(v1.dot(v1))
L2=np.sqrt(v2.dot(v2))
cos_angle=v1.dot(v2)/(L1*L2)
angle=np.arccos(cos_angle)
y_max_high = np.cos(angle-np.pi/2)*L2 # check

for i in range(len(initial.get_positions())):
    r=initial.get_positions()[i,:]

    if (r[1]>tolerance*y_max_high):
        initial.positions[i,:]-=v2
        r = initial.positions[i,:]

    angle2 = angle-(90*2*np.pi/360)
    Prv2 = r[1]/np.cos(angle2)
    x_max =v1[0]- abs(np.linalg.norm(Prv2)*np.sin(angle2))
    if (r[0]>tolerance*x_max):
        initial.positions[i,:]-=v1


write("POSCAR",initial, format="vasp",direct=True)
os.system("/home/adastra/Programas/my_scripts/ase_view/edit_my_poscar.py")
