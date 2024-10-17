def calcul_indicatori(tabel, variabile_numerice):
    # Medie
    # Standard Deviation
    # Covarianta

    # Verificam daca tabelul nostru este dictionar
    try:
        assert isinstance(tabel, dict)

        t = {}
    except AssertionError:
        return