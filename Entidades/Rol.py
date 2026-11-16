from enum import Enum

class Rol(Enum):
    ADMIN = 1
    USUARIO =  2
    @classmethod
    def desde_numero(cls, numero: int) -> 'Rol':
        for opcion in cls:
            if opcion.value == numero:
                return opcion
        raise ValueError(f"Rol inválido: {numero}")