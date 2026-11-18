from enum import Enum

class FormaPago(Enum):
    TARJETA = 1
    TRANSFERENCIA =  2
    EFECTIVO = 3
    @classmethod
    def desde_numero(cls, numero: int) -> 'FormaPago':
        for opcion in cls:
            if opcion.value == numero:
                return opcion
        raise ValueError(f"Forma de pago inválida: {numero}")
class Estado(Enum):
    PENDIENTE = "Pendiente"
    CONFIRMADO =  "Confirmado"
    TERMINADO = "Terminado"
    CANCELADO = "Cancelado"
    @classmethod
    def desde_numero(cls, numero: int) -> 'FormaPago':
        for opcion in cls:
            if opcion.value == numero:
                return opcion
        raise ValueError(f"Forma de pago inválida: {numero}")