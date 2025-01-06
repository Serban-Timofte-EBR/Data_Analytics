
def sum(x):
    def calcul(x, y):
        return x + y

    suma = 0
    for v in x:
        suma = calcul(suma, v)
    return suma
