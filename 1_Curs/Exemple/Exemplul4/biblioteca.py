
class publicatie():
    def __init__(self,titlu):
        # Creare atribut titlu
        self.titlu = titlu

    def __str__(self):
        return self.titlu

class carte(publicatie):
    def __init__(self,titlu,autori,numar_volume):
        super().__init__(titlu)
        self.__autori = autori
        self.__numar_volume = numar_volume

    def __str__(self):
        return self.titlu+","+self.__autori+","+str(self.__numar_volume)

    def get_autori(self):
        return self.__autori

    def set_autori(self,autori):
        self.__autori=autori

    @property
    def nr_vol(self):
        return self.__numar_volume

    @nr_vol.setter
    def nr_vol(self,numar_volume):
        self.__numar_volume=numar_volume



