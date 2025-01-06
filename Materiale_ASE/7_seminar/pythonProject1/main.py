import pandas as pd
from functii import *

# pd.set_option("display.max_columns",None)

etnicitate = pd.read_csv("Ethnicity.csv", index_col=0)
# for index, value in etnicitate.iterrows():
#     print("Index: ", index)
#     print("Value: ", value)
# print("Valori lipsa:", etnicitate.isna().any().any())
etnii = list(etnicitate)[1:]
# print("Etnii:",etnii)

# Cerinta 1
coduri_localitati = pd.read_csv("Coduri_Localitati.csv",index_col=0)
etnicitate_ = etnicitate.merge(right=coduri_localitati,left_index=True,right_index=True)
print(etnicitate_)
etnicitate_judete = etnicitate_[etnii+["County"]].groupby(by="County").sum()
print("etnicitate judete")
print(etnicitate_judete)
etnicitate_judete.to_csv("Ethnicity_County.csv")

coduri_judete = pd.read_csv("Coduri_Judete.csv",index_col=0)
etnicitate_judete_ = etnicitate_judete.merge(coduri_judete,left_index=True,right_index=True)
print(etnicitate_judete_)
etnicitate_regiuni = etnicitate_judete_[etnii+["Regiune"]].groupby(by="Regiune").sum()
print(etnicitate_regiuni)
etnicitate_regiuni.to_csv("ethnicity_region.csv")

coduri_regiuni = pd.read_csv("Coduri_Regiuni.csv",index_col=0)
etnicitate_regiuni_ = etnicitate_regiuni.merge(coduri_regiuni,left_index=True,right_index=True)
etnicitate_macroregiuni = etnicitate_regiuni_[etnii+["MacroRegiune"]].groupby(by="MacroRegiune").sum()
etnicitate_macroregiuni.to_csv("ethnicity_macroregion.csv")

# Cerinta 2
etnicitate_p = etnicitate[etnii].apply(func=procente,axis=1)
etnicitate_p["City"]=etnicitate["City"]
etnicitate_p.to_csv("Ethnicity_p.csv")

etnicitate_judete_p = etnicitate_judete.apply(func=procente,axis=1)
etnicitate_judete_p.to_csv("Ethnicity_County_p.csv")

etnicitate_regiuni_p = etnicitate_regiuni.apply(func=procente,axis=1)
etnicitate_regiuni_p.to_csv("Ethnicity_Region_p.csv")

# Cerinta 3
disim_loc = etnicitate_[etnii+["County"]].groupby(by="County").apply(func=disim,coloane=etnii)
print(disim_loc)
