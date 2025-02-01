# se efectueze diagnosticarea stärii pacientilor unui spital aflati in blocul post-operator utilizând metode de clasificare. Variabilele predictor sunt codificäri numerice ale unor masurätori cum ar fi: L-CORE - temperatura internã a pacientului in grade Celsius, L-SURF - temperatura la suprafatá a pacientului in grade Celsius, L-02 - saturafia in oxigen, L-BP - ultima misurare a presiunii sângelui, SURF-STBL - stabilitatea temperaturii externe a pacientului, CORE-STBL - stabilitatea temperaturii interne a pacientului, BP-STBL -
# stabilitatea presiunii
# sângelui. Variabila fintă este DECISION, care poate avea 3 valori: / - pacientul a fost trimis la sectia de ingrijire intensiva, S - pacientul a fost externat, A - pacientul a fost trimis la sectia de ingrijire generala.
# Setul de inväfare-testare este Paclenti.csv. Setul de aplicare este Pacienti_apply.csv.

import pandas as pd
import numpy as np
import seaborn as sb
import matplotlib.pyplot as plt
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.metrics import confusion_matrix, accuracy_score
from sklearn.model_selection import train_test_split

from sklearn.preprocessing import StandardScaler

# 1. Citirea seturilor de date
df_pacienti = pd.read_csv("data/Pacienti.csv")
df_apply = pd.read_csv("data/Pacienti_apply.csv")

print("Datele din Pacienti.csv:")
print(df_pacienti.head())
print("Datele din Pacienti_apply.csv:")
print(df_apply.head())

# 2. Curățarea datelor
def cleanData(df):
    if df.isna().any().any():
        for col in df.columns:
            if pd.api.types.is_numeric_dtype(df[col]):
                df[col] = df[col].fillna(df[col].mean())
            else:
                df[col] = df[col].fillna(df[col].mode()[0])
    return df

df_pacienti_cleaned = cleanData(df_pacienti)
df_apply_cleaned = cleanData(df_apply)

# 3. Separarea variabilelor
variabile_independente = df_pacienti_cleaned.columns[1:-1]
print("Variabile independente: ", variabile_independente)

X = df_pacienti_cleaned[variabile_independente]
Y = df_pacienti_cleaned["DECISION"]

# 4. Standardizare
scaler = StandardScaler()
X = scaler.fit_transform(X)
X_apply = scaler.fit_transform(df_apply_cleaned[variabile_independente])

# 5. Impartirea datelor
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

# 6. Analiza Discriminanta
modelLDA = LinearDiscriminantAnalysis()
modelLDA.fit(X_train, Y_train)

# Scorurile discriminante
X_train_lda = modelLDA.transform(X_train)
X_test_lda = modelLDA.transform(X_test)

# 7. Evaluarea modelului
Y_pred = modelLDA.predict(X_test)
conf_matrix = confusion_matrix(Y_test, Y_pred)
print("Matricea de confuzie (LDA):\n", conf_matrix)

accuracy = accuracy_score(Y_test, Y_pred)
print("Acuratețea globală (LDA):", accuracy)

accuracy_per_class = conf_matrix.diagonal() / conf_matrix.sum(axis=1)
accuracy_mean = np.mean(accuracy_per_class)
print("Accuraccy mean: ", accuracy_mean)

# Vizualizarea distributiilor pe axele discriminante:
for label in np.unique(Y_train):
    sb.kdeplot(X_train_lda[Y_train == label, 0], label=label)
plt.title("Distribuția pe axa discriminantă 1")
plt.xlabel("Axa discriminantă 1")
plt.legend()
# plt.show()

# 8. Predictia pe setul de date de aplicare
Y_apply_pred = modelLDA.predict(X_apply)
df_apply_cleaned["Predicted Decision"] = Y_apply_pred
df_apply_cleaned.to_csv("data/AppliedDecision.csv")

# Vizualizare in spatiul discriminant nu are logica
# plt.figure(figsize=(10, 6))
# for label, marker, color in zip(np.unique(Y_train), ['o', 'x', 's'], ['blue', 'red', 'green']):
#     indices = np.where(Y_train == label)
#     plt.scatter(X_train_lda[indices, 0], X_train_lda[indices, 1],
#                 label=f"Clasa {label}", marker=marker, color=color)
#
# plt.title("Instanțele în spațiul discriminant (LDA)")
# plt.xlabel("Axa discriminantă 1")
# plt.ylabel("Axa discriminantă 2")
# plt.legend()
# plt.grid()
# plt.show()