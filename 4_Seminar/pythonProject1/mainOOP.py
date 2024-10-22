from abc import abstractmethod

print("OOP in Python\n")

class Animal:
    def __init__(self, name = "", age = 0):   # atributele din constructor sunt privati + Semnul = tine loc de constructor default
        self.name = name
        self.age = age

    def speak(self):
        print("Generic animal sound!")

    @abstractmethod
    def moves(self):
        print("Moving")

    # Echivalentul functiei abstracta
    # def moves(self):
    #     pass

# Mostenirea
class Dog(Animal):          # public Dog extends Animal (in Java)
    def speak(self):
        print("Ham Ham!")

animal1 = Animal("Animal Generic", 10)

# print(animal1)  # Printeaza adresa de memorie

print(animal1.name)
print(animal1.age)

dog1 = Dog("Eusebius", 5)
dog1.speak()