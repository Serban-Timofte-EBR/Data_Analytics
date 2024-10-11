import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)

# Instantiere
varsta = [40, 56, 30, 35, 28]
pacienti = pd.DataFrame(
    data={
        "Nume": ['Pop Adrian', 'Popescu Flavius', 'Ionescu Diana', 'Popa Maria', 'Comsa Ioan'],
        "Varsta": varsta,
        "Greutate": [79.5, np.NaN, 78.4, 67, np.NaN],
        "Sectie": ["P", "P", "C", "C", "P"]
    },
    index=range(1, 6)
)

print("Tabel pacienti:")
print(pacienti)

print("\nAdresari prin at/loc, iat/iloc:")
print("pacienti.at[1, \"Nume\"]:",pacienti.at[1, "Nume"],sep="\n")
print("pacienti.iat[0, 0]:",pacienti.iat[0, 0],sep="\n")
print("pacienti.loc[2:4, \"Nume\":]",pacienti.loc[2:4, "Nume":],sep="\n")
print("pacienti.iloc[1:4, 0:]",pacienti.iloc[1:4, 0:],sep="\n")

print("\nSelectii de coloane:")
print(pacienti["Varsta"])
coloane_selectate=["Nume","Varsta"]
print(pacienti[["Nume","Varsta"]])
print(pacienti["Nume"].loc[2:3])
print(pacienti["Nume"].iloc[0:4:2])
print(pacienti[coloane_selectate].loc[2:3])
print(pacienti[coloane_selectate].iloc[0:4:2])
# exit(0)

print("\n--Selectie pe baza de conditii aplicate coloanelor")
print("Pacienti cu varsta mai mare decat 30:")
print(pacienti[pacienti["Varsta"] > 30])

# exit(0)

print("\n--->Reindexare")
print("Tabel:",pacienti,sep="\n")
print("Reindexare coloane:")
print(pacienti.reindex(columns=["Varsta", "Sectie", "Tensiune_s"]))
print("Reindexare linii:")
print(pacienti.reindex(index=range(3, 8), method="ffill"))

# exit(0)

print("\n--Adaugare:")
print("Tabel pacienti:")
print(pacienti)
print("Adaugare coloana:")
pacienti['SaturatieO'] = [98, 99, 97, 97, 95]
print(pacienti)
print("Adaugare linie prin append:")
linie_adaugata = pd.Series(["Popa Leon",80,80],["Nume","Varsta","Greutate"],name=10)
print(pacienti.append(linie_adaugata))
print("Inserare coloana prin insert:")
pacienti.insert(4,"Tensiune_s",[12,10,12,14,15])
print(pacienti)

# exit(0)

print("\n--Concatenare:")
print("Tabel pacienti:")
print(pacienti)
tabel_concatenare1 = pd.DataFrame(
    data={
        "Temperatura": [39, 37, 36.8, 40, 37.2],
        "Tensiune_d": [8, 6, 6.7, 9, 7]
    }
    # , index=range(1, 6)
)
print("Tabel care se concateneaza pe linii:")
print(tabel_concatenare1)
print("Tabel concatenat:")
pacienti1 = pd.concat([pacienti, tabel_concatenare1], axis=1)
print(pacienti1)
print("Tabel care se concateneaza pe coloane:")
tabel_concatenare2 = pd.DataFrame(data={"Nume": ["Georgescu Liviu", "Popa Mihai"],
                                        "Greutate": (100, 94), "SaturatieO": (80, 92)})
print(tabel_concatenare2)
print("Tabel concatenat:")
pacienti2 = pd.concat([pacienti, tabel_concatenare2], ignore_index=True)
print(pacienti2)

# exit(0)

print("\n--Replace")
print("Tabel:", pacienti, sep="\n")
pacienti.replace(to_replace={97: 94}, inplace=True)
print("Inlocuire saturatie 97 cu 94:")
print(pacienti)


print("\n--Modificari prin serie de date")
print("Tabel:", pacienti, sep="\n")
pacienti.update(pd.Series([75, 70], index=[2, 4], name="Greutate"))
print(pacienti)


print("\n--Stergere coloane 'Nume','Greutate':")
print("Tabel:", pacienti, sep="\n")
print(pacienti.drop(["Nume", "Greutate"], axis=1))
print("\n--Stergere linii cu valori nan:")
print(pacienti.dropna())

