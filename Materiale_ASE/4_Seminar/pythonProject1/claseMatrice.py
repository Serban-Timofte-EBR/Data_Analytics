from array import array


class matrice_rara():
    def __init__(self, i, j, x, n, m):
        if not isinstance(i, (list, tuple, array)):
            raise Exception("Tip nepermis pentru indecsii de linie!")
        if not isinstance(j, (list, tuple, array)):
            raise Exception("Tip nepermis pentru indecsii de coloana!")
        if not isinstance(x, (list, tuple, array)):
            raise Exception("Tip nepermis pentru valori!")
        if len(i) != len(x) or len(j) != len(x):
            raise Exception("Dimensiuni incorecte!")
        if max(i) >= n or max(j) >= m:
            raise Exception("Valori incorecte pentru m sau n!")
        self.__i = array("i", i)
        self.__j = array("i", j)
        self.__x = array("d", x)
        self.__n = n
        self.__m = m

    @property
    def i(self):
        return self.__i

    @property
    def j(self):
        return self.__j

    @property
    def x(self):
        return self.__x

    @property
    def n(self):
        return self.__n

    @property
    def m(self):
        return self.__m

    @n.setter
    def n(self, n):
        if max(self.__i) >= n:
            raise Exception("Valoare incorecta pentru n!")
        self.__n = n

    @m.setter
    def m(self, m):
        if max(self.__j) >= m:
            raise Exception("Valoare incorecta pentru m!")
        self.__m = m

    def __str__(self):
        out = []
        for v in zip(self.__i, self.__j, self.__x):
            out.append(v)
        return str(out) + str((self.__n, self.__m))

    def __eq__(self, other):
        assert isinstance(other, matrice_rara)
        # return self.__i==other.__i and self.__j==other.__j and self.__x==other.__x and self.__n==other.__n and self.__m==other.__m
        l_self = sorted(zip(self.__i, self.__j, self.__x), key=lambda x: x[2])
        l_other = sorted(zip(other.__i, other.__j, other.__x), key=lambda x: x[2])
        return l_self == l_other

    def add(self, i, j, x):
        self.__i.append(i)
        self.__j.append(j)
        self.__x.append(x)

class matrice_diagonala(matrice_rara):
    def __init__(self, x):
        if not isinstance(x, (list, tuple, array)):
            raise Exception("Tip nepermis pentru valori!")
        super().__init__([v for v in range(len(x))], [v for v in range(len(x))],
                         x, len(x), len(x))
