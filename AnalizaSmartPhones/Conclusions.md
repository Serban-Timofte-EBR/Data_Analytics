### Analiza pe componente principale

#### **Introducere**
Analiza pe Componente Principale (ACP) a fost folosită pentru a simplifica interpretarea dataset-ului nostru, reducând numărul de variabile. Prin această metodă, am urmărit să identificăm tipare în date și să înțelegem mai bine relațiile dintre variabile. Graficele prezentate mai jos arată cum contribuie fiecare componentă la explicația variației și cum sunt distribuite observațiile în spațiul redus al primelor două componente principale (PC1 și PC2).

---

#### **Analiza varianței explicate**
![Variance](data/pca/PCA_VARIANCE.png)

Graficul varianței arata că primele două componente principale sunt cele mai relevante. PC1 acaparează cea mai mare parte a variației din dataset, ceea ce înseamnă că există o relație principală între variabilele noastre. Pe scurt, majoritatea informației poate fi descrisă eficient folosind această primă componentă. 

PC2 adaugă o perspectivă complementară, scoțând în evidență detalii suplimentare care nu sunt surprinse de PC1. După aceste două componente, contribuția celorlalte scade considerabil, ceea ce face ca reducerea dataset-ului la doar două dimensiuni să fie atât practică. Practic, putem analiza datele într-un mod mai simplu fără a pierde informații esențiale.

---

#### **Analiza distribuției în spațiul PCA**
![Scatter](data/pca/PCA_SCATTER_PLOT.png)

Graficul de dispersie al datelor în funcție de PC1 și PC2 arată o separare clară între mai multe clustere. Aceste clustere ne arată că există similarități evidente între observațiile din același grup, ceea ce sugerează că variabilele contribuie semnificativ la crearea acestor tipare. De exemplu, în cazul unor grupuri distincte, putem deduce că există caracteristici comune care diferențiază datele într-un mod logic și coerent.

Mai mult decât atât, distanțele dintre clustere indică faptul că avem categorii bine delimitate (între galben, verde și celelalte clustere). Asta arată că dataset-ul nostru nu este "zgomotos" și că există relații consistente între variabile. În același timp, punctele care apar izolate în afara clusterelor principale (observațiile atipice) sunt semnale importante. Acestea pot reprezenta cazuri speciale sau extreme, care fie trebuie analizate separat, fie corectate dacă sunt erori.

---

#### **Concluzii**
Această analiză arată clar că dataset-ul nostru este structurat și poate fi bine descris prin doar două componente principale, fără a pierde informații importante. PC1 și PC2 explică cea mai mare parte a variației, ceea ce face analiza mai eficientă și mai ușor de interpretat. Este evident că variabilele contribuie în mod semnificativ la formarea clusterelor, ceea ce sugerează tipare clare în date.

Clusterele evidențiate în grafic ne oferă informații despre cum sunt grupate observațiile și ce relații există între variabile. Aceste grupuri pot reprezenta categorii sau tipologii relevante pentru setul nostru de date. În plus, observațiile atipice merită analizate mai departe, deoarece ar putea ascunde informații valoroase despre cazuri speciale sau situații rare.

Pe scurt, ACP ne-a ajutat să evidențiem structura dataset-ului și să identificăm tipare în date. Aceste concluzii oferă un punct de plecare pentru analize viitoare.