# exit(0)

print("\n--Inlocuire valori lipsa")
print("Tabel:", pacienti, sep="\n")
print("Inlocuire valori lipsa cu valori aflate inainte:", pacienti.fillna(method='ffill'), sep="\n")
print("Inlocuire valori lipsa pentru Greutate cu 80:")
print(pacienti.fillna(value={"Greutate": 80}))
print("Inlocuire valori lipsa cu media:")
print(pacienti[["Varsta","Greutate"]].fillna(pacienti[["Varsta","Greutate"]].mean()))

# exit(0)

print("\n--Sortare", "Tabel:", pacienti, sep="\n")
print("\nSortare inversa dupa numele coloanelor:")
print(pacienti.sort_index(axis=1, ascending=False))
print("\nSortare inversa dupa 'Varsta':")
print(pacienti.sort_values(by="Varsta", ascending=False))
print("Tabelul 2:")
print(pacienti2)
print(pacienti2.sort_values(by="Greutate",ascending=False))

# exit(0)

print("\n--Apply", "Tabel:", pacienti2, sep="\n")
print("\nIdentificare pacienti supraponderali (>80 kg) prin apply:")
print(pacienti2.apply(lambda x: "Supraponderal" if x["Greutate"] > 80 else "Normal", axis=1))

# exit(0)

print("\n--Agregare", "Tabel:", pacienti, sep="\n")
print("\nAgregare la nivel de sectie cu calcul medii pentru coloanele numerice:")
grup = pacienti[["Sectie"] + ["Varsta", "Greutate", "SaturatieO"]].groupby(by="Sectie")
print(grup.agg(func=np.mean))

# exit(0)

# Instantiere tabel cu indecsi multiplii
studenti = pd.DataFrame(data={
    ("Informatii", "Nume"): ["Popescu Delia", "Ionescu Dan", "Mircea Elena", "Comsa Marius"],
    ("Informatii", "Grupa"): [1075, 1075, 1080, 1081],
    ("Note", "Java"): [8, 9, 7, 6],
    ("Note", "POO"): [7, 7, 6, 8]
}, index=[['A', 'A', 'B', 'B'], np.arange(1, 5)])
index_linii = studenti.index
assert isinstance(index_linii, pd.MultiIndex)
index_linii.set_names(['Seria', 'Id'], inplace=True)
print("\n--Tabel multi-index:", studenti, sep="\n")

# Selectii
print("\n--Multiindexare. Selectii")
print("\nSelectie dupa index coloana. Cheie 'Informatii'", studenti['Informatii'], sep="\n")
print("\nSelectie dupa index coloana. Cheie 'Informatii-'Nume'", studenti["Informatii"]['Nume'], sep="\n")
print("\nSelectie dupa index coloana. Cheie 'Informatii-'Nume' si index linie cheie 'A'",
      studenti["Informatii"]['Nume'][('A', 2)], sep="\n")
print("\nSelectie dupa index linie 'A' si coloana 'Note'", studenti.loc['A', "Note"], sep="\n")
print("\nSelectie dupa index linie 'A' si coloana 'Informatii'", studenti.loc['A', "Informatii"], sep="\n")
print("\nSelectie dupa index linie 'A' si coloana ('Informatii','Note')", studenti.loc['A', ("Informatii", "Nume")],
      sep="\n")
print("\nSelectie prin loc", studenti.loc[('A', 1), "Informatii"], sep="\n")
print("\nSelectie prin iloc", studenti.iloc[1:, :3], sep="\n")

# exit(0)

# Pivotare prin unstack
print("\n--Exemple unstack")
print("Tabel pivotat:", studenti, sep="\n")
print("-->Unstack:")
print("level=1", studenti.unstack(level=1), sep="\n")
print("level=0", studenti.unstack(level=0), sep="\n")

# exit(0)

# Comutare intre niveluri
print("\n--Exemple swaplevel")
print("Tabel:", studenti, sep="\n")
print("Axa de comutare 0:")
print(studenti.swaplevel(axis=0))
print("Axa de comutare 1:")
print(studenti.swaplevel(axis=1))

# exit(0)

