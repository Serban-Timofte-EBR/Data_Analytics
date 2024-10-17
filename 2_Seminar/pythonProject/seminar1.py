from functii import *

fisier = open("Educatie.csv")
# print(type(fisier))
linii = fisier.readlines()
# print(linii)
fisier.close()
# Citire antet
linia0 = linii[0][:-1].split(",")
# print(linia0)
nume_index = linia0[0]
variabile = linia0[1:]
variabile_numerice = variabile[2:]
# print(nume_index, variabile, variabile_numerice, sep="\n")
# Citire date
tabel = dict()
for i in range(1, len(linii)):
    linie_str = linii[i][:-1].split(",")
    linie = linie_str[1:3]
    for j in range(3, len(linie_str)):
        linie.append(float(linie_str[j]))
    tabel[linie_str[0]] = tuple(linie)
print(tabel)
# Cerinta 1
cerinta1 = {}
for v in tabel.keys():
    cerinta1[v] = (sum(tabel[v][2:6]), sum(tabel[v][6:]))
print("--> Cerinta 1")
print(cerinta1)
# Cerinta 2
cerinta2 = calcul_indicatori(tabel, variabile_numerice)
for v in cerinta2:
    print(v, cerinta2[v])
# Cerinta 3
print("--> Cerinta 3")
k = variabile_numerice.index("Abs_univ") + 2
for v in filter(lambda x: functie_filtru(x, k), tabel.values()):
    print(v)


def convert_temp(temperature, unit):
    if unit == 'C':
        fahrenheit = (temperature*9/5) +32
        return f"C {temperature}  is  F {fahrenheit} "
    elif unit  == 'F':
        celcius = (temperature-32) * 5/9
        return f"the F {temperature} is the following amount in celcius: {celcius}"
    else:
        return "Invalid unit. Please enter 'C' for Celsius or 'F' for Fahrenheit."

print("===========") 
print(convert_temp(24,'C'))
