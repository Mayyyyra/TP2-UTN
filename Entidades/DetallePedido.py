from Entidades.Base import Base
from Exepciones.FoodStoreError import DatoInvalidoError
from Entidades.Producto import Producto
class DetallePedido(Base):
    def __init__(self,cantidad:int,producto:Producto) -> None:
        super().__init__()
        self.producto = producto
        self.cantidad = cantidad
        self.subtotal = self.cantidad * self.producto.precio
#------------
    @property
    def cantidad(self) -> int:
        return self.__cantidad
    @property
    def subtotal(self) -> float:
        return self.__subtotal
    @property
    def producto(self) -> Producto:
        return self.__producto
#---------------
    @cantidad.setter
    def cantidad(self,valor) -> None:
        if not isinstance(valor,int):
            raise DatoInvalidoError("la cantidad debe ser un int")
        if valor <= 0:
            raise DatoInvalidoError("este valor no puede ser menor a 0")
        self.__cantidad = int(valor)
        self.subtotal = self.cantidad * self.producto.precio
    @producto.setter
    def producto(self,valor) -> None:
        if not isinstance(valor,Producto):
            raise DatoInvalidoError("este valor necesita ser un producto valido")
        if valor.eliminado:
            raise DatoInvalidoError("No se puede asignar un producto eliminado.")
        self.__producto = valor



    @subtotal.setter
    def subtotal(self,valor) -> None:
        if not isinstance(valor,(int,float)):
            raise DatoInvalidoError("la cantidad debe ser un numero")
        if valor < 0:
            raise DatoInvalidoError("este valor no puede ser negativo")
        self.__subtotal = float(valor)

    def __str__(self) -> str:
        return f"{self.__cantidad}x {self.__producto.nombre} |Subtotal:{self.__subtotal}"