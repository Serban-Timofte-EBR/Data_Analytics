import sqlite3

con = sqlite3.connect("curs6.db")
cursor = con.cursor()
cursor.execute("SELECT name FROM sqlite_master")
exista_tabela = False
for tabela in cursor:
    if tabela[0] == "studenti":
        exista_tabela = True
if exista_tabela:
    print("Exista tabela ", tabela[0])
    print("Stergere tabela ...")
    cursor.execute("drop table studenti")
print("Creare tabela studenti ...")
comanda_creare = "create table studenti (nume varchar(50),media decimal(5,2))"
cursor.execute(comanda_creare)
inregistrari = [['Popescu Diana', 9.5], ['Ionescu Dan', 8.90]]
comanda_adaugare = "INSERT INTO studenti VALUES(?,?)"
for i in inregistrari:
    cursor.execute(comanda_adaugare, i)
cursor.execute("select * from studenti")
con.commit()

print("Continut tabela:")
rows = cursor.fetchall()
for i in rows:
    print(i)
cursor.close()
con.close()
