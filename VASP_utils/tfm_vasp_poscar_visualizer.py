#!/usr/bin/env python3
# This scripts reads the POSCAR file and display with the ase package the image
#   It is reccomended to use an alias (bash alias) and rename this scipt as POSCAR
try:
    from ase.io.vasp import read_vasp
    from ase.visualize import view
except:
    print(error.__class__.__name__+":"+error.message)
try:
    my=read_vasp(file="POSCAR")
except ImportError as error:
    print(error.message)

view(my)
