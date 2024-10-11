import pandas as pd
import numpy as np

# Instantiere obiect serie de timp
date_nastere = ["1968.03.03", "1971.09.08", "1970.05.04", "1980.07.07"]
nume_persoane = ["Pop Eugen", "Popa Marius", "Ionescu Diana", "Comsa Maria"]
persoane = pd.Series(data=nume_persoane, index=pd.to_datetime(date_nastere))
print("--Seria de timp persoane:")
print(persoane, persoane.index, type(persoane.index), sep="\n")

# Generare aleatoare a unei serii de timp
n = 10
serie_t = pd.Series(data=np.random.randn(n), index=pd.date_range('2019.11.12', '2019.12.11', periods=n))
print("\n--Serie aleatoare:", serie_t, type(serie_t.index), sep="\n")

# Eliminare valori
data_limita = '2019.11.30'
print("\n--Eliminare valori inainte de data de", data_limita, ":")
print(serie_t.truncate(before=data_limita))

# Conversie
print("\n--Conversie de la ora Frantei la ora Romaniei:")
print(serie_t.tz_localize("Europe/Paris").tz_convert("Europe/Bucharest"))

# Sumarizare la nivel de luna si an
print("\n--Media valorilor la nivel de luna si an:")
print(serie_t.resample(rule='M').mean())
print(serie_t.resample(rule='Y').mean())
print("\n--Sumarizare ohlc la nivel de luna si an:")
print(serie_t.resample(rule="M").ohlc())
print(serie_t.resample(rule="Y").ohlc())

