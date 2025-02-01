import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

import pandas as pd
import seaborn as sb

from sklearn.preprocessing import StandardScaler
from factor_analyzer import FactorAnalyzer, calculate_bartlett_sphericity, calculate_kmo
import matplotlib.pyplot as plt

# 1. Citim datele
df_vot = pd.read_csv("data/VotBUN.csv", index_col=0)
df_coduri = pd.read_csv("data/Coduri_Localitati.csv", index_col=0)

print("Datele din csv:")
print("Vot:")
print(df_vot)

print("Coduri:")
print(df_coduri)

# 2. Curatam datele
def cleanData(df):
    isinstance(df, pd.DataFrame)
    print("Cleaning data for a df")
    if df.isna().any().any():
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_vot = cleanData(df_vot)
df_coduri = cleanData(df_coduri)

df_vot.to_csv("data/intermediate/Vot.csv")
df_coduri.to_csv("data/intermediate/Coduri.csv")

# 3. Pastram doar datele numerice
lista_coloane_numerice = df_vot.columns[1:]
print("Coloanele numerice:")
print(lista_coloane_numerice)

df_date_numerice = df_vot[lista_coloane_numerice]
print("Datele numerice:")
print(df_date_numerice)

# 4. Standardizare
scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_date_numerice)
print("Datele standardizate:")
print(date_standardizate)

df_date_standardizate = pd.DataFrame(
    data=date_standardizate,
    index=df_vot.index,
    columns=lista_coloane_numerice
)
print("Dataframe date numerice:")
print(df_date_standardizate)
df_date_standardizate.to_csv("data/intermediate/DateStandardizate.csv")

# 5. Modelul Factorial
nr_variabile = len(df_date_standardizate.columns)
modelAf = FactorAnalyzer(n_factors=nr_variabile, rotation=None) # rotation='varimax' daca vrem cu rotatie
F = modelAf.fit(df_date_standardizate)

# 6. Scorurile factoriale
scoruri = modelAf.transform(df_date_standardizate)

etichete = ['F' + str(i + 1) for i in range(nr_variabile)]
df_scoruri = pd.DataFrame(
    data = scoruri,
    index = df_date_standardizate.index,
    columns = etichete
)
print("Dataframe scoruri:")
print(df_scoruri)

# + Vizualizarea scorurilor
plt.figure("Plot scoruri")
plt.scatter(df_scoruri['F1'], df_scoruri['F2'])
plt.xlabel('F1')
plt.ylabel('F2')
plt.title("Plot scoruri")
plt.show()

# 7. Teste
    # Bartlett
bartlet_test = calculate_bartlett_sphericity(df_date_standardizate)
print("Bartlet Test: ", bartlet_test[1])

    # KMO
kmo_test = calculate_kmo(df_date_standardizate)
print("KMO Test: ", kmo_test[1])

# •	P-Value < 0.05: Matricea de corelație este potrivită pentru analiza factorială.
# •	P-Value ≥ 0.05: Matricea de corelație poate să nu fie potrivită pentru analiza factorială.

# 8. Variante
variance = modelAf.get_factor_variance()[0]
print("Varianta: ", variance)

# 9. Corelatii factoriale
corelatii = modelAf.loadings_
print("Corelatii: ", corelatii)
df_corelatii = pd.DataFrame(
    data = corelatii,
    index = df_date_numerice.columns,
    columns=etichete
)
print("Dataframe corelatii:")
print(df_corelatii)

plt.figure("Heatmap Corelatii")
sb.heatmap(df_corelatii)
plt.title("Corelograma Factoriala")
plt.show()

# 10. Comunalități
comunalitati = modelAf.get_communalities()
df_comunalitati = pd.DataFrame(
    data=comunalitati,
    index=df_date_numerice.columns,
    columns=['Comunalitati']
)
print("Dataframe comunalitati:")
print(df_comunalitati)

plt.figure("Corelograma Comunalitati", figsize=(9, 9))
sb.heatmap(data=df_comunalitati, vmin=0, annot=True, cmap="coolwarm")
plt.title("Corelograma Comunalitati")
plt.show()