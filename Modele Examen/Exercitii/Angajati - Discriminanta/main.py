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

variabile_independete = df_employee_clean.columns[1:]
print("Variabile independete: ", variabile_independete)

X = df_employee_clean[variabile_independete]
Y = df_employee_clean["Department"]
X_apply = df_employee_clean[variabile_independete]

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_apply = scaler.transform(X_apply)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

modelADL = LinearDiscriminantAnalysis()
modelADL.fit(X_train, Y_train)

# Scoruri
X_train_lda = modelADL.transform(X_train)
X_test_lda = modelADL.transform(X_test)

df_XTtrainLDA = pd.DataFrame(
    X_train_lda,
    columns=["LD" + str(i+1) for i in range(X_train_lda.shape[1])]
)
df_XTtrainLDA.to_csv("data/results/B/XTrainLDA.csv", index=False)

df_XTestLDA = pd.DataFrame(
    X_test_lda,
    columns=["LD" + str(i+1) for i in range(X_test_lda.shape[1])]
)
df_XTestLDA.to_csv("data/results/B/XTestLDA.csv", index=False)

# Evaluarea model
Y_pred = modelADL.predict(X_test)

matrice_confuzie = confusion_matrix(Y_test, Y_pred)
df_matrice = pd.DataFrame(
    matrice_confuzie,
    index=np.unique(Y_test),
    columns=np.unique(Y_test)
)
df_matrice.to_csv("data/results/B/MatriceConfuzie.csv")

acuratetea = accuracy_score(Y_test, Y_pred)
print("Acuratetea: ", acuratetea)

acuratetea_per_class = matrice_confuzie.diagonal() / matrice_confuzie.sum(axis=1)
acurateteaMedie = np.mean(acuratetea_per_class)
print("Acuratetea medie: ", acurateteaMedie)

# Predictii pe setul apply
Y_apply = modelADL.predict(X_apply)
df_apply_clean["Departament"] = Y_apply
df_apply_clean.to_csv("data/results/B/ApplyPredicted.csv")

for label in np.unique(Y_train):
    sb.kdeplot(X_train_lda[Y_train == label, 0], label = label)
plt.title("Distributia pe axele discriminante")
plt.show()
