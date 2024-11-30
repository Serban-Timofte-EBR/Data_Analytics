import pandas as pd
import numpy as np

# Generăm fișierul `populatie.csv` cu valori lipsă
populatie_data = {
    "Cod_Judet": ["AB", "AR", "AG", "BC", "BH", "BR", "BT", "BZ", "CS", "CL"],
    "Populatie_Totala": [342376, 409072, 612431, 701371, None, 321234, 451678, None, 279345, 643212],
    "Urban": [198375, 239452, 324431, None, 350545, 187654, 232134, 245321, None, 354321],
    "Rural": [144001, 169620, 288000, 281240, 260500, None, 219544, 233000, 155667, 288891]
}
populatie_df = pd.DataFrame(populatie_data)
populatie_df.to_csv("populatie.csv", index=False)

# Generăm fișierul `economia.csv` cu valori lipsă
economia_data = {
    "Cod_Judet": ["AB", "AR", "AG", "BC", "BH", "BR", "BT", "BZ", "CS", "CL"],
    "PIB": [12932, 14052, None, 18952, 17544, 10523, 9876, 11532, 8234, None],
    "Somaj": [5.2, None, 6.1, 7.0, 5.5, 8.1, None, 6.9, 9.2, 4.5]
}
economia_df = pd.DataFrame(economia_data)
economia_df.to_csv("economia.csv", index=False)

# Generăm fișierul `judete.csv` fără valori lipsă
judete_data = {
    "Cod_Judet": ["AB", "AR", "AG", "BC", "BH", "BR", "BT", "BZ", "CS", "CL"],
    "Nume_Judet": ["Alba", "Arad", "Arges", "Bacau", "Bihor", "Braila", "Botosani", "Buzau", "Caras-Severin", "Calarasi"],
    "Regiune": ["Centru", "Vest", "Sud", "Nord-Est", "Nord-Vest", "Sud-Est", "Nord-Est", "Sud-Est", "Vest", "Sud"]
}
judete_df = pd.DataFrame(judete_data)
judete_df.to_csv("judete.csv", index=False)

print("Fișierele CSV extinse cu valori lipsă au fost generate cu succes!")