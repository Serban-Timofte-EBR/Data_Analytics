import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, average_precision_score, accuracy_score
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler, LabelEncoder

df_industrie = pd.read_csv("data/Industrie.csv", index_col=0)
df_populatie = pd.read_csv("data/PopulatieLocalitati.csv", index_col=0)

# A
# Cerinta 1
numeric_cols = df_industrie.columns[1:]
print("Coloane numerice: ", numeric_cols)

df_merged = df_industrie.merge(
    df_populatie,
    left_index=True,
    right_index=True
).drop(columns=["Localitate_y"])
df_merged.to_csv("data/helpers/1_Merge.csv")

cerinta1_rows = []
for index, row in df_merged.iterrows():
    rowPerCapita = row[numeric_cols] / row["Populatie"]

    cerinta1_rows.append({
        "Siruta": index,
        "Localitate": row["Localitate_x"],
        **rowPerCapita
    })

df_cerinta1 = pd.DataFrame(cerinta1_rows)
df_cerinta1.to_csv("data/results/Cerinta1.csv", index=False)

# Cerinta 2
df_judete = df_merged.groupby("Judet").sum().drop(columns=["Localitate_x", "Populatie"])
df_judete.to_csv("data/helpers/2_Judete.csv")

cerinta2_rows=[]
for index, row in df_judete.iterrows():
    industrieDominanta = row.idxmax()
    cifraAfaceri = row[industrieDominanta]

    cerinta2_rows.append({
        "Judet": index,
        "Activitate": industrieDominanta,
        "Cifra Afaceri": cifraAfaceri
    })

df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/results/Cerinta2.csv", index=False)

# B - analiza discriminanta

df_proiecte = pd.read_csv("data/ProiectB.csv")
df_apply = pd.read_csv("data/ProiectB_apply.csv")

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

df_proiecte_clean = cleanData(df_proiecte)
df_apply_clean = cleanData(df_apply)

variabile_independete = df_proiecte_clean.columns[1:-1]
print("Variabile independente: ", variabile_independete)

X = df_proiecte_clean[variabile_independete]
Y = df_proiecte_clean["VULNERAB"]
X_apply = df_apply_clean[variabile_independete]

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

modelADL = LinearDiscriminantAnalysis()
modelADL.fit(X_train, Y_train)

# Scorurile discriminante
X_train_lda = modelADL.transform(X_train)
X_test_lda = modelADL.transform(X_test)

df_train_lda = pd.DataFrame(
    X_train_lda,
    index=X_train.index,
    columns=["Z" + str(i+1) for i in range(X_train_lda.shape[1])]
)
df_train_lda.to_csv("data/results/z.csv", index=False)

# Evaluarea modelului
Y_pred = modelADL.predict(X_test)
conf_matrix = confusion_matrix(Y_test, Y_pred)
print("Matricea de confuzie: ", conf_matrix)

accuracy = accuracy_score(Y_test, Y_pred)
print("Accuracy: ", accuracy)

accuracy_per_class = conf_matrix.diagonal() / conf_matrix.sum(axis=1)
accuraccy_mean = np.mean(accuracy_per_class)
print("Accuracy mean: ", accuraccy_mean)

# Predictii
Y_pred_apply = modelADL.predict(X_apply)
df_apply_clean["VULNERAB"] = Y_pred_apply
print(df_apply_clean.head())

Y_pred_test = modelADL.predict(X_test)
df_X_test = pd.DataFrame(X_test)
df_X_test["VULNERAB"] = Y_pred_test
print(df_X_test.head())