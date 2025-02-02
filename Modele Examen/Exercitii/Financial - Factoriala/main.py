import pandas as pd

df_financial = pd.read_csv("data/FinancialMarkets.csv", index_col=0)
df_regions = pd.read_csv("data/RegionCodes.csv", index_col=0)

# Cerinta 1:
# Să se determine țările în care rata dobânzii (InterestRate) este mai mică decât rata inflației (InflationRate).
# Rezultatele să fie salvate într-un fișier numit InterestVsInflation.csv, cu următoarele coloane:
# 	•	Country: Numele țării
# 	•	InterestRate: Rata dobânzii
# 	•	InflationRate: Rata inflației

df_filtred = df_financial[df_financial["InterestRate"] < df_financial["InflationRate"]]
df_cerinta1 = df_filtred[["InterestRate", "InflationRate"]]
df_cerinta1.to_csv("data/results/Cerinta1.csv")