import builtins
import inspect

import functii


def sum(x):
    suma = 0
    for v in x:
        suma += v
    return suma + 20


x = [10, 20, 30, 1000]
# Acces la functia sum din spatiul builtins
suma = builtins.sum(x)
print(suma)
print(functii.sum(x))
print(sum(x))

print(inspect.currentframe().f_locals["sum"](x))
