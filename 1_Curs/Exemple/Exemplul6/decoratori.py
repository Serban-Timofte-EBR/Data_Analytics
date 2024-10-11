def decorator_medie(functie):
    def suma_media(x):
        rez = functie(x)
        return rez, rez / len(x)

    return suma_media
