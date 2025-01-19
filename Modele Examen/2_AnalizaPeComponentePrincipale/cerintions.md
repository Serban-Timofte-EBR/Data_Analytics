# Subiect Examen

## A. Analiza populației naturale și a altor caracteristici demografice

În fișierul `MiseNatPopTari.csv` este prezentată populația naturală și alte caracteristici demografice pentru diferite țări, pe ani. În fișierul `CoduriTariExtins.csv` se află codificări ale țărilor și împărțirea acestora pe continente.

### Cerințe:

1. **Calcularea mediei populației naturale pentru fiecare țară**
   - Calculați media populației naturale pe întreaga perioadă analizată pentru fiecare țară.
   - Se va salva un fișier `cerinta1.csv` cu următoarele coloane:
     - `Code` - Codul țării
     - `Medie` - Media populației naturale

     **Exemplu:**
     ```
     Code,Medie
     AFG,1.25
     ALB,0.73
     ```

2. **Determinarea continentului cu cea mai mare medie**
   - Determinați continentul care are cea mai mare medie a populației naturale și anul în care această medie a fost maximă.
   - Se va salva un fișier `cerinta2.csv` cu următoarele coloane:
     - `Continent_Name` - Numele continentului
     - `Anul` - Anul în care s-a înregistrat media maximă

     **Exemplu:**
     ```
     Continent_Name,Anul
     Europe,2015
     ```

---

## B. Analiza PCA pentru populația naturală a țărilor

1. **Preprocesarea datelor**:
   - Standardizați valorile populației naturale pentru fiecare țară.

2. **Calcularea PCA**:
   - Determinați numărul de componente principale care explică cel puțin 90% din variația datelor.
   - Se va salva un fișier `pca_variance.csv` cu următoarele coloane:
     - `Component` - Componenta principală
     - `Explained_Variance` - Procentul de variație explicat de componenta respectivă

     **Exemplu:**
     ```
     Component,Explained_Variance
     PC1,0.55
     PC2,0.30
     ```

3. **Proiectarea datelor**:
   - Proiectați datele inițiale în spațiul redus la două componente principale.
   - Se va salva un fișier `pca_projection.csv` cu următoarele coloane:
     - `Country` - Țara
     - `PC1` - Valoarea primei componente principale
     - `PC2` - Valoarea celei de-a doua componente principale

     **Exemplu:**
     ```
     Country,PC1,PC2
     Afghanistan,2.31,-1.47
     Albania,-0.98,0.56
     ```

4. **Vizualizarea datelor proiectate**:
   - Realizați un scatter plot al primelor două componente principale, colorat pe continente.

---

### Criterii de acordare a punctajului
- Fișierele generate să fie corect create și să conțină informațiile solicitate.
- Graficele să fie corect realizate și lizibile.
