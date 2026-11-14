from ..Entidades.Categoria import Categoria
from ..Entidades.Producto import Producto
from ..Exepciones.FoodStoreError import DuplicadoError, EntidadNoEncontradaError, OperacionNoPermitidaError

class CategoriaServicio():
    def __init__(self) -> None:
        self.__categorias: list[Categoria] = []

    @property
    def categorias(self) -> tuple[Categoria, ...]:
        return tuple(self.__categorias)

    def crear(self, nombre: str, descripcion: str) -> Categoria:
        for i in self.__categorias:
            if not i.eliminado and i.nombre.lower() == nombre.lower():
                raise DuplicadoError(f"La categoría '{nombre}' ya existe.")
                
        nueva = Categoria(nombre, descripcion)
        self.__categorias.append(nueva)
        return nueva

    def buscar_por_id(self, id_categoria: int) -> Categoria:
        for i in self.__categorias:
            if i.id == id_categoria and not i.eliminado:
                return i
        raise EntidadNoEncontradaError(f"No se encontró la categoría activa con ID {id_categoria}.")

    def listar(self) -> list[Categoria]:
        return [i for i in self.__categorias if not i.eliminado]

    def editar(self, id_categoria: int, nombre: str | None = None, descripcion: str | None = None) -> None:
        categoria = self.buscar_por_id(id_categoria)
        
        if nombre is not None and nombre.lower() != categoria.nombre.lower():
            for i in self.__categorias:
                if not i.eliminado and i.id != categoria.id and i.nombre.lower() == nombre.lower():
                    raise DuplicadoError(f"La categoría '{nombre}' ya existe.")
            categoria.nombre = nombre

        if descripcion is not None:
            categoria.descripcion = descripcion

    def eliminar(self, id_categoria: int, productos: list[Producto]) -> None:
        categoria = self.buscar_por_id(id_categoria)
        
        productos_activos = [p for p in productos if p.categoria == categoria and not p.eliminado]
        
        if len(productos_activos) > 0:
            raise OperacionNoPermitidaError(
                f"No se puede eliminar la categoría. Tiene {len(productos_activos)} producto(s) activo(s)."
            )
            
        categoria.eliminar()