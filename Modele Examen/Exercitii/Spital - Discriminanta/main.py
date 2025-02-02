import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df_pacienti = pd.read_csv("data/Patients_Training.csv", index_col=0)

# Cerinta 1 - Statistica descriptiva
numeric_cols = df_pacienti.columns[0:-1]
print("Numeric cols: ", numeric_cols)

cerinta1_rows = []

for col in numeric_cols:
    mean = round(df_pacienti[col].mean(), 1)
    median = round(df_pacienti[col].median(), 1)
    stdDev = round(df_pacienti[col].std(), 1)

    cerinta1_rows.append({
        "Variable": col,
        "Mean": mean,
        "Median": median,
        "StdDev": stdDev
    })
df_cerinta1 = pd.DataFrame(cerinta1_rows)
df_cerinta1.to_csv("data/results/Statistics.csv", index=False)

# Cerinta 2 - Statistica descriptiva pe departamente
df_pacienti["Counter"]=1

df_grouped = df_pacienti.groupby("DEPARTMENT").sum()
df_grouped.to_csv("data/helpers/1_Grouped.csv")

cerinta2_rows=[]
for index, row in df_grouped.iterrows():
    rowDescriptive = round(row[numeric_cols] / row["Counter"],2)

    cerinta2_rows.append({
        "DEPARTMENT": index,
        **rowDescriptive
    })
df_cerinta2 = pd.DataFrame(cerinta2_rows)
df_cerinta2.to_csv("data/results/Grouped_Means.csv", index=False)

# B - Analiza discriminanta

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

df_pacienti_2 = pd.read_csv("data/Patients_Training.csv", index_col=0)
df_apply = pd.read_csv("data/Patients_Training.csv", index_col=0)

df_pacienti_clean = cleanData(df_pacienti_2)
df_apply_clean = cleanData(df_apply)

X = df_pacienti_clean[numeric_cols]
Y = df_pacienti_clean["DEPARTMENT"]
X_apply = df_apply_clean[numeric_cols]

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_apply = scaler.fit_transform(X_apply)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

modelADL = LinearDiscriminantAnalysis()
modelADL.fit(X_train, Y_train)

# Scorurile discriminante
X_train_lda = modelADL.transform(X_train)
X_test_lda = modelADL.transform(X_test)

df_train_lda = pd.DataFrame(
    X_train_lda,
    # index=X_train.index,
    columns=["Z" + str(i+1) for i in range(X_train_lda.shape[1])]
)
df_train_lda.to_csv("data/results/ScoruriDiscriminante.csv")

# Evaluare model
Y_pred = modelADL.predict(X_test)
matrice_confuzie = confusion_matrix(Y_test, Y_pred)
print("Matricea de confuzie:")
print(matrice_confuzie)

acurracy = accuracy_score(Y_test, Y_pred)
print("Acuratetea: ", acurracy)

# acurracy_per_class = matrice_confuzie.diagonal() / matrice_confuzie.sum(axis=1)
# acurracy_mean = np.mean(acurracy_per_class)
# print("Accuracy mean: ", acurracy_mean)

# Predictii
Y_pred_apply = modelADL.predict(X_apply)
df_apply["DEPARTAMENT PREDICT"] = Y_pred_apply
df_apply.to_csv("data/results/ADLApplied.csv")

df_X_test = pd.DataFrame(
    X_test,
    columns=numeric_cols
)
print(Y_test)
df_X_test["DEPARTAMENT"] = Y_test
df_X_test["DEPARTAMENT PREDICT"] = Y_pred
df_X_test.to_csv("data/results/ADLAppliedTest.csv", index=False)

# Vizualizarea distributiilor pe axele discriminante:
for label in np.unique(Y_train):
    sb.kdeplot(X_train_lda[Y_train == label, 0], label = label)
plt.title("Distribuția pe axa discriminantă 1")
plt.xlabel("Axa discriminantă 1")
plt.show()