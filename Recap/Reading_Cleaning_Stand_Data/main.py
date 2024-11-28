import numpy as np
import pandas as pd

# Pasul 1. Citirea din CSV
    # index_col = 0 -> folosim pentru ca prima coloana din fiecare CSV este un index, o cheie primara care ne va ajuta sa identificam o linie din csv-ul nostru
    # Acest index ne va ajuta sa facem acele join-uri intre csv-uri (intre tabelel bazei noastre de date)
coduri_localitati = pd.read_csv('data/coduri_localitati.csv', index_col=0)
coduri_judete = pd.read_csv('data/coduri_judete.csv', index_col=0)
coduri_regiuni = pd.read_csv('data/coduri_regiuni.csv', index_col=0)
ethnicity = pd.read_csv('data/ethnicity.csv', index_col=0)

# Pasul 2. Afisarea primelor randuri pentru verificare pentru a intelege structurile
    # Legătura dintre tabele:
    # 	•	Coduri din ethnicity ar trebui să apară și în coduri_localitati.
    # 	•	County din coduri_localitati ar trebui să apară în coduri_judete.
    # 	•	Regiune din coduri_judete ar trebui să apară în coduri_regiuni.
print("HEAD OF Ethnicity:")
print(ethnicity.head())
print("\nHEAD OF Coduri Localitati:")
print(coduri_localitati.head())
print("\nHEAD OF Coduri Judete:")
print(coduri_judete.head())
print("\nHEAD OF Coduri Regiuni.")
print(coduri_regiuni.head())

# Pasul 3. Merge intre csv = Join intre tabele

# Join intre ethnicity si coduri_localitati
ethnicity_localitati = ethnicity.merge(
    coduri_localitati,  # Tabelul cu localitati
    left_index=True,    # Pentru join folosim indexul din stanga = Indexul din ethnicity
    right_index=True,    # Pentru join folosim indexul din dreapte = Indexul din localitati
    # In acest moment vom avea 2 coloane identice: City_x si City_y pentru ca vom aveam orasul din ethnicity si cel din localitati.
)

# Stergem o coloana pentru a ne fi mai usor
ethnicity_localitati = ethnicity_localitati.drop(columns=["City_y"])

print("\nETHNICITY LOCALITATI:")
print(ethnicity_localitati.head())

# Join intre ethnicity si judete
ethnicity_judete = ethnicity_localitati.merge(
    coduri_judete,
    left_on="County",
    right_index=True
)

print("\nETHNICITY Judete:")
print(ethnicity_judete.head())

# Join intre ethnicity si regiuni
ethnicity_regiuni = ethnicity_judete.merge(
    coduri_regiuni,
    left_on="Regiune",
    right_index=True
)

print("\nETHNICITY REGIUNI:")
print(ethnicity_regiuni.head())

# Cerința 1: Să se calculeze și să se salveze populația pe etnii la nivelul județelor, regiunilor și macroregiunilor.

# Populatia pe etnii pentru fiecare judet

    # Agregam datele pe judet. Folosim ethnicity_localitati

populatie_judete = ethnicity_localitati.groupby("County").sum()
populatie_judete = populatie_judete.drop(columns=["City_x"])

populatie_judete_clean_data = populatie_judete.merge(
    coduri_judete,
    left_on="County",
    right_index=True
)
populatie_judete_clean_data.to_csv('data/outputs/Etnii_per_Judet.csv')

    # Agregam datele pe regiune
populatie_regiune = ethnicity_judete.groupby("Regiune").sum()
populatie_regiune = populatie_regiune.drop(columns=["City_x", "County", "NumeJudet"])
populatie_regiune.to_csv('data/outputs/Etnii_per_Regiune.csv')

    #Agregam datele pe macroregiuni
populatie_macroregiuni = ethnicity_regiuni.groupby("MacroRegiune").sum()
populatie_macroregiuni = populatie_macroregiuni.drop(columns=["City_x", "County", "NumeJudet", "Regiune"])
populatie_macroregiuni.to_csv('data/outputs/Etnii_per_MacroRegiune.csv')

# Cerinta 2: Calcularea și salvarea procentelor pe etnii la nivelul:
#   Localităților,
#   Județelor,
#   Regiunilor,
#   Macroregiunilor.

# def calculate_percentage(df):
#     total_pop = df.sum(axis=1)
#
#     percentages = df.div(total_pop, axis=0) * 100
#
#     return percentages
#
# procente_etnii_localitati = calculate_percentage(ethnicity_localitati)
# procente_etnii_localitati.to_csv('data/outputs/Procente_Etnii_per_Localitati.csv')