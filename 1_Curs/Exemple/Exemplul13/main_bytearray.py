# Initializare cu 0 - obiect cu 10 octeti
x = bytes(10)
print("x:", x)
y = b"abcdabdfrtabe"
print("y:", y, ", y split dupa 'ab' :", y.rsplit(b"ab"))
z = bytearray(b'1234567')
print("z:", z)
# Afisare element cu element cod ASCI
print("z element cu element:")
for v in z:
    print(v, end=" ")
z.append(56)
print("\nAdaugare caracter cu cod ASCI 56:", z)
# Adaugare caracter 'A' specificandu-i codul ASCI
z.append(ord('A'))
print(z)
# Stergere caracter '4' specificandu-i codul ASCI
z.remove(ord('4'))
print(z)
# Inlocuire octeti de la 1 la 3
z[1:4] = [100, 101, 102]
print(z)
# Stergere in interval
del z[1:5]
print(z)
