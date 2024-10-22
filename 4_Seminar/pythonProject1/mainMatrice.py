from claseMatrice import *

try:
    a = matrice_rara([10, 0, 20], [15, 0, 25], (200, 100, 300), 25, 40)
    print("a:", a)
    print("Indecsi linie:", a.i)
    # a.n = 50
    b = matrice_diagonala([111, 222, 888, 999])
    print("Matricea diagonala b:", b)
    c = matrice_rara([0, 10, 20], [0, 15, 25], (100, 200, 300), 25, 40)
    print("Egalitate intre a si c:", a == c)
except Exception as ex:
    print("Eroare!!!", ex.with_traceback(), sep="\n")
