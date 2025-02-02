import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler

df_industrie = pd.read_csv("data/Industrie.csv", index_col=0)
df_populatie = pd.read_csv("data/PopulatieLocalitati.csv", index_col=0)

# Să se salveze în fișierul Cerinta1.csv cifra de afaceri pe locuitor pentru fiecare activitate,
# la nivel de localitate. Pentru fiecare localitate se va salva codul Siruta, numele localității și
# cifra de afaceri pe locuitor pentru fiecare activitate.

df_merged = df_industrie.merge(
    df_populatie,
    left_index=True,
    right_index=True
).drop(columns=["Localitate_y"]).rename(columns={"Localitate_x": "Localitate"})
df_merged.to_csv("data/helpers/1_Merge.csv")

numeric_cols_1 = df_merged.columns[1:-2]
print("Numeric columns: ", numeric_cols_1)

cerinta1_rows = []
for index, row in df_merged.iterrows():
    rowPerCapita = row[numeric_cols_1] / row["Populatie"]
    cerinta1_rows.append({
        "Siruta": index,
        "Localitate": row["Localitate"],
        **rowPerCapita
    })
df_cerinta1 = pd.DataFrame(cerinta1_rows)
df_cerinta1.to_csv("data/results/Cerinta1.csv", index=False)

# Să se calculeze și să se salveze în fișierul Cerinta 2.csv activitatea industrială dominantă
# (cu cifra de afaceri cea mai mare) la nivel de județ

df_grouped = df_merged.groupby("Judet").sum().drop(columns=["Localitate"])
df_grouped.to_csv("data/helpers/2_Grouped.csv")

activitatiDominante = df_grouped.idxmax(axis=1)

cerinta2_rows = []
for judet, industrie in activitatiDominante.items():
    valoareaIndustrie = df_grouped.loc[judet, industrie]

    cerinta2_rows.append({
        "Judet": judet,
        "Activitate": industrie,
        "Valoare": valoareaIndustrie
    })
df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/results/Cerinta2.csv", index=False)

df_date34 = pd.read_csv("data/DataSet_34.csv", index_col=0)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data ...")
        for col in df.columns:
            if df[col].isna().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_date34_clean = cleanData(df_date34)
df_date34_clean.to_csv("data/helpers/3_Clean.csv")
numeric_cols = df_date34_clean.columns[0:]
print("Coloanele numerice: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_date34_clean[numeric_cols])
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_date34_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/helpers/4_Stand.csv")

set_productie = ["prodPorc", "prodVite", "prodOaieSiCapra", "prodPasareDeCurte"]
set_consum = ["consPorc", "consVita", "consumOaieSiCapra", "consPasareDeCurte"]

X = df_date_standardizate[set_productie]
Y = df_date_standardizate[set_consum]

X.to_csv("data/results/Xstd.csv")
Y.to_csv("data/results/Ystd.csv")

modelCCA = CCA()
X_C, Y_C = modelCCA.fit_transform(X, Y)

df_XC = pd.DataFrame(
    X_C,
    index=X.index,
    columns=["X_C1", "X_C2"]
)
df_XC.to_csv("data/results/Xscore.csv")

df_YC = pd.DataFrame(
    Y_C,
    index=Y.index,
    columns=["Y_C1", "Y_C2"]
)
df_YC.to_csv("data/results/Yscore.csv")

plt.figure()
plt.scatter(X_C[:, 0], X_C[:, 1], label="Productie")
plt.scatter(Y_C[:, 0], Y_C[:, 1], label="Consum")
plt.title("Radacinile canonice")
plt.show()

corr_X = np.corrcoef(X.T, X_C.T)[:X.shape[1], X.shape[1]:]
corr_Y = np.corrcoef(Y.T, Y_C.T)[:Y.shape[1], Y.shape[1]:]

df_corrX = pd.DataFrame(
    corr_X,
    index=set_productie,
    columns=["X_C1", "X_C2"]
)
df_corrX.to_csv("data/results/Rxz.csv")

df_corrY = pd.DataFrame(
    corr_Y,
    index=set_consum,
    columns=["Y_C1", "Y_C2"]
)
df_corrY.to_csv("data/results/Ryu.csv")

