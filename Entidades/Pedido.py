from EnumsPedido import Estado,FormaPago
from Usuario import Usuario
from datetime import date
from Calculable import Calculable
from DetallePedido import DetallePedido
from Producto import Producto
from FoodStoreError import DatoInvalidoError, StockInsuficienteError
from Base import Base

class Pedido(Base):
    def __init__(self, usuario: Usuario, forma_pago: FormaPago) -> None:
        super().__init__()
        self.usuario = usuario
        self.forma_pago = forma_pago
        self.__fecha: date = date.today()
        self.__estado: Estado = Estado.PENDIENTE
        self.__total: float = 0
        self.__detalles: list[DetallePedido] = []
    @property
    def usuario(self) -> Usuario:
        return self.__usuario
    @property
    def forma_pago(self) -> FormaPago:
        return self.__forma_pago
    @property
    def fecha(self) -> date:
        return self.__fecha

    @property
    def estado(self) -> Estado:
        return self.__estado
    @property
    def total(self) -> float:
        return self.__total
    @property
    def detalles(self) -> tuple[DetallePedido, ...]:
        return tuple(self.__detalles)

    #------------------

    @usuario.setter
    def usuario(self, valor: Usuario) -> None:
        if not isinstance(valor, Usuario):
            raise DatoInvalidoError("El usuario debe ser una instancia de Usuario")
        if valor.eliminado:
            raise DatoInvalidoError("No se puede asignar un usuario eliminado")
        self.__usuario = valor
    @forma_pago.setter
    def forma_pago(self, valor: FormaPago) -> None:
        if not isinstance(valor, FormaPago):
            raise DatoInvalidoError("La forma de pago no es válida")
        self.__forma_pago = valor

    @estado.setter
    def estado(self, valor: Estado) -> None:
        if not isinstance(valor,Estado):
            raise DatoInvalidoError("este valor no es un estado valido")
        self.__estado = valor
    #-----------------------------------
    def buscar_detalle_por_producto(self, producto: Producto) -> DetallePedido | None:
        for i in self.__detalles:
            if i.producto == producto:
                return i
        return None
    def agregar_detalle(self, cantidad: int, producto: Producto) -> None:
        detalle_existente = self.buscar_detalle_por_producto(producto)
        if detalle_existente is not None:
            nueva_cantidad = detalle_existente.cantidad + cantidad
            if nueva_cantidad > producto.stock:
                raise StockInsuficienteError("No hay stock suficiente para cubrir la cantidad total.")
            detalle_existente.cantidad = nueva_cantidad
        else:
            self.__detalles.append(DetallePedido(cantidad, producto))
        self.calcular_total()
    def eliminar_detalle_por_producto(self, producto: Producto) -> None:
        x = self.buscar_detalle_por_producto(producto)
        if x is not None:
            self.__detalles.remove(x)
        else:
            raise DatoInvalidoError("No se pudo encontrar el producto buscado")
    def calcular_total(self) -> None:
        self.__total = sum(detalle.subtotal for detalle in self.__detalles)
    def __str__(self):
        return f"Usuario:{self.__usuario}|Forma de pago:{self.__forma_pago}|Estado:{self.__estado}|Fecha:{self.__fecha}|Total:{self.__total}$"