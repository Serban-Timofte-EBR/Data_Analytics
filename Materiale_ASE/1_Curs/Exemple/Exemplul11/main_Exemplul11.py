# Exemplu type si zip
# type - crearea si instantierea dinamica a unei clase
def constructor(self, nume_, grupa_):
    self.nume = nume_
    self.grupa = grupa_


def afisare(self):
    return self.nume + "," + str(self.grupa)


clasa_student = type("student", (object,), {
    "__init__": constructor,
    "__str__": afisare
})

print(type(clasa_student))
obiect_student = clasa_student("Popa Mihai", 1120)
print(type(obiect_student))
print(obiect_student)
print(obiect_student.grupa)

# Exemplu zip
nume = ["Popescu Diana", "Moldovan Mihai", "Pop Adrian"]
varsta = [20, 34, 45]
localitate = ("Bucuresti", "Covasna", "Brasov")

for i in zip(nume, varsta, localitate):
    print(type(i), i)
