import pandas as pd
import numpy as np

java_1045 = pd.Series(data={"Pop Adrian": 8, "Popescu Mihai": 6.5, "Ionescu Maria": 8})
poo_1045 = pd.Series(data={"Pop Adrian": 7, "Popescu Mihai": 6, "Ionescu Maria": 10, "Ionescu Dan": 4})
java_1045.name = "Java 1045"
poo_1045.name = "POO 1045"
print(java_1045, poo_1045, sep="\n")
print(java_1045["Popescu Mihai":])

# exit(0)

def medie(x, y):
    return (x + y) / 2


def marire(x, punctaj_adaugat=2):
    y = x + punctaj_adaugat
    if (y > 10):
        y = 10
    return y


def marire2(x):
    if (x > 7):
        x = 10
    return x


def medie_grupa(x, **args):
    y = x[x > args['limita']]
    return np.mean(y)


# Operator +
print("\nMedie prin calcul simplu:")
catalog = (java_1045 + poo_1045) / 2
print(catalog)

print("\nConcatenare cu append:")
print(java_1045._append(poo_1045))
print("\nDrop", java_1045.drop("Pop Adrian"), sep="\n")
tmp = java_1045.copy()
tmp.update(poo_1045)
print("\nActualizare prin update:", tmp, sep="\n")

print("\nReplace:", java_1045.replace(to_replace=8, value=7), sep="\n")
print("\nFill:", catalog.fillna(5), sep="\n")
print("\nReindexare:", catalog.reindex(["student" + str(i) for i in range(len(catalog))]), sep="\n")

# exit(0)

print("\nAgregare prin medie:", poo_1045.agg(func=medie_grupa, limita=4))
print("\nApply -> marire note cu 2 puncte:", poo_1045.apply(func=marire, punctaj_adaugat=2))
print("\nCalcul medie prin combine:", java_1045.combine(poo_1045, func=medie))
print("\nTransformare prin marire cu 2 puncte si marirea notelor peste 7 la 10:",
      java_1045.transform(func=[marire, marire2]), sep="\n")
