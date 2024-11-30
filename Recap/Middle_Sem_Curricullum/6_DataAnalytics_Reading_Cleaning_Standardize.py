import pandas as pd
import numpy as np

#   1.	Citirea fișierelor CSV și analiza inițială a datelor
# 	    •	Citește fișierele vanzari.csv și produse.csv.
# 	    •	Afișează primele 5 rânduri din fiecare fișier.
# 	    •	Verifică dacă există valori lipsă și afișează numărul acestora pentru fiecare coloană.
# 	2.	Îmbinarea datelor (join)
# 	    •	Realizează un merge între cele două DataFrame-uri folosind coloana comună ID_Produs.
# 	    •	Afișează structura tabelului rezultat după merge si salveaza-l întru-un fișier csv
# 	3.	Curățarea datelor
# 	    •	Completează valorile lipsă:
# 	    •	Pentru coloanele numerice, completează cu media lor.
# 	    •	Pentru coloanele categorice, completează cu cel mai frecvent element (modulul).
# 	4.	Standardizarea datelor
# 	    •	Identifică toate coloanele numerice din DataFrame-ul final.
# 	    •	Standardizează fiecare coloană numerică astfel încât să aibă media 0 și abaterea standard 1.
# 	5.	Analiza corelației
# 	    •	Calculează matricea de corelație între variabilele numerice.
# 	    •	Creează un heatmap pentru a vizualiza corelațiile.
# 	6.	Vizualizarea distribuției
# 	    •	Creează un grafic de distribuție (histogramă) pentru coloana Profit.

# 1. Citire din csv
vanzari = pd.read_csv("data/input/vanzari.csv", index_col=0)
produse = pd.read_csv("data/input/produse.csv", index_col=0)

# 2. Imbinarea csv-urilor
database = vanzari.merge(
    produse,
    left_index=True,
    right_index=True
)

print("Baza de date cu produse:")
print(database.head())

# Scrierea rezultatului in csv
database.to_csv("data/output/database.csv")

# Curatarea datelor
def cleanData(df):
    assert isinstance(df, pd.DataFrame)
    for col in df.columns:
        if df[col].isna().any():
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
    return df

valoriLipsa = database.isna().any().any()
if valoriLipsa:
    print("\n\t -> Avem valori lipsa! Curatam baza de date")
    cleanDatabase = cleanData(database)
    valoriLipsa = cleanDatabase.isna().any().any()
    if valoriLipsa == False:
        cleanDatabase.to_csv("data/output/cleanDatabase.csv")
        print("Datele au fost curatate!")

# Standardizarea datelor
def standardizeData(df, numericCols):
    assert isinstance(df, pd.DataFrame)
    for col in numericCols:
        mean = df[col].mean()
        std = df[col].std()
        df[col] = (df[col] - mean) / std
    return df

numericCols = ["Vanzari", "Profit", "Pret"]
standardizeDatabase = standardizeData(database, numericCols)
standardizeDatabase.to_csv("data/output/standardizeDatabase.csv")

standardizeDatabase = standardizeDatabase.drop(columns=["ID_Produs", "Categorie", "Nume_Produs"])
print("Standardize data:")
print(standardizeDatabase.head())