from Base import Base

from FoodStoreError import DatoInvalidoError
class Categoria(Base):
    def __init__(self,nombre:str,descripcion:str) -> None:
        super().__init__()
        self.nombre = nombre
        self.descripcion = descripcion
        
    #---------
    @property
    def nombre(self) -> str:
        return self.__nombre
    @property
    def descripcion(self) -> str:
        return self.__descripcion
    #-----------
    @nombre.setter
    def nombre(self,valor:str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("Este valor esta vacio")
        self.__nombre = valor.strip()

    @descripcion.setter
    def descripcion(self,valor:str) -> None:
        if not valor.strip():
            raise DatoInvalidoError("Este valor esta vacio")
        self.__descripcion = valor.strip()
    #-----------
    def __str__(self) -> str:
        return f"Categoria:{self.__nombre} | Desc.:{self.__descripcion}"