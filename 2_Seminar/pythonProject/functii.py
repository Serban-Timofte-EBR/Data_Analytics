import csv
import math


def csv_to_dic(filename):
    dict = {}
    with open(filename, 'r') as csvFile:
        reader = csv.reader(csvFile)
        next(reader)
        for row in reader:
            siruta = int(row[0])
            localitate = row[1]
            judet = row[2]
            abs_liceal = float(row[3])
            abs_postlic = float(row[4])
            abs_primar_gimn = float(row[5])
            abs_profes = float(row[6])
            abs_tehnic = float(row[7])
            abs_univ = float(row[8])
            pop_liceal = float(row[9])
            pop_profess = float(row[10])
            pop_primar_gimn = float(row[11])
            pop_univ = float(row[12])

            # Stocăm datele într-un tuplu
            dict[siruta] = (localitate, judet, abs_liceal, abs_postlic, abs_primar_gimn, abs_profes,
                             abs_tehnic, abs_univ, pop_liceal, pop_profess, pop_primar_gimn, pop_univ)
    return dict


def calcul_indicatori(tabel_date, denumiri_variabile_numerice):
    """
    Calculează media, deviația standard și coeficientul de variație
    pentru variabilele specificate în tabel. Indicatori calculati pe coloane

    :param tabel_date: Dicționar cu datele (Siruta ca cheie).
    :param denumiri_variabile: Lista cu denumirile variabilelor numerice.
    :return: Un dicționar cu statistici pentru fiecare variabilă.
    """
    rezultate_statistici = {}

    try:
        assert isinstance(tabel_date, dict)

        for index_variabila in range(len(denumiri_variabile_numerice)):
            valori = []
            for siruta in tabel_date.keys():
                # Extragem valorile pentru variabila curentă
                valori.append(tabel_date[siruta][2 + index_variabila])

            # Calculăm media
            media_valori = sum(valori) / len(tabel_date)

            # Calculăm deviația standard
            suma_patrate_diferente = sum((val - media_valori) ** 2 for val in valori)
            deviatia_standard = math.sqrt(suma_patrate_diferente / len(tabel_date))

            # Calculăm coeficientul de variație
            coeficient_variatie = deviatia_standard / media_valori if media_valori != 0 else 0

            # Salvăm rezultatele în dicționar
            rezultate_statistici[denumiri_variabile_numerice[index_variabila]] = (
            media_valori, deviatia_standard, coeficient_variatie)

        return rezultate_statistici

    except AssertionError:
        return {}


def functie_filtru(t, k):
    if t[1][k] > 0:
        return True
    else:
        return False


def criteriu_sortare(t, k):
    # t[0] - Siruta
    # t[1] - tuplu de valori luate de variabile pentru localitatea cu Siruta t[0]
    return t[1][k]


def selector(t):
    return (t[0], t[1][8:])


def salvare(tabel, variabile, nume_instante="", nume_fisier="out.csv"):
    fisier = open(nume_fisier, mode="w")
    fisier.write(nume_instante + "," + ",".join(variabile) + "\n")
    for v in tabel:
        fisier.write(v + "," + ",".join([str(t) for t in tabel[v]])+"\n")
    fisier.close()
