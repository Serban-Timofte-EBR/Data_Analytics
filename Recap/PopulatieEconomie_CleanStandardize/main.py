import pandas as pd
from DataPreparationModule import cleanData, standardizeData

# Fișiere CSV utilizate:
#
# 	1.	populatie.csv: Conține date demografice despre populația din diverse județe.
# 	    •	Coloane: Cod_Judet, Populatie_Totala, Urban, Rural.
# 	2.	economia.csv: Conține informații economice pentru județe.
# 	    •	Coloane: Cod_Judet, PIB, Somaj.
# 	3.	judete.csv: Conține denumirea județelor și regiunea din care fac parte.
# 	    •	Coloane: Cod_Judet, Nume_Judet, Regiune.

# Cerințe:
#
# 	1.	Citește toate fișierele CSV și afișează primele 5 rânduri pentru verificare.
# 	2.	Realizează merge-uri între tabele:
# 	    •	Îmbină populatie.csv cu economia.csv pe baza coloanei comune Cod_Judet.
# 	    •	Îmbină rezultatul cu judete.csv pentru a adăuga denumirea și regiunea fiecărui județ.
# 	3.	Verifică dacă există valori lipsă în DataFrame-ul rezultat.
# 	    •	Completează valorile lipsă:
# 	    •	Cu media pentru coloanele numerice.
# 	    •	Cu modulul pentru coloanele categorice.
# 	4.	Standardizează toate coloanele numerice din DataFrame final.

populatie = pd.read_csv('data/input/populatie.csv', index_col=0)
economie = pd.read_csv('data/input/economia.csv', index_col=0)
judete = pd.read_csv('data/input/judete.csv', index_col=0)

print("POPULATIE:")
print(populatie.head())

print("\nECONOMIE:")
print(economie.head())

print("\nJUDETE:")
print(judete.head())

populatie_economie = populatie.merge(
    economie,
    left_index=True,
    right_index=True
)
print("\n POPULATIE + ECONOMIE:")
print(populatie_economie.head())

populatie_economie_judete = populatie_economie.merge(
    judete,
    left_on="Cod_Judet",
    right_index=True
)
print("\n POPULATIE + ECONOMIE + JUDETE:")
print(populatie_economie_judete.head())

numCols = ["Populatie_Totala", "Urban", "Rural" , "PIB", "Somaj"]
valoriLipsa = populatie_economie_judete.isna().any().any()
if valoriLipsa:
    print("\tAvem valori lipsa. Curatam datele")
    cleanDF = cleanData(populatie_economie_judete)

print("\nFinal DataFrame:")
print(cleanDF.head())
cleanDF.to_csv('data/output/cleanData.csv')
valoriLipsa = populatie_economie_judete.isna().any().any()
print("Valori lipsa: " + str(valoriLipsa))

standardizeDataFrame = standardizeData(cleanDF, numCols);
print("\nStandardized DataFrame:")
print(standardizeDataFrame.head())