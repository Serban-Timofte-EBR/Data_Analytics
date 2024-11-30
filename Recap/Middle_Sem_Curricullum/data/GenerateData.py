import pandas as pd
import numpy as np

# Generăm fișierul `vanzari.csv` cu mai multe date și valori lipsă
vanzari_data = {
    "ID_Produs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Categorie": [
        "Electrocasnice", "Electrocasnice", "Mobila", "Electrocasnice", "Mobila",
        "Electrocasnice", "Mobila", "Electrocasnice", "Mobila", None
    ],
    "Vanzari": [20000, 35000, 50000, None, 30000, 25000, None, 40000, 35000, 28000],
    "Profit": [5000, 12000, 15000, 9000, None, 6000, 8000, None, 10000, 7000]
}
vanzari_df = pd.DataFrame(vanzari_data)
vanzari_df.to_csv("input/vanzari.csv", index=False)

# Generăm fișierul `produse.csv` cu mai multe date și valori lipsă
produse_data = {
    "ID_Produs": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    "Nume_Produs": [
        "Frigider", "Televizor", "Canapea", "Aspirator", "Birou",
        "Masina de spalat", "Pat", "Mixer", "Dulap", None
    ],
    "Pret": [25000, 40000, 60000, 20000, 15000, None, 35000, 8000, 50000, 30000]
}
produse_df = pd.DataFrame(produse_data)
produse_df.to_csv("input/produse.csv", index=False)

print("Fișierele `vanzari.csv` și `produse.csv` cu date extinse și valori lipsă au fost generate cu succes!")