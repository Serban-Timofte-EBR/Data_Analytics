import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.cross_decomposition import CCA
from sklearn.preprocessing import StandardScaler

# A
df_edu = pd.read_csv("data/EduHealthData.csv", index_col=0)

# Cerinta 1 Să se determine țările cu cea mai mare variație între rata de înscriere în învățământul primar (PrimaryEnrollment) și rata de înscriere în învățământul terțiar (TertiaryEnrollment).
df_edu["Difference"] = df_edu["PrimaryEnrollment"] - df_edu["TertiaryEnrollment"]
df_edu = df_edu.sort_values(by="Difference", ascending=False)
df_cerinta1 = df_edu[["PrimaryEnrollment", "TertiaryEnrollment", "Difference"]].head(3)
df_cerinta1.to_csv("data/results/A/Cerinta1.csv")

# Cerinta 2 Să se clasifice țările pe categorii de sănătate în funcție de speranța de viață (LifeExpectancy).
df_edu["HealthCategory"] = np.where(
    df_edu["LifeExpectancy"] >= 80, "High",
    np.where(
        df_edu["LifeExpectancy"] >= 60, "Medium",
        "Low"
    )
)
df_cerinta2 = df_edu[["LifeExpectancy", "HealthCategory"]]
df_cerinta2.to_csv("data/results/A/Cerinta2.csv")

# B - Analiza canonica

df_dataset = pd.read_csv("data/Dataset.csv", index_col=0)

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

df_dataset_clean = cleanData(df_dataset)
numeric_cols = df_dataset_clean.columns[0:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_dataset_clean[numeric_cols])

df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_dataset_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/results/B/1_StandardizedDataset.csv")

set_educatie = ["PrimaryEnrollment", "SecondaryEnrollment", "TertiaryEnrollment", "GraduationRate"]
set_sanatate = ["LifeExpectancy", "InfantMortalityRate", "HealthcareExpenditure", "PhysiciansPer1000", "HospitalBedsPer1000"]

X = df_date_standardizate[set_educatie]
Y = df_date_standardizate[set_sanatate]

X, Y = X.align(Y, join="inner", axis=0)

modelCCA = CCA()
X_C, Y_C = modelCCA.fit_transform(X, Y)

df_XC = pd.DataFrame(
    X_C,
    index=X.index,
    columns=["X_C1", "X_C2"]
)
df_XC.to_csv("data/results/B/2_ScoruriCanoniceX.csv")

df_YC = pd.DataFrame(
    Y_C,
    index=Y.index,
    columns=["Y_C1", "Y_C2"]
)
df_YC.to_csv("data/results/B/3_ScoruriCanoniceY.csv")

plt.figure()
plt.scatter(X_C[:, 0], X_C[:, 1], label="Educatie")
plt.scatter(Y_C[:, 0], Y_C[:, 1], label="Sanatate")
plt.title("Primele doua radacini canonice")
plt.xlabel("C1")
plt.ylabel("C2")
plt.show()

corelatii_canonice = modelCCA.score(X, Y)
print("Corelatii: ", corelatii_canonice)

corr_X = np.corrcoef(X.T, X_C.T)[:X.shape[1], X.shape[1]:]
corr_Y = np.corrcoef(Y.T, Y_C.T)[:Y.shape[1], Y.shape[1]:]

plt.figure()
sb.heatmap(corr_X)
plt.title("Corelograma 1")
plt.show()

plt.figure()
sb.heatmap(corr_Y)
plt.title("Corelograma 2")
plt.show()