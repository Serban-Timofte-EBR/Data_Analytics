# Scrie un program în Python care:
# 	1.	Creează o listă de dicționare, fiecare reprezentând un student cu următoarele informații:
# 	    •	Nume: Numele studentului.
# 	    •	Oras: Orașul de reședință al studentului.
# 	    •	Nota: Nota obținută la examen.
# 	2.	Gruparea studenților după oraș:
# 	    •	Creează o structură de date în care studenții sunt grupați în funcție de orașul de reședință.
# 	3.	Calcularea mediei notelor pe fiecare oraș:
# 	    •	Pentru fiecare oraș, calculează media notelor studenților care locuiesc acolo.
# 	4.	Structura de output:
# 	    •	Structura trebuie să fie un dicționar cu cheile:
# 	    •	"Nume": o listă de nume de studenți.
# 	    •	"Oras": o listă de orașe.
# 	    •	"Note": o listă de medii ale notelor pentru fiecare oraș.

def printDict(dict):
    for key, value in dict.items():
        print(key.upper())
        print("\t" + str(value))

catalog = {
    "Serban": ("Focsani", 9.5),
    "Iulian": ("Arad", 7.5),
    "Maria": ("Focsani", 8.0),
    "Ana": ("Bucuresti", 10.0),
    "Vlad": ("Arad", 6.5),
    "Ioana": ("Bucuresti", 9.0),
    "Andrei": ("Cluj", 8.5),
    "Elena": ("Cluj", 9.0)
}

def generateCatalogOrase(catalog):
    dict = {}
    for key, value in catalog.items():
        if value[0] in dict.keys():
            dict[value[0]].append([key, value[1]])
        else:
            dict[value[0]] = [[key, value[1]]]
    return dict

catalogOrase = generateCatalogOrase(catalog)
print("Catalogul de orase:")
printDict(catalogOrase)