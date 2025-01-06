import random
import sys

print("----> Parametrii liniei de comanda:")
for p in sys.argv:
    print(p)

print("----> byteorder:",sys.byteorder)
b = int(random.random() * 10)
if b % 2 == 0:
    sys.exit("Numar par!")
print("----> Numar generat aleator:",b)
print("Sizeof b:", sys.getsizeof(b))
print("----> Module active:")
for modul in sys.modules.copy():
    print(modul, type(sys.modules.copy()[modul]))
print("----> Path module:")
for cale in sys.path:
    print(cale)
