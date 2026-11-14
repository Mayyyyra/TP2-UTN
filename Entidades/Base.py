from datetime import datetime
from abc import ABC,abstractmethod
from FoodStoreError import EntidadNoEncontradaError
class Base(ABC):
    __contador_id: int = 0
    def __init__(self) -> None:
        Base.__contador_id += 1
        self.__eliminado: bool = False
        self.__id: int = Base.__contador_id
        self.__creado_en: datetime = datetime.now()
    def eliminar(self) -> None:
        if not self.__eliminado:
            self.__eliminado = True
        else:
            raise EntidadNoEncontradaError("No pudimos encontrar la id, revise si la id que puso es correcta o esta eliminada")
    #-----properties
    @property
    def eliminado(self) -> bool:
        return self.__eliminado
    @property
    def creado_en(self) -> datetime:
        return self.__creado_en
    @property
    def id(self) -> int:
        return self.__id
    #--------
    def __eq__(self,other:Base) -> bool:
        if not isinstance(other,Base):
            return False
        return self.__id == other.id
    def __hash__(self) -> int:
        return hash(self.__id)
    @abstractmethod
    def __str__(self) -> str:
        ...