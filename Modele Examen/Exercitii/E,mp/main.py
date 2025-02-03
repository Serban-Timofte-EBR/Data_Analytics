import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df_employee = pd.read_csv("data/EmployeePerformance.csv", index_col=0)
df_apply = pd.read_csv("data/NewEmployees.csv", index_col=0)

df_grouped = df_employee.groupby("Department")["PerformanceRating"].mean()
df_grouped.to_csv("data/results/A/Cerinta1.csv")

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

df_employee_clean = cleanData(df_employee)
df_apply_clean = cleanData(df_apply)

variabile_independente = df_employee_clean.columns[0:-2]
print("Variabile independente: ", variabile_independente)

X = df_employee_clean[variabile_independente]
Y = df_employee_clean["Department"]
X_apply = df_apply_clean[variabile_independente]

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_apply = scaler.transform(X_apply)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

modelADL = LinearDiscriminantAnalysis()
modelADL.fit(X_train, Y_train)

# Scoruri discriminante
X_train_lda = modelADL.transform(X_train)
X_test_lda = modelADL.transform(X_test)

df_X_train_lda = pd.DataFrame(
    X_train_lda,
    columns=["D" + str(i+1) for i in range(X_train_lda.shape[1])]
)
df_X_train_lda.to_csv("data/results/B/1_ScoruriDiscriminante.csv", index=False)

# Evaluarea model
Y_pred = modelADL.predict(X_test)
matrice_confuzie = confusion_matrix(Y_test, Y_pred)
df_matrice_confuzie = pd.DataFrame(
    matrice_confuzie,
    index=np.unique(df_employee_clean["Department"]),
    columns=np.unique(df_employee_clean["Department"])
)
df_matrice_confuzie.to_csv("data/results/B/2_MatriceConfuzie.csv")

accuracy = accuracy_score(Y_test, Y_pred)
print("Acuratetea: ", accuracy)

accuracy_per_class = matrice_confuzie.diagonal() / matrice_confuzie.sum(axis=1)
accuracyMean = np.mean(accuracy_per_class)
print("Acuratetea medie: ", accuracyMean)

Y_apply = modelADL.predict(X_apply)
df_apply["Department"] = Y_apply
df_apply.to_csv("data/results/B/3_Apply.csv")

for label in np.unique(Y_train):
    sb.kdeplot(X_train_lda[Y_train == label, 0], label = label)
plt.title("Axele discriminante")
plt.show()