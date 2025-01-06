class b():
    def __int__(self, v):
        print("Constructor b()")
        self.v = 500

    def afisare(self):
        print("afisare() in clasa b ")
        print("v=",self.v)

    def metoda_b(self):
        print("metoda_b")
        self.metoda_a() #Este referita metoda_a din clasa a prin self
        self.metoda_c() #Idem c

    def alta_metoda_b(self):
        print("alta_metoda_b")


class a():
    def __init__(self, v=1000):
        print("Constructor a()")
        self.v = v

    def afisare(self):
        print("afisare() in clasa a")
        print("v=",self.v)

    def metoda_a(self):
        print("metoda_a")
        self.alta_metoda_b() #Este referita alta_metoda_b


class c(a, b):
    def print_c(self):
        for clasa in self.__class__.__bases__:
            clasa.afisare(self)
        self.afisare()
        print("v=",self.v)
        self.metoda_b()

    def metoda_c(self):
        print("metoda_c")

    def print(self):
        print("__class__ :",self.__class__)
        print(self.__class__.__bases__)
        print(self.__class__.__dict__)
        print(self.__class__.__mro__)
