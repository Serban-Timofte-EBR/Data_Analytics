import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.discriminant_analysis import DiscriminantAnalysisPredictionMixin, LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

# Determinați regiunile unde rata șomajului este mai mică de 5%.

df_employee = pd.read_csv("data/EmployeeData.csv", index_col=0)
df_region = pd.read_csv("data/RegionData.csv", index_col=0)

df_merge = df_employee.merge(
    df_region,
    left_on="Region",
    right_index=True
)
df_merge.to_csv("data/helpers/1_Merge.csv")

df_groupedMean = df_merge.groupby("Region")[["GDP_per_Capita", "UnemploymentRate"]].mean()
df_groupedMean.to_csv("data/helpers/2_Grouped.csv")

df_cerinta1 = df_groupedMean[df_groupedMean["UnemploymentRate"] < 5].sort_values(by="GDP_per_Capita", ascending=False)
df_cerinta1.to_csv("data/results/Cerinta1.csv")

# Calculați distribuția salariaților(Count) pe fiecare regiune și salvați rezultatele într - un
# fișier EmployeeDistribution.csv:

df_merge["Count"] = 1
df_groupedMean2 = df_merge.groupby("Region")[["Age", "YearsExperience", "EducationLevel", "GDP_per_Capita", "UnemploymentRate", "Count"]].sum()
df_groupedMean2.to_csv("data/helpers/3_GroupedComplete.csv")
df_cerinta2 = df_groupedMean2[["Count"]]
df_cerinta2.to_csv("data/results/Cerinta2.csv")

# Cerinta B - discriminanta

df_employee = pd.read_csv("data/EmployeeData.csv", index_col=0)
df_apply = pd.read_csv("data/ApplyData.csv")

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
print("Variabile independete: ", variabile_independente)

X = df_employee_clean[variabile_independente]
Y = df_employee_clean["Attrition"]
X_apply = df_apply_clean[variabile_independente]

scaler = StandardScaler()
X = scaler.fit_transform(X)
X_apply = scaler.fit_transform(X_apply)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

modelADL = LinearDiscriminantAnalysis()
modelADL.fit(X_train, Y_train)

X_train_lda = modelADL.transform(X_train)
X_test_lda = modelADL.transform(X_test)

df_X_train = pd.DataFrame(
    X_train_lda,
    columns=["Scor Discriminanta"]
)
df_X_train.to_csv("data/results/DiscriminantScores.csv", index=False)

Y_pred = modelADL.predict(X_test)
matrice_confuzie = confusion_matrix(Y_test, Y_pred)
df_matrice = pd.DataFrame(
    matrice_confuzie,
    index=["YES", "NO"],
    columns=["YES", "NO"]
)
df_matrice.to_csv("data/results/MatriceConfuzie.csv")

accuracy = accuracy_score(Y_test, Y_pred)
print("Acuratetea: ", accuracy)

accuracy_per_class = matrice_confuzie.diagonal() / matrice_confuzie.sum(axis=1)
accuracy_mean = np.mean(accuracy_per_class)
print("Acuratetea medie: ", accuracy_mean)

Y_apply = modelADL.predict(X_apply)
df_X_apply = pd.DataFrame(
    X_apply,
    columns=variabile_independente
)
df_X_apply["Attrition"] = Y_apply
df_X_apply.to_csv("data/results/Applied.csv", index=False)

for label in np.unique(Y_train):
    sb.kdeplot(X_train_lda[Y_train == label, 0], label = label)
plt.title("Distributia pe axa discriminanta 1")
plt.show()