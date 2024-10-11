from array import *

x_int = array('i', [1, 2, 3, 4])
x_str = array('u', "Roșu")
x_b = array('b')
print(x_int, x_str, x_b, sep="\n")
x_int.extend([2, 3, 4, 5])
print(x_int)
x_str.extend(" Galben")
print(x_str)
x_str.fromunicode(" Albastru")
print(x_str)

fisier = open("swap.dat", "bw")
x_int.tofile(fisier)
fisier.close()
fisier = open("swap.dat", "br")
x_int.fromfile(fisier, 3) #Elementele citite se adauga la x_int
fisier.close()
print("x_int (restaurat):", x_int)
