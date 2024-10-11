def calcule(x, y=20):
    return x + y, x * y, x - y


def initializare(x):
    if isinstance(x, list):
        for i in range(0, len(x)):
            x[i] = 1000
    else:
        x = 10


a, b, c = calcule(y=10, x=20)
print(a, b, c)
v = calcule(10)
print(v)
x = [1, 2, 3, 5]
y = 1
initializare(x)
initializare(y)
print(x, y, sep="\n")
