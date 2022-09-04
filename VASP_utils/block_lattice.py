#! /usr/bin/python3
# This script change a POSCAR file that all their atoms can move ( T   T   T) to a POSCAR where the lattice is blocked 
#   and the rsurface molecules are free to move
text=[]

# From this line forward all atom remains free to move
latt = 27
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

    for line in text[line_to_locate:line_to_locate+latt]:
        text[counter]=line.replace("T","F")
        counter +=1
with open("POSCAR", "w+") as file:
    file.writelines(text)
