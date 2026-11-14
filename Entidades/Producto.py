from Base import Base
from Categoria import Categoria
from ..Exepciones.FoodStoreError import DatoInvalidoError
class Producto(Base):
    def __init__(self,nombre:str,precio:float | int,descripcion:str,stock:int,imagen:str, categoria:Categoria | None, disp:bool = True) -> None:
        super().__init__()
        self.nombre = nombre    
        self.precio = precio
        self.descripcion = descripcion
        self.stock = stock
        self.imagen = imagen
        self.disponible:bool = disp
        self.categoria = categoria

    #-------------
    @property
    def stock(self) -> int:
        return self.__stock
    @property
    def precio(self) -> float:
        return self.__precio
    @property
    def imagen(self) -> str:
        return self.__imagen
    @property
    def disponible(self) -> bool:
        return self.__disponible
    @property
    def nombre(self) -> str:
        return self.__nombre
    @property
    def descripcion(self) -> str:
        return self.__descripcion
    @property
    def categoria(self) -> Categoria | None:
        return self.__categoria
    #--------------
    @stock.setter
    def stock(self,valor) -> None:
        if not isinstance(valor,int):
            raise DatoInvalidoError("El valor del stock debe ser un int")
        if valor < 0:
            raise DatoInvalidoError("este valor no puede ser negativo")
        self.__stock = int(valor)
    @precio.setter
    def precio(self,valor) -> None:
        if not isinstance(valor,(int,float)):
            raise DatoInvalidoError("el precio debe ser un float o un int")
        if valor < 0:
            raise DatoInvalidoError("este valor no puede ser negativo")
        self.__precio = float(valor)
    @imagen.setter
    def imagen(self,valor) -> None:
        if not valor.strip():
            raise DatoInvalidoError("El valor esta vacio")
        self.__imagen = valor.strip()
    @disponible.setter
    def disponible(self,valor) -> None:
        if not isinstance(valor,bool):
            raise DatoInvalidoError(f"El valor {valor} no es valido, solo se acepta True/False")
        self.__disponible = valor
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
    @categoria.setter
    def categoria(self,other) -> None:
        if other is None:
            self.__categoria = None
            return
        if not isinstance(other,Categoria):
            raise DatoInvalidoError("el valor no es una categoria valida")
        if other.eliminado:
            raise DatoInvalidoError("No se puede asignar una categoría eliminada.")
        self.__categoria = other


    def __str__(self) -> str:
        if self.categoria is not None:
            return f"Nombre:{self.nombre}|Precio:{self.__precio}|Desc.:{self.__descripcion}|stock:{self.__stock}|disponible:{self.__disponible}|\nID:{self.id}|Categoria:{self.__categoria.__nombre}"
        else:
            return f"Nombre:{self.nombre}|Precio:{self.__precio}|Desc.:{self.__descripcion}|stock:{self.__stock}|disponible:{self.__disponible}|\nID:{self.id}|Categoria:Sin categoria"