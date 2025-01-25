import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import confusion_matrix, accuracy_score

df_buget = pd.read_csv("data/Buget.csv", index_col=0)
df_populatie_localitati = pd.read_csv("data/PopulatieLocalitati.csv", index_col=0)

print("Dataframe-uri din csv:")
print(df_buget.head())
print(df_populatie_localitati.head())

# A
# Cerinta 1 - Total venituri si total cheltuieli la nivel de localitate

etichete_venituri = ["V" + str(i+1) for i in range(5)]
etichete_cheltuieli = ["C" + str(i+1) for i in range(8)]
cerinta1_rows = []
for index, row in df_buget.iterrows():
    total_venituri = row[etichete_venituri].sum()
    total_cheltuieli = row[etichete_cheltuieli].sum()

    cerinta1_rows.append({
        "Siruta": index,
        "Localitate": row["Localitate"],
        "Venituri": total_venituri,
        "Cheltuieli": total_cheltuieli
    })

df_cerinta1 = pd.DataFrame(
    cerinta1_rows,
    index=df_buget.index
)
df_cerinta1.to_csv("data/cerinta1.csv")

# Cerinta 2 - Veniturile per cap de locuitor pe judet sortate dupa V1 descrescator
df_merged = df_buget.merge(
    df_populatie_localitati,
    left_index=True,
    right_index=True
).drop(columns=["Localitate_y"])
df_merged.to_csv("data/helpers/1_DataframMerged.csv")

df_judete = df_merged.groupby("Judet").sum().drop(columns=["Localitate_x"])
df_judete.to_csv("data/helpers/2_DataframeJudete.csv")

cerinta2_rows = []
for index, row in df_judete.iterrows():
    row_venituri_per_locuitor = row[etichete_venituri] / row["Populatie"]

    cerinta2_rows.append({
        **row_venituri_per_locuitor
    })

df_cerinta2 = pd.DataFrame(
    cerinta2_rows,
    index=df_judete.index
).sort_values(by="V1", ascending=False)
df_cerinta2.to_csv("data/cerinta2.csv")

# B
# Analiza discriminanta

df_pacienti = pd.read_csv("data/Pacienti.csv")
df_apply = pd.read_csv("data/Pacienti_apply.csv")

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

df_pacienti_cleaned = cleanData(df_pacienti)
df_apply_cleaned = cleanData(df_apply)

# Separam variabila dependenta de cele independete
X = df_pacienti_cleaned.drop(columns=["DECISION"])
Y = df_pacienti_cleaned["DECISION"]

# Impartim in date de test si de antrenament
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

# Crearea si antrenarea modelului
lda = LDA()
lda.fit(X_train, Y_train)

# Predictia pentru modelul LDA
Y_pred = lda.predict(X_test)
df_predict = pd.DataFrame({
    "Real": Y_test,
    "Predicted": Y_pred
})
df_predict.to_csv("data/predict.csv")

# Evaluarea performantei modelului

# Matricea de confuzie
conf_matrix = confusion_matrix(Y_test, Y_pred)
print("Matricea de confuzie:")
print(conf_matrix)

# Acuratetea globala
global_accuracy = accuracy_score(Y_test, Y_pred)
print("Acuratetea globala: ", global_accuracy)

# Acuratetea medie
accuracy_per_class = conf_matrix.diagonal() / conf_matrix.sum(axis=1)
accuracy_mean = np.mean(accuracy_per_class)
print("Acuratetea medie: ", accuracy_mean)

# Graficul distributiei

# Transformam datele
X_train_lda = lda.transform(X_train)
X_test_lda = lda.transform(X_test)

num_axes = X_train_lda.shape[1]

if num_axes < 2:
    print("Numărul de axe discriminante este mai mic decât 2. Graficul nu poate fi generat.")
else:
    plt.figure(figsize=(10, 6))
    for label, marker, color in zip(np.unique(Y_train), ('o', 'x', 's'), ('blue', 'red', 'green')):
        label_indices = np.where(Y_train == label)[0]
        plt.scatter(
            X_train_lda[label_indices, 0],
            X_train_lda[label_indices, 1],
            label=f"Clasa {label}",
            marker=marker,
            color=color
        )

    plt.title("Distribuțiile pe axele discriminante")
    plt.xlabel("Axa discriminantă 1")
    plt.ylabel("Axa discriminantă 2")
    plt.legend(title="Clase")
    plt.grid()
    plt.tight_layout()
    plt.show()