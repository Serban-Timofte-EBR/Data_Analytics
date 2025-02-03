import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

df_economic = pd.read_csv("data/EconomicEducation.csv", index_col=0)
df_regions = pd.read_csv("data/RegionData.csv", index_col=0)

# A

# Determinați țara cu cea mai mare valoare totală a cheltuielilor pentru educație (EducationExpenditure_per_Capita * Population).
df_economic["CheltuieliEducatie"] = df_economic["EducationExpenditure_per_Capita"] * df_economic["Population"]
df_cerinta1 = df_economic.sort_values(by="CheltuieliEducatie", ascending=False).head(1)
df_cerinta1 = df_cerinta1[["EducationExpenditure_per_Capita", "Population", "CheltuieliEducatie"]]
df_cerinta1.to_csv("data/results/A/Cerinta1.csv")

# Clasificați țările în funcție de raportul dintre cheltuielile pentru cercetare și dezvoltare
# (ResearchDevelopmentExpenditure) și cheltuielile pentru sănătate (HealthcareExpenditure)
df_economic["Raport"] = df_economic["ResearchDevelopmentExpenditure"] / df_economic["HealthcareExpenditure"]
df_economic["RD_to_Health_Category"] = np.where(
    df_economic["Raport"] >= 0.5, "High",
    np.where(
        (df_economic["Raport"] > 0.2) & (df_economic["Raport"] < 0.5), "Medium",
        "Low"
    )
)
df_cerinta2 = df_economic[["RD_to_Health_Category"]]
df_cerinta2.to_csv("data/results/A/Cerinta2.csv")

# B - ACP
df_dataset = pd.read_csv("data/Dataset.csv", index_col=0)

def cleanData(df):
    isinstance(df, pd.DataFrame)
    if df.isna().any().any():
        print("Cleaning data ...")
        for col in df.columns:
            if df[col].isna().any().any():
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col] = df[col].fillna(df[col].mean())
                else:
                    df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_dataset_clean = cleanData(df_dataset)
df_dataset_clean.to_csv("data/results/B/1_DatasetClean.csv")

numeric_cols = df_dataset_clean.columns[0:]
print("Numeric cols: ", numeric_cols)

scaler = StandardScaler()
date_standardizate = scaler.fit_transform(df_dataset_clean[numeric_cols])
df_date_standardizate = pd.DataFrame(
    date_standardizate,
    index=df_dataset_clean.index,
    columns=numeric_cols
)
df_date_standardizate.to_csv("data/results/B/2_Standardized.csv")

modelACP = PCA()
C = modelACP.fit_transform(df_date_standardizate)

variance = modelACP.explained_variance_ratio_
print("Variance: ", variance)
cumVar = np.cumsum(variance)

plt.figure()
plt.bar(range(1, len(variance) + 1), variance)
plt.step(range(1, len(cumVar) + 1), cumVar)
plt.title("Grafic relevanta Componente Principale")
plt.show()

eticheteACP = ["C" + str(i+1) for i in range(len(variance))]
df_pca = pd.DataFrame(
    C,
    index=df_date_standardizate.index,
    columns=eticheteACP
)
df_pca.to_csv("data/results/B/3_PCA.csv")

plt.figure()
plt.scatter(df_pca["C1"], df_pca["C2"])
plt.title("Scatter Componente Principale")
plt.xlabel("C1")
plt.ylabel("C2")
plt.show()

matrice_corelatie = np.corrcoef(date_standardizate.T, C.T)[:len(numeric_cols), len(numeric_cols):]
df_matrice_corelatie = pd.DataFrame(
    matrice_corelatie,
    index=numeric_cols,
    columns=eticheteACP
)
df_matrice_corelatie.to_csv("data/results/B/4_MatriceCorelatie.csv")

plt.figure()
sb.heatmap(df_matrice_corelatie)
plt.title("Corelograma 1")
plt.show()

comunalitati = np.cumsum(matrice_corelatie**2, axis=1)
df_comunalitati = pd.DataFrame(
    comunalitati,
    index=numeric_cols,
    columns=eticheteACP
)
df_comunalitati.to_csv("data/results/B/5_Comunalitati.csv")

plt.figure()
sb.heatmap(df_comunalitati)
plt.title("Corelograma 2")
plt.show()