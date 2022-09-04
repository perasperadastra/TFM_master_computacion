#!/usr/bin/python3
"""
 Python script that use the ase package NEB process to build images between an initial and final state
 remeber that those states should have the following names:
      initial.POSCAR
      final.POSCAR
 And to have the INCAR, POTCAR and KPOINTS  in the principal directory
"""

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

# Ask the user for the number of images wanted
Nimages = int(input('Choose the number of images: '))
initial = read('initial.POSCAR',format='vasp')
final = read('final.POSCAR',format='vasp')


cell=initial.get_cell()

# we copy the initial and final into a save object
write_initial = initial 
write_final = final
for i in range(len(initial.get_positions())):
   r=initial.get_positions()[i,:]-final.get_positions()[i,:]

   if ( abs(r[0]) > 0.8*cell[0,0] ):
      final.positions[i,0] += (r[0]/abs(r[0]))*cell[0,0]

   if ( abs(r[1]) > 0.8*cell[1,1] ):
      final.positions[i,1] += (r[1]/abs(r[1]))*cell[1,1]

   if ( abs(r[2]) > 0.8*cell[2,2] ):
      final.positions[i,2] += (r[2]/abs(r[2]))*cell[2,2]

#  copy initial to the list of images
images = []
images = [initial]

my_atom = [ atom for atom in write_initial]

write('POSCAR',write_initial,direct=True)

os.system('mkdir 00')
os.system('mv POSCAR 00/')

print("Lecture done")


for i in range(Nimages):
    image = initial.copy()
    images.append(image)

images.append(final)
neb = ase.neb.NEB(images, climb=False, k=0.5)
neb.interpolate('idpp')

print("NEB done")
for j in range(1,Nimages+1):
    my_atom = [ atom for atom in images[j]]
    write('POSCAR',images[j], direct=True)
    
    os.system('mkdir 0'+str(j))
    os.system('mv POSCAR 0'+str(j))


# we write the POSCAR adding the constrain
my_atom = [ atom for atom in write_final]

write('POSCAR',write_final, direct=True)

os.system('mkdir 0'+str(Nimages+1))
os.system('mv POSCAR 0'+str(Nimages+1))

view(images)
