import cx_Oracle
import pandas as pd
import getpass


freelancer = pd.read_csv("FreeLancerT.csv",na_values="",keep_default_na=False)
n = len(freelancer)
l_freelancer = list()
for k in freelancer.index:
    linie = tuple(freelancer.loc[k,:])
    l_freelancer.append(linie)
parola = getpass.getpass(prompt="Parola:")
# con = cx_Oracle.connect('furtuna_felix/'+parola+'@193.226.34.57/oradb')
con = cx_Oracle.connect('titus/'+parola+'@2001b-04/orcl')
cursor = con.cursor()
cursor.execute("SELECT * FROM user_tables WHERE table_name = UPPER('t_freelancer')")
tabela = cursor.fetchone()
if tabela is None:
    print("Creare tabela t_freelancer ...")
    cerere = "create table t_freelancer ( country varchar2(50), countrycode varchar2(10),continent varchar2(10),c decimal(10,5),c_test decimal(10,5),html decimal(10,5),html_test decimal(10,5),java decimal(10,5),java_test decimal(10,5),php decimal(10,5),php_test decimal(10,5))"
    cursor.execute(cerere)
else:
    #     Stergere
    print("Exista tabela t_freelancer. Stergere inregistrari ...")
    comanda_stergere = "delete from T_FREELANCER"
    cursor.execute(comanda_stergere)
con.commit()
print("Adaugare inregistrari ...")
cursor.executemany("insert into t_freelancer(country,countrycode,continent,c,c_test,html,html_test,java,java_test,php,php_test) values (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)", l_freelancer)
con.commit()
print("Interogare baza de date ...")
comanda_interogare = "select * from t_freelancer"
cursor.execute(comanda_interogare)
for i in cursor:
    print(i)
cursor.close()
con.close()
