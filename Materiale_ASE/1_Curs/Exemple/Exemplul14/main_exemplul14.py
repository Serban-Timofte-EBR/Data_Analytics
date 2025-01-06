class student():
    def __init__(self, nume_, grupa_):
        self.nume = nume_
        self.grupa = grupa_

    def __str__(self):
        return self.nume + "," + str(self.grupa)


lista_studenti = [student("Pop Adrian", 1084),
                  student("Manea Iopana", 1091),
                  student("Ionescu Diana", 1082)]
lista_studenti.insert(2, student("Popescu Mihai", 1086))
lista_studenti.append(student("Muntean Mihaela", 1120))

print("Lista studenti:")
for s in lista_studenti:
    print(s)

lista_studenti.sort(key=lambda x: x.grupa)
print("Lista studenti sortata dupa grupa:")
for s in lista_studenti:
    print(s)
lista_studenti.sort(key=lambda x: x.nume)
print("Lista studenti sortata alfabetic:")
for s in lista_studenti:
    print(s)
