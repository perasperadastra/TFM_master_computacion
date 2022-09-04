#!/usr/bin/python3
# This python script use directory enviroment build with the python script "VASP_diff.py" to build with the ase
#   package a representation that have all the steps of the NEB process
import ase, ase.neb
from ase.io import read, write
from ase.io.trajectory import Trajectory
from ase.optimize import FIRE
from copy import deepcopy
from ase.visualize import view
import numpy as np
import os
import sys

Nimages =int( input('Choose the number of images: '))

initial = read('00/POSCAR')
final = read('0'+str(Nimages+1)+'/POSCAR')

images = []
images = [initial]
for i in range(1,Nimages+1):
    image = read('0'+str(i)+'/CONTCAR')
    images.append(image)
images.append(final)

view(images)

