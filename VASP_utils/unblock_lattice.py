#! /usr/bin/python3
# This script change a POSCAR file that all only some of their atoms can move ( T   T   T) to a POSCAR where the lattice is totally 
#    unblocked, so all atoms can move
try:
    from ase.io.vasp import read_vasp, write_vasp
    from ase.visualize import view
    from ase.io.aims import write_aims
except:
    pass
text = read_vasp(file="POSCAR")
write_vasp(file="POSCAR",atoms=text, direct=True)

text=[]
with open("POSCAR", "r") as file:
    text = file.readlines()
    count = 0
    line_to_locate = 0
    for line in text:
        if line.startswith("Direct"):
            line_to_locate = count
        count += 1


    line_to_locate = line_to_locate +1
    counter = line_to_locate

    for line in text[line_to_locate:]:
        text[counter]=line.replace("F","T")
        counter +=1
with open("POSCAR", "w+") as file:
    file.writelines(text)
