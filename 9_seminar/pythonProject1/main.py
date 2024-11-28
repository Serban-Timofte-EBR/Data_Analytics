# Examen:

# Prima parte: pana in seminarul 5 (citit din csv + merges + functii de medii, curatare set de date) -> 2 subiecte
    # Curatare = valori lipsa inlocuite cu media celorlalte valori

# Standardizare de date

# ------------------- Pana in seminarul 4 si 5 -------------------

# Analiza in sine. Pana acum avem ACP + Factoriala de azi inceputa

# -------------- Info seminar: Analiza pe componente principala -----------------

# Reduce dimensiunea si ne arata informatii despre elementele analizei

# Se aplica cand avem mai mult de 2 variabile in setul nostru de date. Daca avem 2 variabile avem reprezentare 2D, daca avem 3 variabile, avem 3D. Pentru mai multe varibile devine si mai problematic.

# ACP -> face o combinatie liniara intre varibile. In loc de un grafic am 1 sau 2 componente principale pentru a putea face un grafic normal.

# In ACP primele 2 componente sunt cele mai importante. Fiecare punct din graficul final este un rand pentru setul nostru de date.

# Este important sa luam in ACP doar elemente numerice

# Avem testul Kaiser si Cattell pentru a ne spune cate combinatii liniare sunt bune pentru analiza. Adica numerul de componente in PCA

# Standardizarea ne aduce valorile la un numitor comun. Spre exemplu daca avem valori de lungime a petalei de 6 cm si de 100 de cm este greu de pus pe grafic. Noi practic prin standardizare aducem datele intr-un range comun pentru a putea fi reprezentate. Recomandare: Sa implementam noi functia de standardizare
        # Ii este mai usor algoritmului sa faca calculele

# De preferat este sa facem plot de varianta pentru a determina numarul de componente principale. De regula se ia 2, dar sunt foarte bune pentru validarec
