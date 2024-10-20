import functii
from functii import *
from seminar2 import filename

filename = "Educatie.csv"
## Citire date din csv si salvare intr-un tabel (dictionar)
tabel = functii.csv_to_dic(filename)
print("Tabelul din CSV:")
print(tabel)

fisier2 = open("Educatie.csv")
linii = fisier2.readlines()
fisier2.close()

# Cerinta 1
cerinta1 = {}
for v in tabel.keys():
    cerinta1[v] = (sum(tabel[v][2:6]), sum(tabel[v][6:]))
print("--> Cerinta 1")
print(cerinta1)

# Cerinta 1.2

linia0 = linii[0].strip().split(",")
print("Linia 0:")
print(linia0)
nume_index = linia0[0]
variabile = linia0[1:]
variabile_numerice = variabile[2:]
# print("Pregatire cerinta 2:")
# print(nume_index, variabile, variabile_numerice, sep="\n")

# Cerinta 2
print("--> Valori numerice:")
print(variabile_numerice)

cerinta2 = calcul_indicatori(tabel, variabile_numerice)
print("--> Cerinta 2:")
for v in cerinta2:
    print(v, cerinta2[v])

# # Cerinta 3
# print("--> Cerinta 3")
# k = variabile_numerice.index("Abs_univ") + 2
# for v in filter(lambda x: functie_filtru(x, k), tabel.values()):
#     print(v)
#
#
# def convert_temp(temperature, unit):
#     if unit == 'C':
#         fahrenheit = (temperature*9/5) +32
#         return f"C {temperature}  is  F {fahrenheit} "
#     elif unit  == 'F':
#         celcius = (temperature-32) * 5/9
#         return f"the F {temperature} is the following amount in celcius: {celcius}"
#     else:
#         return "Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit."
#
# print("===========")
# print(convert_temp(24,'C'))
