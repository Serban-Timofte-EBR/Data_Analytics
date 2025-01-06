import pandas as pd
from grafice import *

t = pd.read_csv("Teritorial.csv", index_col=1)
variabile = list(t)
variabile_1 = variabile[:3]
variabile_2 = variabile[3:]
print(variabile_1, variabile_2, sep="\n")

scatterplot_sb(t,'PAVeg', 'PAAnim')
scatterplot_sb(t,'PAVeg', 'PAAnim', "Regiunea")
scatterplot_sb(t,'PAVeg', 'PAAnim', "Regiunea","Macroregiunea")

r = t[variabile_2].corr()
heatmap(r,-1,1,"Corelograma")

histograma(t,['PAVeg', 'PAAnim', 'ServAgr'])
histograma2(t,['PAVeg', 'PAAnim', 'ServAgr'])

distributie(t,['PAVeg', 'PAAnim', 'ServAgr'])
distributie2D(t,'PAVeg','PAAnim')


boxplot(t,['PAVeg', 'PAAnim', 'ServAgr'])
boxplot_sb(t,['PAVeg', 'PAAnim', 'ServAgr'])
boxplot_sb(t,['PAVeg', 'PAAnim', 'ServAgr'],by1="Regiunea")
boxplot_sb(t,['PAVeg', 'PAAnim', 'ServAgr'],by1="Regiunea",by2="Macroregiunea")

catplot(t,"PIB")
catplot(t,"PIB",by1="Regiunea")
catplot(t,"PIB",by1="Regiunea",by2="Macroregiunea")

pie(t, "PIB")
pie(t, "PIB", "Regiunea")

count_chart(t,"PIB")
count_chart(t,"PIB",by="Regiunea")

mozaic(t,"PIB","Regiunea")
mozaic(t,"PIB","SalNet")


alro = pd.read_csv("Alr.csv").head(550)
variabile = list(alro)
var_data = variabile[0]
var_preturi = ["Desch", "Maxim", "Minim", "Inchid", "Volum"]

alro.index = pd.to_datetime(alro[var_data])

t_curs = alro[var_preturi]
start = pd.to_datetime("2011-01-04", format="%Y-%m-%d")
stop = pd.to_datetime("2011-02-04", format="%Y-%m-%d")
t_curs.columns = ["Open", "High", "Low", "Close", "Volume"]

t_curs_ = t_curs.loc[start:stop, :]
candle(t_curs, titlu="Cotatii ALRO")
candle(t_curs_,titlu="Cotatii ALRO")
candle(t_curs,titlu="Cotatii ALRO",volume=True)
candle(t_curs_,titlu="Cotatii ALRO",volume=True)
