import pandas as pd
from pandas.core.dtypes.common import is_numeric_dtype


def clean_dataframe(df):
    assert isinstance(df, pd.DataFrame)
    # Iteram prin coloanele dataframe-ului
    for col in df.columns:
        # Verificam daca exista valori lipsa in dataframe
        if df[col].isna().any():
            # Verificam daca coloana este de tip numeric
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
    return df

# Citim din csv
dfMortalitate = pd.read_csv("data_2/mortalitate_ro.csv")
print("Dataframe mortalitate")
print(dfMortalitate.head())

# Verificam daca avem valori lipsa
    # isna - returneaza un df de aceeasi dimensiune doar cu True si False (True unde are valori lipsa)
    # primul any() - ia fiecare coloana si verifica daca pe coloana sunt valori lipsa
    # al doilea any() - se aplica pe array ul rezultat pentru a verifica daca avem True din coloane
valoriLipsa = dfMortalitate.isna().any().any()
if valoriLipsa == True:
    print("\tTrebuie sa curatam datele -> inlocuim valorile lipsa cu media")
    dfMortalitate_Clean = clean_dataframe(dfMortalitate);

    print("Dataframe mortalitate - curatat")
    print(dfMortalitate_Clean.head())

    valoriLipsaCuratate = dfMortalitate.isna().any().any()
    print("Valori lipsa in dataframe mortalitate curatat: " + str(valoriLipsaCuratate))

