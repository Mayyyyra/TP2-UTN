from Entidades.Pedido import Pedido
from Entidades.Usuario import Usuario
from Entidades.Producto import Producto
from Entidades.EnumsPedido import Estado, FormaPago
from Servicios.ProductoServicio import ProductoServicio
from Exepciones.FoodStoreError import EntidadNoEncontradaError, OperacionNoPermitidaError, StockInsuficienteError

class PedidoServicio():
    def __init__(self) -> None:
        self.__pedidos: list[Pedido] = []

    @property
    def pedidos(self) -> tuple[Pedido, ...]:
        return tuple(self.__pedidos)

    def crear(self, usuario: Usuario, forma_pago: FormaPago, productos_y_cantidades: list[tuple[Producto, int]], prod_servicio: ProductoServicio) -> Pedido:
    
        nuevo_pedido = Pedido(usuario, forma_pago)
        
        for producto, cantidad in productos_y_cantidades:
            nuevo_pedido.agregar_detalle(cantidad, producto)
            
        for producto, cantidad in productos_y_cantidades:
            producto.stock -= cantidad
            
        self.__pedidos.append(nuevo_pedido)
        return nuevo_pedido

    def buscar_por_id(self, id_pedido: int) -> Pedido:
        for p in self.__pedidos:
            if p.id == id_pedido and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontró un pedido activo con ID {id_pedido}.")

    def listar(self) -> list[Pedido]:
        return [p for p in self.__pedidos if not p.eliminado]

    def listar_por_usuario(self, id_usuario: int) -> list[Pedido]:
        return [p for p in self.__pedidos if not p.eliminado and p.usuario.id == id_usuario]

    def actualizar_estado(self, id_pedido: int, nuevo_estado: Estado) -> None:
        pedido = self.buscar_por_id(id_pedido)
        estado_actual = pedido.estado
        if estado_actual == nuevo_estado:
            return

        if nuevo_estado == Estado.CONFIRMADO:
            if estado_actual != Estado.PENDIENTE:
                raise OperacionNoPermitidaError(f"No se puede pasar de {estado_actual.name} a {nuevo_estado.name}.")
                
        elif nuevo_estado == Estado.TERMINADO:
            if estado_actual != Estado.CONFIRMADO:
                raise OperacionNoPermitidaError(f"No se puede pasar de {estado_actual.name} a {nuevo_estado.name}.")
                
        elif nuevo_estado == Estado.CANCELADO:
            if estado_actual not in (Estado.PENDIENTE, Estado.CONFIRMADO):
                raise OperacionNoPermitidaError(f"No se puede cancelar un pedido en estado {estado_actual.name}.")
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
                
        elif nuevo_estado == Estado.PENDIENTE:
            raise OperacionNoPermitidaError("No se puede volver al estado PENDIENTE.")

        pedido.estado = nuevo_estado

    def eliminar(self, id_pedido: int) -> None:
        pedido = self.buscar_por_id(id_pedido)
        
        if pedido.estado not in (Estado.TERMINADO, Estado.CANCELADO):
            for detalle in pedido.detalles:
                detalle.producto.stock += detalle.cantidad
                
        for detalle in pedido.detalles:
            detalle.eliminar()
        pedido.eliminar()