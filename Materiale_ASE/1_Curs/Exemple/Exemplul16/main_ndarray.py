import numpy as np

# Instantiere prin initializatorul de clasa
buffer = bytearray(8)
buffer[5] = 1
print(buffer)
x = np.ndarray((2, 1), dtype=int, buffer=buffer)
print("Initializare prin buffer:")
print(x)

# Initializare prin functia array()
y = np.array([i for i in range(8)]).reshape((2, 4))
print("Initializare prin array() din lista:")
print(y)

# Initializare de matrice unitate
x_i = np.identity(5)
print("Matrice identitate:")
print(x_i)

# Initializare matrice diagonala
print("Matrice diagonala:")
x_d = np.diag([i for i in range(1, 6)])
print(x_d)

# Initializare aleatoare
print("Matrice initializata aleator:")
x_r = np.array(np.random.random(25) * 100, dtype=int).reshape((5, 5))
print(x_r)

# Indexarea masivelor
print("\n--Indexare")
print("Matrice:",x_r,sep="\n")
print("x_r[1,1],x_r[1][1]", x_r[1, 1], x_r[1][1])
print("x_r[1:,:3] = ", x_r[1:, :3])
print("x_r[1:][:3] = ", x_r[1:][:3])
print("x_r[1:] = ", x_r[1:])
x_copie = x_r[1:, :3]
x_copie[0, 0] = 1000
print("Modificare prin copie:")
print(x_r)

# Indexarea booleana
# Selectie elemente mai mari decat 50
print("\n--Indexarea booleana")
print("Selectie elemente mai mari decat 50:")
index_boolean = x_r > 50
print(index_boolean)
print("x_r[x_r>50] = ", x_r[index_boolean])

# Indexare prin masive
print("\n--Indexare prin masive")
print("Matrice:",x_r,sep="\n")
print("x_r[np.array([1,2])] = ", x_r[np.array([1, 2])],sep="\n")
index_matrice = np.array([1, 2, 3, 4]).reshape((2, 2))
print("index_matrice:",index_matrice)
print("x_r[index_matrice] : ", x_r[index_matrice],sep="\n")

# Indexare prin tupluri
print("\n--Indexare prin tupluri")
print("x_r[(1,2),(3,4)] = ", x_r[(1, 2), (3, 4)])
