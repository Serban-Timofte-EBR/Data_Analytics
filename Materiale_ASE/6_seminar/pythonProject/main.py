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
print("dict_localitati")
for key, value in dict_localitati.items():
    print(key, value)

dict_judete = csv_to_dict_judete(filename_judete)
print("dict_judete")
for key, value in dict_judete.items():
    print(key, value)

dict_regiuni = csv_to_dict_regiuni(filename_regiuni)
print("dict_regiuni")
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

# 2. Ponderi etnii
def procente_etnii_localitati(population):
    dict_localitati = {}
    for pop in population:
        total_pop = sum(pop[2:])
        localitate = pop[1]

        procente_etnii = []
        for i in range(len(pop[2:])):
            procente_etnii.append(round(pop[2+i] / total_pop, 2) * 100)

        dict_localitati[localitate] = procente_etnii

    return dict_localitati

def procente_etnii_judete(dict_judete):
    dict_procente_judete = {}
    for key in dict_judete.keys():
        values = dict_judete.get(key)
        # print(values)
        total_pop_jud = sum(values)
        etnii_procente = [round(value / total_pop_jud,2) * 100 for value in values]
        dict_procente_judete[key] = etnii_procente

    return dict_procente_judete

def procente_etnii_regiuni(dict_pop_regiuni):
    dict_procente_regiuni = {}
    for key in dict_pop_regiuni.keys():
        values = dict_pop_regiuni.get(key)
        total_pop = sum(values)
        regiuni_procente = [round(value / total_pop,2) * 100 for value in values]

        dict_procente_regiuni[key] = regiuni_procente

    return dict_procente_regiuni

etnii_localitati = procente_etnii_localitati(population)
print("Distributia localitati procentuala:")
for key, value in etnii_localitati.items():
    print(key, value)

etnii_judete = procente_etnii_judete(dict_pop_judete)
print("Distributia judete procentuala:")
for key, value in etnii_judete.items():
    print(key, value)

etnii_regiuni = procente_etnii_regiuni(dict_pop_regiuni)
print("Distributia regiuni procentuala:")
for key, value in etnii_regiuni.items():
    print(key, value)

# Indicele de disimilare
    # n = numarul de localitati
    # xi = populatie de o anumita etnie intr o localitate / judet
    # Tx = totalul populatiei de respectiva etnie
    # ri = restul populatiei dintr-o localitate / judet
    # Tr = restul populatiei totale

def calcul_populatie_totala(population):
    total_pop = 0
    for pop in population:
        total_pop += sum(pop[2:])
    return total_pop

def calcul_populatie_etnie(population, index):
    total = 0
    for pop in population:
        total += pop[index]
    return total

def calcul_populatie_etnie_judet(dict_pop_judet, index_etnie_pop, judet):
    return dict_pop_judet[judet][index_etnie_pop]

# print("Total population: " + str(calcul_populatie_totala(population)))
# print("Total pop etnie 2 " + str(calcul_populatie_etnie(population, 3)))

def calcul_indice_disimilare_judete(population, dict_pop_judet):
    dict_indice_disimilare = {}

    total_populatie = calcul_populatie_totala(population)

    # Parcurgem fiecare județ
    for judet, values_etnii in dict_pop_judet.items():
        vector_indici = []  # Indicii pentru fiecare etnie

        for etnie_index in range(len(values_etnii)):  # Iterăm pe fiecare etnie
            xi = values_etnii[etnie_index]  # Populația etniei curente în județ
            tx = calcul_populatie_etnie(population, etnie_index + 2)  # Total populație etnie
            ri = sum(values_etnii) - xi  # Restul populației (în județ)
            tr = total_populatie - tx  # Totalul restului populației (în țară)

            # Calculăm indicele de disimilare pentru această etnie
            suma_disimilare = 0
            for pop in population:
                if dict_localitati.get(pop[0])[1] == judet:  # Localitate din județul curent
                    x_local = pop[2 + etnie_index]  # Populația etniei curente în localitate
                    r_local = sum(pop[2:]) - x_local  # Restul populației în localitate
                    if tx > 0 and tr > 0:  # Evităm divizarea la zero
                        suma_disimilare += abs((x_local / tx) - (r_local / tr))

            D = 0.5 * suma_disimilare
            vector_indici.append(D)

        # Adăugăm vectorul de indici pentru județul curent
        dict_indice_disimilare[judet] = vector_indici

    return dict_indice_disimilare

# dict_indici_disimilare = calcul_indice_disimilare_judete(population, dict_pop_judet)
#
# print("Indicii de disimilare pe județe:")
# for judet, indici in dict_indici_disimilare.items():
#     print(f"Județ: {judet}, Indicii: {indici}")



