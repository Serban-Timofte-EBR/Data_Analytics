import pandas as pd

# Citire din CSV
file = open("Educatie.csv")
lines = file.readlines()
file.close()

table_head = lines[0][:-1].split(",");
print("Capul de tabel: ", table_head)

# Citire din CSV cu dataframe
df = pd.read_csv("Educatie.csv");
print("DataFrame")
print(df)

sum_juds = df.groupby('Judet').agg({'Pop_liceal': 'sum'})
print("Suma pe judete")
print(sum_juds)