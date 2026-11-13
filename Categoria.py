import Base
import Producto

class categoria(Base):
    def __init__(self,nombre:str,descripcion:str):
        self.__nombre = nombre
        self.__descripcion = descripcion
        self.__Lista:Producto = []
        super().__init__(Base)
    def __aniadir_producto__(self,Prod):
        if isinstance(Prod,Producto):
            if Prod in self.__Lista:
                raise ValueError("El producto ya esta en la lista")
            if Prod.disponible == False:
                raise ValueError("El producto no esta disponible")
            self.__Lista.append(Prod)
            Prod.Categoria = self
    def __str__(self):
        raise NotImplementedError