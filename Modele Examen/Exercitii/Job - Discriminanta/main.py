import warnings

import matplotlib.pyplot as plt

warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np
import seaborn as sb
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Să se determine regiunile unde salariul mediu (AverageSalary) depășește PIB-ul pe cap de locuitor (GDP_per_Capita).
# Salvați rezultatele într-un fișier numit HighSalaryRegions.csv cu următoarele coloane:

df_jobs = pd.read_csv("data/JobMarketData.csv", index_col=0)
df_regions = pd.read_csv("data/RegionData.csv", index_col=0)

df_merge = df_jobs.merge(
    df_regions,
    left_on="Region",
    right_index=True
)
df_merge.to_csv("data/helpers/1_Merge.csv")

df_grouped = df_merge.groupby("Region").mean()
df_grouped.to_csv("data/helpers/2_Grouped.csv")

df_cerinta1 = df_grouped[df_grouped["AverageSalary"] > df_grouped["GDP_per_Capita"]]
df_cerinta1 = df_cerinta1.sort_values(by="AverageSalary", ascending=False)

df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Cerinta B - Analiza discriminanta

df_training = pd.read_csv("data/TrainingData.csv", index_col=0)
df_apply = pd.read_csv("data/ApplyData.csv", index_col=0)

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

df_training_clean = cleanData(df_training)
df_apply_clean = cleanData(df_apply)

variabile_independente = df_training_clean.columns[0:-1]
print("Variabile independete: ", variabile_independente)

X = df_training_clean[variabile_independente]
Y = df_training_clean["Attrition"]
X_apply = df_apply_clean[variabile_independente]


scaler = StandardScaler()
X = scaler.fit_transform(X)
X_apply = scaler.fit_transform(X_apply)

pd.DataFrame(
    X,
    index=df_training.index,
    columns=variabile_independente
).to_csv("data/results/TrainingStandardized.csv")

pd.DataFrame(
    X_apply,
    index=df_apply.index,
    columns=variabile_independente
).to_csv("data/results/ApplyStandardized.csv")

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

modelADL = LinearDiscriminantAnalysis()
modelADL.fit(X_train, Y_train)

X_train_lda = modelADL.transform(X_train)
X_test_lda = modelADL.transform(X_test)


df_X_train_lda = pd.DataFrame(
    X_train_lda,
    columns=["LD" + str(i+1) for i in range(X_train_lda.shape[1])]
).to_csv("data/results/TrainingDiscriminantScores.csv")

df_X_test_lda = pd.DataFrame(
    X_test_lda,
    columns=["LD" + str(i+1) for i in range(X_test_lda.shape[1])]
).to_csv("data/results/TestingDiscriminantScores.csv")

# Evaluarea modelului
Y_pred = modelADL.predict(X_test)

matrice_confuzie = confusion_matrix(Y_test, Y_pred)
print("Matricea de confuzie:")
df_matrice_confuzie = pd.DataFrame(
    matrice_confuzie,
    index=["Da", "Nu"],
    columns=["Da", "Nu"]
)
print(df_matrice_confuzie)
df_matrice_confuzie.to_csv("data/results/ConfusionMatrix.csv")

accuracy = accuracy_score(Y_test, Y_pred)
print("Accuracy: ", accuracy)

accuracy_per_clas = matrice_confuzie.diagonal() / matrice_confuzie.sum(axis=1)
accuracyMean = np.mean(accuracy_per_clas)
print("Acuratetea medie: ", accuracyMean)

X_apply = pd.DataFrame(
    X_apply,
    index=df_apply.index,
    columns=variabile_independente
)
Y_pred_apply = modelADL.predict(X_apply)
X_apply["Predicted"] = Y_pred_apply
X_apply.to_csv("data/results/XApply.csv")

for label in np.unique(Y_train):
    sb.kdeplot(X_train_lda[Y_train == label, 0], label = label)
plt.title("Diagrama")
plt.show()

