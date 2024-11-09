import csv
from fileinput import filename
from os import readv

filename_ethnicity = "Ethnicity.csv"
filename_localitati = "Coduri_Localitati.csv"
filename_judete = "Coduri_Judete.csv"
filename_regiuni = "Coduri_Regiuni.csv"

def csv_to_array(filename):
    population = []
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            code = int(row[0])
            city = row[1]
            romanian = int(row[2])
            hungarians = int(row[3])
            romany = int(row[4])
            ukrainians = int(row[5])
            germans = int(row[6])
            turks = int(row[7])
            russians_lippovans = int(row[8])
            tatars = int(row[9])
            serbs = int(row[10])
            slovaks = int(row[11])
            bulgarinas = int(row[12])
            croats = int(row[13])
            greeks = int(row[14])
            italians = int(row[15])
            jews = int(row[16])
            czechs = int(row[17])
            poles = int(row[18])
            chinese = int(row[19])
            armenians = int(row[20])
            csango = int(row[21])
            macedonians = int(row[22])
            another = int(row[23])

            array_code = []
            array_code.append(code)
            array_code.append(city)
            array_code.append(romanian)
            array_code.append(hungarians)
            array_code.append(romany)
            array_code.append(ukrainians)
            array_code.append(germans)
            array_code.append(turks)
            array_code.append(russians_lippovans)
            array_code.append(tatars)
            array_code.append(serbs)
            array_code.append(slovaks)
            array_code.append(bulgarinas)
            array_code.append(croats)
            array_code.append(greeks)
            array_code.append(italians)
            array_code.append(jews)
            array_code.append(czechs)
            array_code.append(poles)
            array_code.count(chinese)
            array_code.append(armenians)
            array_code.append(csango)
            array_code.append(macedonians)
            array_code.append(another)

            population.append(array_code)
    return population

# Code,City,County
# 1017,Municipiul Alba Iulia,ab
def csv_to_dict_localitati(filename):
    dict = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            code = int(row[0])
            city = row[1]
            county = row[2]

            values = [city, county]
            dict[code] = values

    return dict

# IndicativJudet,NumeJudet,Regiune
# ab,Alba,Centru
def csv_to_dict_judete(filename):
    dict = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row  in reader:
            indicativ = row[0]
            name = row[1]
            region = row[2]

            values = [name, region]
            dict[indicativ] = values

    return dict

# Regiune,MacroRegiune
# Centru,1
def csv_to_dict_regiuni(filename):
    dict = {}
    with open(filename, 'r') as file:
        reader = csv.reader(file)
        next(reader)
        for row in reader:
            regiune = row[0]
            macro_regiuni = int(row[1])

            dict[regiune] = macro_regiuni

    return dict

# 0. Citirea datelor din csv
population = csv_to_array(filename_ethnicity)
for line in population:
    print(line)

dict_localitati = csv_to_dict_localitati(filename_localitati)
for key, value in dict_localitati.items():
    print(key, value)

dict_judete = csv_to_dict_judete(filename_judete)
for key, value in dict_judete.items():
    print(key, value)

dict_regiuni = csv_to_dict_regiuni(filename_regiuni)
for key, value in dict_regiuni.items():
    print(key, value)

# Etnii pe judete
def etnii_judete(population, dict_localitati):
    dict_medii = {}
    for pop in population:
        cod_judet = dict_localitati.get(pop[0])[1]

        vector_etnii_pop = pop[2:]

        if cod_judet in dict_medii.keys():
            for i in range(len(vector_etnii_pop)):
                dict_medii[cod_judet][i] += vector_etnii_pop[i]
        else:
            dict_medii[cod_judet] = vector_etnii_pop

    return dict_medii

def etnii_regiuni(population, dict_localitati, dict_judete):
    dict_regiuni = {}
    for pop in population:
        cod_localitate = pop[0]
        cod_judet = dict_localitati.get(cod_localitate)[1]
        regiune = dict_judete.get(cod_judet)[1]

        vector_etnii_pop = pop[2:]

        if regiune in dict_regiuni.keys():
            for i in range(len(vector_etnii_pop)):
                dict_regiuni[regiune][i] += vector_etnii_pop[i]
        else:
            dict_regiuni[regiune] = vector_etnii_pop

    return dict_regiuni

def etnii_macroregiuni(population, dict_localitati, dict_judete, dict_regiuni):
    dict_macroregiuni = {}
    for pop in population:
        cod_localitate = pop[0]
        cod_judet = dict_localitati.get(cod_localitate)[1]
        cod_regiune = dict_judete.get(cod_judet)[1]
        macroregiune = dict_regiuni.get(cod_regiune)

        vector_etnii_pop = pop[2:]

        if macroregiune in dict_macroregiuni.keys():
            for i in range(len(vector_etnii_pop)):
                dict_macroregiuni[macroregiune][i] += vector_etnii_pop[i]
        else:
            dict_macroregiuni[macroregiune] = vector_etnii_pop

    return dict_macroregiuni

dict_pop_judete = etnii_judete(population, dict_localitati)
print("Distributia etniilor pe judete:")
for key, value in dict_pop_judete.items():
    print(key, value)

print("\nDistributia regiuni:")
dict_pop_regiuni = etnii_regiuni(population, dict_localitati, dict_judete)
for key, value in dict_pop_regiuni.items():
    print(key, value)

print("\nDistributia macroregiuni:")
dict_pop_macroregiune = etnii_macroregiuni(population, dict_localitati, dict_judete, dict_regiuni)
for key, value in dict_pop_macroregiune.items():
    print(key, value)
