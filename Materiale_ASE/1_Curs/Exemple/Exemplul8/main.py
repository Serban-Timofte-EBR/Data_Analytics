import inspect
import math
import functii

a = math.pi

print("----> Membrii obiect real a:")
for v in inspect.getmembers(a):
    print(v)
print("----> Membrii modul math:")
for v in inspect.getmembers(math):
    print(v)
print("----> Membrii functii din modulul functii:")
for v in inspect.getmembers(functii,inspect.isfunction):
    print(v)
print("----> Informatii modul math:",inspect.getdoc(math))
print("----> Cod functie adunare din modulul functii:",inspect.getsource(functii.adunare),sep="\n")
print("----> Parametrii functiei sum din builtins:",inspect.signature(sum))
