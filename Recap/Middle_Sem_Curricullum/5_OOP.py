from abc import abstractmethod
from pydoc import describe


# 1. Abstractizare: Clasa abstractă Vehicul
class Vehicle():
    def __init__(self, make, model, year):
        self.make = make    # Variabile protejate (încapsulare)
        self.model = model
        self.year = year

    # Getter pentru brand
    def get_brand(self):
        return self._brand

    # Setter pentru viteza maximă
    def set_viteza_maxima(self, viteza):
        if viteza > 0:
            self._viteza_maxima = viteza
        else:
            raise ValueError("Viteza maximă trebuie să fie pozitivă!")

    @abstractmethod
    def describe(self):
        pass

# 2. Moștenire: Clasa Masina extinde Vehicul
class Car(Vehicle):
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year

    # Implementare metodă abstractă
    def describe(self):
        return f"Masina {self._brand} {self._model} cu {self._numar_usi} uși are o viteză maximă de {self._viteza_maxima} km/h."

# 3. Moștenire: Clasa Motocicleta extinde Vehicul
class Motocicleta(Vehicle):
    def __init__(self, brand, model, viteza_maxima, tip_motocicleta):
        super().__init__(brand, model, viteza_maxima)
        self._tip_motocicleta = tip_motocicleta

    # Implementare metodă abstractă
    def descrie(self):
        return f"Motocicleta {self._brand} {self._model} de tip {self._tip_motocicleta} are o viteză maximă de {self._viteza_maxima} km/h."

# 4. Polimorfism: Funcție care folosește descrierea vehiculelor
def afiseaza_vechicul():
    print(Vehicle.describe())
