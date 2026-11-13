import Base
import Categoria
class Producto(Base):
    def __init__(self,nombre:str,precio:float,descripcion:str,stock:int,imagen:str,disponible:bool):
        self.__nombre = nombre
        self.__precio = precio
        self.__descripcion = descripcion
        self.__stock = stock
        self.__imagen = imagen
        self.__disponible = True
        self.__Categoria = None
        super().__init__(Base)
    @property
    def Categoria(self):
        return self.__Categoria
    @Categoria.setter
    def Categoria(self,Cat):
        if isinstance(Cat,Categoria):
            self.__Categoria = Cat
    def __str__(self):
        return f"Nombre:{self.__nombre}|Precio:{self.__precio}|Desc.:{self.__descripcion}|stock:{self.__stock}|disponible:{self.__disponible}"