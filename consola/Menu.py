from abc import ABC, abstractmethod
from Entidades.Usuario import Usuario
import os
class Menu(ABC):
    def __init__(self, usuario: Usuario) -> None:
        self.usuario = usuario
    def limpiar_pantalla(self) -> None:
        os.system('cls' if os.name == 'nt' else 'clear')
    @abstractmethod
    def mostrar(self) -> bool:
           ...