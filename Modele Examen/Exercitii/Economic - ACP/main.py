import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df_economic = pd.read_csv("data/EconomicDevelopment.csv", index_col=0)

# Determinați țările cu cele mai mari cheltuieli pentru sănătate pe cap de locuitor (HealthcareExpenditure)
# și salvați primele trei țări în fișierul Cerinta1.csv.

df_economic["Health_per_Capita"] = df_economic["HealthcareExpenditure"] / df_economic["Population"]
df_cerinta1 = df_economic[["Health_per_Capita", "HealthcareExpenditure", "Population"]]
df_cerinta1 = df_cerinta1.sort_values(by="Health_per_Capita", ascending=False).head(3)
df_cerinta1.to_csv("data/results/A/Cerinta1.csv")

# Clasificați țările în funcție de raportul dintre cheltuielile pentru sănătate (HealthcareExpenditure)
# și PIB-ul pe cap de locuitor (GDP_per_Capita)

df_economic["Health_GDP"] = df_economic["HealthcareExpenditure"] / df_economic["GDP_per_Capita"] * 100
df_economic["HealthToGDP_Category"] = np.where(
    df_economic["Health_GDP"] >= 20, "High",
    np.where(
        (df_economic["Health_GDP"] > 10) & (df_economic["Health_GDP"] < 20), "Medium",
        "Low"
    )
)
df_economic.to_csv("data/results/A/Cerinta2.csv")

# Cerinta B - ACP
df_economic = pd.read_csv("data/EconomicDevelopment.csv", index_col=0)

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

df_economic_clean = cleanData(df_economic)

numeric_cols = df_economic_clean.columns[0:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_economic_clean[numeric_cols])
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_economic_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/results/B/1_Standardizate.csv")

modelACP = PCA()
C = modelACP.fit_transform(df_date_standardizate)

variance = modelACP.explained_variance_ratio_
print("Variance: ", variance)
cumVariance = np.cumsum(variance)
print("Variance: ", cumVariance)

plt.figure()
plt.bar(range(1, len(variance) + 1), variance)
plt.step(range(1, len(cumVariance) + 1), cumVariance)
plt.title("Reprezentativitatea Componentelor Principale")
plt.show()

etichetePCA = ["C" + str(i+1) for i in range(len(variance))]
df_pca = pd.DataFrame(
    C,
    index=df_date_standardizate.index,
    columns=etichetePCA
)
df_pca.to_csv("data/results/B/2_PCA.csv")

plt.figure()
plt.scatter(df_pca["C1"], df_pca["C2"])
plt.title("Scatter Componente Principale")
plt.xlabel("C1")
plt.ylabel("C2")
plt.show()

matrice_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
print("Matricea de corelatie:")
df_matrice = pd.DataFrame(
    matrice_corelatie,
    index=numeric_cols,
    columns=etichetePCA
)
print(df_matrice)
df_matrice.to_csv("data/results/B/3_MatriceCorelatie.csv")

plt.figure()
sb.heatmap(df_matrice)
plt.title("Corelograma Corelatii")
plt.show()

comunalitati = np.cumsum(matrice_corelatie ** 2, axis=1)
print("Comunalitati:")
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=etichetePCA
)
df_comunalitati.to_csv("data/results/B/4_Comunalitati.csv")

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Corelograma Comunalitati")
plt.show()