# Sortare dupa index
print("\n--Sortare dupa index:")
print("Tabel:", studenti, sep="\n")
print("Sortare dupa index linii nivelul 0:", studenti.sort_index(level=0, ascending=False), sep="\n")
print("Sortare dupa index linii nivelul 1:", studenti.sort_index(level=1, ascending=False), sep="\n")
print("Sortare dupa index coloana nivelul 0:", studenti.sort_index(level=0, axis=1, ascending=False), sep="\n")
print("Sortare dupa index coloana nivelul 1:", studenti.sort_index(level=1, axis=1, ascending=False), sep="\n")

# exit(0)

# Eliminare nivel
print("\n--Eliminare nivel 0 cu rezultat in tabelul 'stud':")
stud = studenti.droplevel(axis=1, level=0).droplevel(level=0)
print(stud, stud.index, stud.columns, sep="\n")

# exit(0)

# Sumarizari la nivel de index
print("\n--Sumarizari dupa index")
print("Tabel:", studenti, sep="\n")
print("Media notelor pe serii:", studenti["Note"].groupby(level=0).mean(), sep="\n")
print("Media disciplinelor:", studenti["Note"].mean(axis=1), sep="\n")

# exit(0)

print("\n--Jonctiune")
print("Tabela stud:", stud, sep="\n")
print("\nCreare tabela 'catalog':")
catalog = pd.DataFrame(
    data={"Probabilitati": [9, 7, 5], 'Nume': ["Comsa Marius", "Popescu Mihai", "Radu Ioana"]},
    index=[3, 4, 5])
catalog.index.name = 'Id'
print(catalog)

# Jonctiune prin join
assert isinstance(stud, pd.DataFrame)
tabela = stud.join(other=catalog, lsuffix="_1", how="inner")
print("\nJonctiune prin join cu 'inner', 'stud' cu 'catalog' in 'tabela':", tabela, sep="\n")

# Jonctiune prin merge
print("Tabelul stud:")
print(stud)
print("Tabelul catalog:")
print(catalog)
tabela1 = stud.merge(right=catalog)
print("\nJonctiune inner prin merge dupa coloana comuna 'Nume' intre 'stud' si 'catalog' in 'tabela1':", tabela1, sep="\n")
tabela2 = stud.merge(catalog,left_index=True,right_index=True,how="left")
print("\nJonctiune stanga prin merge dupa index intre 'stud' si 'catalog' :", tabela2, sep="\n")
tabela3 = stud.merge(catalog,left_index=True,right_index=True,how="right",indicator=True)
print("\nJonctiune dreapta prin merge dupa index intre 'stud' si 'catalog' cu indicator:", tabela3, sep="\n")
tabela4 = stud.merge(catalog,left_index=True,right_index=True,how="outer",indicator=True)
print("\nJonctiune stanga-dreapta prin merge dupa index intre 'stud' si 'catalog' cu indicator:", tabela4, sep="\n")

# exit(0)

# Pivotare
print("\n--Pivotare")
print("Tabel:", stud, "\n")
pivot = stud.pivot(columns="Grupa")
print("\nPivotare 'stud' dupa 'Grupa'", pivot, pivot.index, pivot.columns, sep="\n")

# exit(0)
# Liniarizare
print("\n--Liniarizare")
print("Tabel:", studenti, sep="\n")
print("\nLiniarizare 'student' dupa nivelul 1 in indexul de coloana:", studenti.melt(col_level=1), sep="\n")
print("\nLiniarizare coloane 'POO','Java' dupa 'Grupa' si 'Nume'",
      stud.melt(id_vars=['Grupa', 'Nume'], value_vars=['POO', 'Java']), sep="\n")

# exit(0)

print("\n--Creare tabel de contingenta", stud, sep="\n")
print(pd.crosstab(stud["Grupa"], stud["Java"], margins=True, margins_name="Totaluri", normalize="all"))

grupe = pd.Categorical(values=[1045, 1046, 1045, 1050, 1045, 1045, 1046, 1000, 1000], ordered=True)
print("\nVariabila categoriala 'grupe':", grupe, type(grupe), sep="\n")
print("\nCoduri asociate categoriilor variabilei 'grupe':", grupe.codes, type(grupe.codes), sep="\n")
print("\nAdaugare categorie 1070:\n", grupe.add_categories(new_categories=[1070]))
print("\nEliminare categorie 1000:\n", grupe.remove_categories(removals=[1000]))
print("\nEliminare categorii neutilizate:\n", grupe.remove_unused_categories())
