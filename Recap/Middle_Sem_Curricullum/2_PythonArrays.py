def create_arr(start, end):
    """
    Creează o listă de numere între `start` și `end`.

    Parametri:
        start: Începutul intervalului (inclusiv).
        end: Sfârșitul intervalului (inclusiv).

    Returnează:
        Lista de numere între `start` și `end`.
    """
    arr = []
    for number in range(start, end + 1):
        arr.append(number)
    return arr

arr = create_arr(1, 20)
print("Lista generata: " + str(list))

# Extragem doar numerele pare folosind un lambda function

listNrPare = list(filter(lambda nr : nr % 2 == 0, arr))
print("Lista doar cu numere pare: " + str(listNrPare))