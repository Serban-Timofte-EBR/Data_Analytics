# Scrie un program în Python care:
# 	1.	Creează o listă de studenți, fiecare reprezentat printr-un tuplu care conține:
# 	    •	Numele studentului.
# 	    •	Nota obținută la examen.
# 	2.	Filtrează din această listă doar studenții care au obținut o notă mai mare de 8.
# 	3.	Afișează lista cu studenții care îndeplinesc criteriul de selecție.

stundenti = [("Serban", 8.5), ("Iulian", 8.3), ("Andreea", 4.3), ("Dumitru", 8.45), ("Iustin", 6.9)]
stundentiOver8 = list(filter(lambda stundet : stundet[1] > 8, stundenti))
print("Lista de studenti cu note peste 8: ", str(stundentiOver8))