from clase import c
from clase1 import c as c_

ob_c1 = c(100) #Este invocat indirect constructorul clasei a
ob_c1.print_c()
print("---->")
ob_c2 = c_(100) #Este invocat indirect constructorul clasei a
ob_c2.print_c()

ob_c1.print()
