#!/usr/bin/env python3
# Converts the a CONTCAR or POSCAR file to the .xyz file format, also a ordering process is done before printing the output
#   The aim of this script translate the information to .xyz format, that is a more usual format to visualization.
#  Also a png file is build automatically.
try:
    import ase
    from ase.io import read, write
    from ase.visualize import view
    import numpy as np
    import os
    import sys
except:
    print(error.__class__.__name__+":"+error.message)

# give to the script the output name file
name=input("Type the name of the output file \n    ")

# Read from terminal the file
initial = read(sys.argv[1],format='vasp')
#obtaining the unit cell and their vectors
cell=initial.get_cell()
v1=cell[0]
v2=cell[1]

L1=np.sqrt(v1.dot(v1))
L2=np.sqrt(v2.dot(v2))
cos_angle=v1.dot(v2)/(L1*L2)
angle=np.arccos(cos_angle)
y_max_high = np.cos(angle-np.pi/2)*L2 # check

# reordering of the lattice
for i in range(len(initial.get_positions())):
    r=initial.get_positions()[i,:]
    if (r[1]>0.9*y_max_high):
        initial.positions[i,:]-=v2
        r = initial.positions[i,:]
        angle2 = angle-(90*2*np.pi/360)
        Prv2 = r[1]/np.cos(angle2)
        x_max =v1[0]- abs(np.linalg.norm(Prv2)*np.sin(angle2))
        if (r[0]>0.9*x_max):
            initial.positions[i,:]-=v1
# Adding format to name
name_xyz = name +".xyz"
# Writing xyz
write(name_xyz,initial, format="xyz")
write("Temp_CON", initial, format="vasp")
# Now we will get the photos that we want
name_png= name + ".png"
# writing png
initial = read(name_xyz,format='xyz')
write(name_png, initial, "png")
initial = read("Temp_CON", format="vasp")
view(initial)
os.remove("Temp_CON")


