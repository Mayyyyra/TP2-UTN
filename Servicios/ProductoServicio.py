from Entidades.Producto import Producto
from Servicios.CategoriaServicio import CategoriaServicio
from Exepciones.FoodStoreError import EntidadNoEncontradaError
class ProductoServicio():
    def __init__(self) -> None:
        self.__productos: list[Producto] = []

    @property
    def productos(self) -> tuple[Producto, ...]:
        return tuple(self.__productos)

    def crear(self, nombre: str, precio: float, descripcion: str, stock: int, imagen: str, disponible: bool, id_categoria: int, cat_servicio: CategoriaServicio) -> Producto:
        if id_categoria == 0:
                    categoria = None
        else:
            categoria = cat_servicio.buscar_por_id(id_categoria)
        
        nuevo_producto = Producto(nombre, precio, descripcion, stock, imagen, categoria, disponible)
        
        self.__productos.append(nuevo_producto)
        return nuevo_producto

    def buscar_por_id(self, id_producto: int) -> Producto:
        for p in self.__productos:
            if p.id == id_producto and not p.eliminado:
                return p
        raise EntidadNoEncontradaError(f"No se encontró un producto activo con ID {id_producto}.")

    def listar(self) -> list[Producto]:
        return [p for p in self.__productos if not p.eliminado]

    def listar_disponibles(self) -> list[Producto]:
        return [p for p in self.__productos if not p.eliminado and p.disponible and p.stock > 0]

    def editar(self, id_producto: int, nombre: str | None = None, precio: float | None = None, 
            descripcion: str | None = None, stock: int | None = None, 
            imagen: str | None = None, disponible: bool | None = None, 
            id_categoria: int | None = None, cat_servicio: CategoriaServicio | None = None) -> None:
    
        producto = self.buscar_por_id(id_producto)

        if id_categoria is not None and cat_servicio is not None:
            if id_categoria == 0:
                producto.categoria = None
            else:
                nueva_categoria = cat_servicio.buscar_por_id(id_categoria)
                producto.categoria = nueva_categoria

        if nombre is not None: producto.nombre = nombre
        if precio is not None: producto.precio = precio
        if descripcion is not None: producto.descripcion = descripcion
        if stock is not None: producto.stock = stock
        if imagen is not None: producto.imagen = imagen
        if disponible is not None: producto.disponible = disponible
    def eliminar(self, id_producto: int) -> None:
        producto = self.buscar_por_id(id_producto)
        producto.eliminar()