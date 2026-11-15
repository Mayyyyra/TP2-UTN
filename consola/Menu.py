from abc import ABC, abstractmethod
from ..Entidades.Usuario import Usuario

class Menu(ABC):
    def __init__(self, usuario: Usuario) -> None:
        self.usuario = usuario

    @abstractmethod
    def mostrar(self) -> bool:
           ...