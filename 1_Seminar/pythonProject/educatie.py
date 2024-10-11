import pandas as pd

# Citire dintr-un fisier
csv_educatie = open('Educatie.csv')
lines_educatie = csv_educatie.readlines()
csv_educatie.close()

# Citire din CSV

df_educatie = pd.read_csv('Educatie.csv')
# print(df_educatie)

print("Numarul total de absolventi din Romania: ")
df_absolventi_ro = df_educatie[['Abs_liceal', 'Abs_postlic', 'Abs_primar_gimn', 'Abs_profes', 'Abs_tehnic', 'Abs_univ']].sum()  # Suma absolventilor din romania pe categorie (liceal, postliceal, etc)
total_absolventi_ro = df_absolventi_ro.sum()
print(total_absolventi_ro)
print()

df_suma_absolventi = df_educatie.groupby('Judet')[['Abs_liceal', 'Abs_postlic', 'Abs_primar_gimn', 'Abs_profes', 'Abs_tehnic', 'Abs_univ']].sum()

#    axis = 0(valoare implicită) face operația de - a lungul coloanelor, adică aplică funcția la fiecare coloană.Aceasta înseamnă că face, de exemplu, suma valorilor pe fiecare coloană.
#    axis = 1 face operația de - a lungul rândurilor, adică aplică funcția pe fiecare rând.În cazul tău, asta înseamnă că face suma valorilor din mai multe coloane pentru fiecare rând(sau, în cazul tău, pentru fie care județ).
df_suma_absolventi_total = df_suma_absolventi.sum(axis=1)

print("Numarul total de absolventi pe judet")
print(df_suma_absolventi_total)

print("---------------------------------------------------")
print("Populatie totala eligibila pe judet")
df_pop = df_educatie.groupby('Judet')[['Pop_liceal', 'Pop_primar_gimn', 'Pop_univ', 'Pop_profess']].sum()
df_pop_total = df_pop.sum(axis = 1)
print(df_pop_total)

print("---------------------------------------------------")
print("Raportul absolventi / pop pe judet")
df_raportul_absolventi = df_suma_absolventi_total / df_pop_total * 100
print(df_raportul_absolventi)

print("---------------------------------------------------")
print("Numarul mediu de absolventi dintr-un judet din Romania:")
df_nr_judete = len(df_suma_absolventi)
print(total_absolventi_ro/df_nr_judete)